# Live Stock Data Fetcher

This script fetches and displays near real-time stock data from Yahoo Finance using the `yfinance` library.

## Features

*   Fetches key stock information (current price, day's high/low, volume, open, previous close).
*   Accepts a stock ticker symbol as a command-line argument.
*   Basic error handling for invalid tickers or network issues.

## Setup

### 1. Create a Virtual Environment (Recommended)

It's recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

*   On Windows:
    ```bash
    .\venv\Scripts\activate
    ```
*   On macOS and Linux:
    ```bash
    source venv/bin/activate
    ```

### 2. Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line, providing a stock ticker symbol as an argument. The ticker symbol will be converted to uppercase by the script.

```bash
python stock_fetcher.py <TICKER_SYMBOL>
```

### Examples:

*   Fetch data for Apple Inc. (AAPL):
    ```bash
    python stock_fetcher.py AAPL
    ```

*   Fetch data for Microsoft Corp. (MSFT):
    ```bash
    python stock_fetcher.py msft
    ```

*   Fetch data for SPDR S&P 500 ETF Trust (SPY):
    ```bash
    python stock_fetcher.py SPY
    ```

*   Fetch data for Bitcoin USD (BTC-USD):
    ```bash
    python stock_fetcher.py BTC-USD
    ```

## Output Example (for AAPL)

```
Data for AAPL:
  Current Price: 170.34
  Day's Low: 168.49
  Day's High: 171.27
  Volume: 52048292
  Market Open: 169.58
  Previous Close: 169.3
```
*(Note: Output values are illustrative and will vary based on current market data.)*

## Disclaimer

This script uses the `yfinance` library, which accesses data from Yahoo Finance. Data accuracy and availability depend on Yahoo Finance. Remember that financial data provided by Yahoo Finance can be delayed and is intended for personal, informational purposes only. Refer to Yahoo!'s terms of service for more details.
