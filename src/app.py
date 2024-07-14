from flask import Flask, request, render_template, jsonify
from deta import Deta
from environment import deta_key

app = Flask(__name__)
deta = Deta(deta_key)


def get_neighbors(lst, element):
    if element in lst:
        indx = lst.index(element)
        return lst[indx - 1] if indx > 0 else None, (
            lst[indx + 1] if indx < len(lst) - 1 else None
        )
    else:
        return None, None


@app.route("/")
@app.route("/<drive>")
def index(drive="files"):
    fs = deta.Drive(drive)
    files = fs.list()["names"]
    return render_template("index.html", files=files, drive=drive)


@app.route("/<drive>/<file>", methods=["GET"])
def play_file(drive, file):
    fs = deta.Drive(drive)
    files = fs.list()["names"]
    pre_file, next_file = get_neighbors(files, file)
    return render_template(
        "player.html",
        drive=drive,
        filename=file,
        deta_key=deta_key,
        pre_file=pre_file,
        next_file=next_file,
    )


@app.route("/<drive>/<filename>", methods=["DELETE"])
def delete_route(drive, file):
    fs = deta.Drive(drive)
    fs.delete(file)
    return jsonify(status="success", message=f"file {file} deleted successful")


@app.route("/<drive>", methods=["POST"])
def upload_file(drive):
    fs = deta.Drive(drive)
    if request.files:
        file = request.files["file"]
        filename = file.filename
        fs.put(filename, file.read())
        return jsonify(
            status="success", message=f"file {file.filename} upload completed"
        )
    else:
        data = request.json
        filename = data["name"]
        fs.put(filename, data["content"])
        return jsonify(
            status="success", message=f"file {data['name']} upload completed"
        )


@app.route("/<drive>/list")
def list_files(drive):
    fs = deta.Drive(drive)
    files = fs.list()["names"]
    return jsonify(files=files)
