"""A helper script for local testing. Tests propagation of trace_id."""

from main import entrypoint
import flask
import random
import string


def generate_trace_context():
    """Generate an ID that looks like Google's X-Cloud-Trace-Context"""
    charset = string.hexdigits.lower()
    trace_id = ''.join(random.choices(charset, k=32))
    span_id = ''.join(random.choices(charset, k=16))
    options = 'o=0'
    x_cloud_trace_context = f'{trace_id}/{span_id};{options}'
    return x_cloud_trace_context


def test():
    """Invoke the function's entrypoint, passing a trace_id via headers."""
    app = flask.Flask(__name__)
    x_cloud_trace_context = generate_trace_context()
    headers = {'X-Cloud-Trace-Context': x_cloud_trace_context}
    with app.test_request_context(headers=headers):
        print(entrypoint(flask.request))


if __name__ == '__main__':
    test()
