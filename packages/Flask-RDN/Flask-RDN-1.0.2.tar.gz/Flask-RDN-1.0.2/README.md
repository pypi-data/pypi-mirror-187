# Flask Extension: Request Data Normalizer (RDN)

Streamline and supercharge your query string parameter parsing in Flask! This Flask extension provides support for parsing complex Python objects from base64 encoded query parameters, and makes passed query parameterss of any encoding available via Flask's `Request.get_json()`.

[![Flask](https://img.shields.io/badge/Flask-2.0.3+-blue.svg)](https://pypi.org/project/Flask/)
[![Query String Manager](https://img.shields.io/badge/Query%20String%20Manager-1.0.9+-green.svg)](https://pypi.org/project/Query-String-Manager/)
[![PyPi](https://img.shields.io/badge/View%20On-PyPi-orange.svg)](https://pypi.org/project/Flask-RDN/)

## Installation

```sh
pip install Flask-RDN
```

## Quick Start

```python
from flask_request_data_normalizer import RequestDataNormalizer
from flask import Flask

app = Flask(__name__)
RequestDataNormalizer(app)
```

## Overview

In Flask, parameters passed in a URL query string (such as `test`/`val` in `localhost/?test=val`) are accessed in Dictionary form via the `Request.args` or `Request.values` properties but not the `Request.get_json()` method.

This extension adds these parsed query parameters to the results of `Request.get_json()` making the method a one-stop-shop to retrieve _any_ data passed to an endpoint.

Additionally, this extension provides support for parsing base64 encoded query parameters. This allows complex objects to be encoded in query parameters and automatically parsed by Flask!

## Base64 Parsing Examples

Normally nested data like lists or maps (e.g. `[1,2,3]` or `{"a": "b"}`) can't be sent as a query parameter to a Flask application. But it can if Flask can read base64 encoded data.

For example, a Javascript application could create the following complex query string and base64 encode it:  

```js
var obj = {nested: {a: 'a', b: 'b'}, list: [1, {"in": "list"}, true]};
"?data=" + btoa(JSON.stringify(obj));

'?data=eyJuZXN0ZWQiOnsiYSI6ImEiLCJiIjoiYiJ9LCJsaXN0IjpbMSx7ImluIjoibGlzdCJ9LHRydWVdfQ=='
```

With this extension, Flask will be able to parse this data into a Python object automatically.

Take this sample Flask application with a single endpoint:

```python
from flask_request_data_normalizer import RequestDataNormalizer
from flask import Flask, request

app = Flask(__name__)
RequestDataNormalizer(app)

@app.route('/')
def endpoint():
   return str(request.get_json())

app.run(host="0.0.0.0", debug=True)
```

If we called the above endpoint with our base64 encoded query string we would get the following Python object

```python
{'data': {'nested': {'a': 'a', 'b': 'b'}, 'list': [1, {'in': 'list'}, True]}}
```

The parsing of base64 query strings is done by the [Query String Manager](https://github.com/Topazoo/Query-String-Manager) library under the hood. Check it out for more examples of how base64 query strings are parsed!

## Contributing

Contributions are welcome! Please not the following when contributing:

- Unittests must be added under the `tests/` directory for the PR to be approved. You can run unittests from the root project directory with the following command:

    ```sh
    python setup.py test
    ```

- PRs cannot be merged without all unittests passing (they will execute automatically)
- Merges to `main` will automatically create a new release on PyPi **[unless it is from a forked Repo](https://stackoverflow.com/questions/58737785/github-actions-empty-env-secrets)**
