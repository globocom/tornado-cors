# -*- coding: utf-8 -*-


import inspect

from tornado.web import RequestHandler
from tornado_cors import custom_decorator


def _get_class_that_defined_method(meth):
    for cls in inspect.getmro(meth.__self__.__class__):
        if meth.__name__ in cls.__dict__: return cls
    return None


class CorsMixin(object):

    CORS_ORIGIN = None
    CORS_HEADERS = None
    CORS_METHODS = None
    CORS_CREDENTIALS = None
    CORS_MAX_AGE = 86400
    CORS_EXPOSE_HEADERS = None

    def set_default_headers(self):
        if self.CORS_ORIGIN:
            self.set_header("Access-Control-Allow-Origin", self.CORS_ORIGIN)

        if self.CORS_EXPOSE_HEADERS:
            self.set_header('Access-Control-Expose-Headers', self.CORS_EXPOSE_HEADERS)

    @custom_decorator.wrapper
    def options(self, *args, **kwargs):
        if self.CORS_HEADERS:
            self.set_header('Access-Control-Allow-Headers', self.CORS_HEADERS)
        if self.CORS_METHODS:
            self.set_header('Access-Control-Allow-Methods', self.CORS_METHODS)
        else:
            self.set_header('Access-Control-Allow-Methods', self._get_methods())
        if self.CORS_CREDENTIALS != None:
            self.set_header('Access-Control-Allow-Credentials',
                "true" if self.CORS_CREDENTIALS else "false")
        if self.CORS_MAX_AGE:
            self.set_header('Access-Control-Max-Age', self.CORS_MAX_AGE)

        if self.CORS_EXPOSE_HEADERS:
            self.set_header('Access-Control-Expose-Headers', self.CORS_EXPOSE_HEADERS)

        self.set_status(204)
        self.finish()

    def _get_methods(self):
        supported_methods = [method.lower() for method in self.SUPPORTED_METHODS]
        #  ['get', 'put', 'post', 'patch', 'delete', 'options']
        methods = []
        for meth in supported_methods:
            instance_meth = getattr(self, meth)
            if not meth:
                continue
            handler_class = _get_class_that_defined_method(instance_meth)
            if not handler_class is RequestHandler:
                methods.append(meth.upper())

        return ", ".join(methods)
