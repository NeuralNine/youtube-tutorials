import os, time, requests
from flask import Flask, request, render_template_string
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
TAVUS_API_KEY = os.getenv("TAVUS_API_KEY")

REPLICA_ID = "<REPLICA_ID>"

HEADERS = {"x-api-key": TAVUS_API_KEY, "Content-Type": "application/json"}
API = "https://tavusapi.com/v2"

HTML = """
<!doctype html>
<title>Ask the Tutor → Video</title>
<style>
  body{font-family:system-ui;margin:2rem;max-width:780px}
  form{display:flex;gap:.5rem}
  input,button{padding:.7rem;border-radius:.6rem;border:1px solid #ccc}
  button{cursor:pointer}
  .answer{white-space:pre-wrap;background:#fafafa;padding:1rem;border-radius:.6rem;border:1px solid #eee;margin-top:1rem}
  iframe,video{width:100%;height:420px;border:none;border-radius:.8rem;margin-top:1rem}
</style>
<h1>AI Tutor → Video</h1>
<form method="post">
  <input name="q" placeholder="Ask a question…" style="flex:1" required>
  <button>Answer</button>
</form>

{% if script %}
  <div class="answer"><strong>Script:</strong>\n{{ script }}</div>
{% endif %}

{% if hosted_url %}
  <iframe controls src="{{ hosted_url }}"></iframe>
{% elif video_id %}
  <p>Rendering video (id: {{ video_id }})… refresh in a bit.</p>
{% endif %}
"""

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    script = hosted_url = None
    video_id = None
    if request.method == "POST":
        question = request.form.get("q", "").strip()

        resp = client.responses.create(
            model="gpt-4o",
            input=[
                {"role": "system", "content": "You are a patient, step-by-step math tutor."},
                {"role": "user", "content": question},
            ],
        )
        script = (resp.output_text or "").strip()

        create = requests.post(
            f"{API}/videos",
            headers=HEADERS,
            json={"replica_id": REPLICA_ID, "script": script, "video_name": f"tutor_{int(time.time())}"},
            timeout=60,
        )
        create.raise_for_status()
        data = create.json()
        video_id = data.get("video_id")
        hosted_url = data.get("hosted_url")
        status = data.get("status", "queued")

        for _ in range(30):
            if status == "ready":
                break
            time.sleep(5)
            got = requests.get(f"{API}/videos/{video_id}", headers=HEADERS, timeout=30).json()
            status = got.get("status", status)
            hosted_url = got.get("hosted_url", hosted_url)

    return render_template_string(HTML, script=script, hosted_url=hosted_url, video_id=video_id)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

