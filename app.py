from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

def predict_next_pivot(data):
    close = np.array(data["close"])
    high  = np.array(data["high"])
    low   = np.array(data["low"])

    recent_close = close[-1]
    volatility = np.std(high - low)
    trend = close[-1] - close[-20]

    top_prob = 0.5 - (trend * 0.0001) + (volatility * 0.2)
    top_prob = float(max(0, min(top_prob, 1)))
    bottom_prob = float(1 - top_prob)

    top_target = float(recent_close + volatility * 1.2)
    bottom_target = float(recent_close - volatility * 1.2)

    return {
        "top_prob": top_prob,
        "bottom_prob": bottom_prob,
        "top_target": top_target,
        "bottom_target": bottom_target
    }

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    result = predict_next_pivot(data)
    return jsonify(result)

@app.route('/', methods=['GET'])
def home():
    return "momo-zigzag-ai server running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
