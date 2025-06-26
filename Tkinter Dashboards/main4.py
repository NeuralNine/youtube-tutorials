import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import threading

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec


class AdvancedStockAnalyzer:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Stock Analyzer Pro")
        self.root.geometry("1800x1000")
        self.root.configure(bg="#1a1a1a")
        
        plt.style.use('dark_background')
        
        self.colors = {
            'bg': '#1a1a1a',
            'frame': '#2d2d2d',
            'entry': '#404040',
            'text': '#ffffff',
            'accent': '#00d4aa',
            'danger': '#ff6b6b',
            'warning': '#ffd93d',
            'success': '#6bcf7f',
            'button': '#3f51b5'
        }
        
        self.current_data = None
        self.indicators = {}
        
        self._create_interface()
        self._setup_default_data()
    
    def _create_interface(self):
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._create_control_panel(main_container)
        self._create_notebook(main_container)
        self._create_status_bar()
    
    def _create_control_panel(self, parent):
        control_frame = tk.Frame(parent, bg=self.colors['frame'], relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        top_row = tk.Frame(control_frame, bg=self.colors['frame'])
        top_row.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(top_row, text="Stock Ticker:", font=("Arial", 12, "bold"), 
                bg=self.colors['frame'], fg=self.colors['text']).grid(row=0, column=0, padx=5, sticky="w")
        
        self.ticker_var = tk.StringVar(value="AAPL")
        ticker_entry = tk.Entry(top_row, textvariable=self.ticker_var, width=10, font=("Arial", 12),
                               bg=self.colors['entry'], fg=self.colors['text'], insertbackground=self.colors['text'])
        ticker_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(top_row, text="Period:", font=("Arial", 12, "bold"),
                bg=self.colors['frame'], fg=self.colors['text']).grid(row=0, column=2, padx=(20, 5), sticky="w")
        
        self.period_var = tk.StringVar(value="1y")
        period_combo = ttk.Combobox(top_row, textvariable=self.period_var, width=8,
                                   values=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])
        period_combo.grid(row=0, column=3, padx=5)
        
        tk.Label(top_row, text="Interval:", font=("Arial", 12, "bold"),
                bg=self.colors['frame'], fg=self.colors['text']).grid(row=0, column=4, padx=(20, 5), sticky="w")
        
        self.interval_var = tk.StringVar(value="1d")
        interval_combo = ttk.Combobox(top_row, textvariable=self.interval_var, width=8,
                                     values=["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"])
        interval_combo.grid(row=0, column=5, padx=5)
        
        load_btn = tk.Button(top_row, text="Load Data", command=self._load_data_threaded,
                            bg=self.colors['success'], fg=self.colors['text'], font=("Arial", 12, "bold"),
                            relief=tk.FLAT, padx=20, pady=5)
        load_btn.grid(row=0, column=6, padx=20)
        
        bottom_row = tk.Frame(control_frame, bg=self.colors['frame'])
        bottom_row.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(bottom_row, text="Technical Indicators:", font=("Arial", 12, "bold"),
                bg=self.colors['frame'], fg=self.colors['text']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.sma_var = tk.BooleanVar(value=True)
        sma_check = tk.Checkbutton(bottom_row, text="SMA (20,50)", variable=self.sma_var,
                                  bg=self.colors['frame'], fg=self.colors['text'], selectcolor=self.colors['entry'],
                                  font=("Arial", 10), command=self._update_indicators)
        sma_check.pack(side=tk.LEFT, padx=5)
        
        self.ema_var = tk.BooleanVar()
        ema_check = tk.Checkbutton(bottom_row, text="EMA (12,26)", variable=self.ema_var,
                                  bg=self.colors['frame'], fg=self.colors['text'], selectcolor=self.colors['entry'],
                                  font=("Arial", 10), command=self._update_indicators)
        ema_check.pack(side=tk.LEFT, padx=5)
        
        self.bb_var = tk.BooleanVar()
        bb_check = tk.Checkbutton(bottom_row, text="Bollinger Bands", variable=self.bb_var,
                                 bg=self.colors['frame'], fg=self.colors['text'], selectcolor=self.colors['entry'],
                                 font=("Arial", 10), command=self._update_indicators)
        bb_check.pack(side=tk.LEFT, padx=5)
        
        self.volume_var = tk.BooleanVar(value=True)
        volume_check = tk.Checkbutton(bottom_row, text="Volume", variable=self.volume_var,
                                     bg=self.colors['frame'], fg=self.colors['text'], selectcolor=self.colors['entry'],
                                     font=("Arial", 10), command=self._update_indicators)
        volume_check.pack(side=tk.LEFT, padx=5)
        
        export_btn = tk.Button(bottom_row, text="Export Data", command=self._export_data,
                              bg=self.colors['warning'], fg=self.colors['text'], font=("Arial", 10, "bold"),
                              relief=tk.FLAT, padx=15)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        compare_btn = tk.Button(bottom_row, text="Compare Stocks", command=self._compare_stocks,
                               bg=self.colors['button'], fg=self.colors['text'], font=("Arial", 10, "bold"),
                               relief=tk.FLAT, padx=15)
        compare_btn.pack(side=tk.RIGHT, padx=5)
    
    def _create_notebook(self, parent):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['frame'], borderwidth=0)
        style.configure('TNotebook.Tab', background=self.colors['entry'], foreground=self.colors['text'],
                       padding=[20, 10], borderwidth=1)
        style.map('TNotebook.Tab', background=[('selected', self.colors['accent'])])
        
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self._create_candlestick_tab()
        self._create_analysis_tab()
        self._create_fundamentals_tab()
        self._create_portfolio_tab()
    
    def _create_candlestick_tab(self):
        candlestick_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(candlestick_frame, text="📈 Price Chart")
        
        chart_container = tk.Frame(candlestick_frame, bg=self.colors['bg'])
        chart_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.main_fig = plt.Figure(figsize=(16, 10), facecolor='#1a1a1a')
        self.main_canvas = FigureCanvasTkAgg(self.main_fig, chart_container)
        self.main_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        toolbar_frame = tk.Frame(chart_container, bg=self.colors['bg'])
        toolbar_frame.pack(fill=tk.X)
        self.toolbar = NavigationToolbar2Tk(self.main_canvas, toolbar_frame)
        self.toolbar.config(bg=self.colors['frame'])
    
    def _create_analysis_tab(self):
        analysis_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(analysis_frame, text="📊 Technical Analysis")
        
        self.analysis_fig = plt.Figure(figsize=(16, 10), facecolor='#1a1a1a')
        self.analysis_canvas = FigureCanvasTkAgg(self.analysis_fig, analysis_frame)
        self.analysis_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _create_fundamentals_tab(self):
        fundamentals_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(fundamentals_frame, text="📋 Fundamentals")
        
        left_panel = tk.Frame(fundamentals_frame, bg=self.colors['frame'], width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="Key Metrics", font=("Arial", 16, "bold"),
                bg=self.colors['frame'], fg=self.colors['accent']).pack(pady=10)
        
        self.metrics_frame = tk.Frame(left_panel, bg=self.colors['frame'])
        self.metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        right_panel = tk.Frame(fundamentals_frame, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.fundamentals_fig = plt.Figure(figsize=(12, 8), facecolor='#1a1a1a')
        self.fundamentals_canvas = FigureCanvasTkAgg(self.fundamentals_fig, right_panel)
        self.fundamentals_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _create_portfolio_tab(self):
        portfolio_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(portfolio_frame, text="💼 Portfolio")
        
        controls = tk.Frame(portfolio_frame, bg=self.colors['frame'])
        controls.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(controls, text="Add to Portfolio:", font=("Arial", 12, "bold"),
                bg=self.colors['frame'], fg=self.colors['text']).pack(side=tk.LEFT, padx=10)
        
        self.shares_var = tk.StringVar(value="100")
        tk.Entry(controls, textvariable=self.shares_var, width=8, bg=self.colors['entry'],
                fg=self.colors['text'], insertbackground=self.colors['text']).pack(side=tk.LEFT, padx=5)
        
        tk.Label(controls, text="shares", bg=self.colors['frame'], fg=self.colors['text']).pack(side=tk.LEFT, padx=5)
        
        add_btn = tk.Button(controls, text="Add Position", command=self._add_to_portfolio,
                           bg=self.colors['success'], fg=self.colors['text'], relief=tk.FLAT)
        add_btn.pack(side=tk.LEFT, padx=10)
        
        self.portfolio_fig = plt.Figure(figsize=(16, 8), facecolor='#1a1a1a')
        self.portfolio_canvas = FigureCanvasTkAgg(self.portfolio_fig, portfolio_frame)
        self.portfolio_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.portfolio = {}
    
    def _create_status_bar(self):
        self.status_bar = tk.Frame(self.root, bg=self.colors['frame'], relief=tk.SUNKEN, bd=1)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(self.status_bar, text="Ready", bg=self.colors['frame'],
                                    fg=self.colors['text'], font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT, padx=10, pady=2)
        
        self.progress = ttk.Progressbar(self.status_bar, mode='indeterminate', length=200)
        self.progress.pack(side=tk.RIGHT, padx=10, pady=2)
    
    def _setup_default_data(self):
        self._load_data_threaded()
    
    def _load_data_threaded(self):
        threading.Thread(target=self._load_data, daemon=True).start()
    
    def _load_data(self):
        try:
            self.status_label.config(text="Loading data...")
            self.progress.start()
            
            ticker = self.ticker_var.get().upper()
            period = self.period_var.get()
            interval = self.interval_var.get()
            
            stock = yf.Ticker(ticker)
            self.current_data = stock.history(period=period, interval=interval)
            self.stock_info = stock.info
            
            if self.current_data.empty:
                self.root.after(0, lambda: messagebox.showerror("Error", f"No data found for {ticker}"))
                return
            
            self._calculate_technical_indicators()
            
            self.root.after(0, self._update_all_charts)
            self.root.after(0, lambda: self.status_label.config(text=f"Loaded {ticker} - {len(self.current_data)} records"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load data: {str(e)}"))
            self.root.after(0, lambda: self.status_label.config(text="Error loading data"))
        finally:
            self.root.after(0, self.progress.stop)
    
    def _calculate_technical_indicators(self):
        if self.current_data is None:
            return
        
        df = self.current_data.copy()
        
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['EMA_26'] = df['Close'].ewm(span=26).mean()
        
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        self.indicators = df
    
    def _update_indicators(self):
        if self.current_data is not None:
            self._update_main_chart()
    
    def _update_all_charts(self):
        self._update_main_chart()
        self._update_analysis_chart()
        self._update_fundamentals()
    
    def _update_main_chart(self):
        if self.current_data is None:
            return
        
        self.main_fig.clear()
        
        if self.volume_var.get():
            gs = GridSpec(3, 1, height_ratios=[3, 1, 0.1], hspace=0.1)
            ax_price = self.main_fig.add_subplot(gs[0])
            ax_volume = self.main_fig.add_subplot(gs[1], sharex=ax_price)
        else:
            ax_price = self.main_fig.add_subplot(111)
        
        data = self.indicators
        dates = data.index
        
        up_days = data['Close'] >= data['Open']
        down_days = data['Close'] < data['Open']
        
        width = 0.6
        width2 = 0.05
        
        up_color = self.colors['success']
        down_color = self.colors['danger']
        
        ax_price.bar(dates[up_days], data['Close'][up_days] - data['Open'][up_days], width,
                    bottom=data['Open'][up_days], color=up_color, alpha=0.8)
        ax_price.bar(dates[up_days], data['High'][up_days] - data['Close'][up_days], width2,
                    bottom=data['Close'][up_days], color=up_color)
        ax_price.bar(dates[up_days], data['Open'][up_days] - data['Low'][up_days], width2,
                    bottom=data['Low'][up_days], color=up_color)
        
        ax_price.bar(dates[down_days], data['Open'][down_days] - data['Close'][down_days], width,
                    bottom=data['Close'][down_days], color=down_color, alpha=0.8)
        ax_price.bar(dates[down_days], data['High'][down_days] - data['Open'][down_days], width2,
                    bottom=data['Open'][down_days], color=down_color)
        ax_price.bar(dates[down_days], data['Close'][down_days] - data['Low'][down_days], width2,
                    bottom=data['Low'][down_days], color=down_color)
        
        if self.sma_var.get():
            ax_price.plot(dates, data['SMA_20'], color=self.colors['accent'], linewidth=2, label='SMA 20', alpha=0.8)
            ax_price.plot(dates, data['SMA_50'], color=self.colors['warning'], linewidth=2, label='SMA 50', alpha=0.8)
        
        if self.ema_var.get():
            ax_price.plot(dates, data['EMA_12'], color='#ff9800', linewidth=2, label='EMA 12', alpha=0.8)
            ax_price.plot(dates, data['EMA_26'], color='#e91e63', linewidth=2, label='EMA 26', alpha=0.8)
        
        if self.bb_var.get():
            ax_price.plot(dates, data['BB_Upper'], color='#9c27b0', linewidth=1, alpha=0.6)
            ax_price.plot(dates, data['BB_Lower'], color='#9c27b0', linewidth=1, alpha=0.6)
            ax_price.fill_between(dates, data['BB_Upper'], data['BB_Lower'], 
                                 color='#9c27b0', alpha=0.1, label='Bollinger Bands')
        
        ticker = self.ticker_var.get().upper()
        ax_price.set_title(f'{ticker} Stock Price', fontsize=16, fontweight='bold', color=self.colors['text'], pad=20)
        ax_price.set_ylabel('Price ($)', fontsize=12, color=self.colors['text'])
        ax_price.grid(True, alpha=0.3)
        ax_price.legend(loc='upper left')
        
        if self.volume_var.get():
            volume_colors = [up_color if close >= open_price else down_color 
                           for close, open_price in zip(data['Close'], data['Open'])]
            ax_volume.bar(dates, data['Volume'], color=volume_colors, alpha=0.6)
            ax_volume.set_ylabel('Volume', fontsize=12, color=self.colors['text'])
            ax_volume.grid(True, alpha=0.3)
        
        self.main_fig.autofmt_xdate()
        self.main_fig.tight_layout()
        self.main_canvas.draw()
    
    def _update_analysis_chart(self):
        if self.current_data is None:
            return
        
        self.analysis_fig.clear()
        
        gs = GridSpec(3, 2, hspace=0.3, wspace=0.3)
        
        data = self.indicators
        dates = data.index
        
        ax1 = self.analysis_fig.add_subplot(gs[0, 0])
        ax1.plot(dates, data['RSI'], color=self.colors['accent'], linewidth=2)
        ax1.axhline(y=70, color=self.colors['danger'], linestyle='--', alpha=0.7)
        ax1.axhline(y=30, color=self.colors['success'], linestyle='--', alpha=0.7)
        ax1.fill_between(dates, 70, 100, alpha=0.2, color=self.colors['danger'])
        ax1.fill_between(dates, 0, 30, alpha=0.2, color=self.colors['success'])
        ax1.set_title('RSI (14)', fontweight='bold', color=self.colors['text'])
        ax1.set_ylabel('RSI', color=self.colors['text'])
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 100)
        
        ax2 = self.analysis_fig.add_subplot(gs[0, 1])
        ax2.plot(dates, data['MACD'], color=self.colors['accent'], linewidth=2, label='MACD')
        ax2.plot(dates, data['MACD_Signal'], color=self.colors['warning'], linewidth=2, label='Signal')
        ax2.bar(dates, data['MACD_Histogram'], color=self.colors['text'], alpha=0.3, label='Histogram')
        ax2.set_title('MACD', fontweight='bold', color=self.colors['text'])
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        ax3 = self.analysis_fig.add_subplot(gs[1, 0])
        ax3.scatter(data['Volume'], data['Close'], alpha=0.6, color=self.colors['accent'], s=10)
        ax3.set_title('Price vs Volume', fontweight='bold', color=self.colors['text'])
        ax3.set_xlabel('Volume', color=self.colors['text'])
        ax3.set_ylabel('Price', color=self.colors['text'])
        ax3.grid(True, alpha=0.3)
        
        ax4 = self.analysis_fig.add_subplot(gs[1, 1])
        returns = data['Close'].pct_change().dropna()
        ax4.hist(returns, bins=50, alpha=0.7, color=self.colors['accent'], edgecolor='black')
        ax4.set_title('Daily Returns Distribution', fontweight='bold', color=self.colors['text'])
        ax4.set_xlabel('Returns', color=self.colors['text'])
        ax4.set_ylabel('Frequency', color=self.colors['text'])
        ax4.grid(True, alpha=0.3)
        
        ax5 = self.analysis_fig.add_subplot(gs[2, :])
        ax5.plot(dates, data['Close'], color=self.colors['text'], linewidth=1, alpha=0.7, label='Close')
        ax5.plot(dates, data['SMA_20'], color=self.colors['success'], linewidth=2, label='SMA 20')
        ax5.plot(dates, data['SMA_50'], color=self.colors['danger'], linewidth=2, label='SMA 50')
        
        crossover_up = (data['SMA_20'] > data['SMA_50']) & (data['SMA_20'].shift(1) <= data['SMA_50'].shift(1))
        crossover_down = (data['SMA_20'] < data['SMA_50']) & (data['SMA_20'].shift(1) >= data['SMA_50'].shift(1))
        
        ax5.scatter(dates[crossover_up], data['Close'][crossover_up], color=self.colors['success'], 
                   s=100, marker='^', label='Golden Cross', zorder=5)
        ax5.scatter(dates[crossover_down], data['Close'][crossover_down], color=self.colors['danger'], 
                   s=100, marker='v', label='Death Cross', zorder=5)
        
        ax5.set_title('Moving Average Crossovers', fontweight='bold', color=self.colors['text'])
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        self.analysis_fig.autofmt_xdate()
        self.analysis_canvas.draw()
    
    def _update_fundamentals(self):
        if not hasattr(self, 'stock_info') or not self.stock_info:
            return
        
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()
        
        metrics = [
            ("Market Cap", self.stock_info.get('marketCap', 'N/A')),
            ("P/E Ratio", self.stock_info.get('trailingPE', 'N/A')),
            ("EPS", self.stock_info.get('trailingEps', 'N/A')),
            ("Dividend Yield", self.stock_info.get('dividendYield', 'N/A')),
            ("52W High", self.stock_info.get('fiftyTwoWeekHigh', 'N/A')),
            ("52W Low", self.stock_info.get('fiftyTwoWeekLow', 'N/A')),
            ("Beta", self.stock_info.get('beta', 'N/A')),
            ("Volume", self.stock_info.get('volume', 'N/A'))
        ]
        
        for i, (label, value) in enumerate(metrics):
            if isinstance(value, (int, float)) and value != 'N/A':
                if label == "Market Cap" and value > 1e9:
                    value = f"${value/1e9:.2f}B"
                elif label == "Dividend Yield" and value < 1:
                    value = f"{value*100:.2f}%"
                elif isinstance(value, float):
                    value = f"{value:.2f}"
                elif isinstance(value, int) and value > 1000000:
                    value = f"{value:,}"
            
            row = tk.Frame(self.metrics_frame, bg=self.colors['frame'])
            row.pack(fill=tk.X, pady=2)
            
            tk.Label(row, text=label + ":", font=("Arial", 11, "bold"),
                    bg=self.colors['frame'], fg=self.colors['text']).pack(side=tk.LEFT)
            tk.Label(row, text=str(value), font=("Arial", 11),
                    bg=self.colors['frame'], fg=self.colors['accent']).pack(side=tk.RIGHT)
        
        self.fundamentals_fig.clear()
        
        if self.current_data is not None:
            ax = self.fundamentals_fig.add_subplot(111)
            
            data = self.current_data
            monthly_data = data.resample('M').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            })
            
            ax.plot(monthly_data.index, monthly_data['Close'], marker='o', linewidth=3, 
                   markersize=8, color=self.colors['accent'])
            ax.set_title('Monthly Price Trend', fontsize=14, fontweight='bold', color=self.colors['text'])
            ax.set_ylabel('Price ($)', color=self.colors['text'])
            ax.grid(True, alpha=0.3)
            
            self.fundamentals_fig.autofmt_xdate()
            self.fundamentals_fig.tight_layout()
        
        self.fundamentals_canvas.draw()
    
    def _add_to_portfolio(self):
        if self.current_data is None:
            messagebox.showwarning("Warning", "Please load stock data first")
            return
        
        ticker = self.ticker_var.get().upper()
        try:
            shares = int(self.shares_var.get())
            current_price = self.current_data['Close'].iloc[-1]
            
            if ticker in self.portfolio:
                self.portfolio[ticker]['shares'] += shares
            else:
                self.portfolio[ticker] = {
                    'shares': shares,
                    'price': current_price,
                    'data': self.current_data.copy()
                }
            
            self._update_portfolio_chart()
            messagebox.showinfo("Success", f"Added {shares} shares of {ticker} to portfolio")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of shares")
    
    def _update_portfolio_chart(self):
        if not self.portfolio:
            return
        
        self.portfolio_fig.clear()
        
        ax1 = self.portfolio_fig.add_subplot(221)
        
        tickers = list(self.portfolio.keys())
        values = [self.portfolio[ticker]['shares'] * self.portfolio[ticker]['price'] for ticker in tickers]
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(tickers)))
        wedges, texts, autotexts = ax1.pie(values, labels=tickers, autopct='%1.1f%%', colors=colors)
        ax1.set_title('Portfolio Allocation', fontweight='bold', color=self.colors['text'])
        
        ax2 = self.portfolio_fig.add_subplot(222)
        
        total_value = sum(values)
        ax2.bar(tickers, values, color=colors)
        ax2.set_title(f'Holdings Value (Total: ${total_value:,.2f})', fontweight='bold', color=self.colors['text'])
        ax2.set_ylabel('Value ($)', color=self.colors['text'])
        plt.setp(ax2.get_xticklabels(), rotation=45)
        
        ax3 = self.portfolio_fig.add_subplot(212)
        
        for i, ticker in enumerate(tickers):
            data = self.portfolio[ticker]['data']['Close']
            normalized = (data / data.iloc[0]) * 100
            ax3.plot(data.index, normalized, label=ticker, linewidth=2, color=colors[i])
        
        ax3.set_title('Normalized Performance (Base 100)', fontweight='bold', color=self.colors['text'])
        ax3.set_ylabel('Normalized Price', color=self.colors['text'])
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        self.portfolio_fig.autofmt_xdate()
        self.portfolio_fig.tight_layout()
        self.portfolio_canvas.draw()
    
    def _compare_stocks(self):
        compare_window = tk.Toplevel(self.root)
        compare_window.title("Compare Stocks")
        compare_window.geometry("600x400")
        compare_window.configure(bg=self.colors['bg'])
        
        tk.Label(compare_window, text="Enter tickers separated by commas:", 
                font=("Arial", 12, "bold"), bg=self.colors['bg'], fg=self.colors['text']).pack(pady=10)
        
        tickers_var = tk.StringVar(value="AAPL,GOOGL,MSFT,TSLA")
        entry = tk.Entry(compare_window, textvariable=tickers_var, width=50, font=("Arial", 12),
                        bg=self.colors['entry'], fg=self.colors['text'], insertbackground=self.colors['text'])
        entry.pack(pady=10)
        
        def perform_comparison():
            tickers = [t.strip().upper() for t in tickers_var.get().split(',')]
            self._show_comparison_chart(tickers)
            compare_window.destroy()
        
        tk.Button(compare_window, text="Compare", command=perform_comparison,
                 bg=self.colors['success'], fg=self.colors['text'], font=("Arial", 12, "bold"),
                 relief=tk.FLAT, padx=20, pady=5).pack(pady=20)
    
    def _show_comparison_chart(self, tickers):
        comparison_window = tk.Toplevel(self.root)
        comparison_window.title("Stock Comparison")
        comparison_window.geometry("1200x800")
        comparison_window.configure(bg=self.colors['bg'])
        
        fig = plt.Figure(figsize=(12, 8), facecolor='#1a1a1a')
        canvas = FigureCanvasTkAgg(fig, comparison_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ax = fig.add_subplot(111)
        
        colors = plt.cm.Set1(np.linspace(0, 1, len(tickers)))
        
        for i, ticker in enumerate(tickers):
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(period=self.period_var.get())
                if not data.empty:
                    normalized = (data['Close'] / data['Close'].iloc[0]) * 100
                    ax.plot(data.index, normalized, label=ticker, linewidth=3, color=colors[i])
            except Exception as e:
                print(f"Error loading {ticker}: {e}")
        
        ax.set_title('Stock Comparison (Normalized)', fontsize=16, fontweight='bold', color=self.colors['text'])
        ax.set_ylabel('Normalized Price (Base 100)', color=self.colors['text'])
        ax.set_xlabel('Date', color=self.colors['text'])
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        fig.autofmt_xdate()
        fig.tight_layout()
        canvas.draw()
    
    def _export_data(self):
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")],
            title="Save stock data"
        )
        
        if filename:
            try:
                if filename.endswith('.xlsx'):
                    self.indicators.to_excel(filename)
                else:
                    self.indicators.to_csv(filename)
                messagebox.showinfo("Success", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedStockAnalyzer(root)
    root.mainloop() 
