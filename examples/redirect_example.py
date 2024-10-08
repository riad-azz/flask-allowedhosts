from flask import Flask, request, jsonify, redirect
from flask_allowed_hosts import AllowedHosts

ALLOWED_HOSTS = ["93.184.215.14", "api.example.com"]


# Redirects to `/custom-error` page if the request IP/hostname is not in the allowed hosts
def custom_on_denied():
    return redirect("/custom-error")


app = Flask(__name__)
allowed_hosts = AllowedHosts(app, allowed_hosts=ALLOWED_HOSTS, on_denied=custom_on_denied)


@app.route("/custom-error", methods=["GET"])
def custom_error():
    return "Oops! looks like you are not allowed to access this page!"


# This endpoint will redirect all incoming requests that are not
# from "93.184.215.14" or "api.example.com" to the `/custom-error` page
@app.route("/api/greet", methods=["GET"])
@allowed_hosts.limit()
def greet_endpoint():
    name = request.args.get("name", "Friend")
    data = {"data": f"Hello There {name}!"}
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
