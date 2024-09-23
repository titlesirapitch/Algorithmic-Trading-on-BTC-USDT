import numpy as np
import pandas as pd

class MACDAgent:
    def __init__(self, short_window=12, long_window=26, signal_window=9):
        self.name = "MACD"
        self.position = 0  # 0: No position, 1: Long, -1: Short
        self.cash = 100000  # Starting cash in USD
        self.holdings = 0
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window
        self.macd_line = None
        self.signal_line = None

    def generate_signals(self, data):
        data = data.copy()
        data.loc[:, 'short_ema'] = data['Close'].ewm(span=self.short_window, adjust=False).mean()
        data.loc[:, 'long_ema'] = data['Close'].ewm(span=self.long_window, adjust=False).mean()
        data.loc[:, 'macd_line'] = data['short_ema'] - data['long_ema']
        data.loc[:, 'signal_line'] = data['macd_line'].ewm(span=self.signal_window, adjust=False).mean()

        if data['macd_line'].iloc[-1] > data['signal_line'].iloc[-1]:
            return 1  # Buy signal
        elif data['macd_line'].iloc[-1] < data['signal_line'].iloc[-1]:
            return 2  # Sell signal
        else:
            return 0  # Hold signal

    def trade(self, data):
        signal = self.generate_signals(data)
        price = data['Close'].iloc[-1]
        if signal == 1 and self.position != 1:
            if self.cash > 0:
                self.holdings = self.cash / price
                self.cash = 0
                self.position = 1
                print(f"{pd.Timestamp.now()}: {self.name} Buy at {price}")
        elif signal == 2 and self.position != -1:
            if self.holdings > 0:
                self.cash = self.holdings * price
                self.holdings = 0
                self.position = -1
                print(f"{pd.Timestamp.now()}: {self.name} Sell at {price}")
        else:
            print(f"{pd.Timestamp.now()}: {self.name} Hold")

    def get_portfolio_value(self, current_price):
        return self.cash + (self.holdings * current_price)
