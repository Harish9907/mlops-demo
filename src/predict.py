import joblib
import numpy as np

model = joblib.load("models/model.pkl")
X = np.array([[5.1, 3.5, 1.4, 0.2]])
pred = model.predict(X)
print("Prediction:", pred[0])

