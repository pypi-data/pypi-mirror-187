# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 14 Jan 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
from datetime import datetime

from parse import parse
from webob import Request, Response

VALID_HTTP_METHOD = ['HEAD', 'POST', 'GET', 'PUT', 'DELETE', 'PATCH']


class API:
    def __init__(self):
        self.routes = dict()

    def toJson(self, response_obj, status_code=200):
        response = Response()
        response.status_code = status_code
        response.json = response_obj
        return response

    def add_func(self, path, handler_func, http_method='POST'):
        if http_method in VALID_HTTP_METHOD:
            self.routes['{}:{}'.format(http_method, path)] = {
                'handler_func': handler_func,
                'method': http_method
            }
        else:
            raise Exception('NOT a Valid HTTP Method')

    def find_handler_func(self, http_method, url_path):
        requested_path = '{}:{}'.format(http_method, url_path)

        for path, v in self.routes.items():
            params = parse(path, requested_path)
            if params is not None:
                return v.get('handler_func'), params.named, v.get('method')
        return None, None, None

    def request_processor(self, request):
        # http_method = Request.environ.get('REQUEST_METHOD')
        http_method = request.method
        url_path = request.path
        print('loglog:', http_method, url_path)
        handler_func, params, method = self.find_handler_func(http_method=http_method,
                                                              url_path=url_path)
        params = request.json
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
        print('flag, resp:', flag, resp)
        if flag:
            res_obj = {'response': resp}
            response = self.toJson(res_obj)
        else:
            resp_obj = {'error': str(resp)}
            response = self.toJson(resp_obj, status_code=404)
        return response(environ, start_response)
