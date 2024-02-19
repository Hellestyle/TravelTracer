from flask import Flask, request, redirect, url_for, render_template, flash


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
