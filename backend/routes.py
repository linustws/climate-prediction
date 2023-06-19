from flask import request, jsonify
from models import model
from app import app

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    input_data = request.form['input_field']
    selected_option = request.form['dropdown']

    if selected_option == 'Years':
        num_months = int(input_data) * 12
    else:
        num_months = int(input_data)

    # Perform prediction using the model
    prediction = model.predict(num_months)

    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction})
