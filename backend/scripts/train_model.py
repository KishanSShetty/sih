import pandas as pd
import joblib
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

def train_and_eval():
    print("Starting training...")
    
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    data_dir = os.path.join(base_dir, 'data', 'processed')
    model_dir = os.path.join(base_dir, 'models')
    
    os.makedirs(model_dir, exist_ok=True)
    
    # Load Data
    train_path = os.path.join(data_dir, 'train.csv')
    test_path = os.path.join(data_dir, 'test.csv')
    
    if not os.path.exists(train_path):
        print(f"Train data not found at {train_path}")
        return

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path) if os.path.exists(test_path) else train_df.sample(frac=0.2)
    
    print(f"Train shape: {train_df.shape}")
    print(f"Test shape: {test_df.shape}")
    
    labels = ['urgency', 'authority', 'fear', 'impersonation']
    X_train = train_df['cleaned_text'].fillna('')
    y_train = train_df[labels]
    
    X_test = test_df['cleaned_text'].fillna('')
    y_test = test_df[labels]
    
    # Vectorizer
    print("Vectorizing...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Model
    print("Training Model...")
    clf = MultiOutputClassifier(LogisticRegression(solver='liblinear', class_weight='balanced', random_state=42))
    clf.fit(X_train_vec, y_train)
    
    # Save
    print("Saving models...")
    joblib.dump(vectorizer, os.path.join(model_dir, 'vectorizer_baseline.joblib'))
    joblib.dump(clf, os.path.join(model_dir, 'model_baseline.joblib'))
    
    # Evaluate
    print("Evaluating...")
    y_pred = clf.predict(X_test_vec)
    
    overall_acc = accuracy_score(y_test, y_pred)
    print(f"Overall Accuracy: {overall_acc:.4f}")
    
    for i, label in enumerate(labels):
        print(f"\n--- {label} ---")
        y_true_lbl = y_test[label]
        y_pred_lbl = y_pred[:, i]
        
        rep = classification_report(y_true_lbl, y_pred_lbl, output_dict=True)
        print(f"Precision: {rep['1']['precision']:.4f}")
        print(f"Recall: {rep['1']['recall']:.4f}")
        print(f"F1: {rep['1']['f1-score']:.4f}")
        
        cm = confusion_matrix(y_true_lbl, y_pred_lbl)
        print(f"Confusion Matrix: {cm.tolist()}")

if __name__ == "__main__":
    train_and_eval()
