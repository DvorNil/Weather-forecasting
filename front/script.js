let currentMode = 'forecast';

document.addEventListener('DOMContentLoaded', () => {
    const dateInput = document.getElementById('dateInput');
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('max', today);
    dateInput.value = today;
});


function switchMode(mode) {
    currentMode = mode;
    document.getElementById('dateInput').classList.toggle('hidden', mode === 'forecast');
    document.getElementById('btnForecast').classList.toggle('active', mode === 'forecast');
    document.getElementById('btnTest').classList.toggle('active', mode === 'test');
    document.getElementById('actionBtn').innerText = mode === 'forecast' ? 'Analyze' : 'Run Test';
}

async function handleAction() {
    const city = document.getElementById('cityInput').value;
    const actionBtn = document.getElementById('actionBtn');
    if (!city) return alert("Please enter a city");

    // Start Loading State
    actionBtn.disabled = true;
    const originalText = actionBtn.innerText;
    actionBtn.innerText = "Processing...";

    const endpoint = currentMode === 'forecast' ? '/api/analyze' : '/api/test_algo';
    const payload = { city };
    
    if (currentMode === 'test') {
        payload.date = document.getElementById('dateInput').value;
        if (!payload.date) {
            actionBtn.disabled = false;
            actionBtn.innerText = originalText;
            return alert("Select a date for testing");
        }
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
    } catch (e) { 
        alert(e.message); 
    } finally {
        // Reset Loading State
        actionBtn.disabled = false;
        actionBtn.innerText = originalText;
    }
}

function renderUI(data) {
    document.getElementById('cityName').innerText = data.city;
    const isTest = currentMode === 'test';
    const p = isTest ? data.predicted : {temp: data.prediction, hum: data.humidity_prediction, rain: data.rain_prediction};
    
    document.getElementById('resTemp').innerText = Math.round(p.temp);
    document.getElementById('resHum').innerText = Math.round(p.hum);
    document.getElementById('resRain').innerText = p.rain || 0;

    const accPanel = document.getElementById('accuracyPanel');
    accPanel.classList.toggle('hidden', !isTest);
    if (isTest) document.getElementById('accuracyScore').innerText = data.accuracy + "%";

    ['Temp', 'Hum', 'Rain'].forEach(key => {
        const box = document.getElementById(`act${key}Box`);
        box.classList.toggle('hidden', !isTest);
        if (isTest && data.actual) {
            document.getElementById(`act${key}`).innerText = data.actual[key.toLowerCase()];
        }
    });

    document.getElementById('historyBody').innerHTML = (data.history || []).map(day => `
        <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 12px;">${day.date}</td>
            <td style="padding: 12px;">${Math.round(day.temp_mean)}°C</td>
            <td style="padding: 12px;">${Math.round(day.humidity)}%</td>
            <td style="padding: 12px;">${day.rain} mm</td>
        </tr>`).join('');
    
    document.getElementById('resultArea').classList.remove('hidden');
}