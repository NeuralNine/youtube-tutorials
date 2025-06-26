import tkinter as tk
from tkinter import messagebox

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CandlestickChart:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Candlestick Chart")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2b2b2b")
        
        plt.style.use('dark_background')
        
        control_frame = tk.Frame(self.root, bg="#2b2b2b")
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Stock Ticker:", font=("Arial", 12), bg="#2b2b2b", fg="white").grid(row=0, column=0, padx=5)
        self.ticker_var = tk.StringVar(value="AAPL")
        ticker_entry = tk.Entry(control_frame, textvariable=self.ticker_var, width=10, font=("Arial", 12), bg="#404040", fg="white", insertbackground="white")
        ticker_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(control_frame, text="Start Date:", font=("Arial", 12), bg="#2b2b2b", fg="white").grid(row=0, column=2, padx=5)
        self.start_var = tk.StringVar(value="2023-01-01")
        start_entry = tk.Entry(control_frame, textvariable=self.start_var, width=12, font=("Arial", 12), bg="#404040", fg="white", insertbackground="white")
        start_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(control_frame, text="End Date:", font=("Arial", 12), bg="#2b2b2b", fg="white").grid(row=0, column=4, padx=5)
        self.end_var = tk.StringVar(value="2024-01-01")
        end_entry = tk.Entry(control_frame, textvariable=self.end_var, width=12, font=("Arial", 12), bg="#404040", fg="white", insertbackground="white")
        end_entry.grid(row=0, column=5, padx=5)
        
        load_btn = tk.Button(control_frame, text="Load Chart", command=self.load_chart,
                            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20)
        load_btn.grid(row=0, column=6, padx=10)
        
        chart_frame = tk.Frame(self.root, bg="#2b2b2b")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.load_chart()
    
    def load_chart(self):
        try:
            ticker = self.ticker_var.get().upper()
            start_date = self.start_var.get()
            end_date = self.end_var.get()
            
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            
            if data.empty:
                messagebox.showerror("Error", f"No data found for ticker {ticker}")
                return
            
            self.create_candlestick_chart(data, ticker)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def create_candlestick_chart(self, data, ticker):
        self.ax.clear()
        
        dates = data.index
        opens = data['Open']
        highs = data['High']
        lows = data['Low']
        closes = data['Close']
        
        up_days = closes >= opens
        down_days = closes < opens
        
        width = 0.6
        width2 = 0.05
        
        up_color = '#26a69a'
        down_color = '#ef5350'
        
        self.ax.bar(dates[up_days], closes[up_days] - opens[up_days], width,
                   bottom=opens[up_days], color=up_color, alpha=0.8)
        self.ax.bar(dates[up_days], highs[up_days] - closes[up_days], width2,
                   bottom=closes[up_days], color=up_color)
        self.ax.bar(dates[up_days], opens[up_days] - lows[up_days], width2,
                   bottom=lows[up_days], color=up_color)
        
        self.ax.bar(dates[down_days], opens[down_days] - closes[down_days], width,
                   bottom=closes[down_days], color=down_color, alpha=0.8)
        self.ax.bar(dates[down_days], highs[down_days] - opens[down_days], width2,
                   bottom=opens[down_days], color=down_color)
        self.ax.bar(dates[down_days], closes[down_days] - lows[down_days], width2,
                   bottom=lows[down_days], color=down_color)
        
        self.ax.set_title(f'{ticker} Stock Price', fontsize=16, fontweight='bold', pad=20)
        self.ax.set_ylabel('Price ($)', fontsize=12)
        self.ax.set_xlabel('Date', fontsize=12)
        
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.ax.xaxis.set_major_locator(mdates.MonthLocator())
        
        self.fig.autofmt_xdate()
        self.ax.grid(True, alpha=0.3)
        
        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = CandlestickChart(root)
    root.mainloop() 
