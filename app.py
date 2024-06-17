from io import BytesIO
from quart import Quart, request, send_file, render_template, jsonify
from detafs import DetaFs

app = Quart(__name__)
fs = DetaFs("c0a1xmuzlhz_9ukoxqAYL8nr8w9hPai2kPbyf7qnAaGC")


@app.route("/")
async def index():
    files = fs.ls()
    return await render_template("index.html", items=files)


@app.route("/p/<file>")
async def stream_file(file: str):
    fileobj = BytesIO(fs.open(file).read())
    return await send_file(fileobj, attachment_filename=file)


@app.route("/file/delete")
async def delete_route():
    target_file = request.args.get("file")
    fs.remove(target_file)
    return await jsonify(
        status="success", message=f"file {target_file} deleted successful"
    )


@app.route("/file/upload", methods=["POST"])
async def upload_file():
    file = request.files["file"]
    fs.put(file.filename, file.read())
    return await jsonify(
        status="success", message=f"file {file.filename} upload completed"
    )


@app.route("/file/list")
async def list_files():
    files = fs.ls()
    return await jsonify(files=files)


if __name__ == "__main__":
    from uvicorn import run

    run(app, host="0.0.0.0", port=8080)
