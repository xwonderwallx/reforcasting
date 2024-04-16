import csv


class CsvHelper:
    @staticmethod
    def save_binance_data_csv(data, file_name):
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Timestamp', 'Open', 'High',
                             'Low', 'Close', 'Volume'])
            for candle in data:
                timestamp, open_price, high, low, close, volume = candle
                writer.writerow(
                    [timestamp, open_price, high, low, close, volume])
