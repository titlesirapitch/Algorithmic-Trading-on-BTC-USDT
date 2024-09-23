import numpy as np
import pandas as pd

class EMAVAgent:
    def __init__(self, ema_short_window=12, ema_long_window=26, volume_threshold=1.5):
        self.name = "EMA-Volume"
        self.position = 0  # 0: No position, 1: Long, -1: Short
        self.cash = 100000  # Starting cash in USD
        self.holdings = 0
        self.ema_short_window = ema_short_window
        self.ema_long_window = ema_long_window
        self.volume_threshold = volume_threshold

    def calculate_ema(self, data, window):
        return data['Close'].ewm(span=window, adjust=False).mean().iloc[-1]

    def generate_signals(self, data):
        if len(data) < max(self.ema_short_window, self.ema_long_window):
            return 0  # If there's not enough data, return Hold signal

        ema_short = self.calculate_ema(data, self.ema_short_window)
        ema_long = self.calculate_ema(data, self.ema_long_window)
        current_volume = data['Volume'].iloc[-1]

        # Check if there's enough data to compare with previous volume
        if len(data) > 1:
            previous_volume = data['Volume'].iloc[-2]
        else:
            previous_volume = current_volume

        # Generate signals
        if ema_short > ema_long and current_volume > previous_volume * self.volume_threshold:
            return 1  # Buy signal
        elif ema_short < ema_long and current_volume > previous_volume * self.volume_threshold:
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

