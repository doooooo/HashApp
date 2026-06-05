from flask import Flask, render_template, redirect, url_for, request, jsonify
import hashlib

app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("hash_text"))


@app.route("/hash", methods=["GET", "POST"])
def hash_text():

    if request.method == "GET":
        return render_template("hash.html")

    data = request.get_json()

    plain_text = data.get("text", "")

    hashed_value = hashlib.sha224(
        plain_text.encode()
    ).hexdigest()

    return jsonify({
        "hash": hashed_value
    })


if __name__ == "__main__":
    app.run(debug=True)