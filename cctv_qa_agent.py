import time
import google.generativeai as genai
from PIL import Image
import os
import requests
from io import BytesIO

# ==========================================
# 1. CORE AI CONFIGURATION
# ==========================================
GEMINI_API_KEY = "AQ.Ab8RN6KdaQo2rHAqCxf-RO-JtgM9Y8HebUQVxZxoRWzsExv3VA"  # <-- Paste your Google Studio Key here
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# ==========================================
# 2. NETWORK CONNECTION PARAMS
# ==========================================
# Make sure this matches the base address currently on your smartphone screen!
PHONE_BASE_URL = "http://192.168.137.197:8080"

# Common snapshot route paths used by different smartphone camera apps
SNAPSHOT_ROUTES = ["/shot.jpg", "/snapshot.jpg", "/photo.jpg", "/photoaf.jpg"]

def autonomous_camera_patrol():
    print("\n🚀 Connecting to Hotel Network Camera Stream...")
    
    pil_image = None
    successful_route = None

    # Automatically cycle through pathways to find the active stream
    for route in SNAPSHOT_ROUTES:
        target_url = f"{PHONE_BASE_URL}{route}"
        try:
            response = requests.get(target_url, timeout=5)
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                
                # Check if data payload is a genuine image asset
                if 'image' in content_type.lower():
                    img_bytes = BytesIO(response.content)
                    pil_image = Image.open(img_bytes)
                    successful_route = target_url
                    break  # Valid asset found, stop trying routes
                    
        except requests.exceptions.RequestException:
            continue  # Keep trying alternative routes

    # Handle connection failures cleanly
    if pil_image is None:
        print("❌ Error: Connection failed or phone returned text data instead of a photograph.")
        print(f"💡 DEBUG TIPS:")
        print(f" 1. Verify your phone app server is active and running.")
        print(f" 2. Make sure your computer is connected to your phone's mobile hotspot.")
        print(f" 3. Current target address is set to: {PHONE_BASE_URL}")
        return

    print(f"📸 Image secured via endpoint link: {successful_route}")
    print("🧠 Handing asset to AI computer vision logic for evaluation...")

    # Meticulous analysis instructions matching international resort inspection standards
    prompt = """
    You are a meticulous Autonomous AI CCTV Quality Inspector for a premium 5-star hotel resort. 
    Analyze this real-time camera feed snapshot of the hotel room setup.
    
    Perform a thorough structural audit:
    1. Cleanliness Status: Check for visible clutter, dust, stray trash, stains, or unmade areas.
    2. Presentation: Scan for misaligned pillows, wrinkled bedsheets, or open cabinets/drawers.
    3. Maintenance: Point out any visual technical faults or broken fixtures if apparent.
    
    Output your findings clearly in this exact layout format:
    
    ### 🏨 LIVE AUDIT RECORD REPORT
    * **Audit Result Flag**: [PASS if perfect / FAIL if issues exist]
    * **Calculated Setup Score**: [0% to 100%]
    * **Identified Violations**: (Bullet points listing layout errors or messy components found)
    * **Immediate Staff Directive**: (A single clear, actionable fix command text sentence for the housekeeper)
    """

    try:
        # Run visual model content processing parameters
        ai_response = model.generate_content([prompt, pil_image])
        print("\n🤖 [AI LIVE AUDIT SUMMARY]:")
        print(ai_response.text)
        print("=" * 60)
    except Exception as ai_error:
        print(f"❌ AI Core Matrix Generation Error: {ai_error}")

if __name__ == "__main__":
    print("🛰️ Connected to Autonomous Web Stream Agent Interface.")
    print("⏰ System loop interval configuration: 30 seconds.")
    print("------------------------------------------------------------")
    
    while True:
        autonomous_camera_patrol()
        print("\n💤 Sleeping for 30 seconds before next automated camera sweep...")
        time.sleep(30)
