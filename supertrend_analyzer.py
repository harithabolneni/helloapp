import yfinance as yf
import pandas as pd
import pandas_ta as ta # Attempt to import pandas_ta
import matplotlib.pyplot as plt
import argparse

def analyze_stock_supertrend(ticker_symbol="MSFT", period="1y", atr_length=10, st_multiplier=3.0, interval="daily"):
    """
    Fetches historical stock data, calculates the Supertrend indicator,
    and prints the head and tail of the DataFrame with the indicator.
    Can resample data to weekly interval.
    """
    try:
        print(f"Fetching historical data for {ticker_symbol} for period {period} (interval: {interval})...")
        ticker_data = yf.Ticker(ticker_symbol)
        df = ticker_data.history(period=period) # Daily data is fetched first

        if df.empty:
            print(f"No data found for {ticker_symbol} for the period {period}.")
            return

        print(f"Successfully fetched {len(df)} daily data points.")

        if interval == 'weekly':
            print(f"Resampling data to weekly interval...")
            # Ensure 'Volume' column exists for resampling; yfinance might use 'Volume' or 'volume'
            # Standardize to 'Volume' if 'volume' is present
            if 'volume' in df.columns and 'Volume' not in df.columns:
                df.rename(columns={'volume': 'Volume'}, inplace=True)

            # Check for Volume column for resampling
            # ATR calculation by pandas_ta typically uses High, Low, Close.
            # Volume is good practice for OHLCV resampling but might not be strictly needed for SuperTrend's ATR if pandas_ta's ATR does not use it.
            # If 'Volume' is missing, we proceed but print a warning.
            # Alternatively, one could create a dummy 'Volume' column: df['Volume'] = 0 if 'Volume' not in df.columns else None
            if 'Volume' not in df.columns:
                 print("Warning: 'Volume' column not found. Weekly resampling of volume will be skipped. ATR calculation might be okay if it only uses HLC.")
                 agg_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}
            else:
                 agg_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}

            df = df.resample('W').agg(agg_dict).dropna() # Drop weeks with no trading data

            if df.empty:
                print(f"No data left after resampling to weekly for {ticker_symbol} for the period {period}.")
                return
            print(f"Resampled to {len(df)} weekly data points.")

        # Ensure columns are in the correct case if necessary (usually yfinance is fine)
        # df.rename(columns={"High": "high", "Low": "low", "Close": "close"}, inplace=True) # Example if renaming needed

        print(f"Calculating ATR and Supertrend (length={atr_length}, multiplier={st_multiplier})...")

        # Calculate ATR using pandas_ta
        df.ta.atr(length=atr_length, append=True)

        # Calculate Supertrend using pandas_ta
        # This will add columns like: SUPERT_length_multiplier, SUPERTd_length_multiplier, SUPERTl_length_multiplier, SUPERTs_length_multiplier
        supertrend_data = df.ta.supertrend(length=atr_length, multiplier=st_multiplier, append=True)

        if supertrend_data is None or supertrend_data.empty:
            print("Could not calculate Supertrend. Ensure 'pandas_ta' is installed and data is valid.")
            print("DataFrame head:")
            print(df.head())
            return

        print("\nDataFrame with Supertrend indicator (head):")
        print(df.head())
        print("\nDataFrame with Supertrend indicator (tail):")
        print(df.tail())

        # Print column names to identify the exact Supertrend column names
        print("\nColumn names:")
        print(df.columns.tolist())

        # --- New logic for Trend Analysis ---
        st_direction_col = f'SUPERTd_{atr_length}_{st_multiplier}'
        # st_value_col = f'SUPERT_{atr_length}_{st_multiplier}' # Not directly used for flips, but good to have

        if st_direction_col not in df.columns:
            print(f"Error: Supertrend direction column '{st_direction_col}' not found.")
            return

        buy_flip_dates = []
        sell_flip_dates = []
        trend_segments = []

        current_trend_type = None
        current_trend_start_date = None

        # Ensure enough data points
        if len(df) < 2:
            print("Not enough data to identify trends.")
            return

        # Drop rows with NaN in st_direction_col before iteration, common at the beginning
        df_analysis = df.dropna(subset=[st_direction_col])

        if df_analysis.empty:
            print("Not enough non-NaN data in Supertrend direction column to identify trends.")
            return

        # Initialize first trend based on the first valid data point
        if df_analysis[st_direction_col].iloc[0] == 1:
            current_trend_type = 'bullish'
        elif df_analysis[st_direction_col].iloc[0] == -1:
            current_trend_type = 'bearish'
        current_trend_start_date = df_analysis.index[0]

        for i in range(1, len(df_analysis)):
            prev_direction = df_analysis[st_direction_col].iloc[i-1]
            curr_direction = df_analysis[st_direction_col].iloc[i]

            if curr_direction != prev_direction:
                # Trend flip occurred
                flip_date = df_analysis.index[i]
                if curr_direction == 1: # Flipped to Bullish (was -1 or NaN)
                    buy_flip_dates.append(flip_date)
                    if current_trend_type == 'bearish': # End previous bearish trend
                        trend_segments.append({'type': 'bearish', 'start': current_trend_start_date, 'end': df_analysis.index[i-1]})
                    current_trend_type = 'bullish'
                    current_trend_start_date = flip_date
                elif curr_direction == -1: # Flipped to Bearish (was 1 or NaN)
                    sell_flip_dates.append(flip_date)
                    if current_trend_type == 'bullish': # End previous bullish trend
                        trend_segments.append({'type': 'bullish', 'start': current_trend_start_date, 'end': df_analysis.index[i-1]})
                    current_trend_type = 'bearish'
                    current_trend_start_date = flip_date

        # Add the last ongoing trend segment
        if current_trend_type and current_trend_start_date:
            trend_segments.append({'type': current_trend_type, 'start': current_trend_start_date, 'end': df_analysis.index[-1]})

        print("\n--- Trend Analysis ---")
        print(f"Analysis for {ticker_symbol} (ATR: {atr_length}, Multiplier: {st_multiplier})")
        print("Buy Flip Dates:")
        for date in buy_flip_dates:
            print(f"  {date.strftime('%Y-%m-%d')}")

        print("\nSell Flip Dates:")
        for date in sell_flip_dates:
            print(f"  {date.strftime('%Y-%m-%d')}")

        print("\nTrend Segments:")
        for segment in trend_segments:
            print(f"  Type: {segment['type']}, Start: {segment['start'].strftime('%Y-%m-%d')}, End: {segment['end'].strftime('%Y-%m-%d')}")
        # --- End of New Trend Analysis Logic ---

        print("\nGenerating plot...")
        try:
            plt.figure(figsize=(14, 7))

            # Plotting Close Price
            plt.plot(df.index, df['Close'], label='Close Price', color='blue', alpha=0.7)

            # Plotting Supertrend Line
            st_col = f'SUPERT_{atr_length}_{st_multiplier}' # Dynamic name for the main Supertrend line
            if st_col in df.columns:
                plt.plot(df.index, df[st_col], label=f'Supertrend ({atr_length}, {st_multiplier})', color='orange', linestyle='--')
            else:
                print(f"Warning: Supertrend column {st_col} not found for plotting.")

            # Plotting Buy Signals
            # Ensure buy_flip_dates contains valid dates present in df.index
            valid_buy_flip_dates = [date for date in buy_flip_dates if date in df_analysis.index] # Use df_analysis for consistency
            if valid_buy_flip_dates:
                plt.scatter(valid_buy_flip_dates, df_analysis.loc[valid_buy_flip_dates, 'Low'] * 0.98,
                            label='Buy Signal', marker='^', color='green', s=100, zorder=5)

            # Plotting Sell Signals
            # Ensure sell_flip_dates contains valid dates present in df.index
            valid_sell_flip_dates = [date for date in sell_flip_dates if date in df_analysis.index] # Use df_analysis for consistency
            if valid_sell_flip_dates:
                plt.scatter(valid_sell_flip_dates, df_analysis.loc[valid_sell_flip_dates, 'High'] * 1.02,
                            label='Sell Signal', marker='v', color='red', s=100, zorder=5)

            plt.title(f'{ticker_symbol} {interval.capitalize()} Supertrend Analysis (ATR: {atr_length}, Mult: {st_multiplier})')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            # Attempt to save instead of show for headless environments
            # Sanitize period string for filename
            safe_period_str = period.replace(" ", "").replace("'", "")
            plot_filename = f"{ticker_symbol}_supertrend_{interval}_P{safe_period_str}_ATR{atr_length}_M{st_multiplier}_plot.png"
            plt.savefig(plot_filename)
            print(f"Plot saved to {plot_filename}")
            plt.close() # Close the figure to free memory

        except Exception as e:
            print(f"Error during plotting: {e}")

    except ImportError:
        print("Error: The 'pandas_ta' library is not installed. Please install it using 'pip install pandas_ta'")
    except Exception as e:
        print(f"An error occurred: {e}")
        if 'df' in locals() and not df.empty:
            print("\n--- Debug: DataFrame Info ---")
            print(df.info())
            print("\n--- Debug: DataFrame Head ---")
            print(df.head())
            print("-----------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze stock data with Supertrend indicator and plot results.")

    parser.add_argument(
        "--ticker",
        type=str,
        default="MSFT",
        help="Stock ticker symbol (e.g., MSFT, AAPL)."
    )
    parser.add_argument(
        "--period",
        type=str,
        default="1y",
        help="Period for historical data (e.g., '1mo', '6mo', '1y', '5y', 'max')."
    )
    parser.add_argument(
        "--atr_length",
        type=int,
        default=10,
        help="ATR period length for Supertrend."
    )
    parser.add_argument(
        "--multiplier",
        type=float,
        default=3.0,
        help="Multiplier for Supertrend."
    )
    parser.add_argument(
        "--interval",
        type=str,
        default="daily",
        choices=['daily', 'weekly'],
        help="Data interval for analysis ('daily' or 'weekly'). Default: 'daily'."
    )

    args = parser.parse_args()

    analyze_stock_supertrend(
        ticker_symbol=args.ticker.upper(),
        period=args.period,
        atr_length=args.atr_length,
        st_multiplier=args.multiplier,
        interval=args.interval
    )
