async function analyzeWeather() {
    const city = document.getElementById('cityInput').value;
    if (!city) return alert("Введите город");

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

        // Обновление заголовка и основных карточек
        document.getElementById('cityName').innerText = data.city;
        
        // Температура: вставляем только число, так как °C прописан в HTML
        document.getElementById('predictedTemp').innerText = Math.round(data.prediction);
        
        // Влажность: УБРАНО + "%", так как % уже есть в HTML: <span id="predictedHumidity">--</span>%
        const humElement = document.getElementById('predictedHumidity');
        if (humElement) {
            humElement.innerText = Math.round(data.humidity_prediction);
        }
        
        const tbody = document.getElementById('historyBody');

        // Заполнение таблицы истории
        tbody.innerHTML = data.history.map(day => `
            <tr>
                <td>${day.date}</td>
                <td>${Math.round(day.temp_mean)}°C</td>
                <td>${Math.round(day.temp_min)} / ${Math.round(day.temp_max)}°C</td>
                <td>${Math.round(day.humidity)}%</td>
                <td>${day.rain} мм</td>
            </tr>
        `).join('');

        results.classList.remove('hidden');
    } catch (e) {
        alert("Ошибка: " + e.message);
    } finally {
        loader.classList.add('hidden');
    }
}

async function runTest() {
    const city = document.getElementById('cityInput').value;
    const date = document.getElementById('dateInput').value;
    if(!city || !date) return alert("Заполните все поля");

    const testResult = document.getElementById('testResult');
    testResult.classList.add('hidden'); 

    try {
        const res = await fetch('/api/test_algo', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({city, date})
        });
        const data = await res.json();

        if (!res.ok) throw new Error(data.error);
        
        // 1. Сравнение Температуры (в test.html обычно ед. изм. добавляют через JS)
        document.getElementById('resPred').innerText = Math.round(data.predicted_temp) + "°C";
        document.getElementById('resActual').innerText = (data.actual_temp !== null ? Math.round(data.actual_temp) : "Н/Д") + "°C";
        
        // 2. Сравнение Влажности
        const humPredEl = document.getElementById('resHumPred');
        const humActEl = document.getElementById('resHumActual');
        if (humPredEl) humPredEl.innerText = Math.round(data.predicted_hum) + "%";
        if (humActEl) humActEl.innerText = (data.actual_hum !== null ? Math.round(data.actual_hum) : "Н/Д") + "%";

        document.getElementById('resError').innerText = "Погрешность (t°): " + data.error_temp + "°C";

        // 3. Таблица истории в тесте
        const tbody = document.getElementById('testHistoryBody');
        tbody.innerHTML = data.history.map(day => `
            <tr>
                <td>${day.date}</td>
                <td>${Math.round(day.temp_mean)}°C</td>
                <td>${Math.round(day.temp_min)} / ${Math.round(day.temp_max)}°C</td>
                <td>${Math.round(day.humidity)}%</td>
                <td>${day.rain} мм</td>
            </tr>
        `).join('');

        testResult.classList.remove('hidden');
    } catch (e) {
        alert("Ошибка теста: " + e.message);
    }
}