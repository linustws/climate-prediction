from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

from models import model

routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return render_template('index.html')


@routes.route('/model')
def model_page():
    return render_template('Singapore Weather Prediction.html')


@routes.route('/predict', methods=['POST'])
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
