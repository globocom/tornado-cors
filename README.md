Tornado CORS [![Build Status](https://travis-ci.org/globocom/tornado-cors.png?branch=master)](https://travis-ci.org/globocom/tornado-cors)
============

Makes it easier to add CORS support do tornado apps.

About Cross-Origin Resource Sharing (CORS)
------------------------------------------

- http://en.wikipedia.org/wiki/Cross-origin_resource_sharing
- http://www.w3.org/TR/cors/


Installing
----------

```
pip install tornado-cors
```

Using
-----

```
from tornado_cors import CorsMixin


class MyHandler(CorsMixin, RequestHandler):
    
    # Value for the Access-Control-Allow-Origin header.
    # Default: None (no header).
    CORS_ORIGIN = '*'
    
    # Value for the Access-Control-Allow-Headers header.
    # Default: None (no header).
    CORS_HEADERS = 'Content-Type'
    
    # Value for the Access-Control-Allow-Methods header.
    # Default: Methods defined in handler class.
    # None means no header.
    CORS_METHODS = 'POST'

    # Value for the Access-Control-Allow-Credentials header.
    # Default: None (no header).
    # None means no header.
    CORS_CREDENTIALS = True
    
    # Value for the Access-Control-Max-Age header.
    # Default: 86400.
    # None means no header.
    CORS_MAX_AGE = 21600
    
    ...
```

Advanced
--------

By default, CorsMixin defines "options" method using the decorator
"asynchronous" from "tornado.web".

If your project customizes this decorator for some purpose (eg. usage of
greenlets), CorsMixin allows such customization in options wrapper.

Usage:

```
# custom_wrapper was previously defined

from tornado_cors import custom_decorator
custom_decorator.wrapper = custom_wrapper

```


## License

Tornado CORS is licensed under the MIT License:

The MIT License

Copyright (c) 2013 globo.com

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
