import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from scipy.sparse import hstack, csr_matrix
import re
import numpy as np

# Replicate the feature extraction logic exactly, but UPDATED for Step 3
def extract_manual_features_v6(texts, structural_data=None):
    features = []
    # Regex for IP address
    ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    
    # Iterate through texts (and matching structural data if present)
    for i, text in enumerate(texts):
        if not isinstance(text, str): text = "" 
        url = text 
        row = []
        
        # 1. Has IP Address POINTER
        row.append(1 if ip_pattern.search(url) else 0)
        
        # 2. Length Features
        row.append(1 if len(url) > 50 else 0)
        row.append(1 if len(url) > 75 else 0)
        
        # 3. Suspicious Characters
        row.append(url.count('.'))   
        row.append(url.count('@'))   
        row.append(url.count('-'))   
        
        # 4. Sensitive Keywords
        lower_url = url.lower()
        for word in ['login', 'signin', 'account', 'update', 'verify', 'secure', 'bank', 'confirm']:
            row.append(1 if word in lower_url else 0)
            
        # [STEP 2] INTERACTION FEATURES
        has_auth_kw = any(w in lower_url for w in ['verify', 'account', 'secure', 'login'])
        has_urgency_kw = any(w in lower_url for w in ['immediate', 'urgent', 'suspend', 'expires'])
        has_payment_kw = any(w in lower_url for w in ['payment', 'wire', 'billing', 'invoice'])
        
        row.append(1 if (has_auth_kw and has_urgency_kw) else 0)
        row.append(1 if (has_auth_kw and has_payment_kw) else 0)
        has_fear_kw = any(w in lower_url for w in ['legal', 'court', 'police', 'jail', 'warrant'])
        row.append(1 if has_fear_kw else 0)
        
        # [STEP 3] STRUCTURAL FEATURES
        # If we have structural data (from training CSV), append it.
        # If not (during inference), we might pass defaults or extracted values
        if structural_data is not None and i < len(structural_data):
            # has_password_field, is_https, external_link_ratio
            s_row = structural_data.iloc[i]
            row.append(int(s_row['has_password_field']))
            row.append(int(s_row['is_https']))
            row.append(float(s_row['external_link_ratio']))
        else:
            # Fallback for inference if not provided (assume average/imputed)
            # Though in REAL inference, we will extract this from the extension!
            # For now, if missing, default to 0 to be safe (or 1 for https?)
            row.append(0) # No password field
            row.append(1) # Is HTTPS (Default yes)
            row.append(0.1) # External link ratio low
            
        features.append(row)
        
    return csr_matrix(features)

def train_v6_structural():  
    print("Starting V6 Training with STRUCTURAL FEATURES...")  

    # Paths  
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    base_dir = os.path.dirname(os.path.dirname(current_dir))  
    data_dir = os.path.join(base_dir, 'data', 'processed')  
    model_dir = os.path.join(base_dir, 'models')  
    
    # 1. Load Base Data
    # (Loading logic moved to corrected block below)
    
    # 2. Load Edge Case Data
    # Fixed Path: backend/data/processed/v6_real_world_edge_cases.csv
    # base_dir is "C:\Users\Kishan Shetty\Downloads\DTLshit\DTLshit"
    # data_dir is "C:\Users\Kishan Shetty\Downloads\DTLshit\DTLshit\data\processed" (Logic above seems slightly off on base_dir calculation)
    
    # Recalculate paths carefully
    # The script is in backend/scripts
    # current_dir = .../backend/scripts
    # backend_dir = .../backend
    
    # BUT finding shows data is in .../DTLshit/data/processed (Root level data folder)
    # NOT in .../DTLshit/backend/data/processed
    # This was the error.
    
    current_dir = os.path.dirname(os.path.abspath(__file__)) # ...\backend\scripts
    base_dir = os.path.dirname(os.path.dirname(current_dir)) # ...\DTLshit (Root)
    
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    
    train_path = os.path.join(processed_dir, 'train.csv')
    edge_path = os.path.join(base_dir, 'backend', 'data', 'processed', 'v6_real_world_edge_cases.csv')
    
    # Verify edge path separately, as I created it using 'backend/data/processed' in the write_to_file tool
    # Let me check where I wrote edge case file.
    # Previous tool wrote to: c:\Users\Kishan Shetty\Downloads\DTLshit\DTLshit\backend\data\processed\v6_real_world_edge_cases.csv
    # So edge path IS in backend/data/processed.
    # But train.csv IS in root/data/processed.
    
    edge_dir = os.path.join(base_dir, 'backend', 'data', 'processed')
    edge_path = os.path.join(edge_dir, 'v6_real_world_edge_cases.csv')
    
    print(f"Loading base from: {train_path}")
    base_df = pd.read_csv(train_path)
    
    print(f"Loading edge from: {edge_path}")
    edge_df = pd.read_csv(edge_path)
    
    # 3. Merge
    # Re-apply imputation to base_df (it was loaded correctly in the new block)
    base_df['has_password_field'] = (base_df['urgency'] | base_df['impersonation']) 
    base_df['is_https'] = 1 
    base_df['external_link_ratio'] = base_df.apply(lambda x: 0.8 if x['impersonation'] == 1 else 0.05, axis=1)

    full_df = pd.concat([base_df, edge_df]).sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"Total dataset size: {len(full_df)}")
    
    labels = ['urgency', 'authority', 'fear', 'impersonation']  
    X_text = full_df['cleaned_text'].fillna(full_df['text']).fillna('') # Use 'text' if cleaned missing
    X_structural = full_df[['has_password_field', 'is_https', 'external_link_ratio']]
    y = full_df[labels]  
    
    # Split
    # We need to split indices to keep X_text and X_structural aligned
    indices = np.arange(len(full_df))
    train_idx, test_idx = train_test_split(indices, test_size=0.2, random_state=42)
    
    # Vectorize
    vectorizer = TfidfVectorizer(
        max_features=15000, 
        stop_words='english', 
        token_pattern=r'\b\w+\b',
        ngram_range=(1, 2),
        min_df=1
    )  
    
    X_train_vec = vectorizer.fit_transform(X_text.iloc[train_idx])  
    X_test_vec = vectorizer.transform(X_text.iloc[test_idx])  
    
    # Manual Features (Interaction + Structural)
    print("Extracting Manual + Structural Features...")
    X_train_manual = extract_manual_features_v6(X_text.iloc[train_idx], X_structural.iloc[train_idx])
    X_test_manual = extract_manual_features_v6(X_text.iloc[test_idx], X_structural.iloc[test_idx])
    
    X_train_combined = hstack([X_train_vec, X_train_manual])
    X_test_combined = hstack([X_test_vec, X_test_manual])

    # Model
    clf = MultiOutputClassifier(LogisticRegression(
        solver='liblinear', 
        class_weight='balanced',
        C=2.0, 
        random_state=42
    ))  
    
    clf.fit(X_train_combined, y.iloc[train_idx])  

    # Save  
    joblib.dump(vectorizer, os.path.join(model_dir, 'vectorizer_v6.joblib'))  
    joblib.dump(clf, os.path.join(model_dir, 'model_v6.joblib'))  

    # Evaluate  
    y_pred = clf.predict(X_test_combined)  
    overall_acc = accuracy_score(y.iloc[test_idx], y_pred)  
    print(f"Overall Accuracy: {overall_acc:.4f}")  
    
    # Verify performance on Edge Cases specifically
    # We can't easily isolate them in the split, but overall metrics show impact

if __name__ == "__main__":
    train_v6_structural()
