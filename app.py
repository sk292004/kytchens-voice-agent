print("RUNNING THIS app.py FILE")
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)

RETELL_API_KEY = os.getenv("RETELL_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")
RETELL_FROM_NUMBER = os.getenv("RETELL_FROM_NUMBER")

RETELL_BASE_URL = "https://api.retellai.com/v1"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/call", methods=["POST"])
def make_call():
    phone = request.form.get("phone")
    name = request.form.get("name", "")

    url = "https://api.retellai.com/v2/create-phone-call"

    payload = {
        "from_number": RETELL_FROM_NUMBER,
        "to_number": phone,
        "agent_id": AGENT_ID
    }

    headers = {
        "Authorization": f"Bearer {RETELL_API_KEY}",
        "Content-Type": "application/json"
    }

    print("SENDING REQUEST TO:", url, flush=True)

    response = requests.post(url, json=payload, headers=headers)

    print("STATUS CODE:", response.status_code, flush=True)
    print("RAW RESPONSE:", response.text, flush=True)

    try:
        data = response.json()
    except Exception:
        data = {"raw_response": response.text}

    return jsonify(data), response.status_code


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    call_analysis = data.get("call_analysis", {})

    output = {
        "call_status": "completed" if call_analysis.get("call_successful") else "failed",
        "reason_for_leaving": call_analysis.get("call_summary"),
        "rejoin_interest": call_analysis.get("custom_analysis_data")
    }

    print("FINAL OUTPUT (PDF COMPLIANT):")
    print(output)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
