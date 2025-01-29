const RATE_LIMIT_SECONDS = 3;  // Minimum time between requests (in seconds)
const MAX_WORDS_FOR_REQUEST = 10;

document.getElementById("input-text").addEventListener("input", async function() {
  let prompt = this.value.trim();

  // Check if prompt has less than 10 words and enough time has passed
  const wordCount = prompt.split(/\s+/).length;
  const lastRequestTime = document.getElementById("input-text").dataset.lastRequestTime;
  const currentTime = Math.floor(Date.now() / 1000);

  if (wordCount <= MAX_WORDS_FOR_REQUEST &&
      (!lastRequestTime || (currentTime - lastRequestTime) >= RATE_LIMIT_SECONDS)) {

    try {
      let response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt })
      });

      let result = await response.json();
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      if (result.prediction) {
        document.getElementById("output").innerText = result.prediction;
      } else {
        document.getElementById("output").innerText = "No prediction available";
      }

      // Update last request time for rate limiting
      document.getElementById("input-text").dataset.lastRequestTime = currentTime;

    } catch (error) {
      console.error("Error fetching predictions:", error);
      document.getElementById("output").innerText = "Unable to fetch predictions";
    }
  } else {
    // Don't send request if exceeding word limit or rate limit
    console.log("Skipping request due to word limit or rate limit");
  }
});