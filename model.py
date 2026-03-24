# ==========================================
# model.py - Train Model & Save as Pickle
# ==========================================

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# 1. Load Dataset
df = pd.read_csv("Digital_Payment_Fraud_Detection_Dataset.csv")

print("Dataset Loaded Successfully")
print("Shape:", df.shape)

# 2. Encode Categorical Columns
label_encoders = {}

for col in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

print("Categorical Columns Encoded")

# 3. Define Target Column
if 'isFraud' in df.columns:
    target_col = 'isFraud'
else:
    target_col = df.columns[-1]

X = df.drop(columns=[target_col])
y = df[target_col]

# 4. Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 5. Train Model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

print("Model Trained Successfully")

# 6. Save Model as Pickle
with open("fraud_model.pkl", "wb") as file:
    pickle.dump(model, file)

# 7. Save Encoders
with open("label_encoders.pkl", "wb") as file:
    pickle.dump(label_encoders, file)

print("✅ fraud_model.pkl and label_encoders.pkl created successfully!")
