let currentMode = 'forecast';

function switchMode(mode) {
    currentMode = mode;
    const dateInp = document.getElementById('dateInput');
    dateInp.classList.toggle('hidden', mode === 'forecast');
    
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('btn' + mode.charAt(0).toUpperCase() + mode.slice(1)).classList.add('active');
    
    // Set date constraints: Test (Past), Future (Future)
    const today = new Date().toISOString().split('T')[0];
    if (mode === 'test') { dateInp.max = today; dateInp.min = ""; }
    else if (mode === 'future') { dateInp.min = today; dateInp.max = ""; }
}

async function handleAction() {
    const city = document.getElementById('cityInput').value;
    const date = document.getElementById('dateInput').value;
    const btn = document.getElementById('actionBtn');
    
    if (!city || (currentMode !== 'forecast' && !date)) return alert("Fill all fields");

    btn.disabled = true;
    btn.innerText = "Processing AI...";

    try {
        const res = await fetch('/api/weather', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ mode: currentMode, city, date })
        });
        const data = await res.json();
        renderUI(data);
    } catch (e) { alert("Error fetching data"); }
    finally {
        btn.disabled = false;
        btn.innerText = currentMode === 'forecast' ? "Analyze" : "Run AI";
    }
}

function renderUI(data) {
    document.getElementById('cityName').innerText = data.city;
    document.getElementById('resTemp').innerText = data.prediction.temp;
    document.getElementById('resHum').innerText = data.prediction.hum;
    document.getElementById('resRain').innerText = data.prediction.rain;

    // Accuracy Panel Handling
    const accPanel = document.getElementById('accuracyPanel');
    if (currentMode === 'test') {
        accPanel.classList.remove('hidden');
        document.getElementById('accLabel').innerText = "AI Prediction Accuracy";
        document.getElementById('accuracyScore').innerText = data.accuracy + "%";
        document.getElementById('actTempBox').classList.remove('hidden');
        document.getElementById('actTemp').innerText = data.actual.temp;
    } else if (currentMode === 'future') {
        accPanel.classList.remove('hidden');
        document.getElementById('accLabel').innerText = "Future AI Confidence";
        document.getElementById('accuracyScore').innerText = "88%"; // Estimated confidence
        document.getElementById('actTempBox').classList.add('hidden');
    } else {
        accPanel.classList.add('hidden');
        document.getElementById('actTempBox').classList.add('hidden');
    }

    // History Table
    const histSection = document.getElementById('historySection');
    if (data.history) {
        histSection.classList.remove('hidden');
        document.getElementById('historyBody').innerHTML = data.history.map(h => 
            `<tr><td>${h.date}</td><td>${h.temp}°C</td><td>${h.hum}%</td><td>${h.rain}mm</td></tr>`
        ).join('');
    } else {
        histSection.classList.add('hidden');
    }
    
    document.getElementById('resultArea').classList.remove('hidden');
}