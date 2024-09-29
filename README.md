# Flask Allowed Hosts

Flask Allowed Hosts is a simple and flexible extension for Flask that allows you to restrict access to your application
based on the incoming request hostname/IP address. This extension provides an easy way to implement hostname/IP based
access
control in your Flask applications.

## Features

- Per-route configuration options.
- Customizable denied access behavior.
- Restrict access to your Flask app based on hostnames/IP addresses.
- Legacy decorator for standalone use or if you prefer a decorator-based approach without initializing
  the `AllowedHosts` class.

## Installation

Install the package using pip:

```cmd
pip install flask-allowed-hosts
```

## Extension Usage

### Basic Setup

Here's a basic example of how to use the Flask Allowed Hosts extension:

```python
from flask import Flask, request, jsonify
from flask_allowed_hosts import AllowedHosts

app = Flask(__name__)

ALLOWED_HOSTS = ["93.184.215.14", "api.example.com"]


def custom_on_denied():
    error = {"error": "Oops! Looks like you are not allowed to access this page!"}
    return jsonify(error), 403


allowed_hosts = AllowedHosts(app, allowed_hosts=ALLOWED_HOSTS, on_denied=custom_on_denied)


# Allows all incoming requests
@app.route("/api/hello", methods=["GET"])
def hello_world():
    data = {"message": "Hello, World!"}
    return jsonify(data), 200


# Only allows incoming requests from "93.184.215.14" and "api.example.com"
@app.route("/api/greet", methods=["GET"])
@allowed_hosts.limit()
def greet_endpoint():
    name = request.args.get("name", "Friend")
    data = {"message": f"Hello There {name}!"}
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Per-Route Configuration

You can also override the `allowed_hosts` or `on_denied` configuration for specific views:

```python
from flask import Flask, request, jsonify, abort
from flask_allowed_hosts import AllowedHosts

app = Flask(__name__)

ALLOWED_HOSTS = ["93.184.215.14", "api.example.com"]


def custom_on_denied():
    error = {"error": "Oops! Looks like you are not allowed to access this page!"}
    return jsonify(error), 403


allowed_hosts = AllowedHosts(app, allowed_hosts=ALLOWED_HOSTS, on_denied=custom_on_denied)


# Only allows incoming requests from "93.184.215.14" and "api.example.com"
@app.route("/api/hello", methods=["GET"])
@allowed_hosts.limit()
def hello_world():
    data = {"message": "Hello, World!"}
    return jsonify(data), 200


# Only allows incoming requests from "127.0.0.1" and "localhost" 
# and throws a 503 Service Unavailable for all other requests 
@app.route("/api/greet", methods=["GET"])
@allowed_hosts.limit(allowed_hosts=["127.0.0.1", "localhost"], on_denied=lambda: abort(503))
def greet_endpoint():
    name = request.args.get("name", "Friend")
    data = {"message": f"Hello There {name}!"}
    return jsonify(data), 200
```

### Legacy Decorator

> [!WARNING]
> Using the `@limit_hosts` legacy decorator in combination with the `AllowedHosts` class might cause unexpected
> behavior.

For standalone use or if you prefer a decorator-based approach without initializing the `AllowedHosts` class, you can
use the `@limit_hosts` decorator:

```python
from flask import Flask, jsonify
from flask_allowed_hosts import limit_hosts

app = Flask(__name__)

ALLOWED_HOSTS = ["93.184.215.14", "api.example.com"]


def custom_on_denied():
    error = {"error": "Custom Denied Response"}
    return jsonify(error), 403


# Allows all incoming requests
@app.route("/api/hello", methods=["GET"])
def hello_world():
    data = {"message": "Hello, World!"}
    return jsonify(data), 200


# Only allows incoming requests from "93.184.215.14" and "api.example.com"
@app.route("/api/greet", methods=["GET"])
@limit_hosts(allowed_hosts=ALLOWED_HOSTS, on_denied=custom_on_denied)
def greet_endpoint():
    return jsonify({"message": "This is a legacy endpoint"}), 200
```

The `@limit_hosts` decorator can be used directly on route functions without needing to initialize the `AllowedHosts`
class. It provides the same hostname/IP address restriction functionality but on a per-route basis.

### More Examples

You can find more examples in
the [examples directory](https://github.com/riad-azz/flask-allowed-hosts/tree/main/examples).

## Configuration

### Initialization Parameters

When initializing the `AllowedHosts` class, you can provide the following parameters:

- `app` (optional): The Flask application instance. If not provided, you'll need to call `allowed_hosts.init_app(app)`
  later.
- `allowed_hosts` (optional): A list of allowed IP addresses/hostnames, also can be set to `"*"` or `None` to allow all
  incoming requests. Default is `None`.
- `on_denied` (optional): A callable that will be invoked when access is denied. Default is `None`.

Example:

```python
def custom_denied_handler():
    error = {"error": "Oops! Looks like you are not allowed to access this page!"}
    return jsonify(error), 403


allowed_hosts = AllowedHosts(
    app,
    allowed_hosts=["93.184.215.14", "api.example.com"],
    on_denied=custom_denied_handler,
)
```

As for the `@allowed_hosts.limit` or `@limit_hosts` decorators, you can provide the following parameters to override any
previously provided values:

- `allowed_hosts` (optional): A list of allowed IP addresses/hostnames, also can be set to `"*"` or `None` to allow all
  hosts. Default is `None`.
- `on_denied` (optional): A callable that will be invoked when access is denied. Default is `None`.

### Flask Config and Environment Variables

#### Flask Configuration

The extension also respects the following Flask configuration variables:

- `ALLOWED_HOSTS`: A list of allowed IP addresses or hostnames. This is used if `allowed_hosts` is not provided during
  initialization.
- `ALLOWED_HOSTS_ON_DENIED`: A callable to be used when access is denied. This is used if `on_denied` is not provided
  during initialization.

You can set these in your Flask config:

```python
app.config['ALLOWED_HOSTS'] = ["93.184.215.14", "api.example.com"]
app.config['ALLOWED_HOSTS_ON_DENIED'] = custom_denied_handler
```

> [!IMPORTANT]
> If `allowed_hosts` and `on_denied` are provided during initialization they will override the values
> of the app config.

#### Environment Variables

You can enable debug mode by setting the `ALLOWED_HOSTS_DEBUG` environment variable to `True`:

```shell
export ALLOWED_HOSTS_DEBUG="True"
```

This will print helpful debug messages to the console.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you have any questions or feedback, please feel free
to [open an issue or a pull request](https://github.com/riad-azz/flask-allowed-hosts/issues).

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details.
