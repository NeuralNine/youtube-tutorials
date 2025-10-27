import asyncio
from quart import Quart, websocket

app = Quart(__name__, static_folder="static")

@app.websocket("/ws")
async def ws():
    while True:
        msg = await websocket.receive()
        await websocket.send(f"You said: {msg}")

@app.get("/")
async def index():
    return await app.send_static_file("index.html")

if __name__ == "__main__":
    app.run()

