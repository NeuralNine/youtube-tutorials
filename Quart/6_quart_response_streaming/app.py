import aiofiles
from quart import Quart, Response

app = Quart(__name__)
app.static_folder = 'static'


@app.route('/video')
async def video_endpoint():
    async def generate_video_stream():
        # TODO: You need to put the video into a directory called videos
        async with aiofiles.open('videos/tutorial.mp4', 'rb') as file_handle:
            while chunk := await file_handle.read(1024 * 1024):
                yield chunk

    return Response(generate_video_stream(), mimetype='video/mp4')


@app.route('/')
async def index_endpoint():
    return await app.send_static_file('index.html')


if __name__ == '__main__':
    app.run()

