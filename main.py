"""A function that shows use of `opencensus-trace` with Stackdriver Trace."""

import os
import random
import time
from flask import request
from opencensus.trace.exporters import stackdriver_exporter
from opencensus.trace import tracer as tracer_module
from opencensus.trace.exporters.transports.background_thread \
    import BackgroundThreadTransport


# Get Google Cloud project from environment
project_id = os.environ['GCP_PROJECT']


# Initialize a Tracer that exports to Stackdriver
# Use BackgroundThreadTransport to avoid adding latency during execution
exporter = stackdriver_exporter.StackdriverExporter(
    project_id=project_id, transport=BackgroundThreadTransport)
tracer = tracer_module.Tracer(exporter=exporter)


def execute_task(task_name, min_latency, max_latency):
    """Simulate a running task with name and random bounded latency."""
    latency = random.randint(min_latency, max_latency)
    time.sleep(latency/1000.0)
    print(f'`{task_name}` took {latency} milliseconds')


def run_tasks():
    """Run a series of simulated tasks wrapped in individual trace spans."""
    # An example medium-lived task, e.g., downloading an image
    task_name = 'download_image'
    with tracer.span(name=task_name):
        execute_task(task_name, 200, 400)

    # An example medium-lived task, e.g., processing the image locally
    task_name = 'process_image'
    with tracer.span(name='process_image'):
        execute_task(task_name, 25, 100)

    # An example long-lived task, e.g., uploading the image to a remote server
    task_name = 'upload_image'
    with tracer.span(name='upload_image'):
        execute_task(task_name, 400, 1000)


def entrypoint(request):
    """Execute tasks within a parent trace span when invoked via HTTP."""
    # Get the trace_id from the request's HTTP header
    trace_id = request.headers['X-Cloud-Trace-Context']

    # Wrap function logic in a parent trace
    with tracer.span(name=trace_id):
        run_tasks()

    url = 'https://console.cloud.google.com/traces/traces'
    return (f'Visit `{url}` to see tracing data for this request '
            f'(id: `{trace_id}`).')
