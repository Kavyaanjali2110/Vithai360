async function getRecommendation(event){
event.preventDefault();

const btn = document.getElementById("btn");
const resultBox = document.getElementById("result");

btn.disabled = true;
btn.innerText = "Processing...";

const soil = document.getElementById("soil").value.trim().toLowerCase();
const location = document.getElementById("location").value.trim().toLowerCase();

resultBox.innerHTML = "⏳ Getting AI recommendation...";

try {

const response = await fetch("http://127.0.0.1:8000/recommend", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({
soil: soil,
location: location
})
});

const data = await response.json();
console.log(data);

// ❌ backend error
if(!response.ok || data.error){
resultBox.innerHTML = "❌ " + (data.error || "Server error");
return;
}

// ✅ flexible crop handling (VERY IMPORTANT)
const crop =
    data.crop ||
    data.recommendation?.best_crop ||
    "Not found";

// ✅ weather safe
const weather = data.weather || {};
let weatherHTML = "";

if(!weather || weather.error || weather.temperature === undefined){
weatherHTML = `<p>❌ Weather not available</p>`;
}else{
weatherHTML = `
<h3>🌦 Weather</h3>
<p>🌡 Temperature: ${weather.temperature} °C</p>
<p>💧 Humidity: ${weather.humidity}%</p>
<p>🌤 Condition: ${weather.condition}</p>
`;
}

// ✅ NEW FEATURES (safe fallback)
const irrigation = data.irrigation || "Not available";
const fertilizer = data.fertilizer || "Not available";
const pesticide = data.pesticide || "Not available";
const duration = data.duration || "Not available";

// ✅ FINAL UI
resultBox.innerHTML = `
<h3>📍 Location: ${location}</h3>
<p>🌱 Soil: ${soil}</p>

<h3 style="color:green">🌾 Best Recommended Crop</h3>
<div class="best">🥇 ${crop}</div>

${weatherHTML}

<h3>💧 Irrigation Advice</h3>
<p>${irrigation}</p>

<h3>🌿 Fertilizer Recommendation</h3>
<p>${fertilizer}</p>

<h3>🐛 Pesticide Advice</h3>
<p>${pesticide}</p>

<h3>⏳ Cultivation Duration</h3>
<p>${duration}</p>
`;

} catch(err){
console.log(err);
resultBox.innerHTML = "❌ Backend not connected or server error";
}

// always reset button
btn.disabled = false;
btn.innerText = "Get Recommendation";
}