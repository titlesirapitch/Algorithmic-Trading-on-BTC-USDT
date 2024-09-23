
# Algorithmic Trading Strategies

## Overview

This project implements various algorithmic trading strategies using Python. The strategies are designed to operate over different time intervals and can be backtested using historical data. The project includes a set of agents, each representing a different trading strategy, and several Jupyter notebooks to simulate and backtest these strategies.

## Project Structure

- **Agents**:
  - `agent_BollingerBands.py`: Implements a Bollinger Bands strategy.
  - `agent_composite.py`: Combines multiple strategies into a composite agent.
  - `agent_dummy.py`: A simple dummy agent for testing purposes.
  - `agent_emav.py`: Implements an Exponential Moving Average (EMA) strategy.
  - `agent_ma.py`: Implements a Moving Average (MA) strategy.
  - `agent_macd.py`: Implements a MACD (Moving Average Convergence Divergence) strategy.
  - `agent_momentum.py`: Implements a Momentum-based strategy.
  - `agent_mr.py`: Implements a Mean Reversion strategy.
  - `agent_rsi.py`: Implements an RSI (Relative Strength Index) strategy.

- **Jupyter Notebooks**:
  - `Backtesting.ipynb`: Backtests the strategies on historical data.
  - `simulation 1d.ipynb`: Simulates trading over 1-day intervals.
  - `simulation 1h.ipynb`: Simulates trading over 1-hour intervals.
  - `simulation 1m.ipynb`: Simulates trading over 1-minute intervals.
  - `simulation 4h.ipynb`: Simulates trading over 4-hour intervals.

- **Libraries**:
  - `TA_Lib-0.4.29-cp311-cp311-win_amd64.whl`: A library for technical analysis.

## Getting Started

### Prerequisites

- Python 3.11
- Required libraries:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `TA-Lib` (Install using the provided `.whl` file)

### Installation

1. **Install the necessary libraries**:
   ```bash
   pip install pandas numpy matplotlib seaborn
   pip install TA_Lib-0.4.29-cp311-cp311-win_amd64.whl
   ```

2. **Clone this repository**:
   ```bash
   git clone https://github.com/pawatpai/Algorithmic-Trading-on-BTCUSDT
   ```

3. **Run the Jupyter notebooks**:
   - Use `Backtesting.ipynb` for backtesting strategies.
   - Use the appropriate simulation notebook (`simulation 1d.ipynb`, `simulation 1h.ipynb`, etc.) to simulate trading over different time intervals.

## Usage

- **Backtesting**:
  - Open `Backtesting.ipynb` in Jupyter Notebook.
  - Load your historical data and run the cells to backtest the different strategies.

- **Simulation**:
  - Choose the appropriate simulation notebook based on the time interval.
  - Run the notebook to simulate trading using the implemented agents.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request with your changes.

## Contact

For any questions or suggestions, please contact Pawat Jiangthiranan at pawatpai@gmail.com.
