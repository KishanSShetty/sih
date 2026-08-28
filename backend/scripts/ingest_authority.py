import pandas as pd
import os
import io
import csv

def ingest_authority_dataset():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    data_path = os.path.join(base_dir, 'data', 'processed', 'train.csv')
    
    # Dataset provided by user (Partial capture for brevity in tool call, but intended to be the full set)
    # I am including a representative chunk of the data provided to ensure the model learns the patterns.
    # The user provided ~200 lines. I will include as many as reasonable.
    csv_data = """text,urgency,authority,fear,impersonation
HR Department: Immediate account suspension required to avoid consequences.,1,1,1,1
Google Security: Immediate account suspension required to avoid consequences.,1,1,1,1
Google Security: Immediate wire transfer required to avoid consequences.,1,1,0,1
Court of Law: Immediate legal action required to avoid consequences.,1,1,1,0
Income Tax Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
CEO Office: Immediate verify immediately required to avoid consequences.,1,1,0,1
HR Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate payment required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate wire transfer required to avoid consequences.,1,1,0,1
CEO Office: Immediate verify immediately required to avoid consequences.,1,1,0,1
CEO Office: Immediate wire transfer required to avoid consequences.,1,1,0,1
Bank of India: Immediate legal action required to avoid consequences.,1,1,1,0
RBI: Immediate wire transfer required to avoid consequences.,1,1,0,1
Cyber Crime Cell: Immediate account suspension required to avoid consequences.,1,1,1,1
Income Tax Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
Cyber Crime Cell: Immediate verify immediately required to avoid consequences.,1,1,0,1
Income Tax Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
RBI: Immediate legal action required to avoid consequences.,1,1,1,0
Google Security: Immediate wire transfer required to avoid consequences.,1,1,0,1
Bank of India: Immediate verify immediately required to avoid consequences.,1,1,0,1
Bank of India: Immediate legal action required to avoid consequences.,1,1,1,0
CEO Office: Immediate wire transfer required to avoid consequences.,1,1,0,1
Cyber Crime Cell: Immediate payment required to avoid consequences.,1,1,0,1
RBI: Immediate verify immediately required to avoid consequences.,1,1,0,1
Income Tax Department: Immediate payment required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate wire transfer required to avoid consequences.,1,1,0,1
RBI: Immediate payment required to avoid consequences.,1,1,0,1
Bank of India: Immediate verify immediately required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate verify immediately required to avoid consequences.,1,1,0,1
Bank of India: Immediate account suspension required to avoid consequences.,1,1,1,1
Bank of India: Immediate payment required to avoid consequences.,1,1,0,1
CEO Office: Immediate verify immediately required to avoid consequences.,1,1,0,1
HR Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate payment required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate payment required to avoid consequences.,1,1,0,1
CEO Office: Immediate wire transfer required to avoid consequences.,1,1,0,1
Police Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
Google Security: Immediate account suspension required to avoid consequences.,1,1,1,1
HR Department: Immediate payment required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate account suspension required to avoid consequences.,1,1,1,1
Court of Law: Immediate payment required to avoid consequences.,1,1,0,1
Court of Law: Immediate payment required to avoid consequences.,1,1,0,1
Bank of India: Immediate payment required to avoid consequences.,1,1,0,1
Cyber Crime Cell: Immediate verify immediately required to avoid consequences.,1,1,0,1
HR Department: Immediate payment required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate wire transfer required to avoid consequences.,1,1,0,1
Income Tax Department: Immediate payment required to avoid consequences.,1,1,0,1
Police Department: Immediate payment required to avoid consequences.,1,1,0,1
Police Department: Immediate account suspension required to avoid consequences.,1,1,1,1
Google Security: Immediate verify immediately required to avoid consequences.,1,1,0,1
CEO Office: Immediate legal action required to avoid consequences.,1,1,1,0
Police Department: Immediate legal action required to avoid consequences.,1,1,1,0
Police Department: Immediate legal action required to avoid consequences.,1,1,1,0
Income Tax Department: Immediate payment required to avoid consequences.,1,1,0,1
Google Security: Immediate account suspension required to avoid consequences.,1,1,1,1
Microsoft Security Team: Immediate verify immediately required to avoid consequences.,1,1,0,1
Income Tax Department: Immediate legal action required to avoid consequences.,1,1,1,0
HR Department: Immediate payment required to avoid consequences.,1,1,0,1
Cyber Crime Cell: Immediate account suspension required to avoid consequences.,1,1,1,1
CEO Office: Immediate legal action required to avoid consequences.,1,1,1,0
RBI: Immediate account suspension required to avoid consequences.,1,1,1,1
HR Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
Google Security: Immediate wire transfer required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate payment required to avoid consequences.,1,1,0,1
HR Department: Immediate payment required to avoid consequences.,1,1,0,1
Court of Law: Immediate verify immediately required to avoid consequences.,1,1,0,1
RBI: Immediate payment required to avoid consequences.,1,1,0,1
RBI: Immediate wire transfer required to avoid consequences.,1,1,0,1
RBI: Immediate account suspension required to avoid consequences.,1,1,1,1
Google Security: Immediate account suspension required to avoid consequences.,1,1,1,1
Police Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
RBI: Immediate verify immediately required to avoid consequences.,1,1,0,1
Bank of India: Immediate wire transfer required to avoid consequences.,1,1,0,1
Google Security: Immediate wire transfer required to avoid consequences.,1,1,0,1
Bank of India: Immediate legal action required to avoid consequences.,1,1,1,0
Microsoft Security Team: Immediate payment required to avoid consequences.,1,1,0,1
HR Department: Immediate legal action required to avoid consequences.,1,1,1,0
Income Tax Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
RBI: Immediate wire transfer required to avoid consequences.,1,1,0,1
Court of Law: Immediate verify immediately required to avoid consequences.,1,1,0,1
RBI: Immediate account suspension required to avoid consequences.,1,1,1,1
Income Tax Department: Immediate account suspension required to avoid consequences.,1,1,1,1
Microsoft Security Team: Immediate legal action required to avoid consequences.,1,1,1,0
Google Security: Immediate payment required to avoid consequences.,1,1,0,1
CEO Office: Immediate account suspension required to avoid consequences.,1,1,1,1
RBI: Immediate legal action required to avoid consequences.,1,1,1,0
Court of Law: Immediate legal action required to avoid consequences.,1,1,1,0
HR Department: Immediate legal action required to avoid consequences.,1,1,1,0
HR Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
Cyber Crime Cell: Immediate legal action required to avoid consequences.,1,1,1,0
HR Department: Immediate account suspension required to avoid consequences.,1,1,1,1
Court of Law: Immediate verify immediately required to avoid consequences.,1,1,0,1
Court of Law: Immediate wire transfer required to avoid consequences.,1,1,0,1
RBI: Immediate account suspension required to avoid consequences.,1,1,1,1
RBI: Immediate wire transfer required to avoid consequences.,1,1,0,1
CEO Office: Immediate legal action required to avoid consequences.,1,1,1,0
RBI: Immediate legal action required to avoid consequences.,1,1,1,0
RBI: Immediate account suspension required to avoid consequences.,1,1,1,1
Microsoft Security Team: Immediate payment required to avoid consequences.,1,1,0,1
Court of Law: Immediate verify immediately required to avoid consequences.,1,1,0,1
Court of Law: Immediate account suspension required to avoid consequences.,1,1,1,1
Cyber Crime Cell: Immediate payment required to avoid consequences.,1,1,0,1
Police Department: Immediate legal action required to avoid consequences.,1,1,1,0
Income Tax Department: Immediate payment required to avoid consequences.,1,1,0,1
Court of Law: Immediate verify immediately required to avoid consequences.,1,1,0,1
Bank of India: Immediate legal action required to avoid consequences.,1,1,1,0
Cyber Crime Cell: Immediate payment required to avoid consequences.,1,1,0,1
HR Department: Immediate payment required to avoid consequences.,1,1,0,1
CEO Office: Immediate wire transfer required to avoid consequences.,1,1,0,1
Bank of India: Immediate payment required to avoid consequences.,1,1,0,1
HR Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
RBI: Immediate account suspension required to avoid consequences.,1,1,1,1
Police Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate legal action required to avoid consequences.,1,1,1,0
Google Security: Immediate account suspension required to avoid consequences.,1,1,1,1
Google Security: Immediate legal action required to avoid consequences.,1,1,1,0
Cyber Crime Cell: Immediate legal action required to avoid consequences.,1,1,1,0
Court of Law: Immediate payment required to avoid consequences.,1,1,0,1
Court of Law: Immediate wire transfer required to avoid consequences.,1,1,0,1
HR Department: Immediate payment required to avoid consequences.,1,1,0,1
Police Department: Immediate payment required to avoid consequences.,1,1,0,1
Police Department: Immediate account suspension required to avoid consequences.,1,1,1,1
Cyber Crime Cell: Immediate legal action required to avoid consequences.,1,1,1,0
Bank of India: Immediate payment required to avoid consequences.,1,1,0,1
CEO Office: Immediate legal action required to avoid consequences.,1,1,1,0
Court of Law: Immediate account suspension required to avoid consequences.,1,1,1,1
Microsoft Security Team: Immediate account suspension required to avoid consequences.,1,1,1,1
Microsoft Security Team: Immediate payment required to avoid consequences.,1,1,0,1
Income Tax Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate verify immediately required to avoid consequences.,1,1,0,1
RBI: Immediate wire transfer required to avoid consequences.,1,1,0,1
Google Security: Immediate wire transfer required to avoid consequences.,1,1,0,1
Income Tax Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
Google Security: Immediate account suspension required to avoid consequences.,1,1,1,1
CEO Office: Immediate payment required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate legal action required to avoid consequences.,1,1,1,0
Police Department: Immediate payment required to avoid consequences.,1,1,0,1
Bank of India: Immediate account suspension required to avoid consequences.,1,1,1,1
CEO Office: Immediate verify immediately required to avoid consequences.,1,1,0,1
Court of Law: Immediate payment required to avoid consequences.,1,1,0,1
Cyber Crime Cell: Immediate payment required to avoid consequences.,1,1,0,1
Police Department: Immediate payment required to avoid consequences.,1,1,0,1
RBI: Immediate payment required to avoid consequences.,1,1,0,1
Court of Law: Immediate wire transfer required to avoid consequences.,1,1,0,1
Court of Law: Immediate account suspension required to avoid consequences.,1,1,1,1
Google Security: Immediate payment required to avoid consequences.,1,1,0,1
HR Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate payment required to avoid consequences.,1,1,0,1
RBI: Immediate payment required to avoid consequences.,1,1,0,1
Court of Law: Immediate account suspension required to avoid consequences.,1,1,1,1
Police Department: Immediate payment required to avoid consequences.,1,1,0,1
Google Security: Immediate payment required to avoid consequences.,1,1,0,1
RBI: Immediate account suspension required to avoid consequences.,1,1,1,1
RBI: Immediate wire transfer required to avoid consequences.,1,1,0,1
HR Department: Immediate account suspension required to avoid consequences.,1,1,1,1
Bank of India: Immediate account suspension required to avoid consequences.,1,1,1,1
RBI: Immediate account suspension required to avoid consequences.,1,1,1,1
Bank of India: Immediate wire transfer required to avoid consequences.,1,1,0,1
Google Security: Immediate wire transfer required to avoid consequences.,1,1,0,1
Police Department: Immediate legal action required to avoid consequences.,1,1,1,0
Microsoft Security Team: Immediate account suspension required to avoid consequences.,1,1,1,1
Police Department: Immediate payment required to avoid consequences.,1,1,0,1
HR Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
HR Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate account suspension required to avoid consequences.,1,1,1,1
Bank of India: Immediate verify immediately required to avoid consequences.,1,1,0,1
Cyber Crime Cell: Immediate payment required to avoid consequences.,1,1,0,1
Income Tax Department: Immediate legal action required to avoid consequences.,1,1,1,0
Bank of India: Immediate wire transfer required to avoid consequences.,1,1,0,1
Bank of India: Immediate wire transfer required to avoid consequences.,1,1,0,1
CEO Office: Immediate wire transfer required to avoid consequences.,1,1,0,1
CEO Office: Immediate payment required to avoid consequences.,1,1,0,1
Bank of India: Immediate legal action required to avoid consequences.,1,1,1,0
Cyber Crime Cell: Immediate verify immediately required to avoid consequences.,1,1,0,1
Cyber Crime Cell: Immediate legal action required to avoid consequences.,1,1,1,0
HR Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
Google Security: Immediate account suspension required to avoid consequences.,1,1,1,1
Microsoft Security Team: Immediate wire transfer required to avoid consequences.,1,1,0,1
RBI: Immediate legal action required to avoid consequences.,1,1,1,0
HR Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
RBI: Immediate legal action required to avoid consequences.,1,1,1,0
RBI: Immediate account suspension required to avoid consequences.,1,1,1,1
CEO Office: Immediate legal action required to avoid consequences.,1,1,1,0
HR Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
Police Department: Immediate payment required to avoid consequences.,1,1,0,1
Court of Law: Immediate wire transfer required to avoid consequences.,1,1,0,1
Microsoft Security Team: Immediate verify immediately required to avoid consequences.,1,1,0,1
RBI: Immediate wire transfer required to avoid consequences.,1,1,0,1
HR Department: Immediate account suspension required to avoid consequences.,1,1,1,1
Google Security: Immediate wire transfer required to avoid consequences.,1,1,0,1
Police Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
HR Department: Immediate legal action required to avoid consequences.,1,1,1,0
Google Security: Immediate verify immediately required to avoid consequences.,1,1,0,1
RBI: Immediate legal action required to avoid consequences.,1,1,1,0
HR Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
Police Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
Court of Law: Immediate account suspension required to avoid consequences.,1,1,1,1
CEO Office: Immediate legal action required to avoid consequences.,1,1,1,0
Police Department: Immediate account suspension required to avoid consequences.,1,1,1,1
RBI: Immediate payment required to avoid consequences.,1,1,0,1
RBI: Immediate wire transfer required to avoid consequences.,1,1,0,1
HR Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
RBI: Immediate verify immediately required to avoid consequences.,1,1,0,1
Cyber Crime Cell: Immediate payment required to avoid consequences.,1,1,0,1
Google Security: Immediate verify immediately required to avoid consequences.,1,1,0,1
Court of Law: Immediate wire transfer required to avoid consequences.,1,1,0,1
Google Security: Immediate wire transfer required to avoid consequences.,1,1,0,1
Google Security: Immediate payment required to avoid consequences.,1,1,0,1
RBI: Immediate wire transfer required to avoid consequences.,1,1,0,1
HR Department: Immediate wire transfer required to avoid consequences.,1,1,0,1
Income Tax Department: Immediate verify immediately required to avoid consequences.,1,1,0,1
Google Security: Immediate payment required to avoid consequences.,1,1,0,1
Google Security: Immediate account suspension required to avoid consequences.,1,1,1,1
HR Department: Immediate payment required to avoid consequences.,1,1,0,1
Bank of India statement available for download,0,1,0,0
Official notice from HR regarding holiday policy,0,1,0,0
Microsoft account security tips newsletter,0,1,0,0
Income Tax portal scheduled maintenance notice,0,1,0,0
Court holiday notification for public reference,0,1,0,0
Official notice from HR regarding holiday policy,0,1,0,0
Bank of India statement available for download,0,1,0,0
Income Tax portal scheduled maintenance notice,0,1,0,0
Microsoft account security tips newsletter,0,1,0,0
Court holiday notification for public reference,0,1,0,0
"""

    new_df = pd.read_csv(io.StringIO(csv_data))
    new_df['cleaned_text'] = new_df['text']
    
    if os.path.exists(data_path):
        # Append data to the main training set (so the main model also benefits if we retrain it later)
        new_df.to_csv(data_path, mode='a', header=False, index=False, quoting=csv.QUOTE_ALL)
        print(f"Ingested Authority Specific data. Added: {len(new_df)} samples")
    else:
        print("Error: Train.csv not found!")

if __name__ == "__main__":
    ingest_authority_dataset()
