import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_squared_error

# 1. Load Data
data_path = 'backend/data/temporal_dataset.csv'
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit()

df = pd.read_csv(data_path)
print(f"Loaded {len(df)} samples.")

# 2. Preprocessing
X = df['text']
y_category = df['category']
y_temporal = df['temporal_score']
y_urgency = df['urgency']
y_fear = df['fear']

# 3. Train/Test Split
# Since the dataset is small, we'll train on most of it, but good practice to split.
X_train, X_test, y_cat_train, y_cat_test, y_temp_train, y_temp_test = train_test_split(
    X, y_category, y_temporal, test_size=0.1, random_state=42
)

print("Training Category Classifier...")
# 4. Category Classifier Pipeline
cat_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])
cat_pipeline.fit(X_train, y_cat_train)
print("Category Accuracy:", cat_pipeline.score(X_test, y_cat_test))

print("Training Temporal Score Regressor...")
# 5. Temporal Score Regressor Pipeline
temp_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
    ('reg', RandomForestRegressor(n_estimators=100, random_state=42))
])
temp_pipeline.fit(X_train, y_temp_train)
print("Temporal MSE:", mean_squared_error(y_temp_test, temp_pipeline.predict(X_test)))

# 6. Save Models
model_dir = 'backend/models'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

with open(f'{model_dir}/temporal_analysis_v1.pkl', 'wb') as f:
    pickle.dump({
        'category_model': cat_pipeline,
        'temporal_model': temp_pipeline
    }, f)

print(f"✅ Models saved to {model_dir}/temporal_analysis_v1.pkl")
