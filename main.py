from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "instabot123")

@app.route('/', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    print(f"🔎 VERIFY REQUEST: mode={mode}, token={token}, challenge={challenge}")

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✅ Webhook verified successfully!")
        return challenge, 200
    else:
        print("❌ Webhook verification failed!")
        return "Verification failed", 403


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 Received event:", data)
    return "EVENT_RECEIVED", 200
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 Received event:", data)

    if data and 'entry' in data:
        for entry in data['entry']:
            changes = entry.get('changes', [])
            for change in changes:
                if change.get('field') == 'comments':
                    comment = change['value'].get('text', '')
                    user = change['value'].get('from', {}).get('username', '')
                    print(f"💬 New comment from {user}: {comment}")

    return "EVENT_RECEIVED", 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
