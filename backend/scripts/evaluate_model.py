import pandas as pd
import joblib
import os
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from scipy.sparse import hstack, csr_matrix
import re
import numpy as np
from sklearn.model_selection import train_test_split

def extract_manual_features_v6(texts, structural_data=None):
    features = []
    ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    for i, text in enumerate(texts):
        if not isinstance(text, str): text = "" 
        url = text 
        row = []
        row.append(1 if ip_pattern.search(url) else 0)
        row.append(1 if len(url) > 50 else 0)
        row.append(1 if len(url) > 75 else 0)
        row.append(url.count('.'))   
        row.append(url.count('@'))   
        row.append(url.count('-'))   
        lower_url = url.lower()
        for word in ['login', 'signin', 'account', 'update', 'verify', 'secure', 'bank', 'confirm']:
            row.append(1 if word in lower_url else 0)
        has_auth_kw = any(w in lower_url for w in ['verify', 'account', 'secure', 'login'])
        has_urgency_kw = any(w in lower_url for w in ['immediate', 'urgent', 'suspend', 'expires'])
        has_payment_kw = any(w in lower_url for w in ['payment', 'wire', 'billing', 'invoice'])
        row.append(1 if (has_auth_kw and has_urgency_kw) else 0)
        row.append(1 if (has_auth_kw and has_payment_kw) else 0)
        has_fear_kw = any(w in lower_url for w in ['legal', 'court', 'police', 'jail', 'warrant'])
        row.append(1 if has_fear_kw else 0)
        if structural_data is not None and i < len(structural_data):
            s_row = structural_data.iloc[i]
            row.append(int(s_row['has_password_field']))
            row.append(int(s_row['is_https']))
            row.append(float(s_row['external_link_ratio']))
        else:
             row.append(0); row.append(1); row.append(0.1)
        features.append(row)
    return csr_matrix(features)

def evaluate_model():
    print("Evaluating V6 Model...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    model_dir = os.path.join(base_dir, 'models')
    try:
        vectorizer = joblib.load(os.path.join(model_dir, 'vectorizer_v6.joblib'))
        clf = joblib.load(os.path.join(model_dir, 'model_v6.joblib'))
    except Exception as e:
        print(f"Error: {e}"); return
    train_path = os.path.join(processed_dir, 'train.csv')
    edge_path = os.path.join(base_dir, 'backend', 'data', 'processed', 'v6_real_world_edge_cases.csv')
    base_df = pd.read_csv(train_path)
    base_df['has_password_field'] = (base_df['urgency'] | base_df['impersonation']) 
    base_df['is_https'] = 1 
    base_df['external_link_ratio'] = base_df.apply(lambda x: 0.8 if x['impersonation'] == 1 else 0.05, axis=1)
    edge_df = pd.read_csv(edge_path)
    full_df = pd.concat([base_df, edge_df]).sample(frac=1, random_state=42).reset_index(drop=True)
    if 'cleaned_text' not in full_df.columns: full_df['cleaned_text'] = full_df['text']
    X_text = full_df['cleaned_text'].fillna(full_df['text']).fillna('')
    X_structural = full_df[['has_password_field', 'is_https', 'external_link_ratio']]
    y = full_df[['urgency', 'authority', 'fear', 'impersonation']]
    X_vec = vectorizer.transform(X_text)
    X_manual = extract_manual_features_v6(X_text, X_structural)
    X_combined = hstack([X_vec, X_manual])
    indices = np.arange(len(full_df))
    _, test_idx = train_test_split(indices, test_size=0.2, random_state=42)
    X_test = X_combined.tocsr()[test_idx]
    y_test = y.iloc[test_idx]
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nModel: V6 (Structural)\nValidation Accuracy: {acc:.4f}\n" + "-" * 30)
    labels = ['urgency', 'authority', 'fear', 'impersonation']
    for i, label in enumerate(labels):
        print(f"\n[ {label.upper()} ]")
        y_true = y_test.iloc[:, i]; y_p = y_pred[:, i]
        print(classification_report(y_true, y_p))
        print(f"Confusion Matrix (TN FP FN TP): {confusion_matrix(y_true, y_p).ravel()}")

if __name__ == "__main__":
    evaluate_model()
