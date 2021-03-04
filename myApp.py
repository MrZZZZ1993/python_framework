import os

from werkzeug.exceptions import MethodNotAllowed, HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from my_context import AppContext, RequestContext
from my_globals import _request_stack, request
from jinja2 import Environment, FileSystemLoader


def render_template(template_name, **context):
    template_path = os.path.join(os.getcwd(), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_path),autoescape=True)
    text = jinja_env.get_template(template_name).render(context)
    return text


class MyApp(object):
    request_class = Request

    def __init__(self):
        self.url_map = Map()
        self.view_function = {}

    def app_context(self):
        return AppContext(self)

    def request_context(self, environ):
        return RequestContext(self, environ)

    def wsgi_app(self, environ, start_response):
        req_ctx = self.request_context(environ)
        req_ctx.push()

        response = self.dispatch_request()
        if response:
            response = Response(response, content_type='text/html; charset=UTF-8')
        else:
            response = Response('<h1>404 source not found</h1>', content_type='text/html; charset=UTF-8', status=404)
        return response(environ, start_response)

    def dispatch_request(self):
        req = _request_stack.top.request
        endpoint = req.url_rule.endpoint
        values = req.view_args
        return self.view_function[endpoint](**values)

    def add_url_rule(self, url, endpoint, view_func):
        if endpoint is None:
            endpoint = view_func.__name__
        rule = Rule(url, endpoint=endpoint)
        self.url_map.add(rule)
        self.view_function[endpoint] = view_func

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def run(self, ip='127.0.0.1', port=8001, debug=True):
        run_simple(ip, port, self, use_reloader=True, use_debugger=debug)

    def route(self, url, **options):

        def decorator(func):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(url, endpoint, func)
            return func

        return decorator

    def create_adapter(self, req):
        adapter = self.url_map.bind_to_environ(req.environ)
        return adapter


app = MyApp()


@app.route('/')
def index():
    name = 'Hello'
    return render_template('index.html', name=name)


@app.route('/test')
def test():
    return 'test'


@app.route('/favicon.ico')
def icon():
    return None


if __name__ == '__main__':
    app.run()
