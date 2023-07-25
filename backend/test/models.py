# setup
import threading
from datetime import datetime
from time import sleep

from schedule import every
from schedule import repeat
from schedule import run_pending

model_lock = threading.Lock()
model = None


def prepare_data():
    return "preparing data"


class LSTMModel:
    def __init__(self):
        self.is_trained = False

        self.df = prepare_data()

        self.train()
        # self.predict()

    def train(self):
        print("Training model...")

        self.is_trained = True

    def predict(self, num_months):
        print("Predicting...")


def setup():
    with model_lock:
        print("Initializing...")
        global model
        model = LSTMModel()
        print(f"Model trained on {datetime.now()}")

    # schedule the job to run every sunday
    @repeat(every().sunday)
    def job():
        with model_lock:
            # update model and retrain data
            print("Initializing new model...")
            global model
            # initialize new instance of model
            model = LSTMModel()
            print(f"Model trained on {datetime.now()}")

    while True:
        # print(idle_seconds())
        run_pending()
        sleep(1)
