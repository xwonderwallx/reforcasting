#
#
#
# __init__.py
#
#
#

from sklearn.feature_selection import f_regression
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
from modules.handlers.BinanceHandler import BinanceHandler
from modules.DataPreparator import DataPreparator
from modules.DataAnalyzer import DataAnalyzer
from modules.ModelTrainer import ModelTrainer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.dates as mdates
import matplotlib


def main():
    matplotlib.use('Agg')
    
    params = {
        'symbol': 'BTCUSDT',
        'timeframe': '1d',
        'limit': 1000,
        'days': 8650,
        'file_name': 'btc_data.csv'
    }
    dataHandler = BinanceHandler(params)
    dataHandler.handle()




    data_preparator = DataPreparator('btc_data.csv')
    data = data_preparator.load_data()
    if data is None:
        print("Data loading failed.")
        return
    
    prepared_data = data_preparator.prepare_data(data)
    data_analyzer = DataAnalyzer('btc_data.csv')
    
    prepared_data = data_analyzer.add_technical_indicators(prepared_data)
    prepared_data = data_analyzer.macd(prepared_data)
    prepared_data = data_analyzer.rsi(prepared_data)

    # returns = data['Close'].pct_change().dropna()
    # garch_model = data_analyzer.fit_garch_model(returns)





    # print(f"GARCH Model: {garch_model}")
    train_data, test_data = data_preparator.split_train_test(prepared_data)
    print(f"Length of train_data: {len(train_data)}")
    print(f"Length of test_data: {len(test_data)}")
    # train_data['Timestamp'] = train_data['Timestamp'].apply(lambda x: x.timestamp())
    # test_data['Timestamp'] = test_data['Timestamp'].apply(lambda x: x.timestamp())
    print(train_data)
    if 'Date' not in train_data.columns or 'Date' not in test_data.columns:
        raise ValueError("Date column is missing after train-test split.")

    X_train = train_data.drop(['Close'], axis=1)
    y_train = train_data['Close']
    X_test = test_data.drop(['Close'], axis=1)
    y_test = test_data['Close']
    # x_train = train_data.iloc[:, :-1]
    # y_train = train_data.iloc[:, -1]
    # x_test = test_data.iloc[:, :-1]
    X = data[['Timestamp', 'Open', 'High', 'Low', 'Volume']]
    y = data['Close']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    
    print(f"Length of X_train: {len(X_train)}, y_train: {len(y_train)}")
    print(f"Length of X_test: {len(X_test)}, y_test: {len(y_test)}")


    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    y_scaler = MinMaxScaler()
    y_train_scaled = y_scaler.fit_transform(y_train.values.reshape(-1, 1))
    y_test_scaled = y_scaler.transform(y_test.values.reshape(-1, 1))
    # Train the model
    model = RandomForestRegressor()
    model_trainer = ModelTrainer(model)
    
    trained_model = model_trainer.train_model(X_train_scaled, y_train_scaled)
    
    predictions_scaled = trained_model.predict(X_test_scaled)
    predictions = y_scaler.inverse_transform(predictions_scaled.reshape(-1, 1))

    # Now, inverse scale the predictions to bring them back to the original scale
    # predictions = scaler.inverse_transform(predictions_scaled.reshape(-1, 1))




    # Make predictions
    # predictions = model.predict(X_test)
    if len(test_data) != len(predictions):
        print(f"Mismatch: test_data has {len(test_data)} rows, but got {len(predictions)} predictions")
        return
    else:
        test_data['Predictions'] = predictions.flatten()
    
    
    
    
    test_data['Predictions'] = predictions.flatten()

    print(f"predictions: {predictions}")
    print(f"Number of predictions: {len(predictions)}")

    # Check the lengths
    print(f"Length of test_data: {len(test_data)}")
    print(f"Length of predictions: {len(predictions)}")
    

    # Ensure that test_data and predictions have the same number of rows
    if len(test_data) == len(predictions):
        test_data['Predictions'] = predictions
    else:
        print("Mismatch in length between test_data and predictions")
        return

    # Sort and reset the index for test_data
    test_data_sorted = test_data.sort_values(by='Date').reset_index(drop=True)

    # Reset the index for y_test to align with test_data_sorted
    y_test_sorted = y_test.reset_index(drop=True)

    # Create a DataFrame for plotting
    predictions_df = pd.DataFrame({
        'Date': test_data_sorted['Date'],
        'Actual': y_test_sorted,
        'Predicted': test_data_sorted['Predictions']
    })
    # predictions_df = pd.DataFrame(predictions, columns=['Predicted'])
    # predictions_df['Date'] = test_data_sorted['Date'].values

    rmse = mean_squared_error(y_test_sorted, predictions_df['Predicted'], squared=False)
    print(f'Test RMSE: {rmse}')




    # Prepare data for plotting
    plt.figure(figsize=(15, 8))
    plt.plot(test_data['Date'], test_data['Close'], label='Actual Prices', color='blue')
    plt.plot(test_data['Date'], test_data['Predictions'], label='Predicted Prices', color='red')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    plt.title('Historical and Predicted Bitcoin Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    # Replace 'path_to_save' with the actual path where you want to save the figure
    plt.savefig('historical_and_predicted_prices_fixed.png')


if __name__ == "__main__":
    main()
