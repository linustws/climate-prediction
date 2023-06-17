from flask import Flask, request, jsonify
from models import LSTMModel

app = Flask(__name__)

# Instantiate the model
model = LSTMModel()

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    data = request.json

    # Perform prediction using the model
    prediction = model.predict(data)

    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction})

@app.route('/health', methods=['GET'])
def health_check():
    # Perform health check
    status = model.check_health()

    # Return the health status as a JSON response
    return jsonify({'status': status})

if __name__ == '__main__':
    app.run(debug=True)
