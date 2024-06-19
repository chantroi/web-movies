from flask import Flask, request, jsonify, send_file, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")
