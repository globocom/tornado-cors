# -*- coding: utf-8 -*-


import logging

from tornado.web import asynchronous, RequestHandler

import inspect

def get_class_that_defined_method(meth):
    for cls in inspect.getmro(meth.im_class):
        if meth.__name__ in cls.__dict__: return cls
    return None

class CorsMixin(object):

    CORS_ORIGIN = None
    CORS_HEADERS = None
    CORS_MAX_AGE = 86400

    def prepare(self):
        if self.CORS_ORIGIN:
            self.set_header('Access-Control-Allow-Origin', self.CORS_ORIGIN)

    def _get_methods(self):
        methods = []
        for meth in ['get', 'put', 'post', 'patch', 'delete', 'options']:
            instance_meth = getattr(self, meth)
            if not meth:
                continue
            handler_class = get_class_that_defined_method(instance_meth)
            if not handler_class is RequestHandler:
                methods.append(meth.upper())

        return ", ".join(methods)

    @asynchronous
    def options(self, *args, **kwargs):
        if self.CORS_HEADERS:
            self.set_header('Access-Control-Allow-Headers', self.CORS_HEADERS)
        self.set_header('Access-Control-Allow-Methods', self._get_methods())
        if self.CORS_MAX_AGE:
            self.set_header('Access-Control-Max-Age', self.CORS_MAX_AGE)
        self.set_status(204)
        self.finish()
