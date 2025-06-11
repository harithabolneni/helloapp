import yfinance as yf
import sys
import json # For pretty printing the .info dict in case of errors

def fetch_stock_data(ticker_symbol):
    """
    Fetches and displays stock data for a given ticker symbol.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.info

        # Check if data is empty or symbol is missing, indicating a potential bad ticker
        if not data or not data.get('symbol'):
            print(f"Could not retrieve valid data for {ticker_symbol}. It might be an invalid ticker or delisted.")
            # Optionally print what was received for debugging
            if data:
                print("\n--- Debug: Received Data ---")
                print(json.dumps(data, indent=4))
                print("-----------------------------")
            return

        # Common keys to display.
        symbol = data.get('symbol', 'N/A')
        print(f"Data for {symbol}:")

        current_price = data.get('currentPrice') or data.get('regularMarketPrice') or data.get('previousClose', 'N/A')
        print(f"  Current Price: {current_price}")

        day_low = data.get('dayLow', 'N/A')
        print(f"  Day's Low: {day_low}")

        day_high = data.get('dayHigh', 'N/A')
        print(f"  Day's High: {day_high}")

        volume = data.get('volume') or data.get('regularMarketVolume', 'N/A') # Added fallback
        print(f"  Volume: {volume}")

        market_open = data.get('regularMarketOpen', 'N/A')
        print(f"  Market Open: {market_open}")

        previous_close = data.get('previousClose', 'N/A')
        print(f"  Previous Close: {previous_close}")

        # Option to print all available data if needed for debugging
        # print("\nFull data dictionary:")
        # print(json.dumps(data, indent=4))

    except Exception as e:
        print(f"An unexpected error occurred while fetching data for {ticker_symbol}: {e}")
        # Attempt to print ticker.info if it exists, even on error, for debugging
        try:
            if 'ticker' in locals() and hasattr(ticker, 'info') and ticker.info:
                print("\n--- Debug: Full Ticker Info ---")
                print(json.dumps(ticker.info, indent=4))
                print("---------------------------------")
        except Exception as debug_e:
            print(f"(Could not print ticker.info for debugging: {debug_e})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stock_fetcher.py <TICKER_SYMBOL>")
        sys.exit(1)

    ticker_arg = sys.argv[1]
    fetch_stock_data(ticker_arg.upper())
