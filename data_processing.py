import pandas as pd
import numpy as np
from scipy.stats import kurtosis
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc

# === Step 1: Load and clean CSV ===
df = pd.read_csv(r'C:\Users\ACER\Desktop\Monitoring Dashboard\TAPO SENSOR DATA\tapo_sensor_data.csv')

# Format datetime and numeric columns
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
df['Humidity'] = pd.to_numeric(df['Humidity'], errors='coerce')
df.dropna(subset=['DateTime', 'Temperature', 'Humidity'], inplace=True)

# Feature Extraction (Daily Statistical Features) 
daily_features = df.groupby(df['DateTime'].dt.date).agg({
    'Temperature': ['mean', 'var', lambda x: kurtosis(x, fisher=True)],
    'Humidity': ['mean', 'var', lambda x: kurtosis(x, fisher=True)]
})

daily_features.columns = [
    'Temp_mean', 'Temp_var', 'Temp_kurtosis',
    'Humidity_mean', 'Humidity_var', 'Humidity_kurtosis'
]

daily_features.reset_index(inplace=True)
daily_features.rename(columns={'DateTime':'Date'}, inplace=True)

# Create label (Example threshold: Temp_mean > 30°C = "High")
daily_features['Temp_Label'] = np.where(daily_features['Temp_mean'] > 30, 'High', 'Normal')

# Train Decision Tree and Random Forest 
X = daily_features[['Temp_mean', 'Temp_var', 'Temp_kurtosis', 
                    'Humidity_mean', 'Humidity_var', 'Humidity_kurtosis']]
y = daily_features['Temp_Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Decision Tree
dtree = DecisionTreeClassifier(random_state=42)
dtree.fit(X_train, y_train)
y_pred_tree = dtree.predict(X_test)

# Random Forest
rforest = RandomForestClassifier(n_estimators=100, random_state=42)
rforest.fit(X_train, y_train)
y_pred_forest = rforest.predict(X_test)

# === Step 4: Evaluation ===
print("\nDecision Tree Classification Report:\n", classification_report(y_test, y_pred_tree))
print("\nRandom Forest Classification Report:\n", classification_report(y_test, y_pred_forest))

# === Step 5: Feature Importance Visualization ===
feature_importance = pd.Series(rforest.feature_importances_, index=X.columns).sort_values(ascending=False)

plt.figure(figsize=(10,6))
sns.barplot(x=feature_importance, y=feature_importance.index, palette='viridis')
plt.title("Feature Importance (Random Forest)", fontsize=15)
plt.xlabel("Importance")
plt.ylabel("Features")
plt.tight_layout()
plt.show()

