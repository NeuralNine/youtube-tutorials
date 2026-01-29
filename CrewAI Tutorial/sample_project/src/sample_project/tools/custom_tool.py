import yfinance as yf
from crewai.tools import tool


@tool('Get Stock Data')
def get_stock_data(ticker: str) -> str:
    """Get current price and recent news for a stock ticker."""
    stock = yf.Ticker(ticker)

    info = stock.info

    current_price = info.get('currentPrice', 'N/A')
    previous_close = info.get('previousClose', 'N/A')

    if current_price != 'N/A' and previous_close != 'N/A':
        change_pct = ((current_price - previous_close) / previous_close) * 100
        price_info = f'Price: ${current_price:.2f} ({change_pct:+.2f}%)'
    else:
        price_info = 'Price data unavailable'

    news = stock.news

    headlines = []

    for item in news[:8]:
        title = item['content'].get('title', '').strip()

        if title:
            headlines.append(f'- {title}')

    if not headlines:
        headlines = ['- No recent news headlines available']

    news_text = '\n'.join(headlines)

    return f'{price_info}\n\nRecent Headlines:\n{news_text}'
