import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

def train_final_v5():  
    print("Starting Final V5 Training (Max Performance)...")  

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
    print("Class Distribution (Positive samples):")
    print(full_df[['urgency', 'authority', 'fear', 'impersonation']].sum())
    
    # Shuffle
    full_df = full_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    labels = ['urgency', 'authority', 'fear', 'impersonation']  
    X = full_df['cleaned_text'].fillna('')  
    y = full_df[labels]  
    
    # 80/20 Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  

    # Vectorize - Enhanced n-grams (1,2)
    vectorizer = TfidfVectorizer(
        max_features=10000, 
        stop_words='english', 
        token_pattern=r'\b\w+\b',
        ngram_range=(1, 2),
        min_df=1
    )  
    
    X_train_vec = vectorizer.fit_transform(X_train)  
    X_test_vec = vectorizer.transform(X_test)  

    # Model - Balanced Weights
    clf = MultiOutputClassifier(LogisticRegression(
        solver='liblinear', 
        class_weight='balanced',
        C=1.0, 
        random_state=42
    ))  
    
    clf.fit(X_train_vec, y_train)  

    # Save  
    joblib.dump(vectorizer, os.path.join(model_dir, 'vectorizer_baseline.joblib'))  
    joblib.dump(clf, os.path.join(model_dir, 'model_baseline.joblib'))  

    # Evaluate  
    y_pred = clf.predict(X_test_vec)  
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
    train_final_v5()
