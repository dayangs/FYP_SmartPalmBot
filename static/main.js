// main.js

// 1) Smooth scroll for side-nav
document.querySelectorAll('.nav-icon').forEach(icon => {
  icon.addEventListener('click', () => {
    const target = document.getElementById(icon.dataset.target);
    if (target) target.scrollIntoView({ behavior: 'smooth' });
  });
});

// 2) Simple chatbot placeholder

function sendMsg() {
  const text = userInput.value.trim();
  if (!text) return;
  chatlog.innerHTML += `<div class="chat user">${text}</div>`;
  userInput.value = '';
  // fake bot reply
  setTimeout(() => {
    const reply = '🤖 Sorry, the API connection is not active. For now, I’m unable to respond..';
    chatlog.innerHTML += `<div class="chat bot">${reply}</div>`;
    chatlog.scrollTop = chatlog.scrollHeight;
  }, 500);
}

sendBtn.addEventListener('click', sendMsg);
userInput.addEventListener('keypress', e => {
  if (e.key === 'Enter') sendMsg();
});

// 3) Poll sensor data every minute
async function fetchSensor() {
  try {
    const res = await fetch('/api/sensor');
    if (!res.ok) throw new Error('Network error');
    const { temperature, humidity, weather } = await res.json();
    document.getElementById('tempValue').textContent = `${temperature}°C`;
    document.getElementById('humValue').textContent  = `${humidity}%`;
    document.getElementById('weatherValue').textContent = weather;
  } catch (err) {
    console.warn('Sensor fetch failed:', err);
  }
}

setInterval(fetchSensor, 60_000);
fetchSensor();
