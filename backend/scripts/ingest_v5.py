import pandas as pd
import os
import io
import csv

def ingest_v5():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    data_path = os.path.join(base_dir, 'data', 'processed', 'train.csv')
    
    # Data provided by user (Partial capture of likely larger dataset)
    # This data is highly specific and balanced.
    csv_data = """text,urgency,authority,fear,impersonation
CEO Office Notice: unauthorized access was detected on your account. this request is time-sensitive. Please log in to your Netflix account to verify your details.,1,1,1,1
WhatsApp Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
WhatsApp Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Income Tax Department Notice: multiple failed login attempts were observed. immediate action is required. Please log in to your Instagram account to verify your details.,1,1,1,1
Reserve Bank of India Notice: your account is scheduled for temporary suspension. failure to act may result in permanent suspension. Please log in to your Instagram account to verify your details.,1,1,1,1
Microsoft Security Team Notice: multiple failed login attempts were observed. immediate action is required. Please log in to your WhatsApp account to verify your details.,1,1,1,1
Reserve Bank of India Notice: multiple failed login attempts were observed. immediate action is required. Please log in to your Amazon account to verify your details.,1,1,1,1
Reserve Bank of India Notice: multiple failed login attempts were observed. failure to act may result in permanent suspension. Please log in to your Google account to verify your details.,1,1,1,1
Your password was successfully updated,0,0,0,0
Microsoft Security Team Notice: unauthorized access was detected on your account. failure to act may result in permanent suspension. Please log in to your WhatsApp account to verify your details.,1,1,1,1
PayPal Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Bank Fraud Department Notice: your account has been flagged for suspicious activity. verify your identity immediately. Please log in to your PayPal account to verify your details.,1,1,1,1
Local Police Station Notice: multiple failed login attempts were observed. immediate action is required. Please log in to your Microsoft account to verify your details.,1,1,1,1
Invoice generated for your recent purchase,0,0,0,0
Invoice generated for your recent purchase,0,0,0,0
Your subscription has been renewed successfully,0,0,0,0
IT Administration Notice: your account has been flagged for suspicious activity. please respond within 24 hours. Please log in to your Apple ID account to verify your details.,1,1,1,1
Your subscription has been renewed successfully,0,0,0,0
PayPal Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
IT Administration Notice: unauthorized access was detected on your account. immediate action is required. Please log in to your Instagram account to verify your details.,1,1,1,1
Microsoft Security Team Notice: your account has been flagged for suspicious activity. immediate action is required. Please log in to your Facebook account to verify your details.,1,1,1,1
HR Compliance Office Notice: your account has been flagged for suspicious activity. immediate action is required. Please log in to your Instagram account to verify your details.,1,1,1,1
Microsoft Security Team Notice: your account is scheduled for temporary suspension. immediate action is required. Please log in to your Netflix account to verify your details.,1,1,1,1
Google Security Notice: multiple failed login attempts were observed. verify your identity immediately. Please log in to your Instagram account to verify your details.,1,1,1,1
Local Police Station Notice: your account is scheduled for temporary suspension. please respond within 24 hours. Please log in to your Netflix account to verify your details.,1,1,1,1
Income Tax Department Notice: unauthorized access was detected on your account. verify your identity immediately. Please log in to your Amazon account to verify your details.,1,1,1,1
Local Police Station Notice: a data breach has potentially exposed your information. failure to act may result in permanent suspension. Please log in to your Amazon account to verify your details.,1,1,1,1
Monthly account statement is now available,0,0,0,0
Your delivery has been completed successfully,0,0,0,0
Your password was successfully updated,0,0,0,0
IT Administration Notice: your account has been flagged for suspicious activity. verify your identity immediately. Please log in to your Microsoft account to verify your details.,1,1,1,1
Local Police Station Notice: multiple failed login attempts were observed. please respond within 24 hours. Please log in to your Instagram account to verify your details.,1,1,1,1
IT Administration Notice: your account has been flagged for suspicious activity. verify your identity immediately. Please log in to your Facebook account to verify your details.,1,1,1,1
Microsoft Security Team Notice: unauthorized access was detected on your account. immediate action is required. Please log in to your WhatsApp account to verify your details.,1,1,1,1
HR Compliance Office Notice: a data breach has potentially exposed your information. verify your identity immediately. Please log in to your Microsoft account to verify your details.,1,1,1,1
Reserve Bank of India Notice: multiple failed login attempts were observed. this request is time-sensitive. Please log in to your PayPal account to verify your details.,1,1,1,1
HR Compliance Office Notice: multiple failed login attempts were observed. verify your identity immediately. Please log in to your Facebook account to verify your details.,1,1,1,1
Google Security Notice: your account is scheduled for temporary suspension. immediate action is required. Please log in to your Microsoft account to verify your details.,1,1,1,1
Invoice generated for your recent purchase,0,0,0,0
HR Compliance Office Notice: unauthorized access was detected on your account. verify your identity immediately. Please log in to your Amazon account to verify your details.,1,1,1,1
Income Tax Department Notice: your account has been flagged for suspicious activity. verify your identity immediately. Please log in to your Instagram account to verify your details.,1,1,1,1
Google Security Notice: a data breach has potentially exposed your information. this request is time-sensitive. Please log in to your Apple ID account to verify your details.,1,1,1,1
Local Police Station Notice: your account is scheduled for temporary suspension. failure to act may result in permanent suspension. Please log in to your Google account to verify your details.,1,1,1,1
Your password was successfully updated,0,0,0,0
Microsoft Security Team Notice: unauthorized access was detected on your account. verify your identity immediately. Please log in to your Amazon account to verify your details.,1,1,1,1
CEO Office Notice: multiple failed login attempts were observed. immediate action is required. Please log in to your Facebook account to verify your details.,1,1,1,1
Thank you for contacting customer support,0,0,0,0
Local Police Station Notice: your account is scheduled for temporary suspension. this request is time-sensitive. Please log in to your Facebook account to verify your details.,1,1,1,1
Google Security Notice: unauthorized access was detected on your account. failure to act may result in permanent suspension. Please log in to your Netflix account to verify your details.,1,1,1,1
WhatsApp Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
HR Compliance Office Notice: a data breach has potentially exposed your information. this request is time-sensitive. Please log in to your PayPal account to verify your details.,1,1,1,1
Your subscription has been renewed successfully,0,0,0,0
Cyber Crime Cell Notice: your account is scheduled for temporary suspension. verify your identity immediately. Please log in to your Amazon account to verify your details.,1,1,1,1
Local Police Station Notice: unauthorized access was detected on your account. this request is time-sensitive. Please log in to your WhatsApp account to verify your details.,1,1,1,1
Local Police Station Notice: a data breach has potentially exposed your information. verify your identity immediately. Please log in to your WhatsApp account to verify your details.,1,1,1,1
CEO Office Notice: your account is scheduled for temporary suspension. failure to act may result in permanent suspension. Please log in to your WhatsApp account to verify your details.,1,1,1,1
CEO Office Notice: multiple failed login attempts were observed. verify your identity immediately. Please log in to your Apple ID account to verify your details.,1,1,1,1
CEO Office Notice: unauthorized access was detected on your account. verify your identity immediately. Please log in to your Netflix account to verify your details.,1,1,1,1
HR Compliance Office Notice: multiple failed login attempts were observed. this request is time-sensitive. Please log in to your Netflix account to verify your details.,1,1,1,1
PayPal Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Google Security Notice: a data breach has potentially exposed your information. verify your identity immediately. Please log in to your Amazon account to verify your details.,1,1,1,1
Bank Fraud Department Notice: a data breach has potentially exposed your information. verify your identity immediately. Please log in to your Facebook account to verify your details.,1,1,1,1
IT Administration Notice: your account is scheduled for temporary suspension. failure to act may result in permanent suspension. Please log in to your Netflix account to verify your details.,1,1,1,1
Microsoft Security Team Notice: a data breach has potentially exposed your information. immediate action is required. Please log in to your Netflix account to verify your details.,1,1,1,1
Microsoft Security Team Notice: your account is scheduled for temporary suspension. this request is time-sensitive. Please log in to your Google account to verify your details.,1,1,1,1
Reserve Bank of India Notice: multiple failed login attempts were observed. verify your identity immediately. Please log in to your WhatsApp account to verify your details.,1,1,1,1
Microsoft Security Team Notice: a data breach has potentially exposed your information. please respond within 24 hours. Please log in to your WhatsApp account to verify your details.,1,1,1,1
Your password was successfully updated,0,0,0,0
IT Administration Notice: multiple failed login attempts were observed. immediate action is required. Please log in to your Microsoft account to verify your details.,1,1,1,1
Cyber Crime Cell Notice: your account is scheduled for temporary suspension. this request is time-sensitive. Please log in to your Microsoft account to verify your details.,1,1,1,1
Microsoft Security Team Notice: unauthorized access was detected on your account. this request is time-sensitive. Please log in to your Google account to verify your details.,1,1,1,1
Local Police Station Notice: unauthorized access was detected on your account. failure to act may result in permanent suspension. Please log in to your WhatsApp account to verify your details.,1,1,1,1
Bank Fraud Department Notice: multiple failed login attempts were observed. please respond within 24 hours. Please log in to your Apple ID account to verify your details.,1,1,1,1
Facebook Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Local Police Station Notice: multiple failed login attempts were observed. verify your identity immediately. Please log in to your Apple ID account to verify your details.,1,1,1,1
Income Tax Department Notice: your account has been flagged for suspicious activity. verify your identity immediately. Please log in to your WhatsApp account to verify your details.,1,1,1,1
Local Police Station Notice: your account is scheduled for temporary suspension. verify your identity immediately. Please log in to your Amazon account to verify your details.,1,1,1,1
Google Security Notice: multiple failed login attempts were observed. immediate action is required. Please log in to your Netflix account to verify your details.,1,1,1,1
Google Security Notice: multiple failed login attempts were observed. this request is time-sensitive. Please log in to your Microsoft account to verify your details.,1,1,1,1
Google Security Notice: your account is scheduled for temporary suspension. failure to act may result in permanent suspension. Please log in to your Amazon account to verify your details.,1,1,1,1
Cyber Crime Cell Notice: your account has been flagged for suspicious activity. verify your identity immediately. Please log in to your Instagram account to verify your details.,1,1,1,1
Cyber Crime Cell Notice: your account has been flagged for suspicious activity. please respond within 24 hours. Please log in to your Amazon account to verify your details.,1,1,1,1
CEO Office Notice: multiple failed login attempts were observed. immediate action is required. Please log in to your Netflix account to verify your details.,1,1,1,1
Reserve Bank of India Notice: unauthorized access was detected on your account. failure to act may result in permanent suspension. Please log in to your Apple ID account to verify your details.,1,1,1,1
CEO Office Notice: your account has been flagged for suspicious activity. verify your identity immediately. Please log in to your Apple ID account to verify your details.,1,1,1,1
Bank Fraud Department Notice: a data breach has potentially exposed your information. please respond within 24 hours. Please log in to your WhatsApp account to verify your details.,1,1,1,1
Invoice generated for your recent purchase,0,0,0,0
WhatsApp Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Apple ID Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
CEO Office Notice: your account is scheduled for temporary suspension. failure to act may result in permanent suspension. Please log in to your Apple ID account to verify your details.,1,1,1,1
CEO Office Notice: your account has been flagged for suspicious activity. failure to act may result in permanent suspension. Please log in to your PayPal account to verify your details.,1,1,1,1
Cyber Crime Cell Notice: unauthorized access was detected on your account. please respond within 24 hours. Please log in to your WhatsApp account to verify your details.,1,1,1,1
HR Compliance Office Notice: your account is scheduled for temporary suspension. this request is time-sensitive. Please log in to your Netflix account to verify your details.,1,1,1,1
CEO Office Notice: unauthorized access was detected on your account. immediate action is required. Please log in to your Netflix account to verify your details.,1,1,1,1
Instagram Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Google Security Notice: your account is scheduled for temporary suspension. verify your identity immediately. Please log in to your Netflix account to verify your details.,1,1,1,1
Instagram Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Bank Fraud Department Notice: unauthorized access was detected on your account. immediate action is required. Please log in to your Netflix account to verify your details.,1,1,1,1
Bank Fraud Department Notice: multiple failed login attempts were observed. verify your identity immediately. Please log in to your Google account to verify your details.,1,1,1,1
WhatsApp Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Instagram Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Microsoft Security Team Notice: unauthorized access was detected on your account. immediate action is required. Please log in to your Facebook account to verify your details.,1,1,1,1
Your delivery has been completed successfully,0,0,0,0
Reserve Bank of India Notice: multiple failed login attempts were observed. failure to act may result in permanent suspension. Please log in to your Microsoft account to verify your details.,1,1,1,1
Reserve Bank of India Notice: a data breach has potentially exposed your information. please respond within 24 hours. Please log in to your Google account to verify your details.,1,1,1,1
CEO Office Notice: your account has been flagged for suspicious activity. failure to act may result in permanent suspension. Please log in to your Apple ID account to verify your details.,1,1,1,1
CEO Office Notice: your account has been flagged for suspicious activity. failure to act may result in permanent suspension. Please log in to your Microsoft account to verify your details.,1,1,1,1
Your delivery has been completed successfully,0,0,0,0
Bank Fraud Department Notice: unauthorized access was detected on your account. verify your identity immediately. Please log in to your WhatsApp account to verify your details.,1,1,1,1
Welcome to the new dashboard experience,0,0,0,0
Local Police Station Notice: your account is scheduled for temporary suspension. this request is time-sensitive. Please log in to your Instagram account to verify your details.,1,1,1,1
Google Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Team meeting scheduled for next Monday,0,0,0,0
PayPal Security Update: Your account activity was reviewed and no action is required at this time.,0,0,0,0
Google Security Notice: your account has been flagged for suspicious activity. this request is time-sensitive. Please log in to your Amazon account to verify your details.,1,1,1,1
Google Security Notice: your account has been flagged for suspicious activity. please respond within 24 hours. Please log in to your Apple ID account to verify your details.,1,1,1,1
Bank Fraud Department Notice: your account has been flagged for suspicious activity. failure to act may result in permanent suspension. Please log in to your Apple ID account to verify your details.,1,1,1,1
Thank you for contacting customer support,0,0,0,0"""

    new_df = pd.read_csv(io.StringIO(csv_data))
    new_df['cleaned_text'] = new_df['text']
    
    if os.path.exists(data_path):
        # We append, but we also check for duplicates to avoid data bloat if run multiple times
        existing_df = pd.read_csv(data_path)
        
        # Combine and drop duplicates based on 'text'
        combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['text'])
        
        combined_df.to_csv(data_path, index=False, quoting=csv.QUOTE_ALL)
        print(f"Ingested V5 data. Total dataset size: {len(combined_df)}")
    else:
        new_df.to_csv(data_path, index=False, quoting=csv.QUOTE_ALL)
        print(f"Created dataset with V5 data. Size: {len(new_df)}")

if __name__ == "__main__":
    ingest_v5()
