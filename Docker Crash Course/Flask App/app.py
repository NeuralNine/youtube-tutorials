import os
from flask import Flask, render_template, request

app = Flask(__name__)

LOG_FILE = os.getenv("LOG_FILE", "message_log.txt")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')

        with open(LOG_FILE, 'a') as f:
            f.write(message + '\n')

    messages = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            messages = f.read().split('\n')[:-1]

    return render_template('index.html', messages=[m.strip() for m in messages])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("DEBUG", "False") == "True")

