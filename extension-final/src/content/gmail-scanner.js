/**
 * SecureSentinel Universal Scanner
 * 
 * Works on ALL websites.
 * 1. Checks if it's Gmail (uses deep scanning).
 * 2. If not, uses generic page scanning.
 * 3. Proxies all requests through background script.
 */

console.log("%c[WebSentinel] ACTIVE", "font-size: 16px; color: cyan;");

if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    const existing = document.getElementById('ss-status-panel');
    if (existing) existing.remove();
}

const scannedContent = new Set();
let statusPanel = null;
let lastScanResult = null; // CACHE FOR POPUP

// ============================================
// UI: UNIVERSAL STATUS PANEL
// ============================================
function createStatusPanel() {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        const existing = document.getElementById('ss-status-panel');
        if (existing) existing.remove();
        return;
    }

    if (document.getElementById('ss-status-panel')) return;

    const panel = document.createElement('div');
    panel.id = 'ss-status-panel';
    panel.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #09090b;
        color: white;
        padding: 10px 14px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        z-index: 2147483647;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
        border: 1px solid #27272a;
        transition: all 0.3s ease;
        cursor: default;
        user-select: none;
    `;

    const dot = document.createElement('div');
    dot.id = 'ss-status-dot';
    dot.style.cssText = "width: 8px; height: 8px; background: #71717a; border-radius: 50%; transition: all 0.3s;";

    const content = document.createElement('div');
    content.innerHTML = `
        <div style="font-weight: 800; font-size: 10px; text-transform: uppercase; color: #52525b; letter-spacing: 1px; margin-bottom: 2px;">SecureSentinel</div>
        <div id="ss-status-text" style="font-weight: 600; color: #d4d4d8;">Standby</div>
    `;

    panel.appendChild(dot);
    panel.appendChild(content);
    document.body.appendChild(panel);
    statusPanel = panel;
}

function updateStatus(text, type = 'normal') {
    if (!statusPanel) createStatusPanel();
    const textEl = document.getElementById('ss-status-text');
    const dotEl = document.getElementById('ss-status-dot');

    if (!textEl || !dotEl) return;

    textEl.innerText = text;

    const colors = {
        scanning: '#3b82f6', // Blue
        safe: '#10b981',     // Green
        danger: '#ef4444',   // Red
        idle: '#71717a'      // Gray
    };

    if (type === 'scanning') {
        textEl.style.color = colors.scanning;
        dotEl.style.background = colors.scanning;
        dotEl.style.boxShadow = `0 0 8px ${colors.scanning}`;
    } else if (type === 'safe') {
        textEl.style.color = colors.safe;
        dotEl.style.background = colors.safe;
        dotEl.style.boxShadow = `0 0 8px ${colors.safe}`;
    } else if (type === 'danger') {
        textEl.style.color = colors.danger;
        dotEl.style.background = colors.danger;
        dotEl.style.boxShadow = `0 0 12px ${colors.danger}`;
    } else {
        textEl.style.color = '#d4d4d8';
        dotEl.style.background = colors.idle;
        dotEl.style.boxShadow = 'none';
    }
}

// ============================================
// CONTENT EXTRACTION
// ============================================
function extractContent() {
    const isGmail = window.location.hostname.includes("mail.google.com");

    if (isGmail) {
        // GMAIL LOGIC
        const bodySelectors = ['.a3s.aiL', '.ii.gt', '.adP.adO', 'div[role="listitem"] .a3s'];
        let bodyEl = null;
        for (const sel of bodySelectors) {
            bodyEl = document.querySelector(sel);
            if (bodyEl) break;
        }

        if (!bodyEl) return null;

        const subject = (document.querySelector('h2.hP') || document.querySelector('h2'))?.innerText || "Unknown Subject";
        const senderEl = document.querySelector('.gD') || document.querySelector('span[email]');
        const sender = senderEl ? (senderEl.getAttribute('email') || senderEl.innerText) : "Unknown Sender";

        return {
            type: 'email',
            subject,
            sender,
            senderDomain: sender.includes('@') ? sender.split('@')[1] : 'unknown',
            body: bodyEl.innerText,
            fullText: `Subject: ${subject}\nFrom: ${sender}\n\n${bodyEl.innerText}`,
            id: subject + (bodyEl.innerText.substring(0, 50))
        };
    } else {
        // GENERIC LOGIC
        const hostname = window.location.hostname;
        if (hostname === 'localhost' || hostname === '127.0.0.1') return null;

        const bodyText = document.body.innerText;
        if (bodyText.length < 100) return null;

        return {
            type: 'webpage',
            subject: document.title,
            sender: window.location.hostname,
            senderDomain: window.location.hostname,
            body: bodyText.substring(0, 5000),
            fullText: `Page: ${document.title}\nURL: ${window.location.href}\n\n${bodyText.substring(0, 5000)}`,
            id: document.title + bodyText.substring(0, 100)
        };
    }
}

// ============================================
// SCANNING
// ============================================
function scanContent(data) {
    updateStatus("Scanning Content...", "scanning");

    chrome.runtime.sendMessage({
        type: "SCAN_CONTENT",
        data: {
            subject: data.subject,
            senderDomain: data.senderDomain,
            fullText: data.fullText,
            timestamp: new Date().toISOString()
        }
    }, (response) => {
        if (chrome.runtime.lastError) {
            console.error("Extension Error:", chrome.runtime.lastError);
            updateStatus("Extension Error", "danger");
            return;
        }

        if (response && response.success && response.data) {
            let risk = response.data.global_risk_score;
            // Ensure valid number
            if (typeof risk !== 'number' || isNaN(risk)) {
                risk = response.data.max_risk_score || 0;
            }

            const score = Math.round(risk * 100);

            // USER REQUEST: Status Panel must reflect Domain Safety (Gmail = Safe)
            // We do NOT show "Threat" in the floating widget for email text checks.
            updateStatus("SecureSentinel: Active", "safe");

            const resultData = {
                subject: data.subject,
                sender_domain: data.senderDomain,
                risk_score: risk,
                risk_level: response.data.status || (score > 50 ? "SUSPICIOUS" : "SAFE"),
                signals: response.data.signals, // PASS SIGNALS
                timestamp: new Date().toISOString()
            };

            // CACHE RESULT
            lastScanResult = resultData;

            // SAVE TO STORAGE (Robust Fix)
            chrome.storage.local.set({
                'latestScan': resultData
            }, () => {
                console.log("[WebSentinel] Saved scan to storage");
            });

            chrome.runtime.sendMessage({
                type: 'EMAIL_SCANNED',
                data: resultData
            });

        } else {
            console.error("Scan Failed:", response?.error);
            updateStatus("Connection Fail", "danger");
        }
    });
}

// ============================================
// COMMUNICATE WITH POPUP
// ============================================
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.type === 'GET_LAST_SCAN') {
        console.log("[WebSentinel] Sending cached result to popup:", lastScanResult);
        sendResponse(lastScanResult);
    }
});

// ============================================
// MONITORING
// ============================================
function startMonitor() {
    const hostname = window.location.hostname;
    if (hostname === 'localhost' || hostname === '127.0.0.1') return;

    createStatusPanel();
    updateStatus("Sentinel Active", "idle");

    setInterval(() => {
        const data = extractContent();
        if (data) {
            if (!scannedContent.has(data.id)) {
                scannedContent.add(data.id);
                console.log("[WebSentinel] New content:", data.subject);
                scanContent(data);
            }
        }
    }, 2000);
}

if (document.readyState === "complete") {
    setTimeout(startMonitor, 1000);
} else {
    window.addEventListener('load', () => setTimeout(startMonitor, 1000));
}
