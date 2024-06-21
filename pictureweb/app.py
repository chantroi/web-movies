from flask import Flask, request, jsonify, render_template
from s3fs import S3FileSystem

s3url = "https://detas3server-1-d8694513.deta.app"
app = Flask(__name__)
fs = S3FileSystem(
    endpoint_url=s3url,
    key="a1000",
    secret="c0Jtyij8pU2_5T5DgCv2L7G6SvpQXR8pU8ujNJbqbW7v",
)


@app.route("/")
def home():
    files = fs.ls("files")
    return render_template("index.html", files=files, s3url=s3url)


@app.route("/upload", methods=["POST"])
def upload_picture():
    file = request.files["file"]
    with fs.open(f"files/{file.filename}", "w") as f:
        f.write(file.read())
    return jsonify(status="success", message="file upload successfully")


@app.route("/list")
def list_picture():
    return jsonify(fs.ls("files"))
