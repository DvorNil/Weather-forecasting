import requests
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='front')

class WeatherAI:
    @staticmethod
    def get_history(lat, lon, start, end):
        url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&"
               f"start_date={start}&end_date={end}&daily=temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum&timezone=auto")
        try:
            res = requests.get(url).json()
            d = res['daily']
            return [{
                "date": d['time'][i], "temp": d['temperature_2m_mean'][i],
                "hum": d['relative_humidity_2m_mean'][i], "rain": d['precipitation_sum'][i]
            } for i in range(len(d['time']))]
        except: return []

    @staticmethod
    def predict_logic(history):
        if not history: return {"temp": 0, "hum": 0, "rain": 0}
        temps = [h['temp'] for h in history if h['temp'] is not None]
        avg_temp = (temps[-1] * 0.5 + temps[-2] * 0.3 + temps[-3] * 0.2) if len(temps) >= 3 else temps[-1]
        return {
            "temp": round(avg_temp, 1),
            "hum": int(sum(h['hum'] for h in history)/len(history)),
            "rain": round(sum(h['rain'] for h in history)/len(history), 1)
        }

@app.route('/')
def index(): return send_from_directory('front', 'index.html')

@app.route('/api/weather', methods=['POST'])
def handle_weather():
    data = request.json
    mode, city, date_str = data.get('mode'), data.get('city'), data.get('date')
    
    geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1").json()
    if not geo.get('results'): return jsonify({"error": "City not found"}), 404
    loc = geo['results'][0]
    lat, lon = loc['latitude'], loc['longitude']

    if mode == 'forecast':
        end = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        start = (datetime.now() - timedelta(days=9)).strftime('%Y-%m-%d')
        hist = WeatherAI.get_history(lat, lon, start, end)
        return jsonify({"city": loc['name'], "prediction": WeatherAI.predict_logic(hist), "history": hist[::-1]})

    elif mode == 'test':
        target = datetime.strptime(date_str, '%Y-%m-%d')
        hist = WeatherAI.get_history(lat, lon, (target-timedelta(days=7)).strftime('%Y-%m-%d'), (target-timedelta(days=1)).strftime('%Y-%m-%d'))
        actual = WeatherAI.get_history(lat, lon, date_str, date_str)
        pred = WeatherAI.predict_logic(hist)
        acc = max(0, 100 - (abs(pred['temp'] - actual[0]['temp']) * 10)) if actual else 0
        return jsonify({"city": loc['name'], "prediction": pred, "actual": actual[0], "accuracy": round(acc, 1), "history": hist[::-1]})

    elif mode == 'future':
        # AI logic: Sample same date from last 3 years
        target = datetime.strptime(date_str, '%Y-%m-%d')
        samples = []
        for i in range(1, 4):
            d = f"{target.year - i}-{target.month:02d}-{target.day:02d}"
            s = WeatherAI.get_history(lat, lon, d, d)
            if s: samples.append(s[0])
        pred = {"temp": round(sum(s['temp'] for s in samples)/3, 1), "hum": int(sum(s['hum'] for s in samples)/3), "rain": round(sum(s['rain'] for s in samples)/3, 1)}
        return jsonify({"city": loc['name'], "prediction": pred, "is_future": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)