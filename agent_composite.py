import numpy as np
import pandas as pd
import talib

class CompositeAgent:
    def __init__(self, short_window=50, long_window=200):
        self.name = "Composite Agent"
        self.position = 0  # 0: No position, 1: Long, -1: Short
        self.cash = 100000  # Starting cash in USD
        self.holdings = 0
        self.short_window = short_window
        self.long_window = long_window
        self.bollinger_window = 20
        self.macd_fast = 12
        self.macd_slow = 26
        self.rsi_window = 14
        self.atr_window = 14

    def generate_signals(self, data):
        # Create a copy of the data to avoid SettingWithCopyWarning
        data = data.copy()

        # Calculate indicators
        data['EMA'] = talib.EMA(data['Close'].values, timeperiod=self.short_window)
        data['SMA'] = talib.SMA(data['Close'].values, timeperiod=self.long_window)
        data['upper_band'], data['middle_band'], data['lower_band'] = talib.BBANDS(data['Close'].values, timeperiod=self.bollinger_window)
        data['macd'], data['macd_signal'], _ = talib.MACD(data['Close'].values, fastperiod=self.macd_fast, slowperiod=self.macd_slow)
        data['rsi'] = talib.RSI(data['Close'].values, timeperiod=self.rsi_window)
        data['atr'] = talib.ATR(data['High'].values, data['Low'].values, data['Close'].values, timeperiod=self.atr_window)

        # Generate signals based on indicators
        if (data['EMA'].iloc[-1] > data['SMA'].iloc[-1] and
            data['Close'].iloc[-1] > data['upper_band'].iloc[-1] and
            data['macd'].iloc[-1] > data['macd_signal'].iloc[-1] and
            data['rsi'].iloc[-1] > 50 and
            data['Close'].iloc[-1] > data['Close'].iloc[-2] and
            data['Close'].iloc[-1] > (data['Close'].iloc[-2] + data['atr'].iloc[-1])):
            return 1  # Buy signal
        elif (data['EMA'].iloc[-1] < data['SMA'].iloc[-1] and
              data['Close'].iloc[-1] < data['lower_band'].iloc[-1] and
              data['macd'].iloc[-1] < data['macd_signal'].iloc[-1] and
              data['rsi'].iloc[-1] < 50 and
              data['Close'].iloc[-1] < data['Close'].iloc[-2] and
              data['Close'].iloc[-1] < (data['Close'].iloc[-2] - data['atr'].iloc[-1])):
            return -1  # Sell signal
        else:
            return 0  # Hold signal

    def trade(self, data):
        signal = self.generate_signals(data)
        price = data['Close'].iloc[-1]

        if signal == 1 and self.position != 1:  # Buy signal
            if self.cash > 0:
                self.holdings = self.cash / price
                self.cash = 0
                self.position = 1
                print(f"{pd.Timestamp.now()}: {self.name} Buy at {price}")
        elif signal == -1 and self.position != -1:  # Sell signal
            if self.holdings > 0:
                self.cash = self.holdings * price
                self.holdings = 0
                self.position = -1
                print(f"{pd.Timestamp.now()}: {self.name} Sell at {price}")
        else:
            print(f"{pd.Timestamp.now()}: {self.name} Hold")

    def get_portfolio_value(self, current_price):
        return self.cash + (self.holdings * current_price)
