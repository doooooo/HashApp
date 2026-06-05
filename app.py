from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import json
import os

app = Flask(__name__)
app.secret_key = "my_secret_key"

USERS_FILE = "users.json"

@app.route("/", methods=["GET"])
def default():
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():

    error_message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]

        if password!=password2 :
            error_message = "password fields does not match"
            return render_template(
                "signup.html",
                error=error_message
            )

        # Hash entered password
        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        # save username:hash_password dictionary entry in a root json file
        json_users = {}
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE) as f:
                json_users = json.load(f)

        if username in json_users:
            return render_template("signup.html", error="username already exists")

        json_users[username] = hashed_password
        with open(USERS_FILE, "w") as f:
            json.dump(json_users, f)

        # redirect to login page
        return redirect(url_for("login"))

    return render_template(
        "signup.html",
        error=error_message
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    error_message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Hash entered password
        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        #check username,hash_password in json file
        json_users = {}
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE) as f:
                json_users = json.load(f)

        if username in json_users and json_users[username] == hashed_password:
            session["username"] = username
            session["fullname"] = username
            return redirect(url_for("home"))

        error_message = "wrong username or password"

    return render_template(
        "login.html",
        error=error_message
    )


@app.route("/home")
def home():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "home.html",
        fullname=session["fullname"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)