"""A Google Cloud Functions sample that uses Stackdriver Trace."""

import datetime
import os
import random
import time
from google.cloud.storage import Client
from opencensus.trace.exporters import stackdriver_exporter
from opencensus.trace import tracer as tracer_module
from opencensus.trace.exporters.transports.background_thread \
    import BackgroundThreadTransport
from opencensus.trace.propagation import google_cloud_format
from opencensus.trace import config_integration

FILE_NAME = 'journal.txt'
BUCKET_NAME = 'tracing-example'


# Get Google Cloud project from environment
PROJECT_ID = os.environ['GCP_PROJECT']


# Initialize a Tracer that exports to Stackdriver
# Use BackgroundThreadTransport to avoid adding latency during execution
exporter = stackdriver_exporter.StackdriverExporter(
    project_id=PROJECT_ID, transport=BackgroundThreadTransport)
tracer = tracer_module.Tracer(exporter=exporter)
propagator = google_cloud_format.GoogleCloudFormatPropagator()


def execute_task(task_name, min_latency, max_latency):
    """Simulate a running task with name and random bounded latency."""
    latency = random.randint(min_latency, max_latency)
    time.sleep(latency/1000.0)
    print(f'`{task_name}` took {latency} milliseconds')


def download_file(bucket, source_file_name, destination_file_name):
    """Download a file from Cloud Storage."""
    blob = bucket.blob(source_file_name)
    blob.download_to_filename(destination_file_name)
    print(f'`{source_file_name}` downloaded from Cloud Storage to '
          f'`{destination_file_name}`.')


def append_timestamp_to_file(file_name):
    """Generate a timestamp and append it to the file."""
    timestamp = datetime.datetime.now()
    with open(file_name, 'a+') as f:
        entry = f'{timestamp}\n'
        f.write(entry)
    print(f'Appended `{timestamp}` to `{file_name}`.')


def upload_file(bucket, source_file_name, destination_file_name):
    """Upload a file to Cloud Storage."""
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)
    print(f'`{source_file_name}` uploaded to Cloud Storage.')


def add_journal_entry():
    """Download a journal file, append a timestamp and upload the file."""

    # Initialize a storage client
    with tracer.span(name='initialize_client'):
        storage_client = Client()
        bucket = storage_client.get_bucket(BUCKET_NAME)

    # Download 'journal.txt' from Cloud Storage.
    with tracer.span(name='download_file'):
        source_file_name = FILE_NAME
        destination_file_name = f'/tmp/{FILE_NAME}'
        download_file(bucket, source_file_name, destination_file_name)

    # Append timestamp to downloaded copy of 'journal.txt'.
    with tracer.span(name='append_timestamp_to_file'):
        append_timestamp_to_file(f'/tmp/{FILE_NAME}')

    # Upload 'journal.txt' back to Cloud Storage.
    with tracer.span(name='upload_file'):
        source_file_name = f'/tmp/{FILE_NAME}'
        destination_file_name = FILE_NAME
        upload_file(bucket, source_file_name, destination_file_name)


def entrypoint(request):
    """Execute tasks within a parent trace span when invoked via HTTP."""
    # Get the trace_id from the request's HTTP header
    span_context = \
        propagator.from_header(request.headers['X-Cloud-Trace-Context'])
    tracer.span_context = span_context

    # Enable tracing HTTP/gRPC calls issued by Google Cloud client libraries
    config_integration.trace_integrations(['google_cloud_clientlibs'], tracer)

    # Wrap function logic in a parent trace
    function_name = os.environ['FUNCTION_NAME']
    with tracer.span(name=function_name):
        add_journal_entry()

    url = 'https://console.cloud.google.com/traces/traces'
    return f'Visit `{url}` to see tracing data for this request.'
