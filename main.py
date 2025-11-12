from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "instabot123")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

@app.route('/', methods=['GET'])
def verify_webhook():
    """Verify webhook endpoint with Meta callback"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✅ Webhook verified successfully!")
        return challenge, 200
    else:
        print("❌ Webhook verification failed!")
        return 'Verification failed', 403


@app.route('/', methods=['POST'])
def receive_webhook():
    """Receive webhook events from Instagram"""
    data = request.get_json()
    print("📩 Received data:", data)

    try:
        if data and 'entry' in data:
            for entry in data['entry']:
                messaging = entry.get('messaging', [])
                for message_event in messaging:
                    sender_id = message_event['sender']['id']
                    if 'message' in message_event:
                        text = message_event['message'].get('text', '')
                        print(f"💬 New message: {text}")

                        # reply message
                        reply = f"Hey! You said: {text}"
                        requests.post(
                            f"https://graph.facebook.com/v19.0/me/messages?access_token={ACCESS_TOKEN}",
                            json={
                                "recipient": {"id": sender_id},
                                "message": {"text": reply}
                            }
                        )
    except Exception as e:
        print("Error:", e)

    return "EVENT_RECEIVED", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
