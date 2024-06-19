from io import BytesIO
from flask import Flask, request, send_file, render_template, jsonify
from detafs import DetaFs

app = Flask(__name__)
fs = DetaFs("c0Jtyij8pU2_5T5DgCv2L7G6SvpQXR8pU8ujNJbqbW7v")


@app.route("/")
def index():
    files = fs.ls()
    return render_template("index.html", items=files)


@app.route("/p/")
def stream_file(file: str):
    fileobj = BytesIO(fs.open(file).read())
    return send_file(fileobj, attachment_filename=file)


@app.route("/file/delete")
def delete_route():
    target_file = request.args.get("file")
    fs.remove(target_file)
    return jsonify(status="success", message=f"file {target_file} deleted successful")


@app.route("/file/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    fs.put(file.filename, file.read())
    return jsonify(status="success", message=f"file {file.filename} upload completed")


@app.route("/file/list")
def list_files():
    files = fs.ls()
    return jsonify(files=files)
