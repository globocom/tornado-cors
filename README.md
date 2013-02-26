Tornado CORS [![Build Status](https://travis-ci.org/globocom/tornado-cors.png?branch=master)](https://travis-ci.org/globocom/tornado-cors)
============

Makes it easier to add CORS support do tornado apps.

About Cross-Origin Resource Sharing (CORS)
------------------------------------------

- http://en.wikipedia.org/wiki/Cross-origin_resource_sharing
- http://www.w3.org/TR/cors/


Installing
----------

`pip install tornado-cors`

Using
-----

```
class MyHandler(CorsMixin, RequestHandler):
    
    # Value for the Access-Control-Allow-Origin header. Default: None (no header)
    CORS_ORIGIN = '*'
    
    # Value for the Access-Control-Allow-Headers header. Default: None (no header)
    CORS_HEADERS = 'Content-Type'
    
    # Value for the Access-Control-Max-Age header. Default: 86400
    CORS_MAX_AGE = 21600
    
    ...
```
