# -*- coding: utf-8 -*-


import logging

from tornado.web import asynchronous


class CorsMixin(object):

    CORS_ORIGIN = None
    CORS_HEADERS = None
    CORS_METHODS = None
    CORS_MAX_AGE = 86400

    def prepare(self):
        if self.CORS_ORIGIN:
            self.set_header('Access-Control-Allow-Origin', self.CORS_ORIGIN)

    @asynchronous
    def options(self, *args, **kwargs):
        if self.CORS_HEADERS:
            self.set_header('Access-Control-Allow-Headers', self.CORS_HEADERS)
        if self.CORS_METHODS:
            self.set_header('Access-Control-Allow-Methods', self.CORS_METHODS)
        if self.CORS_MAX_AGE:
            self.set_header('Access-Control-Max-Age', self.CORS_MAX_AGE)
        self.set_status(204)
        self.finish()
