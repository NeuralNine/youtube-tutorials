from mcp.server.fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("yf", host='0.0.0.0', port=9999)


@mcp.tool()
def price(ticker: str) -> float:
    return yf.Ticker(ticker).fast_info["last_price"]


@mcp.tool()
def news(ticker: str) -> list[str]:
    return [x['content']['title'] for x in yf.Ticker(ticker).news[:5]]


mcp.run(transport='streamable-http')

