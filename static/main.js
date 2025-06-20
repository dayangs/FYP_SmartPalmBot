// main.js

// 1) Smooth scroll for side-nav
document.querySelectorAll('.nav-icon').forEach(icon => {
  icon.addEventListener('click', () => {
    const target = document.getElementById(icon.dataset.target);
    if (target) target.scrollIntoView({ behavior: 'smooth' });
  });
});

// 2) Chatbot interaction logic
const userInput = document.getElementById("text");
const sendBtn = document.getElementById("send");
const chatlog = document.getElementById("messageFormeight");

// Get chatbot logo source from hidden span
const botLogo = document.getElementById("botLogo")?.getAttribute("data-src") || "https://i.ibb.co/d5b84Xw/Untitled-design.png";

function scrollToBottom() {
  chatlog.scrollTop = chatlog.scrollHeight;
}

function sendMsg() {
  const text = userInput.value.trim();
  if (!text) return;

  const date = new Date();
  const time = `${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;

  const userHtml = `
    <div class="d-flex justify-content-end mb-4">
      <div class="msg_cotainer_send">${text}<span class="msg_time_send">${time}</span></div>
      <div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div>
    </div>`;
  chatlog.innerHTML += userHtml;
  userInput.value = '';
  scrollToBottom();

  fetch("/get", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ msg: text }),
  })
    .then((res) => res.text())
    .then((data) => {
      const botHtml = `
        <div class="d-flex justify-content-start mb-4">
          <div class="img_cont_msg"><img src="${botLogo}" class="rounded-circle user_img_msg"></div>
          <div class="msg_cotainer">${data}<span class="msg_time">${time}</span></div>
        </div>`;
      chatlog.innerHTML += botHtml;
      scrollToBottom();
    })
    .catch((err) => {
      const errorMsg = `<div class="chat bot">⚠️ Connection failed: ${err.message}</div>`;
      chatlog.innerHTML += errorMsg;
      scrollToBottom();
    });
}

sendBtn.addEventListener("click", sendMsg);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMsg();
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
