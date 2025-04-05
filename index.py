from flask import Flask, request, jsonify
from flask_lambda import FlaskLambda
import random, uuid, requests
from concurrent.futures import ThreadPoolExecutor

app = FlaskLambda(__name__)

thai_syllables = ["สวัสดี", "ขอบคุณ", "ทดสอบ", "สุดยอด", "พัฒนา", "คับ"]

def random_thai_word():
    return random.choice(thai_syllables)

def send_request(username):
    payload = {
        "username": username,
        "question": random_thai_word(),
        "deviceId": str(uuid.uuid4()),
        "gameSlug": "",
        "referrer": ""
    }
    headers = {
        "Host": "ngl.link",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0",
        "origin": "https://ngl.link",
        "referer": f"https://ngl.link/{username}",
        "x-requested-with": "XMLHttpRequest"
    }
    r = requests.post("https://ngl.link/api/submit", data=payload, headers=headers)
    return {"status_code": r.status_code, "message": payload["question"]}

@app.route('/send')
def send():
    username = request.args.get('username')
    num = int(request.args.get('num', 1))
    if not username:
        return jsonify({"error": "missing username"}), 400
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(lambda _: send_request(username), range(num)))
    return jsonify(results)
