import requests
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='front')

class WeatherEngine:
    @staticmethod
    def predict_next_day(history):
        if not history or len(history) < 3: return 0
        temps = [day['temp_mean'] for day in history]
        weighted_avg = (temps[-1] * 0.5) + (temps[-2] * 0.3) + (temps[-3] * 0.2)
        trend = (temps[-1] - temps[0]) / len(temps)
        return round(weighted_avg + trend, 1)

    @staticmethod
    def predict_humidity(history):
        if not history or len(history) < 3: return 0
        h_values = [day['humidity'] for day in history]
        weighted_h = (h_values[-1] * 0.6) + (h_values[-2] * 0.3) + (h_values[-3] * 0.1)
        return int(max(0, min(100, weighted_h)))

    @staticmethod
    def predict_precipitation(history):
        """Predicts precipitation probability based on recent rain volume and frequency."""
        if not history: return 0.0
        rain_values = [day['rain'] for day in history]
        # Recent rain is the strongest indicator of tomorrow's rain
        prediction = (rain_values[-1] * 0.7) + (rain_values[-2] * 0.2) + (rain_values[-3] * 0.1)
        return round(max(0, prediction), 1)

def get_coords(city_name):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        res = requests.get(url).json()
        return res['results'][0] if res.get('results') else None
    except: return None

def get_weather_data(lat, lon, start, end):
    url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&"
           f"start_date={start}&end_date={end}&"
           f"daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,"
           f"precipitation_sum,relative_humidity_2m_mean&timezone=auto")
    try:
        data = requests.get(url).json()
        if 'daily' not in data: return []
        d = data['daily']
        return [{
            "date": d['time'][i],
            "temp_mean": d['temperature_2m_mean'][i],
            "temp_max": d['temperature_2m_max'][i],
            "temp_min": d['temperature_2m_min'][i],
            "rain": d['precipitation_sum'][i],
            "humidity": d['relative_humidity_2m_mean'][i]
        } for i in range(len(d['time']))]
    except: return []

@app.route('/')
def index(): return send_from_directory('front', 'index.html')

@app.route('/front/<path:path>')
def static_files(path): return send_from_directory('front', path)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    city = request.json.get('city')
    if not city: return jsonify({"error": "City name required"}), 400
    loc = get_coords(city)
    if not loc: return jsonify({"error": "City not found"}), 404
    
    end = datetime.now().date() - timedelta(days=2)
    start = end - timedelta(days=7)
    history = get_weather_data(loc['latitude'], loc['longitude'], start, end)
    
    return jsonify({
        "city": f"{loc['name']}, {loc.get('country', '')}",
        "history": history[::-1],
        "temp_pred": WeatherEngine.predict_next_day(history),
        "hum_pred": WeatherEngine.predict_humidity(history),
        "rain_pred": WeatherEngine.predict_precipitation(history)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)