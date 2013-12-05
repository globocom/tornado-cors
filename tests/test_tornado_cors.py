# -*- coding: utf-8 -*-
import imp
import functools
import sys

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application, asynchronous, RequestHandler

import tornado_cors as cors
from tornado_cors import custom_decorator


passed_by_custom_wrapper = False


def custom_wrapper(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        return result
    global passed_by_custom_wrapper
    passed_by_custom_wrapper = id(wrapper)
    return wrapper


class CorsTestCase(AsyncHTTPTestCase):

    def test_should_return_headers_with_default_values_in_options_request(self):
        self.http_client.fetch(self.get_url('/default'), self.stop, method='OPTIONS')
        headers = self.wait().headers

        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertNotIn('Access-Control-Allow-Headers', headers)
        self.assertNotIn('Access-Control-Allow-Credentials', headers)
        self.assertEqual(headers['Access-Control-Allow-Methods'], 'POST, DELETE, PUT, OPTIONS')
        self.assertEqual(headers['Access-Control-Max-Age'], '86400')

    def test_should_return_headers_with_custom_values_in_options_request(self):
        self.http_client.fetch(self.get_url('/custom'), self.stop, method='OPTIONS')
        headers = self.wait().headers
        print headers

        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
        self.assertEqual(headers['Access-Control-Allow-Headers'], 'Content-Type')
        self.assertEqual(headers['Access-Control-Allow-Methods'], 'POST')
        self.assertEqual(headers['Access-Control-Allow-Credentials'], 'true')
        self.assertNotIn('Access-Control-Max-Age', headers)

    def test_should_return_origin_header_for_requests_other_than_options(self):
        self.http_client.fetch(self.get_url('/custom'), self.stop, method='POST', body='')
        headers = self.wait().headers
        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')

    def test_should_support_custom_methods(self):
        response = self.http_client.fetch(self.get_url('/custom_method'), self.stop, method='OPTIONS')
        headers = self.wait().headers
        self.assertEqual(headers["Access-Control-Allow-Methods"], 'OPTIONS, NEW_METHOD')

    def test_should_support_custom_methods(self):
        response = self.http_client.fetch(self.get_url('/custom_method'), self.stop, method='OPTIONS')
        headers = self.wait().headers
        self.assertEqual(headers["Access-Control-Allow-Methods"], 'OPTIONS, NEW_METHOD')

    def get_app(self):
        return Application([(r'/default', DefaultValuesHandler), (r'/custom', CustomValuesHandler), (r'/custom_method', CustomMethodValuesHandler)])


class CustomWrapperTestCase(AsyncHTTPTestCase):

    def setUp(self):
        self.original_wrapper = custom_decorator.wrapper

    def tearDown(self):
        custom_decorator.wrapper = self.original_wrapper

    def test_wrapper_customization(self):
        version = sys.version_info[0]
        if version == 2:
            # assert default wrapper is being used
            wrapper_module_name = cors.CorsMixin.options.im_func.func_code.co_filename
            self.assertFalse(passed_by_custom_wrapper)
            self.assertTrue(wrapper_module_name.endswith("tornado/web.py"))

        self.assertEquals(cors.custom_decorator.wrapper, asynchronous)

        # overwrite using custom wrapper and reload module
        custom_decorator.wrapper = custom_wrapper
        imp.reload(cors)

        if version == 2:
            # assert new wrapper is being used
            wrapper_module_name = cors.CorsMixin.options.im_func.func_code.co_filename
            self.assertTrue(passed_by_custom_wrapper)
            self.assertTrue(wrapper_module_name.endswith("tests/test_tornado_cors.py"))

        self.assertEquals(cors.custom_decorator.wrapper, custom_wrapper)


class DefaultValuesHandler(cors.CorsMixin, RequestHandler):

    @asynchronous
    def post(self):
        self.finish()

    @asynchronous
    def put(self):
        self.finish()

    @asynchronous
    def delete(self):
        self.finish()


class CustomValuesHandler(cors.CorsMixin, RequestHandler):

    CORS_ORIGIN = '*'
    CORS_HEADERS = 'Content-Type'
    CORS_METHODS = 'POST'
    CORS_CREDENTIALS = True
    CORS_MAX_AGE = None

    @asynchronous
    def post(self):
        self.finish()

    @asynchronous
    def put(self):
        self.finish()

    @asynchronous
    def delete(self):
        self.finish()


class CustomMethodValuesHandler(cors.CorsMixin, RequestHandler):

    SUPPORTED_METHODS = list(CustomValuesHandler.SUPPORTED_METHODS) + ["NEW_METHOD"]

    @asynchronous
    def new_method(self):
        self.finish()
