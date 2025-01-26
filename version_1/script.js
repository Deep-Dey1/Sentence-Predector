document.getElementById("predictBtn").addEventListener("click", function() {
    let userInput = document.getElementById("inputBox").value;
    
    document.getElementById("outputBox").innerText = "Predicting...";

    fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userInput })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("outputBox").innerText = data.prediction;
    })
    .catch(error => console.error("Error:", error));
});
