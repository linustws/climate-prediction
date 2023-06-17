# setup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.offline as pyo
import requests
import tensorflow as tf
import os
import schedule

from datetime import datetime, timedelta
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.models import Sequential
from keras.preprocessing.sequence import TimeseriesGenerator
from pmdarima import auto_arima
from sklearn import preprocessing
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.statespace.varmax import VARMAX
from schedule import every, repeat, run_pending, idle_seconds
from time import time
from time import sleep

px.defaults.template = 'plotly'  # plotly, plotly_dark
pyo.init_notebook_mode(connected=True)
pio.renderers.default = "iframe"  # must trust notebook for it to work, use iframe for lab

# set the seed for numpy module
np.random.seed(123)

# set the seed for tensorflow module
tf.random.set_seed(123)

api_endpoint = "https://data.gov.sg/api/action/datastore_search"

# resource ids
surface_air_temp_monthly_mean_resource_id = "07654ce7-f97f-49c9-81c6-bd41beba4e96"
# surface_air_temp_monthly_abs_extreme_max_resource_id = "96e66346-68bb-4ca9-b001-58bbf39e36a7"
# surface_air_temp_monthly_abs_extreme_min_resource_id = "0c5b9752-2488-46cc-ae1c-42318d0f8865"
# rainfall_monthly_total_resource_id = "778814b8-1b96-404b-9ac9-68d6c00e637b"
# rainfall_monthly_max_daily_total_resource_id = "df4d391e-6950-4fc6-80cd-c9b9ef6354fe"
# rainfall_monthly_num_rain_days_resource_id = "8b94f596-91fd-4545-bf9e-7a426493b674"
# relative_humidity_monthly_mean_resource_id = "4631174f-9858-463d-8a88-f3cb21588c67"
# relative_humidity_monthly_abs_extreme_min_resource_id = "585c24a5-76cd-4c48-9341-9223de5adc1d"
# sunshine_duration_monthly_mean_daily_resource_id = "0230819f-1c83-4980-b738-56136d6dc300"

resource_ids = [surface_air_temp_monthly_mean_resource_id]


# resource_ids = [surface_air_temp_monthly_mean_resource_id,
# surface_air_temp_monthly_abs_extreme_max_resource_id,
# surface_air_temp_monthly_abs_extreme_min_resource_id,
# rainfall_monthly_total_resource_id,
# rainfall_monthly_max_daily_total_resource_id,
# rainfall_monthly_num_rain_days_resource_id,
# relative_humidity_monthly_mean_resource_id,
# relative_humidity_monthly_abs_extreme_min_resource_id,
# sunshine_duration_monthly_mean_daily_resource_id]

# call APIs
def prepare_data():
    merged_df = None
    for resource_id in resource_ids:
        url = api_endpoint + "?resource_id=" + resource_id + "&limit=1000"
        response = requests.get(url).json()
        data = response['result']['records']
        df = pd.DataFrame(data).set_index('month').drop('_id', axis=1)
        if merged_df is None:
            print("Acquiring data...")
            merged_df = df
            continue
        merged_df = pd.merge(merged_df, df, on='month')

    # data until April 2023 when this was executed
    merged_df = merged_df[:496]
    # print(merged_df)

    # rename columns
    new_names = {'max_temperature': 'max_temp', 'temp_extremes_min': 'min_temp',
                 'maximum_rainfall_in_a_day': 'max_rainfall_daily', 'no_of_rainy_days': 'num_rainy_days',
                 'rh_extremes_minimum': 'min_rh', 'mean_sunshine_hrs': 'mean_sunshine_hrs_daily'}
    df = merged_df.rename(columns=new_names)
    df = df.rename_axis('datetime')
    df.index = pd.to_datetime(df.index)
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='raise')
    print(df)
    return df


class LSTMModel:
    def __init__(self):
        # set seed to ensure determinism and reproducibility (always retest from here)
        os.environ['TF_DETERMINISTIC_OPS'] = '1'
        tf.keras.utils.set_random_seed(1)
        tf.config.experimental.enable_op_determinism()

        self.df = prepare_data()
        self.series_monthly_mean_temp = self.df['mean_temp'].resample('M').mean()
        self.series_yearly_mean_temp = self.df['mean_temp'].resample('Y').mean()
        self.scaler = MinMaxScaler()
        # split to test 1 year of data
        self.train_end = datetime(2022, 1, 1)
        self.test_end = datetime(2023, 1, 1)
        self.train_data = None
        self.test_data = None
        self.train_data_norm = None
        self.test_data_norm = None
        self.n_input = 12
        self.n_features = 1
        # define model
        self.model = Sequential()
        self.model.add(LSTM(100, activation='tanh', input_shape=(
            self.n_input, self.n_features)))  # here i used tanh instead of relu to take advantage of cuDNN to speed up
        # training
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1))
        # optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')
        # self.model.summary()
        self.loss = None

        self.train()
        self.predict()

    def train(self):
        df_monthly_mean_temp = self.series_monthly_mean_temp.to_frame()  # convert Series to DataFrame
        self.scaler.fit(df_monthly_mean_temp)
        df_normalised_monthly_mean_temp = self.scaler.transform(df_monthly_mean_temp)

        # create a new DataFrame with the normalized values
        df_normalised_monthly_mean_temp = pd.DataFrame(df_normalised_monthly_mean_temp, columns=['normalised'],
                                                       index=df_monthly_mean_temp.index)
        mean_normalised_monthly_mean_temp = df_normalised_monthly_mean_temp['normalised'].mean()

        # plot the normalized data
        fig_normalised_monthly_mean_temp = px.line(df_normalised_monthly_mean_temp,
                                                   labels={df_normalised_monthly_mean_temp.index.name: 'Datetime',
                                                           'value': 'Normalised'}, title='Normalised Mean Temperature')
        fig_normalised_monthly_mean_temp.update_xaxes(dtick='M12', tickangle=45)
        fig_normalised_monthly_mean_temp.update_yaxes(dtick=0.2, tickangle=45)
        fig_normalised_monthly_mean_temp.update_traces(hovertemplate='Datetime: %{x}<br>Normalised Value: %{y}')

        # add the mean line
        fig_normalised_monthly_mean_temp.add_shape(
            type="line",
            x0=df_normalised_monthly_mean_temp.index[0],
            y0=mean_normalised_monthly_mean_temp,
            x1=df_normalised_monthly_mean_temp.index[-1],
            y1=mean_normalised_monthly_mean_temp,
            line=dict(color="red", dash="dot"),
        )
        # fig_normalised_monthly_mean_temp.show()

        self.train_data = df_monthly_mean_temp[:self.train_end]
        self.test_data = df_monthly_mean_temp[self.train_end + timedelta(days=1):self.test_end]
        self.train_data_norm = df_normalised_monthly_mean_temp[:self.train_end].values
        self.test_data_norm = df_normalised_monthly_mean_temp[self.train_end + timedelta(days=1):self.test_end].values

        # define generator
        generator = TimeseriesGenerator(self.train_data_norm, self.train_data_norm, length=self.n_input, batch_size=1)

        # fit model and save history
        history = self.model.fit(generator, epochs=300)
        self.loss = history.history['loss']

    def predict(self):
        predictions_norm = []

        first_eval_batch = self.train_data_norm[-self.n_input:]
        current_batch = first_eval_batch.reshape((1, self.n_input, self.n_features))

        for i in range(len(self.test_data)):

            # get the prediction value for the first batch
            current_pred = self.model.predict(current_batch)[0]

            # append the prediction into the array
            predictions_norm.append(current_pred)

            # use the prediction to update the batch and remove the first value
            current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

        predictions = self.scaler.inverse_transform(predictions_norm)

        residuals = self.test_data - predictions

        # plot_data = pd.DataFrame({'datetime': self.test_data.index, 'test_data': self.test_data.values.flatten(),
        #                           'predictions': predictions.flatten()})
        # fig_pred_test = px.line(plot_data, x='datetime', y=['test_data', 'predictions'], labels={'datetime': 'Datetime', 'value': 'Mean Temperature (°C)'}, title='Test Data and Predictions')
        # fig_pred_test.update_xaxes(dtick='M1', tickangle=45)
        # fig_pred_test.update_yaxes(dtick=0.5, tickangle=45)
        # fig_pred_test.update_traces(hovertemplate='Datetime: %{x}<br>Mean Temperature: %{y}°C')
        # fig_pred_test.show()

        print(f"Mean Absolute Percent Error: {round(np.mean(abs(residuals/self.test_data), axis=0).item(), 4)}")
        print(f"Root Mean Squared Error: {np.sqrt(np.mean(residuals**2, axis=0)).item()}")


model = LSTMModel()


# schedule the job to run every sunday
@repeat(every().sunday)
def job():
    # update model and retrain data
    print("Updating model and retraining...")
    global model
    model = LSTMModel()


while True:
    # print(idle_seconds())
    run_pending()
    sleep(1)
