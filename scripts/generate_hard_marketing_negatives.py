import os
import time
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv('.env.local')
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("⚠️ GEMINI_API_KEY not found in .env.local. Skipping hard negative generation.")
    exit(0)

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

PROMPT = """
As an AI security researcher, generate 20 examples of "Hard Negative Marketing" emails.
These are emails that use intense URGENCY (e.g., "ends in 2 hours", "exclusive offer today"), 
but have absolutely NO malicious intent (no fear-mongering, no fake authority, no impersonation of services).

The goal is to teach a model that Urgency alone does not mean Phishing.

Format the output as a JSON list of objects:
- text: the email snippet
- urgency: 1
- authority: 0
- fear: 0
- impersonation: 0

Examples:
- "Flash sale! 70% off everything for the next 45 minutes only. Don't miss out on these savings!"
- "Your exclusive rewards points expire tonight at midnight. Redeem them now for a bonus gift."

Return ONLY the JSON list.
"""

def main():
    print("🎯 Generating Hard Negative Marketing Samples (Step 5)...")
    try:
        response = model.generate_content(PROMPT)
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
             text = text.split("```")[1].split("```")[0]
             
        data = json.loads(text.strip())
        df = pd.DataFrame(data)
        
        output_dir = 'data/hard_negatives'
        os.makedirs(output_dir, exist_ok=True)
        filename = f"hard_negatives_marketing_{int(time.time())}.csv"
        df.to_csv(os.path.join(output_dir, filename), index=False)
        
        print(f"✅ Successfully generated {len(df)} hard negatives in {filename}")
        print("💡 These samples will help decouple Urgency from Malicious Intent during the next training cycle.")
        
    except Exception as e:
        print(f"❌ Error during generation: {e}")

if __name__ == "__main__":
    main()
