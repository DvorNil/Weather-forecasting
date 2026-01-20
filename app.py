import requests
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='front')

class WeatherEngine:
    @staticmethod
    def predict_next_day(history):
        """Predicts temperature using weighted average and trend."""
        if not history or len(history) < 3: return 0
        temps = [day['temp_mean'] for day in history]
        # Weighted average (Recent days have more impact)
        weighted_avg = (temps[-1] * 0.5) + (temps[-2] * 0.3) + (temps[-3] * 0.2)
        # Linear trend calculation
        trend = (temps[-1] - temps[0]) / len(temps)
        return round(weighted_avg + trend, 1)

    @staticmethod
    def predict_humidity(history):
        """Predicts humidity using Exponential Moving Average logic."""
        if not history or len(history) < 3: return 0
        h_values = [day['humidity'] for day in history]
        # Humidity persists more than temperature changes
        # Using a 60/30/10 weight distribution
        weighted_h = (h_values[-1] * 0.6) + (h_values[-2] * 0.3) + (h_values[-3] * 0.1)
        # Clamp between 0 and 100%
        return int(max(0, min(100, weighted_h)))

def get_coords(city_name):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru&format=json"
        res = requests.get(url).json()
        return res['results'][0] if res.get('results') else None
    except: return None

def get_weather_data(lat, lon, start, end):
    """Fetches archive data including temperature and humidity."""
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
    except Exception as e:
        print(f"Data Fetch Error: {e}")
        return []

# --- ROUTES ---

@app.route('/')
def index(): 
    return send_from_directory('front', 'index.html')

@app.route('/test')
def test_page(): 
    return send_from_directory('front', 'test.html')

@app.route('/front/<path:path>')
def static_files(path): 
    return send_from_directory('front', path)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    city = request.json.get('city')
    if not city: return jsonify({"error": "Введите город"}), 400
    
    loc = get_coords(city)
    if not loc: return jsonify({"error": "Город не найден"}), 404
    
    # Open-Meteo Archive has a 2-day delay for free tier usually
    end = datetime.now().date() - timedelta(days=2)
    start = end - timedelta(days=7)
    
    history = get_weather_data(loc['latitude'], loc['longitude'], start, end)
    if not history: return jsonify({"error": "Данные погоды недоступны"}), 500

    temp_prediction = WeatherEngine.predict_next_day(history)
    hum_prediction = WeatherEngine.predict_humidity(history)
    
    return jsonify({
        "city": f"{loc['name']}, {loc.get('country', '')}",
        "history": history[::-1], # Newest first for the table
        "prediction": temp_prediction,
        "humidity_prediction": hum_prediction
    })

@app.route('/api/test_algo', methods=['POST'])
def test_algo():
    city = request.json.get('city')
    date_str = request.json.get('date')
    loc = get_coords(city)
    if not loc: return jsonify({"error": "Город не найден"}), 404
    
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return jsonify({"error": "Неверный формат даты"}), 400
    
    history = get_weather_data(loc['latitude'], loc['longitude'], 
                               target_date - timedelta(days=7), 
                               target_date - timedelta(days=1))
    
    actual_data = get_weather_data(loc['latitude'], loc['longitude'], target_date, target_date)
    
    predicted_temp = WeatherEngine.predict_next_day(history)
    predicted_hum = WeatherEngine.predict_humidity(history)
    
    actual_temp = actual_data[0]['temp_mean'] if actual_data else None
    actual_hum = actual_data[0]['humidity'] if actual_data else None
    
    return jsonify({
        "city": loc['name'],
        "predicted_temp": predicted_temp,
        "actual_temp": actual_temp,
        "predicted_hum": predicted_hum,
        "actual_hum": actual_hum,
        "error_temp": round(abs(predicted_temp - actual_temp), 1) if actual_temp is not None else "N/A",
        "history": history[::-1]
    })

if __name__ == '__main__':
    # Using 0.0.0.0 allows access from other devices on your network
    app.run(debug=True, host='0.0.0.0', port=5000)