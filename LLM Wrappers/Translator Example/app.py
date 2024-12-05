import os

from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)

languages = [
    "English", "Spanish", "French", "German", "Chinese", "Japanese", 
    "Korean", "Italian", "Portuguese", "Russian", "Arabic"
]

system_prompt_template = "The user will provide you with a text in {in_language}. Your job is to return the same content in {out_language}. Nothing else. Under no circumstances ever add context, clarifications or anything like that. Just the translation and nothing else."

@app.route("/", methods=["GET", "POST"])
def index():
    translation = ""
    if request.method == "POST":
        in_language = request.form["in_language"]
        out_language = request.form["out_language"]
        user_text = request.form["user_text"]

        system_prompt = system_prompt_template.format(in_language=in_language, out_language=out_language)

        try:
            response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ])
            translation = response.choices[0].message.content.strip()
        except Exception as e:
            translation = f"Error: {e}"

    return render_template("index.html", languages=languages, translation=translation)

if __name__ == "__main__":
    app.run(debug=True)

