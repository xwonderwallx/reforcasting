# DataVisualizer.py
# 
# 
# 
# 
# 
# 
# 
# 
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


class DataVisualizer():
    
    
    def __init__(self,):
        matplotlib.use('Agg')
    
    
    def save_scale(self, test_data):
        # # Prepare data for plotting
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