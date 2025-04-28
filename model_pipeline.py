# train_and_save_model.py

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
iris = load_iris()
X, y = iris.data, iris.target

# Train a model
model = RandomForestClassifier()
model.fit(X, y)

# Save the model
joblib.dump(model, 'model.pkl')