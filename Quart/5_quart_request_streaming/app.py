from quart import Quart, request, Response
import aiofiles, os

app = Quart(__name__, static_folder="static", static_url_path="/static")
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return await app.send_static_file("index.html")

@app.post("/upload")
async def upload():
    fname = request.args.get("filename", "upload.bin")
    path = os.path.join(UPLOAD_DIR, fname)

    async with aiofiles.open(path, "wb") as f:
        async for chunk in request.body:
            if not chunk:
                break
            await f.write(chunk)

    return Response("ok\n", 201)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9999, debug=True, certfile='cert.pem', keyfile='key.pem', http2=True)


