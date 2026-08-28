import pandas as pd
import joblib
import os
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def train_authority_head():
    print("Training Dedicated Authority Binary Head...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    data_path = os.path.join(base_dir, 'data', 'processed', 'train.csv')
    model_dir = os.path.join(base_dir, 'models')
    
    # Load full dataset
    df = pd.read_csv(data_path)
    
    # Filter for Authority Only
    # We want to train "Is prediction Authority?"
    # y = 1 if authority column is 1, else 0
    df['target'] = df['authority']
    
    # Create clean subset
    authority_df = df[['text', 'target']]
    
    # Save for reference
    authority_df.to_csv(os.path.join(base_dir, 'data', 'processed', 'authority_only.csv'), index=False)
    print(f"Created authority_only.csv with {len(authority_df)} samples")
    
    # Vectorizer (Hashing for Speed/Scale as requested)
    vectorizer = HashingVectorizer(
        n_features=2**20,
        alternate_sign=False,
        ngram_range=(3, 5), # Character n-grams for robustness
        analyzer="char"
    )
    
    X = vectorizer.transform(authority_df['text'].fillna(''))
    y = authority_df['target']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Classifier
    clf = SGDClassifier(loss="log_loss", random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    print("\n--- Authority Binary Head Performance ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))
    
    # Save
    joblib.dump(clf, os.path.join(model_dir, 'authority_head.joblib'))
    joblib.dump(vectorizer, os.path.join(model_dir, 'authority_vectorizer.joblib'))
    print("Saved authority_head.joblib and authority_vectorizer.joblib")

if __name__ == "__main__":
    train_authority_head()
