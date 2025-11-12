from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "instabot123")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

@app.route('/', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("Webhook verified successfully ✅")
        return challenge, 200
    else:
        print("Webhook verification failed ❌")
        return 'Verification failed', 403


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming webhook data:", data)

    try:
        if data and 'entry' in data:
            message = data['entry'][0]['messaging'][0]['message']['text']
            sender_id = data['entry'][0]['messaging'][0]['sender']['id']

            reply_text = f"Hey there! You said: {message}"
            requests.post(
                f"https://graph.facebook.com/v19.0/me/messages?access_token={ACCESS_TOKEN}",
                json={"recipient": {"id": sender_id}, "message": {"text": reply_text}}
            )
    except Exception as e:
        print("Error:", e)

    return "EVENT_RECEIVED", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
