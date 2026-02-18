console.log("🔥 BACKGROUND SCRIPT IS ALIVE!");
// Handles communication between Content Script and Backend API
const API_URL = "http://localhost:8000/analyze";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "analyze_text") {
    
    // Fetch user settings for sensitivity before calling API
    chrome.storage.local.get(['sensitivity'], (result) => {
        const threshold = (result.sensitivity || 70) / 100;

        fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
              text: request.text,
              threshold: threshold
          })
        })
        .then(response => response.json())
        .then(data => sendResponse({ success: true, data: data }))
        .catch(error => {
            console.error("API Error:", error);
            sendResponse({ success: false, error: error.message });
        });
    });

    return true; // Keep channel open for async response
  }
});