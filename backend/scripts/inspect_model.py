import joblib
import os
import sys

def inspect():
    # Base directory setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir)) # DTLshit/DTLshit
    model_dir = os.path.join(base_dir, 'models')
    
    v_path = os.path.join(model_dir, 'vectorizer_baseline.joblib')
    print(f"Loading from {v_path}")
    
    try:
        vec = joblib.load(v_path)
        print(f"Type: {type(vec)}")
        print(f"Dir: {dir(vec)}")
        if hasattr(vec, 'idf_'):
            print(f"idf_ shape: {vec.idf_.shape}")
        else:
            print("idf_ attribute MISSING")
            
        # Try a dummy transform to see if it fails here
        try:
            res = vec.transform(["test"])
            print("Transform successful")
        except Exception as e:
            print(f"Transform failed: {e}")

    except Exception as e:
        print(f"Load vectorizer failed: {e}")

    m_path = os.path.join(model_dir, 'model_baseline.joblib')
    print(f"Loading model from {m_path}")
    try:
        clf = joblib.load(m_path)
        print(f"Model Type: {type(clf)}")
        print(f"Model Dir: {dir(clf)}")
    except Exception as e:
        print(f"Load model failed: {e}")

if __name__ == "__main__":
    inspect()
