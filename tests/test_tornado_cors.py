# -*- coding: utf-8 -*-


from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application, asynchronous, RequestHandler

from tornado_cors import CorsMixin


class CorsTestCase(AsyncHTTPTestCase):

    def test_should_return_headers_with_default_values_in_options_request(self):
        self.http_client.fetch(self.get_url('/default'), self.stop, method='OPTIONS')
        headers = self.wait().headers
        
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertNotIn('Access-Control-Allow-Headers', headers)
        self.assertEqual(headers['Access-Control-Allow-Methods'], 'OPTIONS')
        self.assertEqual(headers['Access-Control-Max-Age'], '86400')

    def test_should_return_headers_with_custom_values_in_options_request(self):
        self.http_client.fetch(self.get_url('/custom'), self.stop, method='OPTIONS')
        headers = self.wait().headers

        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
        self.assertEqual(headers['Access-Control-Allow-Headers'], 'Content-Type')
        self.assertEqual(headers['Access-Control-Allow-Methods'], 'PUT, POST, DELETE, OPTIONS')
        self.assertNotIn('Access-Control-Max-Age', headers)

    def test_should_return_origin_header_for_requests_other_than_options(self):
        self.http_client.fetch(self.get_url('/custom'), self.stop, method='POST', body='')
        headers = self.wait().headers
        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')

    def get_app(self):
        return Application([(r'/default', DefaultValuesHandler), (r'/custom', CustomValuesHandler)])


class DefaultValuesHandler(CorsMixin, RequestHandler):
    pass

class CustomValuesHandler(CorsMixin, RequestHandler):
    
    CORS_ORIGIN = '*'
    CORS_HEADERS = 'Content-Type'
    CORS_METHODS = 'POST, PUT, DELETE'
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
