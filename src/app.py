from flask import Flask, request, render_template, jsonify
from deta import Deta
from environment import deta_key

app = Flask(__name__)
deta = Deta(deta_key)


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
        "player.html", drive=drive, filename=target_file, deta_key=deta_key
    )


@app.route("/<drive>/<folder>/<filename>", methods=["DELETE"])
def delete_route(drive, folder, filename):
    fs = deta.Drive(drive)
    target_file = folder + "/" + filename
    fs.delete(target_file)
    return jsonify(status="success", message=f"file {target_file} deleted successful")


@app.route("/<drive>/<folder>", methods=["POST"])
@app.route("/<drive>", methods=["POST"])
def upload_file(drive, folder=None):
    fs = deta.Drive(drive)
    if request.files:
        file = request.files["file"]
        filename = file.filename
        if folder:
            filename = folder + "/" + filename
        fs.put(filename, file.read())
        return jsonify(
            status="success", message=f"file {file.filename} upload completed"
        )
    else:
        data = request.json
        filename = data["name"]
        if folder:
            filename = folder + "/" + data["name"]
        fs.put(filename, data["content"])
        return jsonify(
            status="success", message=f"file {data['name']} upload completed"
        )


@app.route("/<drive>/<folder>")
@app.route("/<drive>/root")
def list_files(drive, folder=None):
    fs = deta.Drive(drive)
    files = fs.list()["names"]
    if folder:
        files = [file for file in files if file.startswith(folder)]
    return jsonify(files=files)
