# Using OpenCensus and Stackdriver Trace with Google Cloud Functions

## Overview
This sample demonstrates use of the `opencensus-trace` package and Stackdriver
Trace integration with Google Cloud Functions on the Python 3.7 runtime.

The resulting trace data is exported to [Stackdriver Trace](https://cloud.google.com/trace/).

The function mimics latency patterns that might be observed when downloading an
image, processing it locally and then uploading it to a remote server.

## Set up your local development environment

### Pre-requisites
* The Python 3.7 interpreter
* `pip`
* `virtualenv`
* `curl`
* The `gcloud` command-line tool

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
pip install -r requirements.txt
```

### Set up local authentication
The local development approach for this sample involves interacting with live
Google APIs (specifically, Stackdriver Trace). Calls to Google APIs must be
authenticated. Fortunately, the client library handles authentication
automatically once you [create a service account](https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account)
and [set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable](https://cloud.google.com/docs/authentication/getting-started).

Note that your deployed function will automatically use a default service
account associated with Google Cloud Functions. You may delete the service
account use for local authentication example once you've completed local
development.

## Run locally
Set the 'GCP_PROJECT' environment variable:
```console
$ export GCP_PROJECT=<YOUR PROJECT ID>
```

Execute the `bin/test-local` script to generate a mock request and send it to
your function:
```console
$ bash bin/test-local
Background thread started.
`download_image` took 298 milliseconds
`process_image` took 78 milliseconds
`upload_image` took 949 milliseconds
Visit `https://console.cloud.google.com/traces/traces` to see tracing data for this request (id: `dev_ipxsnNLx`).
Sending all pending spans before terminated.
Background thread exited.
Sent all pending spans.
```

Visit [Stackdriver Trace](https://console.cloud.google.com/traces/traces) in
your Google Cloud Console to see traces associated with your test request.

## Deploy your function
Execute the `bin/test-local` script to deploy a function named `tracing`
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
Visit `https://console.cloud.google.com/traces/traces` to see tracing data for this request (id: `592f8cbcc21afd43b571a7f729b23bdc/12812703197617869446;o=1`).
```
