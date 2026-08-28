import sys
import time
import json
from playwright.sync_api import sync_playwright

def run_browser_verification():
    print("[Verification] Launching Playwright with unpacked SecureSentinel Chrome Extension...")
    ext_path = r"c:\Users\Kishan Shetty\Downloads\DTLEL (1)\DTLEL\extension-final"
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=r"c:\Users\Kishan Shetty\Downloads\DTLEL (1)\DTLEL\scratch\chrome_user_data",
            headless=False,
            args=[
                f"--disable-extensions-except={ext_path}",
                f"--load-extension={ext_path}"
            ]
        )
        
        page = context.new_page()
        
        # Listen to console messages to capture gmail-scanner logs
        logs = []
        page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
        
        # Test 1: Load a local mock Gmail page to test DOM extraction and banner injection
        print("[Verification] Navigating to simulated Gmail thread page...")
        mock_gmail_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Gmail - Urgent Account Security Notice</title></head>
        <body>
            <div id="gmail-wrapper">
                <h2 class="hP">URGENT Account Security Notice</h2>
                <div class="gD" email="security-update@paypal-phish-alert.top">PayPal Security Support &lt;security-update@paypal-phish-alert.top&gt;</div>
                <div class="ha">To: user@example.com</div>
                <div class="ii gt" id=":m1">
                    <div class="a3s aiL">
                        Dear Customer,<br><br>
                        Your account access has been restricted due to suspicious login attempts.<br>
                        Please click the link below to verify your account immediately: <a href="http://paypal-security-alert.top/login">http://paypal-security-alert.top/login</a><br><br>
                        Thank you,<br>PayPal Security Team
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        page.set_content(mock_gmail_html, wait_until="domcontentloaded")
        
        # Manually trigger gmail-scanner.js functions on mock Gmail page
        page.evaluate("""
            window.location.hostname = 'mail.google.com';
        """)
        
        time.sleep(3)
        
        # Check if status panel or banner exists
        banner_present = page.evaluate("() => !!document.getElementById('ss-gmail-banner')")
        print(f"[Verification] In-Gmail Banner Present: {banner_present}")
        
        # Save screenshot
        screenshot_path = r"c:\Users\Kishan Shetty\Downloads\DTLEL (1)\DTLEL\scratch\gmail_live_verification.png"
        page.screenshot(path=screenshot_path)
        print(f"[Verification] Screenshot saved to: {screenshot_path}")
        
        print("\n--- EXTENSION CONSOLE LOGS ---")
        for log in logs[:20]:
            print(log)
        print("------------------------------")
        
        context.close()

if __name__ == "__main__":
    run_browser_verification()
