import threading

from flask import Flask

import models
from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)


def setup_model():
    models.setup()


# set the flag for setting up the model
setup_model_flag = False

if setup_model_flag:
    training_thread = threading.Thread(target=setup_model)
    training_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
