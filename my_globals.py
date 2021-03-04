from functools import partial

from werkzeug.local import LocalProxy, LocalStack


def _find_request_obj(name):
    top = _request_stack.top
    return getattr(top, name)


def _find_app_obj(name):
    top = _app_stack.top
    return getattr(top, name)


def _get_app():
    top = _app_stack.top
    return top.app


_request_stack = LocalStack()
_app_stack = LocalStack()
current_app = LocalProxy(_get_app)
request = LocalProxy(partial(_find_request_obj, 'request'))
session = LocalProxy(partial(_find_request_obj, 'session'))
g = LocalProxy(partial(_find_app_obj, 'g'))
