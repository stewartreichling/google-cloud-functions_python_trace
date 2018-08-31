# Using OpenCensus and Stackdriver Trace with Google Cloud Functions

## Overview
This sample demonstrates use of the `opencensus-trace` package and Stackdriver
Trace integration with Google Cloud Functions on the Python 3.7 runtime. The
following features are covered:

* setting the span context using request headers set by Google Cloud Platform
* automatically tracing HTTP/gRPC calls issued by Google Cloud client libraries
* exporting traces to Stackdriver Trace using background thread transport

The function downloads a text file (`journal.txt`) from a Cloud Storage bucket,
appends a timestamp to that file and then uploads it back to the bucket.

The resulting trace data is exported to [Stackdriver Trace](https://cloud.google.com/trace/).

## Set up your local development environment

### Pre-requisites
* `git`
* The Python 3.7 interpreter
* `pip`
* `virtualenv`
* `curl`
* The `gcloud` command-line tool

### Get the repo
Use `git` to grab a local copy of the repo:
```console
$ git clone https://github.com/stewblr/google-cloud-functions_python_trace.git
Cloning into 'google-cloud-functions_python_trace'...
remote: Counting objects: 84, done.
remote: Compressing objects: 100% (59/59), done.
remote: Total 84 (delta 42), reused 63 (delta 23), pack-reused 0
Unpacking objects: 100% (84/84), done.
```

Navigate to your local copy:
```console
$ cd google-cloud-functions_python_trace/
$ ls
LICENSE  README.md  bin  main.py  requirements.txt  test_main.py
```

### Create and activate a virtual environment
Use `virtualenv` to create a python3 virtual environment:
```console
$ virtualenv --python python3 env
```

Activate your newly-created virtual environment:
```console
$ source env/bin/activate
```

### Install dependencies
Use `pip` to install project dependencies:
```console
$ pip install -r requirements.txt
```

### Set up local authentication
Running this sample locally involves interacting with live Google APIs. Calls
to Google APIs must be authenticated. Fortunately, the client library handles
authentication automatically once you [create a service account](https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account)
and [set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable](https://cloud.google.com/docs/authentication/getting-started).

Note that your deployed function will automatically use a default service
account associated with Google Cloud Functions. You may delete the service
account created as part of this sample once you've completed local development.

### Create a Cloud Storage bucket with an empty text file
This example downloads a text file from a Cloud Storage bucket, appends a
timestamp to the body of the file, then uploads that file to the same bucket.

Use `gsutil` (installed as part of `gcloud`) to create a bucket:
```console
$ gsutil mb gs://tracing-example
Creating gs://tracing-example/...
```

Use `touch` to create a text file:
```console
$ touch journal.txt
```

Upload the file to your newly-created Cloud Storage bucket:
```console
$ gsutil cp journal.txt gs://tracing-example
Copying file://journal.txt [Content-Type=text/plain]...
/ [1 files][    0.0 B/    0.0 B]
Operation completed over 1 objects.
```

## Run locally
Set the `GCP_PROJECT` and `FUNCTION_NAME` environment variables:
```console
$ export GCP_PROJECT=<YOUR PROJECT ID>
$ export FUNCTION_NAME=tracing_local
```

Note that Cloud Functions automatically sets the `GCP_PROJECT` and
`FUNCTION_NAME` environment variables. You won't need to set these environment
variables during deployment.

Execute the `bin/test-local` script to generate a mock request and send it to
your function:
```console
$ bash bin/test-local
Background thread started.
`journal.txt` downloaded from Cloud Storage to `/tmp/journal.txt`.
Appended `2018-08-26 10:33:05.852129` to `/tmp/journal.txt`.
`/tmp/journal.txt` uploaded to Cloud Storage.
Visit `https://console.cloud.google.com/traces/traces` to see tracing data for this request.
Sending all pending spans before terminated.
Background thread exited.
Sent all pending spans.
```

Visit [Stackdriver Trace](https://console.cloud.google.com/traces/traces) in
your Google Cloud Console to see traces associated with your test request.

## Deploy your function
Execute the `bin/deploy` script to deploy a function named `tracing`
using `gcloud`:

```console
$ bash bin/deploy
Deploying function (may take a while - up to 2 minutes)...done.
```

# Test your deployed function
Execute the `bin/test-deployed` script to send a request over HTTP to your
deployed function:

```console
$ bash bin/test-deployed
Visit `https://console.cloud.google.com/traces/traces` to see tracing data for this request. 
```
