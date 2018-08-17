# Overview
This example shows how to use `opencensus-trace` in a Python function deployed
to Google Cloud Functions to trace a request. The resulting trace data is
exported to [Stackdriver Trace](https://cloud.google.com/trace/).

The Python function follows the pattern of a function that downloads an image,
processes that image locally and then uploads the image to a remote server.

# Set up your local development environment

## Create and activate a virtual environment
Use `virtualenv` to create a python3 virtual environment:
```console
$ virtualenv --python python3 env
```

Activate your newly-created virtual environment:
```console
$ source env/bin/activate
```

## Install dependencies
Use `pip` to install project dependencies:
```console
pip install -r requirements.txt
```

## Set up local authentication
The local development approach for this example involves interacting with live
Google APIs (specifically, Stackdriver Trace). Calls to Google APIs must be
authenticated. The client libraries handle authentication automatically once
you [create a service account](https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account)
and [set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable](https://cloud.google.com/docs/authentication/getting-started).

Note that your deployed function will automatically use a default service
account associated with Google Cloud Functions. You may delete the service
account created as part of this example once you've completed local development.

# Run locally
Execute the `bin/test-local` script to generate a mock request and send it to
your function:

```console
$ bash bin/test-local
`download_image` took 299 milliseconds
`process_image` took 35 milliseconds
`upload_image` took 878 milliseconds
Visit `https://console.cloud.google.com/traces/traces` to see tracing data for this request (id: `dev_LuhaxMkC`).
```

Visit [Stackdriver Trace](https://console.cloud.google.com/traces/traces) in
your Google Cloud Console to see traces associated with your test request.

# Deploy your function
Execute the `bin/test-local` script to execute the `gcloud functions deploy`
command with the appropriate parameters:

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
