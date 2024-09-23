import numpy as np
import pandas as pd

class BollingerBandsAgent:
    def __init__(self, window=20, num_std_dev=2, stop_loss=0.05, take_profit=0.1):
        self.name = "Bollinger Bands"
        self.position = 0  # 0: No position, 1: Long, -1: Short
        self.cash = 100000  # Starting cash in USD
        self.holdings = 0
        self.window = window
        self.num_std_dev = num_std_dev
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.entry_price = None

    def generate_signals(self, data):
        data = data.copy()
        data['mean'] = data['Close'].rolling(window=self.window).mean()
        data['std'] = data['Close'].rolling(window=self.window).std()
        data['upper_band'] = data['mean'] + (self.num_std_dev * data['std'])
        data['lower_band'] = data['mean'] - (self.num_std_dev * data['std'])
        
        if len(data) < self.window:
            return 0  # Hold signal

        if self.position == 0:  # No position
            if data['Close'].iloc[-1] < data['lower_band'].iloc[-1]:
                return 1  # Buy signal
            elif data['Close'].iloc[-1] > data['upper_band'].iloc[-1]:
                return 2  # Sell signal
        elif self.position == 1:  # Long position
            if data['Close'].iloc[-1] >= self.entry_price * (1 + self.take_profit):
                return 2  # Take profit
            elif data['Close'].iloc[-1] <= self.entry_price * (1 - self.stop_loss):
                return 2  # Stop loss
        elif self.position == -1:  # Short position
            if data['Close'].iloc[-1] <= self.entry_price * (1 - self.take_profit):
                return 1  # Take profit
            elif data['Close'].iloc[-1] >= self.entry_price * (1 + self.stop_loss):
                return 1  # Stop loss

        return 0  # Hold signal

    def trade(self, data):
        signal = self.generate_signals(data)
        price = data['Close'].iloc[-1]
        if signal == 1 and self.position != 1:
            if self.cash > 0:
                self.holdings = self.cash / price
                self.cash = 0
                self.position = 1
                self.entry_price = price
                print(f"{pd.Timestamp.now()}: {self.name} Buy at {price}")
        elif signal == 2 and self.position != -1:
            if self.holdings > 0:
                self.cash = self.holdings * price
                self.holdings = 0
                self.position = -1
                self.entry_price = price
                print(f"{pd.Timestamp.now()}: {self.name} Sell at {price}")
        else:
            print(f"{pd.Timestamp.now()}: {self.name} Hold")

    def get_portfolio_value(self, current_price):
        return self.cash + (self.holdings * current_price)
