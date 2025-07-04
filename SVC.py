"""
svc.py

Trains a Support Vector Classifier (SVC) to predict menstrual cycle phases
using physiological and exertion data, with PCA for dimensionality reduction,
and includes SHAP explainability for feature importance analysis.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import shap

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# -----------------------------
# 1️⃣ Load and preprocess data
# -----------------------------
# Load dataset
df = pd.read_csv("C:\\Users\\shruj\\Downloads\\SMOTE4_updated.csv")

# Drop ID column if present
df = df.drop(columns=['ID'])

# Split features and target
X = df.drop(columns=['phase'])  # Features
y = df['phase']                 # Target

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA to retain 95% variance
pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)

# -----------------------------
# 2️⃣ Split data for training/testing
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_pca, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# 3️⃣ Train SVM Model
# -----------------------------
clf = SVC(
    kernel='rbf',
    C=10.0,
    gamma='scale',
    random_state=42,
    probability=True  # Enables predict_proba for SHAP
)
clf.fit(X_train, y_train)

# -----------------------------
# 4️⃣ Evaluate Model
# -----------------------------
y_pred = clf.predict(X_test)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(
    cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=np.unique(y), yticklabels=np.unique(y)
)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Accuracy and Classification Report
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}\n')
print("Classification Report:\n", classification_report(y_test, y_pred))

# -----------------------------
# 5️⃣ SHAP Explainability
# -----------------------------
print("Computing SHAP values for model explainability...")
explainer = shap.Explainer(clf.predict_proba, X_train)
shap_values = explainer(X_test)

# SHAP Summary Plot
shap.summary_plot(shap_values, X_test)
