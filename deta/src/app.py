import os
from flask import Flask, render_template, jsonify
from deta import Deta

DETA_PROJECT_KEY = os.environ["DETA_PROJECT_KEY"]
DETA_KEY = os.getenv("DETA_KEY", DETA_PROJECT_KEY)

app = Flask(__name__)
deta = Deta(DETA_KEY)


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
        deta_key=DETA_KEY,
        pre_file=pre_file,
        next_file=next_file,
    )


@app.route("/<drive>/<file>", methods=["DELETE"])
def delete_route(drive, file):
    fs = deta.Drive(drive)
    fs.delete(file)
    return jsonify(status="success", message=f"file {file} deleted successful")


@app.route("/<drive>/json", methods=["GET"])
def list_files(drive):
    fs = deta.Drive(drive)
    files = fs.list()["names"]
    return jsonify(files=files)
