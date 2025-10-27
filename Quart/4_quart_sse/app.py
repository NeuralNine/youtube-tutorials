import asyncio, json
from quart import Quart, Response

app = Quart(__name__, static_folder="static")


async def stream():
    i = 0
    while True:
        await asyncio.sleep(1)
        yield f"data: {json.dumps({'count': i})}\n\n"
        i += 1


@app.get("/events")
async def events():
    return Response(stream(), content_type="text/event-stream")


@app.get("/")
async def index():
    return await app.send_static_file("index.html")


if __name__ == "__main__":
    app.run()

