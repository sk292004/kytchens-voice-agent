print("🔥 RUNNING THIS app.py FILE 🔥")
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

    print("📤 SENDING REQUEST TO:", url)

    response = requests.post(url, json=payload, headers=headers)

    print("📥 STATUS CODE:", response.status_code)
    print("📥 RAW RESPONSE:", response.text)

    try:
        data = response.json()
    except Exception:
        data = {"raw_response": response.text}

    return jsonify(data), response.status_code


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    
    # Log the raw data to a file for debugging
    with open("webhook_log.json", "w") as f:
        import json
        json.dump(data, f, indent=4)

    print("RECEIVED WEBHOOK DATA:", data)

    output = {
        "call_status": data.get("call_status"),
        "reason_for_leaving": data.get("analysis", {}).get("reason_for_leaving"),
        "rejoin_interest": data.get("analysis", {}).get("rejoin_interest")
    }

    print("FINAL OUTPUT (PDF COMPLIANT):")
    print(output)

    return jsonify({"status": "received"})


if __name__ == "__main__":
    app.run(debug=True)
