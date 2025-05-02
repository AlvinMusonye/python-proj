import tkinter as tk
from tkinter import ttk
import yfinance as yf
import pandas as pd


def fetch_recent_prices(symbols, period='5d', interval='1h'):
    stock_data = {}
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval=interval)
        stock_data[symbol] = data
    return stock_data


def show_prices():
    stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
    recent_prices = fetch_recent_prices(stock_symbols)

    for symbol, data in recent_prices.items():
        output_text.insert(tk.END, f"\nRecent prices for {symbol}:\n")
        output_text.insert(tk.END, data[['Close']].to_string())
        output_text.insert(tk.END, "\n\n") 

root = tk.Tk()
root.title("Stock Prices Viewer ")
root.geometry("800x600")


fetch_button = tk.Button(root, text="Fetch Stock Prices", command=show_prices, font=("Arial", 14))
fetch_button.pack(pady=10)


output_text = tk.Text(root, wrap=tk.WORD, font=("Courier", 10))
output_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

root.mainloop()
