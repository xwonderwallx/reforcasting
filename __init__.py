#
#
#
# __init__.py
#
#
#
import logging
import matplotlib
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV

from modules.handlers.BinanceHandler import BinanceHandler
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

from scipy.stats import randint as sp_randint


def main():
    matplotlib.use('Agg')

    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    file_path = 'btc_data.csv'

    params = {
        'symbol': 'BTCUSDT',
        'timeframe': '1d',
        'file_name': file_path
    }
    data_handler = BinanceHandler(params)
    data_handler.handle()
    logging.debug(f'\nData handler: {data_handler}')
    logging.debug(f'\n---------------------------------------\n')




if __name__ == "__main__":
    main()
