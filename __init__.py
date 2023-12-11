#
#
#
# __init__.py
#
#
#


from sklearn.metrics import mean_squared_error
import pandas as pd
from modules.handlers.BinanceHandler import BinanceHandler
import numpy as np
import matplotlib
import logging
from modules.DataProcessor import DataProcessor
from modules.ModelTrainer import ModelTrainer
from modules.DataVisualizer import DataVisualizer
from sklearn.ensemble import RandomForestRegressor


def main():
    
    matplotlib.use('Agg')
    
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    
    file_path = 'btc_data.csv'
    
    params = {
        'symbol': 'BTCUSDT',
        'timeframe': '1d',
        'limit': 1000,
        'days': 400,
        'file_name': file_path
    }
    data_handler = BinanceHandler(params)
    data_handler.handle()
    logging.debug('\nThis is a debug message')
    
    data_processor =  DataProcessor(file_path)
    train_data, test_data = data_processor.get_test_and_train_sets()
    if train_data is None or test_data is None:
        logging.error("Data loading or splitting failed.")
        return

    # Initialize the model trainer with a RandomForestRegressor model
    model_trainer = ModelTrainer(RandomForestRegressor(), 'btc_data.csv')
    
    # Handle training data preparation
    X_train, y_train, X_test, y_test = model_trainer.handle_train_data()
    
    # Train the model
    trained_model, scaler = model_trainer.train_model(X_train, y_train)
    
    # Predict using the trained model
    predictions = model_trainer.predict(X_test, scaler)
    test_data = test_data.copy()
    test_data['Predictions'] = predictions
    
    # # Visualize the results
    visualizer = DataVisualizer()
    visualizer.save_scale(test_data)


if __name__ == "__main__":
    main()
