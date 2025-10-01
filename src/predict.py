import joblib
import numpy as np

model = joblib.load("models/model.joblib")
X = np.array([[5.1, 3.5]])
pred = model.predict(X)
print("Prediction:", pred[0])

