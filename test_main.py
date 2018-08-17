"""A helper script for local testing. Tests propagation of trace_id."""

from main import entrypoint
import flask
import random
import string


def test():
    """Invoke the function's entrypoint, passing a trace_id via headers."""
    app = flask.Flask(__name__)
    trace_id = f"dev_{''.join(random.choices(string.ascii_letters, k=8))}"
    headers = {'X-Cloud-Trace-Context': trace_id}
    with app.test_request_context(headers=headers):
        entrypoint(flask.request)


if __name__ == '__main__':
    test()
