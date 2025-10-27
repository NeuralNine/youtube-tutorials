from quart import Quart, render_template

app = Quart(__name__)


@app.route('/')
async def index():
    return "Hello World"


@app.route('/htmlpage')
async def htmlpage():
    return await render_template('page.html')


app.run(debug=True, host='0.0.0.0', port=9999)

