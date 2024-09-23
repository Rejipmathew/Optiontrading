# 📈 Option Trading App

A Streamlit application for option trading analysis. This app allows users to:

1. **Input a Stock Ticker**: Enter a stock symbol to fetch its current price and available option contracts.
2. **Select Option Parameters**: Choose expiration dates, option types (Call or Put), and strike prices.
3. **View Options Chain**: Display the fetched options chain in a table format.
4. **Calculate Option Price**: Use the Black-Scholes model to compute theoretical option prices.
5. **Visualize Payoff**: Plot the payoff diagram for the selected option strategy.

## Features

- **Real-Time Data**: Fetches real-time stock and option data using the `yfinance` library.
- **User-Friendly Interface**: Interactive widgets for easy selection of options parameters.
- **Visualization**: Graphical representation of option payoff using `matplotlib`.
- **Error Handling**: Graceful handling of invalid inputs or data fetching issues.

## Prerequisites

Ensure you have Python installed (preferably Python 3.7 or higher).

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/option-trading-app.git
   cd option-trading-app
