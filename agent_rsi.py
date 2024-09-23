import numpy as np
import pandas as pd

class RSIAgent:
    def __init__(self, sma_window=50, rsi_window=14, overbought=70, oversold=30):
        self.name = "SMA-RSI"
        self.position = 0  # 0: No position, 1: Long, -1: Short
        self.cash = 100000  # Starting cash in USD
        self.holdings = 0
        self.sma_window = sma_window
        self.rsi_window = rsi_window
        self.overbought = overbought
        self.oversold = oversold

    def calculate_sma(self, data):
        return data['Close'].rolling(window=self.sma_window, min_periods=1).mean().iloc[-1]

    def calculate_rsi(self, data):
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=self.rsi_window, min_periods=1).mean()
        avg_loss = loss.rolling(window=self.rsi_window, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]

    def generate_signals(self, data):
        sma = self.calculate_sma(data)
        rsi = self.calculate_rsi(data)

        # Generate signals
        if data['Close'].iloc[-1] > sma and rsi > self.overbought:
            return 2  # Sell signal (overbought and above SMA)
        elif data['Close'].iloc[-1] < sma and rsi < self.oversold:
            return 1  # Buy signal (oversold and below SMA)
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