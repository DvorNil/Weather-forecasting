import requests
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory
import math

app = Flask(__name__, static_folder='front')

class WeatherEngine:
    @staticmethod
    def linear_regression_predict(values):
        """
        Implements Simple Linear Regression (Least Squares Method).
        Fits a line y = mx + b to the historical data and predicts the next point.
        """
        n = len(values)
        if n < 2: return values[-1] if values else 0

        # X is time (0, 1, 2...), Y is weather metric
        x = list(range(n))
        y = values

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(i * j for i, j in zip(x, y))
        sum_xx = sum(i * i for i in x)

        # Calculate slope (m) and intercept (b)
        denominator = n * sum_xx - sum_x ** 2
        if denominator == 0: return sum_y / n  # Fallback to average if vertical line
        
        m = (n * sum_xy - sum_x * sum_y) / denominator
        b = (sum_y - m * sum_x) / n

        # Predict for x = n (the next day)
        next_value = m * n + b
        return next_value

    @staticmethod
    def predict_next_day(history):
        """Predicts temperature using Linear Regression to capture warming/cooling trends."""
        if not history: return 0
        temps = [day['temp_mean'] for day in history]
        prediction = WeatherEngine.linear_regression_predict(temps)
        return round(prediction, 1)

    @staticmethod
    def predict_humidity(history):
        """
        Predicts humidity using Exponential Weighted Moving Average (EWMA).
        Recent days have significantly more weight.
        """
        if not history: return 0
        h_values = [day['humidity'] for day in history]
        
        # Alpha 0.7 means 70% weight to recent data (very reactive)
        alpha = 0.7
        weighted_h = h_values[0] 
        for h in h_values[1:]:
            weighted_h = alpha * h + (1 - alpha) * weighted_h
            
        return int(max(0, min(100, weighted_h)))

    @staticmethod
    def predict_rain(history):
        """
        Predicts rain. Uses a threshold: if the trend is very low, assume 0 rain.
        Rain is sporadic, so we dampen negative trends.
        """
        if not history: return 0.0
        rain_vals = [day['rain'] for day in history]
        
        # Use regression but clamp output because rain can't be negative
        prediction = WeatherEngine.linear_regression_predict(rain_vals)
        
        # Logic: If prediction is tiny, round to 0 (rain is binary-ish)
        if prediction < 0.3: return 0.0
        return round(max(0, prediction), 1)

def get_coords(city_name):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        res = requests.get(url, timeout=5).json()
        return res['results'][0] if res.get('results') else None
    except Exception:
        return None

def get_weather_data(lat, lon, start, end):
    url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&"
           f"start_date={start}&end_date={end}&"
           f"daily=temperature_2m_mean,precipitation_sum,relative_humidity_2m_mean&timezone=auto")
    try:
        data = requests.get(url, timeout=5).json()
        d = data.get('daily', {})
        if not d: return []
        
        length = len(d['time'])
        return [{
            "date": d['time'][i],
            "temp_mean": d['temperature_2m_mean'][i],
            "rain": d['precipitation_sum'][i],
            "humidity": d['relative_humidity_2m_mean'][i]
        } for i in range(length)]
    except Exception:
        return []

@app.route('/')
def index():
    return send_from_directory('front', 'index.html')

@app.route('/front/<path:path>')
def serve_static(path):
    return send_from_directory('front', path)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    city = data.get('city')
    if not city: return jsonify({"error": "City required"}), 400

    loc = get_coords(city)
    if not loc: return jsonify({"error": "City not found"}), 404
    
    # Get last 10 days for better trend analysis
    end = datetime.now().date() - timedelta(days=1) # Yesterday as last known point
    start = end - timedelta(days=9) 
    
    history = get_weather_data(loc['latitude'], loc['longitude'], start, end)
    
    # We need at least 3 days for a decent trend
    if len(history) < 3:
        return jsonify({"error": "Not enough historical data available"}), 500

    return jsonify({
        "city": f"{loc['name']}, {loc.get('country', '')}",
        "history": history[::-1], # Reverse for UI (newest first)
        "prediction": WeatherEngine.predict_next_day(history),
        "humidity_prediction": WeatherEngine.predict_humidity(history),
        "rain_prediction": WeatherEngine.predict_rain(history)
    })

@app.route('/api/test_algo', methods=['POST'])
def test_algo():
    data = request.json
    city = data.get('city')
    date_str = data.get('date')
    
    loc = get_coords(city)
    if not loc: return jsonify({"error": "City not found"}), 404
    
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return jsonify({"error": "Invalid date"}), 400
    
    # 1. Input: 7 days BEFORE target
    hist_end = target_date - timedelta(days=1)
    hist_start = target_date - timedelta(days=8) # 8 days range to ensure we get ~7 points
    history = get_weather_data(loc['latitude'], loc['longitude'], hist_start, hist_end)
    
    # 2. Actual: Target date
    actual_data_list = get_weather_data(loc['latitude'], loc['longitude'], target_date, target_date)
    
    if not history or not actual_data_list:
        return jsonify({"error": "Data fetch failed"}), 500

    actual = actual_data_list[0]
    
    # 3. Predict
    pred_temp = WeatherEngine.predict_next_day(history)
    
    # 4. Accuracy (100 - |diff| * 10)
    diff = abs(pred_temp - actual['temp_mean'])
    accuracy = max(0, 100 - (diff * 10))

    return jsonify({
        "city": loc['name'],
        "predicted": {
            "temp": pred_temp,
            "hum": WeatherEngine.predict_humidity(history),
            "rain": WeatherEngine.predict_rain(history)
        },
        "actual": actual,
        "accuracy": round(accuracy, 1),
        "history": history[::-1]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)