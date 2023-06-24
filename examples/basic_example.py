from flask import Flask, request, jsonify
from flask_allowedhosts import check_host

app = Flask(__name__)

ALLOWED_HOSTS = ['127.0.0.1:5000', 'localhost:5000']

@app.route("/api")
@check_host(allowed_hosts=ALLOWED_HOSTS)
def greet_endpoint():
    name = request.args.get("name", "Friend")
    greeting = {"greeting": f"Hello There {name}!"}
    return jsonify(greeting), 200


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
