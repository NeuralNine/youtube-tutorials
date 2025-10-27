from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route('/htmlpage')
def htmlpage():
    return render_template('page.html')


app.run(debug=True, host='0.0.0.0', port=9999)

