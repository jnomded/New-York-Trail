#!/usr/bin/env python3
"""
generate_yearly_plots.py

1. Downloads weekly SPY data from 2004-06-01 through 2009-06-30.
2. For each month m from 2005-06 to 2009-05 (48 points),
   creates a plot of the prior 52 weeks ending at m.
3. Saves each plot as data/plots/spy_year_ending_<YYYY-MM>.png
"""

import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def fetch_weekly_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download weekly-adjusted SPY from start (inclusive) to end (inclusive)."""
    sd = pd.to_datetime(start)
    ed = pd.to_datetime(end) + pd.Timedelta(days=1)  # make end inclusive
    df = yf.download(
        ticker,
        start=sd.strftime("%Y-%m-%d"),
        end=ed.strftime("%Y-%m-%d"),
        interval="1wk",
        auto_adjust=True,
        progress=False
    )
    if df.empty:
        raise RuntimeError(f"No data for {ticker} between {start} and {end}")
    df.index = pd.to_datetime(df.index)
    return df

def generate_monthly_windows(df: pd.DataFrame,
                             window_weeks: int = 52,
                             first_month: str = "2005-06-01",
                             last_month:  str = "2009-05-01",
                             output_dir:  str = "data/plots"):
    """
    For each month between first_month and last_month inclusive:
      - Let M be the first calendar day of that month.
      - Window = [M - window_weeks*7 days, M]
      - Plot df['Close'] over Window, save PNG.
    """
    os.makedirs(output_dir, exist_ok=True)
    # generate the list of month-start dates
    month_starts = pd.date_range(first_month, last_month,
                                 freq="MS")  # Month Start frequency
    for dt in month_starts:
        window_start = dt - pd.Timedelta(weeks=window_weeks)
        window_df = df[(df.index > window_start) & (df.index <= dt)]
        if window_df.empty:
            print(f"Skipping {dt.date()}: no data in window")
            continue

        plt.figure(figsize=(8, 4))
        plt.plot(window_df.index, window_df["Close"], linewidth=1)
        plt.title(f"SPY Weekly Close: {window_start.date()} → {dt.date()}")
        plt.xlabel("Date")
        plt.ylabel("Adjusted Close")
        plt.grid(True)
        plt.tight_layout()

        fname = os.path.join(output_dir,
                             f"spy_year_ending_{dt.strftime('%Y-%m')}.png")
        plt.savefig(fname)
        plt.close()
        print(f"Saved plot for ending {dt.strftime('%Y-%m')}: {fname}")

if __name__ == "__main__":
    TICKER = "SPY"
    FETCH_START = "2004-06-01"
    FETCH_END   = "2009-06-30"
    df_weekly = fetch_weekly_data(TICKER, FETCH_START, FETCH_END)

    generate_monthly_windows(
        df_weekly,
        window_weeks=52,
        first_month="2005-06-01",
        last_month="2009-05-01",
        output_dir="../data/plots"
    )
