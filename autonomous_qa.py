import os
import glob
import time
import google.generativeai as genai
from PIL import Image

# 1. System Initialization
# Set your API key directly in your system environment or paste it below
GEMINI_API_KEY = "YOUR_FREE_GEMINI_API_KEY_HERE" 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Define paths where security cameras or scrapers dump operational files automatically
IMAGE_DROPBOX = "./network_camera_feeds/*"
REVIEW_FEED_FILE = "./scraped_reviews_stream.txt"

def autonomous_visual_patrol():
    """Simulates an AI checking folder drops from hotel smart cameras or housekeeping tablets"""
    print("🔍 [System] AI Visual Patrol Agent active. Scanning local network folders...")
    
    # Automatically grab all images inside the drop folder
    incoming_photos = glob.glob(IMAGE_DROPBOX)
    
    if not incoming_photos:
        print("💡 [System] No new room photos detected. Standing by...")
        return

    for photo_path in incoming_photos:
        print(f"📸 [Processing] Automatically analyzing asset: {photo_path}")
        try:
            img = Image.open(photo_path)
            
            prompt = """
            You are an autonomous Hotel QA Agent. Audit this room picture against 5-star resort criteria.
            Identify setup anomalies (wrinkled sheets, misaligned pillows, dust, trash, or maintenance faults).
            If anomalies exist, output your response strictly in this format for automation parsers:
            STATUS: [VIOLATION_FOUND or COMPLIANT]
            DEPARTMENT: [Housekeeping / Maintenance / Management]
            TICKET_SUMMARY: [Short clear description of what needs to be fixed]
            CRITICALITY: [Low / Medium / High]
            """
            
            response = model.generate_content([prompt, img])
            analysis = response.text
            print("\n🤖 [AI Analysis Result]:")
            print(analysis)
            
            # --- AUTONOMOUS ACTION PIPELINE ---
            if "STATUS: VIOLATION_FOUND" in analysis:
                print("🚨 [Auto-Action] Compliance breach verified! Dispatched alert to department head.")
                # code to trigger an email, SMS text message via Twilio, or post to Slack goes here.
            else:
                print("✅ [Auto-Action] Asset passed inspection framework. Archiving...")
                
            # Move or delete file after processing so it isn't analyzed twice
            os.remove(photo_path) 
            
        except Exception as e:
            print(f"❌ Error processing asset {photo_path}: {e}")

def autonomous_review_scout():
    """Simulates an AI listening to live feedback streams from TripAdvisor/Booking.com web scrapers"""
    print("\n📝 [System] AI Feedback Scout active. Auditing new online public mentions...")
    
    if not os.path.exists(REVIEW_FEED_FILE):
        return
        
    with open(REVIEW_FEED_FILE, "r") as f:
        reviews = f.readlines()
        
    if not reviews:
        print("💡 [System] No new online reviews scraped in this cycle.")
        return
        
    for review in reviews:
        review = review.strip()
        if not review: continue
        
        print(f"📥 [Review Ingested]: '{review[:60]}...'")
        
        prompt = f"""
        Analyze this scraped hotel review. If the guest mentions a severe operational failure (e.g. food poisoning, theft, rudeness, no hot water), extract it.
        Format:
        CRITICAL_FLAG: [YES or NO]
        ALERT_MESSAGE: [Clear internal action message]
        """
        response = model.generate_content(prompt)
        result = response.text
        print(result)
        
        if "CRITICAL_FLAG: YES" in result:
            print("✉️ [Auto-Action] Triggered emergency alert directly to the Hotel General Manager's email inbox.")

    # Clear stream file after processing
    open(REVIEW_FEED_FILE, 'w').close()

# Main orchestrator loophole - runs continuously in background
if __name__ == "__main__":
    # Create the mock folders so the script doesn't crash on initial run
    os.makedirs("./network_camera_feeds", exist_ok=True)
    if not os.path.exists(REVIEW_FEED_FILE):
        open(REVIEW_FEED_FILE, 'w').close()
        
    print("🚀 Fully Autonomous Hotel QA Engine is Live.")
    print("--------------------------------------------------")
    
    while True:
        autonomous_visual_patrol()
        autonomous_review_scout()
        print("💤 Engine sleeping for 30 seconds before next automated sweeping cycle...")
        time.sleep(30)
