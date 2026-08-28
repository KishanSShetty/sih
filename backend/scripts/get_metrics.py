import pandas as pd
import joblib
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import os
import sys
import numpy as np

def get_metrics():
    # Base directory setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir)) # DTLshit/DTLshit
    data_dir = os.path.join(base_dir, 'data', 'processed')
    model_dir = os.path.join(base_dir, 'models')
    
    print(f"Looking for data in: {data_dir}")
    print(f"Looking for models in: {model_dir}")

    # Load Data
    try:
        test_df = pd.read_csv(os.path.join(data_dir, 'test.csv'))
        print("Loaded test.csv")
    except FileNotFoundError:
        print("test.csv not found, trying val.csv", file=sys.stderr)
        try:
            test_df = pd.read_csv(os.path.join(data_dir, 'val.csv'))
            print("Loaded val.csv")
        except FileNotFoundError:
            print("No data found.", file=sys.stderr)
            return

    # Prepare Data
    if 'cleaned_text' not in test_df.columns:
        print("cleaned_text column missing")
        return
        
    X_test = test_df['cleaned_text'].fillna('')
    labels = ['urgency', 'authority', 'fear', 'impersonation']
    
    # Ensure label columns exist
    if not all(col in test_df.columns for col in labels):
        print("Label columns missing")
        return
        
    y_test = test_df[labels]

    # Load Models
    try:
        vectorizer = joblib.load(os.path.join(model_dir, 'vectorizer_baseline.joblib'))
        clf = joblib.load(os.path.join(model_dir, 'model_baseline.joblib'))
    except Exception as e:
        print(f"Error loading models: {e}", file=sys.stderr)
        return

    # Predict
    try:
        X_test_vec = vectorizer.transform(X_test)
        y_pred = clf.predict(X_test_vec)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return
    
    # Calculate metrics
    print("Optimization Analysis")
    print("=====================")
    
    overall_acc = accuracy_score(y_test, y_pred)
    print(f"Overall Subset Accuracy: {overall_acc:.4f}")
    
    report = classification_report(y_test, y_pred, target_names=labels, output_dict=True)
    
    print("\nClass-wise Metrics:")
    for i, label in enumerate(labels):
        print(f"\nLabel: {label}")
        print(f"Precision: {report[label]['precision']:.4f}")
        print(f"Recall:    {report[label]['recall']:.4f}")
        print(f"F1 Score:  {report[label]['f1-score']:.4f}")
        print(f"Support:   {report[label]['support']}")
        
        # Confusion Matrix
        # Handle different y_pred shapes if necessary, assumming numpy array [n_samples, n_classes]
        if isinstance(y_pred, list):
             # Some sklearn wrappers return list of arrays
             current_y_pred = y_pred[i]
        elif len(y_pred.shape) > 1:
             current_y_pred = y_pred[:, i]
        else:
             # Should not happen for multilabel with 4 classes
             current_y_pred = y_pred
             
        cm = confusion_matrix(y_test[label], current_y_pred)
        # TN, FP, FN, TP
        tn, fp, fn, tp = cm.ravel()
        print(f"Confusion Matrix: TN={tn}, FP={fp}, FN={fn}, TP={tp}")

if __name__ == "__main__":
    get_metrics()
