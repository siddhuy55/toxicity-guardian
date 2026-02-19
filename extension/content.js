// content.js - Robust Version (FIXED)

const SCANNED_ATTR = "data-tg-scanned";
const MIN_TEXT_LENGTH = 4; 

const SELECTORS = {
    "youtube.com": "#content-text",
    "twitter.com": "[data-testid='tweetText']",
    "x.com": "[data-testid='tweetText']",
    "facebook.com": "div[dir='auto']",
    "instagram.com": "._a9zs, span[dir='auto'], div[dir='auto']", 
    "reddit.com": "p"
};

function getSelector() {
    const host = window.location.hostname;
    for (const key in SELECTORS) {
        if (host.includes(key)) return SELECTORS[key];
    }
    return null;
}

function processNode(node) {
    if (node.getAttribute(SCANNED_ATTR)) return;
    node.setAttribute(SCANNED_ATTR, "true");

    const text = node.innerText.trim();
    if (text.length < MIN_TEXT_LENGTH) return;
    
    // Send to Background Script
    chrome.runtime.sendMessage({ action: "analyze_text", text: text }, (response) => {
        if (chrome.runtime.lastError) {
             // Backend might be down or sleeping
            return;
        }

        if (response && response.success && response.data.is_toxic) {
            console.log("Found TOXIC:", text); 
            censorContent(node, response.data.categories);
        }
    });
}

function censorContent(node, categories) {
    node.style.filter = "blur(6px)";
    node.title = `Hidden: ${categories.join(", ")}`;
    node.style.cursor = "pointer";
    node.style.borderBottom = "2px solid #ef4444"; 

    const revealHandler = (e) => {
        e.preventDefault();
        e.stopPropagation();
        node.style.filter = "none";
        node.style.borderBottom = "none";
        node.removeEventListener("click", revealHandler);
    };
    node.addEventListener("click", revealHandler);
}

// Start Scanning
const selector = getSelector();
if (selector) {
    console.log("Toxicity Guardian: Active with selector:", selector);

    document.querySelectorAll(selector).forEach(processNode);

    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1) { 
                    if (node.matches(selector)) processNode(node);
                    const children = node.querySelectorAll(selector);
                    children.forEach(processNode);
                }
            });
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
}