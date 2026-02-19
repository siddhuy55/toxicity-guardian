// background.js - Cloud Version ☁️
console.log("🔥 BACKGROUND SCRIPT IS ALIVE & CONNECTED TO CLOUD!");

// 🟢 TO RUN LOCALLY (ON YOUR LAPTOP): Uncomment the line below
// const API_URL = "http://127.0.0.1:8000/analyze";

// ✅ UPDATED: Pointing to your live Render server
const API_URL = "https://toxicity-guardian-api.onrender.com/analyze";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "analyze_text") {
    
    // Fetch user settings (default threshold 60%)
    chrome.storage.local.get(['sensitivity'], (result) => {
        const threshold = (result.sensitivity || 60) / 100;

        fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
              text: request.text,
              threshold: threshold
          })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server Error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("✅ Cloud Analysis Result:", data);
            sendResponse({ success: true, data: data });
        })
        .catch(error => {
            console.error("❌ Connection Failed:", error);
            // If server is waking up (Spinning up), it might fail once. That's okay.
            sendResponse({ success: false, error: error.message });
        });
    });

    return true; // Keep channel open for async response
  }
});