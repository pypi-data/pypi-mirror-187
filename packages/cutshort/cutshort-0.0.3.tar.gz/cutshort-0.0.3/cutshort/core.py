# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 14 Jan 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
from datetime import datetime

from parse import parse
from webob import Request, Response

VALID_HTTP_METHOD = ['POST', 'GET', 'PUT', 'DELETE', 'PATCH']
METHOD_MAPPING = {
    'CREATE': 'POST',
    'UPDATE': 'PUT',
    'RETRIEVE': 'GET',
    'GET': 'GET',
    'POST': 'POST',
    'PUT': 'PUT',
    'DELETE': 'DELETE',

}


class API:
    def __init__(self, debug=True):
        self.routes = dict()
        self.debug = debug

    def toJson(self, response_obj, status_code=200):
        response = Response()
        response.status_code = status_code
        response.json = response_obj
        return response

    def add_func(self, handler_func, path=None, http_method=None):
        prefix_name = str(handler_func.__name__).lower().split('_')[0]
        mapped_prefix_name = METHOD_MAPPING.get(prefix_name.upper(), None)
        if http_method is None and mapped_prefix_name in VALID_HTTP_METHOD:
            http_method = mapped_prefix_name
        else:
            http_method = http_method
        if self.debug:
            print('http-method:', http_method)

        if http_method in VALID_HTTP_METHOD:
            path = path if path else '/{}'.format(str(handler_func.__name__).lower())
            if self.debug:
                print('path:', path)
            self.routes['{}:{}'.format(http_method, path)] = {
                'handler_func': handler_func,
                'method': http_method
            }
            if self.debug:
                print(self.routes)
        else:
            raise Exception('NOT a Valid HTTP Method')

    def find_handler_func(self, http_method, url_path):
        requested_path = '{}:{}'.format(http_method, url_path)

        if self.debug:
            print('requested-path:', requested_path)

        for path, v in self.routes.items():
            params = parse(path, requested_path)
            if params is not None:
                return v.get('handler_func'), params.named, v.get('method')
        return None, None, None

    def request_processor(self, request):
        # http_method = Request.environ.get('REQUEST_METHOD')
        http_method = request.method
        url_path = request.path
        handler_func, params, method = self.find_handler_func(http_method=http_method,
                                                              url_path=url_path)
        try:
            params = request.json
        except Exception as e:
            params = {}
        if self.debug:
            print('req:json', params.items())
            print('log:', handler_func, params, method)
        if handler_func is not None:
            if method == str(http_method).upper():
                try:
                    resp = handler_func(**params)
                    return True, resp
                except Exception as e:
                    return False, e
        else:
            return False, 'No Method'

    def __call__(self, environ, start_response):
        self.environ = environ
        self.request = Request(self.environ)
        req_info = f'''
        Method:     {self.request.method}
        URL Path:   {self.request.url}
        Time:       {datetime.now()}
                    '''
        print(datetime.now(), '-', self.request.method, '-', self.request.url)
        flag, resp = self.request_processor(self.request)
        if self.debug:
            print('flag, resp:', flag, resp)
        if flag:
            res_obj = {'response': resp}
            response = self.toJson(res_obj)
        else:
            resp_obj = {'error': str(resp)}
            response = self.toJson(resp_obj, status_code=404)
        return response(environ, start_response)


def simple_server(application: API,
                  host: str = 'localhost',
                  port: int = 8456):
    from werkzeug import run_simple
    run_simple(hostname=host, port=port, application=application)
