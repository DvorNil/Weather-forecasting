async function analyzeWeather() {
    const city = document.getElementById('cityInput').value;
    if (!city) return alert("Please enter a city name");

    const loader = document.getElementById('loading');
    const results = document.getElementById('resultArea');
    
    loader.classList.remove('hidden');
    results.classList.add('hidden');

    try {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ city })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);

        // Map data to UI
        document.getElementById('cityName').innerText = data.city;
        document.getElementById('predictedTemp').innerText = Math.round(data.temp_pred);
        document.getElementById('predictedHumidity').innerText = Math.round(data.hum_pred);
        document.getElementById('predictedRain').innerText = data.rain_pred;
        
        const tbody = document.getElementById('historyBody');
        tbody.innerHTML = data.history.map(day => `
            <tr>
                <td>${day.date}</td>
                <td>${Math.round(day.temp_mean)}°C</td>
                <td>${Math.round(day.temp_min)} / ${Math.round(day.temp_max)}°C</td>
                <td>${Math.round(day.humidity)}%</td>
                <td>${day.rain} mm</td>
            </tr>
        `).join('');

        results.classList.remove('hidden');
    } catch (e) {
        alert("Error: " + e.message);
    } finally {
        loader.classList.add('hidden');
    }
}