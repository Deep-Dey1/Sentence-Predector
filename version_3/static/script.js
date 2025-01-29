document.getElementById("input-text").addEventListener("input", async function() {
    let prompt = this.value;

    if (prompt.length > 0) {
        try {
            let response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: prompt })
            });

            let result = await response.json();
            console.log("Response from Flask:", result); // Debugging

            if (result.prediction) {
                document.getElementById("output").innerText = result.prediction;
            } else {
                document.getElementById("output").innerText = "No prediction available";
            }
        } catch (error) {
            console.error("Error fetching predictions:", error);
            document.getElementById("output").innerText = "Unable to fetch predictions";
        }
    }
});
