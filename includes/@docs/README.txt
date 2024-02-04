The config.json have this structure:
{
    "configuration"
}


{
  "configuration": {
    "paths":  {
      "exchange_data": "./includes/exchange_data/",
      "models": "./includes/models/"
    },
    "google": {
      "keys": {
        "google_search_api_key": "AIzaSyAqyM54rnijEfhWEknjRIkcg9ckRNbGZEY",
        "google_search_engine_id": "63291c7fac9464af2"
      }
    },
    "exchange_data": {
      "trading_pairs": {
        "binance": [
          "BTCUSDT",
          "ETHUSDT",
          "BNBUSDT",
          "XRPUSDT",
          "ADAUSDT",
          "SOLUSDT",
          "DOGEUSDT",
          "DOTUSDT",
          "LTCUSDT",
          "BCHUSDT",
          "LINKUSDT",
          "XLMUSDT",
          "UNIUSDT",
          "EOSUSDT",
          "TRXUSDT",
          "XTZUSDT",
          "AAVEUSDT"
        ]
      }
    }
  },
  "default_handler_cdata": {
    "symbol": "BTCUSDT",
    "timeframe": "1d",
    "save_csv_path": "btc_data.csv"
  },
  "ml_model": {
    "cdata": {
      "hyper_parameters": {
        "features": [
          "Close",
          "Volume",
          "RSI",
          "MACD",
          "Signal_Line",
          "MACD_Histogram",
          "Upper_BB",
          "Lower_BB"
        ],
        "epochs": 150,
        "batch_size": 16
      },
      "datasets_params": {
        "features": [
          "Close",
          "Volume",
          "RSI",
          "MACD",
          "Signal_Line",
          "MACD_Histogram",
          "Upper_BB",
          "Lower_BB"
        ],
        "test_set": {
          "size": 0.2
        },
        "train_set": {
          "size": 0.8
        },
        "sequence_default_length": 60,
        "look_back": 60,
        "callbacks": {
          "early_stopping": {
            "monitor": "val_loss",
            "patience": 20,
            "restore_best_weights": true
          },
          "model_checkpoint": {
            "save_file_path": "cdata_model.keras",
            "save_best_only": true,
            "monitor": "val_loss",
            "mode": "min"
          },
          "reduce_lr": {
            "monitor": "val_loss",
            "factor": 0.2,
            "patience": 5,
            "min_lr": 0.0001
          }
        }
      },
      "technical_indicators": {
        "sma_period": 20,
        "standard_deviation_multiplier": 2,
        "relative_volatility_index_period": 10
      }
    },
    "pdirection": {
      "hyper_parameters": {
        "features": [
          "Close",
          "Volume",
          "RSI",
          "MACD",
          "Signal_Line",
          "MACD_Histogram",
          "Upper_BB",
          "Lower_BB"
        ],
        "epochs": 150,
        "batch_size": 16,
        "look_back": 60,
        "callbacks": {
          "early_stopping": {
            "monitor": "val_loss",
            "patience": 20,
            "restore_best_weights": true
          },
          "model_checkpoint": {
            "save_file_path": "pd_model.keras",
            "save_best_only": true,
            "monitor": "val_loss",
            "mode": "min"
          },
          "reduce_lr": {
            "monitor": "val_loss",
            "factor": 0.2,
            "patience": 5,
            "min_lr": 0.0001
          }
        },
        "compiling": {
          "optimizer": {
            "name": "Adam",
            "learning_rate": 0.0005
          },
          "loss": "binary_crossentropy",
          "metrics": [
            "accuracy"
          ]
        },
        "model_layers": {
          "first": {
            "bidirectional": {
              "gru": {
                "units": 128,
                "return_sequences": true
              }
            }
          },
          "second": {
            "dropout": 0.4
          },
          "third": {
            "bidirectional": {
              "gru": {
                "units": 64,
                "return_sequences": false
              }
            }
          },
          "fourth": {
            "dropout": 0.4
          },
          "fifth": {
            "dense": {
              "units": 1,
              "activation_function": "sigmoid"
            }
          }
        }
      },
      "datasets_params": {
      }
    }
  }
}