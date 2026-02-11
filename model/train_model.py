import os
import pandas as pd
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ---------- PATH SETUP (MUST BE FIRST) ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "stress_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "stress_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "model", "label_encoder.pkl")
# ----------------------------------------------

# Load dataset
data = pd.read_csv(DATA_PATH)

# Encode output labels
label_encoder = LabelEncoder()
data['stress_level'] = label_encoder.fit_transform(data['stress_level'])

# Features & target
X = data[['sleep_hours', 'study_hours', 'mood_level']]
y = data['stress_level']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Test accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Save model & encoder
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

with open(ENCODER_PATH, "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Model trained and saved successfully")
print(f"🎯 Model Accuracy: {accuracy * 100:.2f}%")
