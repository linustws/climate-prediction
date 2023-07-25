import threading

from flask import Flask
from flask_cors import CORS

import models
from routes import routes

app = Flask(__name__)
CORS(app)
app.register_blueprint(routes)


def setup_model():
    models.setup()


# set the flag for setting up the model
setup_model_flag = True

if setup_model_flag:
    training_thread = threading.Thread(target=setup_model)
    training_thread.start()

if __name__ == '__main__':
    app.run(debug=False)
