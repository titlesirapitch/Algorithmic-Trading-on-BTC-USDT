import numpy as np
import pandas as pd

class MomentumAgent:
    def __init__(self, window=10, momentum_threshold=0.01, stop_loss=0.05, take_profit=0.1):
        self.name = "Momentum"
        self.position = 0  # 0: No position, 1: Long, -1: Short
        self.cash = 100000  # Starting cash in USD
        self.holdings = 0
        self.window = window
        self.momentum_threshold = momentum_threshold
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.entry_price = None

    def generate_signals(self, data):
        data = data.copy()
        data['momentum'] = data['Close'].diff(self.window)

        if self.position == 0:  # No position
            if data['momentum'].iloc[-1] > self.momentum_threshold:
                return 1  # Buy signal
            elif data['momentum'].iloc[-1] < -self.momentum_threshold:
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
