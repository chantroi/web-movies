from flask import Flask, request, redirect, render_template, jsonify
from deta import Deta
from environment import deta_key, project_id

app = Flask(__name__)
fs = Deta(deta_key).Drive("files")
api_url = f"https://drive.deta.sh/v1/{project_id}/files"


@app.route("/")
def index():
    files = fs.list()["names"]
    return render_template("index.html", files=files)


@app.route("/p")
def stream_file():
    file = request.args.get("file")
    res_url = f"{api_url}/files?name={file}"
    return render_template("redirect.html", res_url=res_url, deta_key=deta_key)


@app.route("/file/delete")
def delete_route():
    target_file = request.args.get("file")
    fs.delete(target_file)
    return jsonify(status="success", message=f"file {target_file} deleted successful")


@app.route("/file/upload", methods=["POST"])
def upload_file():
    if request.files:
        file = request.files["file"]
        fs.put(file.filename, file.read())
        return jsonify(
            status="success", message=f"file {file.filename} upload completed"
        )
    else:
        data = request.json
        fs.put(data["name"], data["content"])
        return jsonify(
            status="success", message=f"file {data['name']} upload completed"
        )


@app.route("/file/list")
def list_files():
    files = fs.list()["names"]
    return jsonify(files=files)
