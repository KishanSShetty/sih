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

# Replicate the feature extraction logic exactly
def extract_manual_features_training(texts):
    features = []
    # Regex for IP address
    ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    
    for text in texts:
        if not isinstance(text, str): text = "" 
        url = text # In training, text is the content
        row = []
        
        # 1. Has IP Address
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
        
        # Interaction 1: Authority + Urgency
        row.append(1 if (has_auth_kw and has_urgency_kw) else 0)
        # Interaction 2: Authority + Payment
        row.append(1 if (has_auth_kw and has_payment_kw) else 0)
        # Interaction 3: Fear + Legal
        has_fear_kw = any(w in lower_url for w in ['legal', 'court', 'police', 'jail', 'warrant'])
        row.append(1 if has_fear_kw else 0)
            
        features.append(row)
        
    return csr_matrix(features)

def train_max_potential_v6():  
    print("Starting MAX POTENTIAL V6 Training (Interaction Features)...")  

    # Paths  
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    base_dir = os.path.dirname(os.path.dirname(current_dir))  
    data_dir = os.path.join(base_dir, 'data', 'processed')  
    model_dir = os.path.join(base_dir, 'models')  
    
    # Load Data  
    train_path = os.path.join(data_dir, 'train.csv')  
    full_df = pd.read_csv(train_path)
    
    # Check distribution
    print(f"Total dataset size: {len(full_df)}")
    
    # Shuffle
    full_df = full_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    labels = ['urgency', 'authority', 'fear', 'impersonation']  
    X = full_df['cleaned_text'].fillna('')  
    y = full_df[labels]  
    
    # 80/20 Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  

    # Vectorize - Enhanced n-grams (1,2)
    vectorizer = TfidfVectorizer(
        max_features=15000, 
        stop_words='english', 
        token_pattern=r'\b\w+\b',
        ngram_range=(1, 2),
        min_df=1
    )  
    
    X_train_vec = vectorizer.fit_transform(X_train)  
    X_test_vec = vectorizer.transform(X_test)  
    
    # [IMPORTANT] ADD INTERACTION FEATURES TO TRAINING DATA
    # We must combine sparse matrix from vectorizer with our manual features
    print("Extracting Manual Interaction Features...")
    X_train_manual = extract_manual_features_training(X_train)
    X_test_manual = extract_manual_features_training(X_test)
    
    X_train_combined = hstack([X_train_vec, X_train_manual])
    X_test_combined = hstack([X_test_vec, X_test_manual])

    # Model - Regularized Logistic Regression
    clf = MultiOutputClassifier(LogisticRegression(
        solver='liblinear', 
        class_weight='balanced',
        C=2.0, 
        random_state=42
    ))  
    
    clf.fit(X_train_combined, y_train)  

    # Save  
    # Note: We save as 'model_enhanced' to stick to convention in backend loading if we switched to it
    # Currently backend loads 'vectorizer_enhanced.joblib' and 'model_enhanced.joblib' check?
    # Backend loads: 'vectorizer_enhanced.joblib' and 'model_enhanced.joblib' (Lines 121-122)
    # BUT backend does NOT currently use manual feature extraction in the "Enhanced" block (it uses Hashing).
    # Wait, looking at backend:
    # It tries to load 'model_enhanced'.
    # Then falls back to 'model_scalable'.
    # AND lines 570+ do: X_vec = vectorizer.transform... X_manual = extract_manual... X_combined = hstack.
    # So we MUST serve a model trained on COMBINED features if we want Step 2 features to work.
    
    joblib.dump(vectorizer, os.path.join(model_dir, 'vectorizer_enhanced.joblib'))  
    joblib.dump(clf, os.path.join(model_dir, 'model_enhanced.joblib'))  

    # Evaluate  
    y_pred = clf.predict(X_test_combined)  
    overall_acc = accuracy_score(y_test, y_pred)  
    print(f"Overall Accuracy: {overall_acc:.4f}")  

    for i, label in enumerate(labels):  
        print(f"\n--- {label} ---")  
        y_true_lbl = y_test.iloc[:, i]  
        y_pred_lbl = y_pred[:, i]  
        
        rep = classification_report(y_true_lbl, y_pred_lbl, output_dict=True)
        prec = rep['1']['precision'] if '1' in rep else 0.0
        rec = rep['1']['recall'] if '1' in rep else 0.0
        f1 = rep['1']['f1-score'] if '1' in rep else 0.0
        
        print(f"Precision: {prec:.4f}")
        print(f"Recall: {rec:.4f}")
        print(f"F1: {f1:.4f}")
        
        cm = confusion_matrix(y_true_lbl, y_pred_lbl)
        print(f"Confusion Matrix: {cm.tolist()}")

if __name__ == "__main__":
    train_max_potential_v6()
