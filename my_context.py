from my_globals import _request_stack, _app_stack


class AppContext(object):

    def __init__(self, app):
        self.app = app
        self._cnt = 0

    def push(self):
        self._cnt += 1
        _app_stack.push(self)

    def pop(self):
        self._cnt -= 1
        _app_stack.pop()


class RequestContext(object):

    def __init__(self, app, environ, request=None):
        self.app = app
        if request is None:
            request = app.request_class(environ)
        self.request = request
        self.adapter = app.create_adapter(request)

        self._implicit_app_stack = []

    def match_request(self):
        result = self.adapter.match(return_rule=True)
        self.request.url_rule, self.request.view_args = result

    def push(self):
        app = _app_stack.top
        if app is None or app != self.app:
            app = self.app.app_context()
            app.push()
            self._implicit_app_stack.append(app)
        else:
            self._implicit_app_stack.append(None)

        _request_stack.push(self)
        self.match_request()

    def pop(self):
        clear_request = False
        if not self._implicit_app_stack:
            clear_request = True

        rv = _request_stack.pop()
        if clear_request:
            rv.request.environ["werkzeug.request"] = None


