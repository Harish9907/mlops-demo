from flask import Flask, request, jsonify
import pandas as pd
import joblib
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Load model
model = joblib.load("models/model.joblib")

# Metrics
PREDICTIONS = Counter('predictions_total', 'Total number of predictions made')

# Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame(data)
    preds = model.predict(df)
    PREDICTIONS.inc(len(preds))
    return jsonify(preds.tolist())

# Prometheus metrics endpoint
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

