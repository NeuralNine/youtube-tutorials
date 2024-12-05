import os

from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, render_template

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)

SYSTEM_PROMPT = (
    "The user will provide you with information about a YouTube video. This can but does not have to include title, description and other notes. As a response return tags for YouTube to optimize for performance. Your answer should only include tags separated by commas. Nothing else. Under no circumstances EVER provide context, clarification or anything else. Just the tags separated by commas. Aim for roughly 300-400 characters."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_tags", methods=["POST"])
def generate_tags():
    user_input = request.form["video_info"]
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ])
        tags = response.choices[0].message.content
        return tags
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)

