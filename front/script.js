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

        document.getElementById('cityName').innerText = data.city;
        document.getElementById('predictedTemp').innerText = data.prediction;
        
        const tbody = document.getElementById('historyBody');

        tbody.innerHTML = data.history.map(day => `
            <tr>
                <td>${day.date}</td>
                <td>${Math.round(day.temp_mean)}°C</td>
                <td>${Math.round(day.temp_min)} / ${Math.round(day.temp_max)}°C</td>
                <td>${day.rain} мм</td>
            </tr>
        `).join('');

        document.getElementById('predictedTemp').innerText = Math.round(data.prediction);

        results.classList.remove('hidden');
    } catch (e) {
        alert(e.message);
    } finally {
        loader.classList.add('hidden');
    }
}

async function runTest() {
            const city = document.getElementById('cityInput').value;
            const date = document.getElementById('dateInput').value;
            if(!city || !date) return alert("Заполните все поля");

            const testResult = document.getElementById('testResult');
            testResult.classList.add('hidden'); // Скрываем на время загрузки

            try {
                const res = await fetch('/api/test_algo', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({city, date})
                });
                const data = await res.json();

                if (!res.ok) throw new Error(data.error);
                
                // 1. Показываем карточки сравнения
                document.getElementById('resPred').innerText = Math.round(data.predicted) + "°C";
                document.getElementById('resActual').innerText = (data.actual !== null ? Math.round(data.actual) : "Н/Д") + "°C";
                document.getElementById('resError').innerText = "Погрешность алгоритма: " + Math.round(data.error) + "°C";

                // 2. Отрисовываем историю
                const tbody = document.getElementById('testHistoryBody');
                tbody.innerHTML = data.history.map(day => `
                    <tr>
                        <td>${day.date}</td>
                        <td>${Math.round(day.temp_mean)}°C</td>
                        <td>${Math.round(day.temp_min)} / ${Math.round(day.temp_max)}°C</td>
                        <td>${day.rain} мм</td>
                    </tr>
                `).join('');

                testResult.classList.remove('hidden');
            } catch (e) {
                alert("Ошибка: " + e.message);
            }
        }