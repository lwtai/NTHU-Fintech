# Cryptocurrency Grid Trading Bot

## Project Overview
This project implements a grid trading strategy for the BTC/USDT trading pair using API from [Crypto Arsenal](https://docs.crypto-arsenal.io/), they also provide detail [documentation](https://docs.crypto-arsenal.io/docs/developer/get-started/python/hello-world) about how to use it.

The strategy was developed as part of the "Financial Technology Innovation and Application" course at National Tsing Hua University. This implementation achieved notable success in two course competitions:
- 1st Place in the Mid-term Strategy Competition
- 3rd Place in the Final Strategy Competition

## Development Environment
- Platform: Crypto Arsenal
- Exchange: Binance Futures
- Trading Period: March 2023
- Strategy: Grid Trading

## Grid Trading Strategy
Grid trading is a systematic trading strategy that creates a network of orders at incrementally increasing and decreasing prices. The core concept is to:
- Buy when price falls below a grid line
- Sell when price rises above a grid line
- Profit from market volatility within a sideways trend

### Key Components & Parameters
#### 1. Trading Range
- Upper Bound (ceiling): Defines the maximum price for grid placement
- Lower Bound (floor): Sets the minimum price for grid placement
- *These boundaries should be set based on market analysis and expected trading range*

#### 2. Grid Configuration
- Grid Size: The price interval between each grid line
  - Smaller intervals: More frequent trades, higher potential profit in volatile markets
  - Larger intervals: Fewer trades, better for stable markets with clear trends
- Number of Grids: Determined by the range and grid size
  - More grids: Higher potential profit but requires more capital
  - Fewer grids: Lower capital requirement but might miss opportunities
