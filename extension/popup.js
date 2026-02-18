document.addEventListener('DOMContentLoaded', () => {
    const sensitivityInput = document.getElementById('sensitivity');
    const sensDisplay = document.getElementById('sens-display');
    const saveBtn = document.getElementById('save-btn');

    // 1. Load Saved Settings
    chrome.storage.local.get(['sensitivity'], (result) => {
        if (result.sensitivity) {
            sensitivityInput.value = result.sensitivity;
            sensDisplay.textContent = result.sensitivity + "%";
        }
    });

    // 2. Update Display on Slide
    sensitivityInput.addEventListener('input', (e) => {
        sensDisplay.textContent = e.target.value + "%";
    });

    // 3. Save Settings
    saveBtn.addEventListener('click', () => {
        const val = sensitivityInput.value;
        chrome.storage.local.set({ sensitivity: val }, () => {
            saveBtn.textContent = "Saved!";
            setTimeout(() => saveBtn.textContent = "Save Settings", 1500);
        });
    });
});