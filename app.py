import requests
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='front')

class WeatherEngine:
    @staticmethod
    def predict_next_day(history):
        if not history or len(history) < 3: return 0
        temps = [day['temp_mean'] for day in history]
        # Взвешенное среднее + тренд
        weighted_avg = (temps[-1] * 0.5) + (temps[-2] * 0.3) + (temps[-3] * 0.2)
        trend = (temps[-1] - temps[0]) / len(temps)
        return round(weighted_avg + trend, 1)

def get_coords(city_name):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru&format=json"
        res = requests.get(url).json()
        return res['results'][0] if res.get('results') else None
    except: return None

def get_weather_data(lat, lon, start, end):
    url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&"
           f"start_date={start}&end_date={end}&"
           f"daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto")
    data = requests.get(url).json()
    if 'daily' not in data: return []
    
    d = data['daily']
    return [{
        "date": d['time'][i],
        "temp_mean": d['temperature_2m_mean'][i],
        "temp_max": d['temperature_2m_max'][i],
        "temp_min": d['temperature_2m_min'][i],
        "rain": d['precipitation_sum'][i]
    } for i in range(len(d['time']))]

@app.route('/')
def index(): return send_from_directory('front', 'index.html')

@app.route('/test')
def test_page(): return send_from_directory('front', 'test.html')

@app.route('/<path:path>')
def static_files(path): return send_from_directory('front', path)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    city = request.json.get('city')
    loc = get_coords(city)
    if not loc: return jsonify({"error": "Город не найден"}), 404
    
    end = datetime.now().date() - timedelta(days=1)
    start = end - timedelta(days=7)
    
    history = get_weather_data(loc['latitude'], loc['longitude'], start, end)
    prediction = WeatherEngine.predict_next_day(history)
    
    return jsonify({
        "city": f"{loc['name']}, {loc.get('country', '')}",
        "history": history[::-1],
        "prediction": prediction
    })

@app.route('/api/test_algo', methods=['POST'])
def test_algo():
    city = request.json.get('city')
    date_str = request.json.get('date')
    loc = get_coords(city)
    if not loc: return jsonify({"error": "Город не найден"}), 404
    
    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Получаем историю за неделю ДО целевой даты
    history = get_weather_data(loc['latitude'], loc['longitude'], 
                               target_date - timedelta(days=7), 
                               target_date - timedelta(days=1))
    
    # Получаем данные за сам целевой день (факт)
    actual_data = get_weather_data(loc['latitude'], loc['longitude'], target_date, target_date)
    
    predicted = WeatherEngine.predict_next_day(history)
    actual = actual_data[0]['temp_mean'] if actual_data else None
    
    return jsonify({
        "city": loc['name'],
        "predicted": predicted,
        "actual": actual,
        "error": round(abs(predicted - actual), 1) if actual is not None else "N/A",
        "history": history[::-1]  # Добавляем историю в ответ (от новых к старым)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)