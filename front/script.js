let currentMode = 'forecast';

function switchMode(mode) {
    currentMode = mode;
    document.getElementById('dateInput').classList.toggle('hidden', mode === 'forecast');
    document.getElementById('btnForecast').classList.toggle('active', mode === 'forecast');
    document.getElementById('btnTest').classList.toggle('active', mode === 'test');
    document.getElementById('actionBtn').innerText = mode === 'forecast' ? 'Analyze' : 'Run Test';
}

async function handleAction() {
    const city = document.getElementById('cityInput').value;
    if (!city) return alert("Enter city name");

    toggleLoading(true);
    const endpoint = currentMode === 'forecast' ? '/api/analyze' : '/api/test_algo';
    const payload = { city };
    if (currentMode === 'test') {
        payload.date = document.getElementById('dateInput').value;
        if (!payload.date) { toggleLoading(false); return alert("Select a date"); }
    }

    try {
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);

        renderUI(data);
    } catch (e) { alert(e.message); }
    finally { toggleLoading(false); }
}

function renderUI(data) {
    document.getElementById('displayCity').innerText = data.city;
    const isTest = currentMode === 'test';
    const p = isTest ? data.predicted : {temp: data.temp_pred, hum: data.hum_pred, rain: data.rain_pred};
    
    document.getElementById('resTemp').innerText = Math.round(p.temp);
    document.getElementById('resHum').innerText = Math.round(p.hum);
    document.getElementById('resRain').innerText = p.rain;

    ['Temp', 'Hum', 'Rain'].forEach(key => {
        const box = document.getElementById(`act${key}Box`);
        box.classList.toggle('hidden', !isTest);
        if (isTest && data.actual) {
            document.getElementById(`act${key}`).innerText = data.actual[key.toLowerCase()];
        }
    });

    document.getElementById('historyBody').innerHTML = data.history.map(day => `
        <tr>
            <td>${day.date}</td>
            <td>${Math.round(day.temp_mean)}°C</td>
            <td>${Math.round(day.temp_min)} / ${Math.round(day.temp_max)}°C</td>
            <td>${Math.round(day.humidity)}%</td>
            <td>${day.rain} mm</td>
        </tr>`).join('');
    document.getElementById('resultArea').classList.remove('hidden');
}

function toggleLoading(isLoading) {
    document.getElementById('loading').classList.toggle('hidden', !isLoading);
    if (isLoading) document.getElementById('resultArea').classList.add('hidden');
}