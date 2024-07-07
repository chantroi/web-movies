import os
from flask import Flask, render_template, jsonify
from deta import Deta

DETA_PROJECT_KEY = os.environ["DETA_PROJECT_KEY"]
DETA_KEY = os.getenv("DETA_KEY", DETA_PROJECT_KEY)

app = Flask(__name__)
deta = Deta(DETA_KEY)


@app.route("/")
@app.route("/<drive>")
def index(drive="files"):
    fs = deta.Drive(drive)
    files = fs.list()["names"]
    return render_template("index.html", files=files, drive=drive)


@app.route("/<drive>/<folder>/<file>", methods=["GET"])
def play_file(drive, folder, file):
    target_file = folder + "/" + file
    return render_template(
        "player.html", drive=drive, filename=target_file, deta_key=DETA_KEY
    )


@app.route("/<drive>/<folder>/<file>", methods=["DELETE"])
def delete_route(drive, folder, file):
    target_file = folder + "/" + file
    fs = deta.Drive(drive)
    fs.delete(target_file)
    return jsonify(status="success", message=f"file {target_file} deleted successful")


@app.route("/<drive>/<folder>", methods=["GET"])
@app.route("/<drive>/root", methods=["GET"])
def list_files(drive, folder=None):
    fs = deta.Drive(drive)
    files = fs.list()["names"]
    if folder:
        files = [file for file in files if file.startswith(folder)]
    return jsonify(files=files)
