import pandas as pd
import os
import io
import csv

def ingest_final_safe():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    data_path = os.path.join(base_dir, 'data', 'processed', 'train.csv')
    
    # User's final MASSIVE safe dataset
    csv_data = """text,urgency,authority,fear,impersonation
Google account settings page,0,0,0,0
Welcome to Microsoft developer documentation,0,0,0,0
Amazon official help center,0,0,0,0
Apple privacy policy update,0,0,0,0
Facebook user dashboard overview,0,0,0,0
Learn more about Instagram services,0,0,0,0
Netflix account activity summary,0,0,0,0
PayPal official login help page,0,0,0,0
LinkedIn support documentation portal,0,0,0,0
Twitter terms and conditions,0,0,0,0
WhatsApp account settings page,0,0,0,0
Welcome to RBI developer documentation,0,0,0,0
SBI official help center,0,0,0,0
ICICI privacy policy update,0,0,0,0
Google user dashboard overview,0,0,0,0
Learn more about Microsoft services,0,0,0,0
Amazon account activity summary,0,0,0,0
Apple official login help page,0,0,0,0
Facebook support documentation portal,0,0,0,0
Instagram terms and conditions,0,0,0,0
Netflix account settings page,0,0,0,0
Welcome to PayPal developer documentation,0,0,0,0
LinkedIn official help center,0,0,0,0
Twitter privacy policy update,0,0,0,0
WhatsApp user dashboard overview,0,0,0,0
Learn more about RBI services,0,0,0,0
SBI account activity summary,0,0,0,0
ICICI official login help page,0,0,0,0
Google support documentation portal,0,0,0,0
Microsoft terms and conditions,0,0,0,0
Amazon account settings page,0,0,0,0
Welcome to Apple developer documentation,0,0,0,0
Facebook official help center,0,0,0,0
Instagram privacy policy update,0,0,0,0
Netflix user dashboard overview,0,0,0,0
Learn more about PayPal services,0,0,0,0
LinkedIn account activity summary,0,0,0,0
Twitter official login help page,0,0,0,0
WhatsApp support documentation portal,0,0,0,0
RBI terms and conditions,0,0,0,0
SBI account settings page,0,0,0,0
Welcome to ICICI developer documentation,0,0,0,0
Google official help center,0,0,0,0
Microsoft privacy policy update,0,0,0,0
Amazon user dashboard overview,0,0,0,0
Learn more about Apple services,0,0,0,0
Facebook account activity summary,0,0,0,0
Instagram official login help page,0,0,0,0
Netflix support documentation portal,0,0,0,0
PayPal terms and conditions,0,0,0,0
LinkedIn account settings page,0,0,0,0
Welcome to Twitter developer documentation,0,0,0,0
WhatsApp official help center,0,0,0,0
RBI privacy policy update,0,0,0,0
SBI user dashboard overview,0,0,0,0
Learn more about ICICI services,0,0,0,0
Google account activity summary,0,0,0,0
Microsoft official login help page,0,0,0,0
Amazon support documentation portal,0,0,0,0
Apple terms and conditions,0,0,0,0
Facebook account settings page,0,0,0,0
Welcome to Instagram developer documentation,0,0,0,0
Netflix official help center,0,0,0,0
PayPal privacy policy update,0,0,0,0
LinkedIn user dashboard overview,0,0,0,0
Learn more about Twitter services,0,0,0,0
WhatsApp account activity summary,0,0,0,0
RBI official login help page,0,0,0,0
SBI support documentation portal,0,0,0,0
ICICI terms and conditions,0,0,0,0
Google account settings page,0,0,0,0
Welcome to Microsoft developer documentation,0,0,0,0
Amazon official help center,0,0,0,0
Apple privacy policy update,0,0,0,0
Facebook user dashboard overview,0,0,0,0
Learn more about Instagram services,0,0,0,0
Netflix account activity summary,0,0,0,0
PayPal official login help page,0,0,0,0
LinkedIn support documentation portal,0,0,0,0
Twitter terms and conditions,0,0,0,0
WhatsApp account settings page,0,0,0,0
Welcome to RBI developer documentation,0,0,0,0
SBI official help center,0,0,0,0
ICICI privacy policy update,0,0,0,0
Google user dashboard overview,0,0,0,0
Learn more about Microsoft services,0,0,0,0
Amazon account activity summary,0,0,0,0
Apple official login help page,0,0,0,0
Facebook support documentation portal,0,0,0,0
Instagram terms and conditions,0,0,0,0
Netflix account settings page,0,0,0,0
Welcome to PayPal developer documentation,0,0,0,0
LinkedIn official help center,0,0,0,0
Twitter privacy policy update,0,0,0,0
WhatsApp user dashboard overview,0,0,0,0
Learn more about RBI services,0,0,0,0
SBI account activity summary,0,0,0,0
ICICI official login help page,0,0,0,0
Google support documentation portal,0,0,0,0
Microsoft terms and conditions,0,0,0,0
Amazon account settings page,0,0,0,0
Welcome to Apple developer documentation,0,0,0,0
Facebook official help center,0,0,0,0
Instagram privacy policy update,0,0,0,0
Netflix user dashboard overview,0,0,0,0
Learn more about PayPal services,0,0,0,0
LinkedIn account activity summary,0,0,0,0
Twitter official login help page,0,0,0,0
WhatsApp support documentation portal,0,0,0,0
RBI terms and conditions,0,0,0,0
SBI account settings page,0,0,0,0
Welcome to ICICI developer documentation,0,0,0,0
Google official help center,0,0,0,0
Microsoft privacy policy update,0,0,0,0
Amazon user dashboard overview,0,0,0,0
Learn more about Apple services,0,0,0,0
Facebook account activity summary,0,0,0,0
Instagram official login help page,0,0,0,0
Netflix support documentation portal,0,0,0,0
PayPal terms and conditions,0,0,0,0
LinkedIn account settings page,0,0,0,0
Welcome to Twitter developer documentation,0,0,0,0
WhatsApp official help center,0,0,0,0
RBI privacy policy update,0,0,0,0
SBI user dashboard overview,0,0,0,0
Learn more about ICICI services,0,0,0,0
Google account activity summary,0,0,0,0
Microsoft official login help page,0,0,0,0
Amazon support documentation portal,0,0,0,0
Apple terms and conditions,0,0,0,0
Facebook account settings page,0,0,0,0
Welcome to Instagram developer documentation,0,0,0,0
Netflix official help center,0,0,0,0
PayPal privacy policy update,0,0,0,0
LinkedIn user dashboard overview,0,0,0,0
Learn more about Twitter services,0,0,0,0
WhatsApp account activity summary,0,0,0,0
RBI official login help page,0,0,0,0
SBI support documentation portal,0,0,0,0
ICICI terms and conditions,0,0,0,0
Google account settings page,0,0,0,0
Welcome to Microsoft developer documentation,0,0,0,0
Amazon official help center,0,0,0,0
Apple privacy policy update,0,0,0,0
Facebook user dashboard overview,0,0,0,0
Learn more about Instagram services,0,0,0,0
Netflix account activity summary,0,0,0,0
PayPal official login help page,0,0,0,0
LinkedIn support documentation portal,0,0,0,0
Twitter terms and conditions,0,0,0,0
WhatsApp account settings page,0,0,0,0
Welcome to RBI developer documentation,0,0,0,0
SBI official help center,0,0,0,0
ICICI privacy policy update,0,0,0,0
Google user dashboard overview,0,0,0,0
Learn more about Microsoft services,0,0,0,0
Amazon account activity summary,0,0,0,0
Apple official login help page,0,0,0,0
Facebook support documentation portal,0,0,0,0
Instagram terms and conditions,0,0,0,0
Netflix account settings page,0,0,0,0
Welcome to PayPal developer documentation,0,0,0,0
LinkedIn official help center,0,0,0,0
Twitter privacy policy update,0,0,0,0
WhatsApp user dashboard overview,0,0,0,0
Learn more about RBI services,0,0,0,0
SBI account activity summary,0,0,0,0
ICICI official login help page,0,0,0,0
Google support documentation portal,0,0,0,0
Microsoft terms and conditions,0,0,0,0
Amazon account settings page,0,0,0,0
Welcome to Apple developer documentation,0,0,0,0
Facebook official help center,0,0,0,0
Instagram privacy policy update,0,0,0,0
Netflix user dashboard overview,0,0,0,0
Learn more about PayPal services,0,0,0,0
LinkedIn account activity summary,0,0,0,0
Twitter official login help page,0,0,0,0
WhatsApp support documentation portal,0,0,0,0
RBI terms and conditions,0,0,0,0
SBI account settings page,0,0,0,0
Welcome to ICICI developer documentation,0,0,0,0
Google official help center,0,0,0,0
Microsoft privacy policy update,0,0,0,0
Amazon user dashboard overview,0,0,0,0
Learn more about Apple services,0,0,0,0
Facebook account activity summary,0,0,0,0
Instagram official login help page,0,0,0,0
Netflix support documentation portal,0,0,0,0
PayPal terms and conditions,0,0,0,0
LinkedIn account settings page,0,0,0,0
Welcome to Twitter developer documentation,0,0,0,0
WhatsApp official help center,0,0,0,0
RBI privacy policy update,0,0,0,0
SBI user dashboard overview,0,0,0,0
Learn more about ICICI services,0,0,0,0
Google account activity summary,0,0,0,0
Microsoft official login help page,0,0,0,0
Amazon support documentation portal,0,0,0,0
Apple terms and conditions,0,0,0,0
Facebook account settings page,0,0,0,0
Welcome to Instagram developer documentation,0,0,0,0
Netflix official help center,0,0,0,0
PayPal privacy policy update,0,0,0,0
LinkedIn user dashboard overview,0,0,0,0
Learn more about Twitter services,0,0,0,0
WhatsApp account activity summary,0,0,0,0
RBI official login help page,0,0,0,0
SBI support documentation portal,0,0,0,0
ICICI terms and conditions,0,0,0,0
Google account settings page,0,0,0,0
Welcome to Microsoft developer documentation,0,0,0,0
Amazon official help center,0,0,0,0
Apple privacy policy update,0,0,0,0
Facebook user dashboard overview,0,0,0,0
Learn more about Instagram services,0,0,0,0
Netflix account activity summary,0,0,0,0
PayPal official login help page,0,0,0,0
LinkedIn support documentation portal,0,0,0,0
Twitter terms and conditions,0,0,0,0
WhatsApp account settings page,0,0,0,0
Welcome to RBI developer documentation,0,0,0,0
SBI official help center,0,0,0,0
ICICI privacy policy update,0,0,0,0
Google user dashboard overview,0,0,0,0
Learn more about Microsoft services,0,0,0,0
Amazon account activity summary,0,0,0,0
Apple official login help page,0,0,0,0
Facebook support documentation portal,0,0,0,0
Instagram terms and conditions,0,0,0,0
Netflix account settings page,0,0,0,0
Welcome to PayPal developer documentation,0,0,0,0
LinkedIn official help center,0,0,0,0
Twitter privacy policy update,0,0,0,0
WhatsApp user dashboard overview,0,0,0,0
Learn more about RBI services,0,0,0,0
SBI account activity summary,0,0,0,0
ICICI official login help page,0,0,0,0
Google support documentation portal,0,0,0,0
Microsoft terms and conditions,0,0,0,0
Amazon account settings page,0,0,0,0
Welcome to Apple developer documentation,0,0,0,0
Facebook official help center,0,0,0,0
Instagram privacy policy update,0,0,0,0
Netflix user dashboard overview,0,0,0,0
Learn more about PayPal services,0,0,0,0
LinkedIn account activity summary,0,0,0,0
Twitter official login help page,0,0,0,0
WhatsApp support documentation portal,0,0,0,0
RBI terms and conditions,0,0,0,0
SBI account settings page,0,0,0,0
Welcome to ICICI developer documentation,0,0,0,0
Google official help center,0,0,0,0
Microsoft privacy policy update,0,0,0,0
Amazon user dashboard overview,0,0,0,0
Learn more about Apple services,0,0,0,0
Facebook account activity summary,0,0,0,0
Instagram official login help page,0,0,0,0
Netflix support documentation portal,0,0,0,0
PayPal terms and conditions,0,0,0,0
LinkedIn account settings page,0,0,0,0
Welcome to Twitter developer documentation,0,0,0,0
WhatsApp official help center,0,0,0,0
RBI privacy policy update,0,0,0,0
SBI user dashboard overview,0,0,0,0
Learn more about ICICI services,0,0,0,0
Google account activity summary,0,0,0,0
Microsoft official login help page,0,0,0,0
Amazon support documentation portal,0,0,0,0
Apple terms and conditions,0,0,0,0
Facebook account settings page,0,0,0,0
Welcome to Instagram developer documentation,0,0,0,0
Netflix official help center,0,0,0,0
PayPal privacy policy update,0,0,0,0
LinkedIn user dashboard overview,0,0,0,0
Learn more about Twitter services,0,0,0,0
WhatsApp account activity summary,0,0,0,0
RBI official login help page,0,0,0,0
SBI support documentation portal,0,0,0,0
ICICI terms and conditions,0,0,0,0"""

    new_df = pd.read_csv(io.StringIO(csv_data))
    new_df['cleaned_text'] = new_df['text']
    
    if os.path.exists(data_path):
        # Append safe data
        # We don't worry about duplicates as much here because "Safe" duplication is actually good
        # It reinforces the "Normal" baseline.
        
        new_df.to_csv(data_path, mode='a', header=False, index=False, quoting=csv.QUOTE_ALL)
        print(f"Ingested FINAL SAFE data. Added: {len(new_df)} samples")
    else:
        print("Error: Train.csv not found!")

if __name__ == "__main__":
    ingest_final_safe()
