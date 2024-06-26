from io import BytesIO
from os import environ
from flask import Flask, request, Response, render_template, jsonify
from detafs import DetaFs

app = Flask(__name__)
fs = DetaFs(environ["DETA_KEY"])


@app.route("/")
def index():
    files = fs.ls()
    return render_template("index.html", files=files)


@app.route("/p/<file>")
def stream_file(file: str):
    fileobj = fs.get(file).iter_chunks()
    if file.endswith('.mp4'):
        return Response(fileobj, mimetype="video/mp4")
    elif any(file.endswith(ext) for ext in ['.jpg', '.png', '.gif','.jpeg'])):
        return Response(fileobj, mimetype="image/jpeg")
    else:
        return Response(fileobj, mimetype="text/plain")


@app.route("/file/delete")
def delete_route():
    target_file = request.args.get("file")
    fs.remove(target_file)
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
    files = fs.ls()
    return jsonify(files=files)
