# option_trading_app.py

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from datetime import datetime



# Configure the page
st.set_page_config(page_title="Option Trading App", layout="wide")

# Title
st.title("📈 Option Trading App")

# Sidebar for user inputs
st.sidebar.header("User Input Parameters")

def user_input_ticker():
    ticker = st.sidebar.text_input("Stock Ticker", "AAPL")
    return ticker.upper()

def get_option_expirations(ticker):
    stock = yf.Ticker(ticker)
    return stock.options

def get_option_chain(ticker, expiration):
    stock = yf.Ticker(ticker)
    try:
        opt = stock.option_chain(expiration)
        calls = opt.calls
        puts = opt.puts
        return calls, puts
    except Exception as e:
        st.error(f"Error fetching option chain: {e}")
        return pd.DataFrame(), pd.DataFrame()

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calculate Black-Scholes option price
    S: Current stock price
    K: Strike price
    T: Time to expiration in years
    r: Risk-free interest rate
    sigma: Volatility of the underlying stock
    option_type: 'call' or 'put'
    """
    try:
        d1 = (np.log(S / K) + (r + 0.5 * sigma **2 ) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return price
    except Exception as e:
        st.error(f"Error in Black-Scholes calculation: {e}")
        return np.nan

# Main content
ticker = user_input_ticker()

if ticker:
    stock = yf.Ticker(ticker)
    try:
        # Get current stock price
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        st.subheader(f"📊 Current Price of {ticker}: ${current_price:.2f}")
    except Exception as e:
        st.error(f"Error fetching stock price: {e}")
        current_price = None

    # Get option expirations
    expirations = get_option_expirations(ticker)
    if not expirations:
        st.warning("No option expirations available.")
    else:
        # Select expiration date
        expiration = st.sidebar.selectbox("Expiration Date", expirations)
        
        # Get option chains
        calls, puts = get_option_chain(ticker, expiration)
        
        if not calls.empty and not puts.empty:
            st.subheader(f"🔍 Options Chain for {ticker} - {expiration}")
            
            # Display calls and puts
            tab1, tab2 = st.tabs(["Calls", "Puts"])
            
            with tab1:
                st.dataframe(calls)
            with tab2:
                st.dataframe(puts)
            
            # Option selection
            st.sidebar.subheader("Select Option Parameters")
            option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
            if option_type == "call":
                options = calls
            else:
                options = puts
            
            strike = st.sidebar.selectbox("Strike Price", options['strike'].unique())
            
            # Get option details
            option = options[options['strike'] == strike].iloc[0]
            bid = option['bid']
            ask = option['ask']
            last_price = option['lastPrice']
            volume = option['volume']
            open_interest = option['openInterest']
            
            st.write(f"### Selected Option: {option_type.capitalize()} {strike}")
            st.write(f"**Bid:** ${bid} | **Ask:** ${ask} | **Last Price:** ${last_price}")
            st.write(f"**Volume:** {volume} | **Open Interest:** {open_interest}")
            
            # Black-Scholes Parameters
            st.sidebar.subheader("Black-Scholes Parameters")
            risk_free_rate = st.sidebar.number_input("Risk-Free Rate (%)", value=1.5) / 100
            volatility = st.sidebar.number_input("Volatility (%)", value=20.0) / 100
            today = datetime.today()
            expiration_date = datetime.strptime(expiration, "%Y-%m-%d")
            T = (expiration_date - today).days / 365
            if T <= 0:
                st.error("Expiration date must be in the future.")
                T = 0.01  # Prevent division by zero
            
            # Calculate Black-Scholes price
            bs_price = black_scholes(S=current_price, K=strike, T=T, r=risk_free_rate, sigma=volatility, option_type=option_type)
            st.write(f"**Black-Scholes {option_type.capitalize()} Price:** ${bs_price:.2f}")
            
            # Plot Payoff
            st.subheader("Option Payoff Diagram")
            # Define range for underlying price
            S = np.linspace(current_price * 0.5, current_price * 1.5, 100)
            if option_type == 'call':
                payoff = np.maximum(S - strike, 0) - bs_price
            else:
                payoff = np.maximum(strike - S, 0) - bs_price
            
            fig, ax = plt.subplots()
            ax.plot(S, payoff, label='Payoff')
            ax.axhline(0, color='black', lw=0.5)
            ax.axvline(current_price, color='red', linestyle='--', label='Current Price')
            ax.set_xlabel('Stock Price at Expiration ($)')
            ax.set_ylabel('Profit / Loss ($)')
            ax.set_title(f'{option_type.capitalize()} Option Payoff')
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("No option data available for the selected expiration date.")
else:
    st.info("Please enter a valid stock ticker symbol.")

# Footer
st.markdown("---")
st.markdown("Developed by [Your Name](https://www.example.com)")
