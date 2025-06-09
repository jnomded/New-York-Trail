#!/usr/bin/env python3
"""
collect_data.py

1. Downloads weekly SPY data between two dates.
2. Saves the full series to CSV.
3. Splits into 12-month windows and plots each window.
"""

import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_weekly_spy(start_date: str, end_date: str,
                     ticker: str = "SPY", output_dir: str = ".") -> pd.DataFrame:
    """
    Downloads weekly OHLCV data for `ticker` between start_date and end_date (inclusive)
    and saves it to CSV. Returns the DataFrame.
    """
    # Because yfinance treats `end` as exclusive, bump it by one day:
    sd = datetime.strptime(start_date, "%Y-%m-%d")
    ed = datetime.strptime(end_date,   "%Y-%m-%d") + pd.Timedelta(days=1)

    df = yf.download(
        ticker,
        start=sd.strftime("%Y-%m-%d"),
        end=ed.strftime("%Y-%m-%d"),
        interval="1wk",
        auto_adjust=True,
        progress=False
    )
    if df.empty:
        raise RuntimeError(f"No data for {ticker} between {start_date} and {end_date}")

    # Ensure output dir exists
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"{ticker}_weekly_{start_date}_to_{end_date}.csv")
    df.to_csv(csv_path)
    print(f"Downloaded {len(df)} weekly rows → {csv_path}")

    return df

def plot_yearly_windows(df: pd.DataFrame, window_months: int = 12, output_dir: str = "."):
    """
    Splits `df` into consecutive windows of `window_months` months,
    and creates one plot per window.
    """
    # Ensure directory
    plots_dir = os.path.join(output_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    # Make sure our index is a DatetimeIndex
    df = df.copy()
    df.index = pd.to_datetime(df.index)

    # Generate window start dates from the first full month onward
    start = df.index.min().to_period("M").to_timestamp()
    end   = df.index.max().to_period("M").to_timestamp()
    # Create list of window start timestamps
    window_starts = pd.date_range(start, end, freq=f"{window_months}M")

    for i, ws in enumerate(window_starts):
        we = ws + pd.DateOffset(months=window_months) - pd.Timedelta(days=1)
        window_df = df[(df.index >= ws) & (df.index <= we)]
        if window_df.empty:
            continue

        plt.figure(figsize=(8, 4))
        plt.plot(window_df.index, window_df["Close"], label="Close")
        plt.title(f"{df.index.min().year}-{df.index.max().year}: SPY Close from {ws.date()} to {we.date()}")
        plt.xlabel("Date")
        plt.ylabel("Adjusted Close")
        plt.grid(True)
        plt.tight_layout()

        fname = os.path.join(plots_dir, f"spy_weekly_{ws.date()}_to_{we.date()}.png")
        plt.savefig(fname)
        plt.close()
        print(f"Saved plot {i+1}: {fname}")

if __name__ == "__main__":
    # 5-year span
    START = "2004-06-01"
    END   = "2009-06-30"
    OUT   = "data"

    weekly_df = fetch_weekly_spy(START, END, output_dir=OUT)

    # Optional: split into 12-month windows (you can adjust window_months if you like)
    plot_yearly_windows(weekly_df, window_months=12, output_dir=OUT)
