from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib, os

def train():
    iris = load_iris(as_frame=True)
    X, y = iris.data, iris.target
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.pkl")
    print("Model trained and saved at models/model.pkl")

if __name__ == "__main__":
    train()

