import requests
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='front')

class WeatherEngine:
    @staticmethod
    def predict_next_day(history):
        """Calculates temperature prediction using weighted average and linear trend."""
        if not history or len(history) < 3: return 0
        temps = [day['temp_mean'] for day in history]
        # Weighted average: Yesterday (50%), 2 days ago (30%), 3 days ago (20%)
        weighted_avg = (temps[-1] * 0.5) + (temps[-2] * 0.3) + (temps[-3] * 0.2)
        # Trend calculation over the sample period
        trend = (temps[-1] - temps[0]) / len(history)
        return round(weighted_avg + trend, 1)

    @staticmethod
    def predict_humidity(history):
        """Predicts humidity using high-persistence weighting."""
        if not history or len(history) < 3: return 0
        h_values = [day['humidity'] for day in history]
        weighted_h = (h_values[-1] * 0.6) + (h_values[-2] * 0.3) + (h_values[-3] * 0.1)
        return int(max(0, min(100, weighted_h)))

    @staticmethod
    def predict_rain(history):
        """Estimates rain volume based on recent precipitation persistence."""
        if not history: return 0.0
        rain_vals = [day['rain'] for day in history]
        prediction = (rain_vals[-1] * 0.7) + (rain_vals[-2] * 0.2) + (rain_vals[-3] * 0.1)
        return round(max(0, prediction), 1)

def get_coords(city_name):
    """Retrieves latitude and longitude for a given city."""
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        res = requests.get(url).json()
        return res['results'][0] if res.get('results') else None
    except Exception:
        return None

def get_weather_data(lat, lon, start, end):
    """Fetches historical weather records from the archive API."""
    url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&"
           f"start_date={start}&end_date={end}&"
           f"daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,"
           f"precipitation_sum,relative_humidity_2m_mean&timezone=auto")
    try:
        data = requests.get(url).json()
        d = data['daily']
        return [{
            "date": d['time'][i],
            "temp_mean": d['temperature_2m_mean'][i],
            "temp_max": d['temperature_2m_max'][i],
            "temp_min": d['temperature_2m_min'][i],
            "rain": d['precipitation_sum'][i],
            "humidity": d['relative_humidity_2m_mean'][i]
        } for i in range(len(d['time']))]
    except Exception:
        return []

@app.route('/')
def index():
    return send_from_directory('front', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Route for Live Forecast mode based on the current week's data."""
    city = request.json.get('city')
    loc = get_coords(city)
    if not loc: return jsonify({"error": "City not found"}), 404
    
    # Archive data is usually available with a 2-day delay
    end = datetime.now().date() - timedelta(days=2)
    start = end - timedelta(days=7)
    
    history = get_weather_data(loc['latitude'], loc['longitude'], start, end)
    
    return jsonify({
        "city": f"{loc['name']}, {loc.get('country', '')}",
        "history": history[::-1],
        "prediction": WeatherEngine.predict_next_day(history),
        "humidity_prediction": WeatherEngine.predict_humidity(history),
        "rain_prediction": WeatherEngine.predict_rain(history)
    })

@app.route('/api/test_algo', methods=['POST'])
def test_algo():
    """Route for Algorithm Test mode: Compares AI prediction vs Actual history."""
    city = request.json.get('city')
    date_str = request.json.get('date')
    loc = get_coords(city)
    if not loc: return jsonify({"error": "City not found"}), 404
    
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        return jsonify({"error": "Invalid date format"}), 400
    
    # 1. Fetch 7 days prior to target date for the AI input
    hist_start = target_date - timedelta(days=7)
    hist_end = target_date - timedelta(days=1)
    history = get_weather_data(loc['latitude'], loc['longitude'], hist_start, hist_end)
    
    # 2. Fetch actual data for the target date itself
    actual_data = get_weather_data(loc['latitude'], loc['longitude'], target_date, target_date)
    
    # 3. Calculate Predictions and Actuals
    p_temp = WeatherEngine.predict_next_day(history)
    a_temp = actual_data[0]['temp_mean'] if actual_data else 0
    
    # 4. Accuracy Logic: 100% minus 10% for every 1°C of error
    accuracy = max(0, 100 - (abs(p_temp - a_temp) * 10))
    
    return jsonify({
        "city": loc['name'],
        "predicted": {
            "temp": p_temp, 
            "hum": WeatherEngine.predict_humidity(history), 
            "rain": WeatherEngine.predict_rain(history)
        },
        "actual": {
            "temp": a_temp, 
            "hum": actual_data[0]['humidity'] if actual_data else 0, 
            "rain": actual_data[0]['rain'] if actual_data else 0
        },
        "accuracy": round(accuracy, 1),
        "history": history[::-1]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)