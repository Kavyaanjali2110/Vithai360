function getRecommendation(event) {
    event.preventDefault();

    const soil = document.getElementById("soil").value;
    const season = document.getElementById("season").value;


    let crop = "";
    let reason = "";


    if (soil === "Black") {
        if (season === "monsoon") {
            crop = "🌾 Cotton / Wheat";
            reason = "Black soil retains moisture and is suitable during monsoon.";
        } else if (season === "winter") {
            crop = "🌿 Wheat";
            reason = "Winter season with black soil favors wheat cultivation.";
        } else {
            crop = "🌻 Sunflower";
            reason = "Sunflower grows well in black soil during summer.";
        }
    }

    
    else if (soil === "Loamy") {
        if (season === "monsoon") {
            crop = "🌾 Rice";
            reason = "Loamy soil holds nutrients and water, ideal for rice.";
        } else if (season === "winter") {
            crop = "🥕 Vegetables";
            reason = "Cool climate and loamy soil suit vegetables.";
        } else {
            crop = "🌽 Maize";
            reason = "Loamy soil and summer season support maize growth.";
        }
    }

    
    else if (soil === "Sandy") {
        if (season === "monsoon") {
            crop = "🥜 Groundnut";
            reason = "Sandy soil drains well and supports groundnut.";
        } else if (season === "winter") {
            crop = "🌾 Millets";
            reason = "Millets require less water and grow in sandy soil.";
        } else {
            crop = "🌾 Millets";
            reason = "Sandy soil with low moisture favors millets.";
        }
    }

    
    else if (soil === "Clay") {
        if (season === "monsoon") {
            crop = "🌱 Rice";
            reason = "Clay soil retains water, making it suitable for rice.";
        } else if (season === "winter") {
            crop = "🌾 Wheat";
            reason = "Clay soil can support wheat with proper drainage.";
        } else {
            crop = "🌿 Sugarcane";
            reason = "Clay soil with adequate water is good for sugarcane.";
        }
    }

    
    document.getElementById("result").innerHTML = `
        <h3>🌾 Recommended Crop</h3>
        <p><strong>${crop}</strong></p>
        <p>${reason}</p>
    `;

}
