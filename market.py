"""
Market simulation for Credit Trail game.
"""

import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import random
import numpy as np
import pandas as pd
from rich.console import Console

console = Console()

def display_sp500(current_turn_date):
    """
    Displays the pre-generated S&P 500 plot for the correct month from the data/plots/ folder.
    Shows the plot for 25 seconds before auto-closing.

    Parameters:
    - current_turn_date (datetime.date or datetime.datetime): The reference date for the end of the 52-week window.
    """
    import os
    # Ensure we have a datetime.date object
    if isinstance(current_turn_date, datetime.datetime):
        end_date = current_turn_date.date()
    else:
        end_date = current_turn_date

    # Build the filename for the plot image
    plot_filename = f"spy_year_ending_{end_date.year}-{end_date.month:02d}.png"
    plot_path = os.path.join("data", "plots", plot_filename)

    if not os.path.exists(plot_path):
        console.print(f"[red]Market plot for {end_date.strftime('%B %Y')} not found.[/red]")
        return

    # Display the image using matplotlib
    import matplotlib.image as mpimg
    img = mpimg.imread(plot_path)
    plt.figure(figsize=(10, 5))
    plt.imshow(img)
    plt.axis('off')
    plt.title(f"S&P 500 Last 52 Weeks up to {end_date.strftime('%Y-%m-%d')}")
    console.print("[green]Displaying market chart (closes automatically after 25 seconds)...[/green]")
    plt.show(block=False)
    plt.pause(25)
    plt.close()

def generate_mock_sp500_data(start_date, end_date, current_date):
    """
    Generate simulated S&P 500 data when real data can't be fetched.
    
    Parameters:
    - start_date: Start date for the data
    - end_date: End date for the data
    - current_date: Current game date to determine market trend
    
    Returns:
    - DataFrame with simulated market data
    """
    # Create date range with business days
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # Determine starting point based on historical averages
    if current_date.year < 2007:
        # Pre-crisis: S&P around 1200-1400
        base_value = 1300
        volatility = 0.01
        trend = 0.0002  # slight upward trend
    elif current_date.year == 2007:
        # Early crisis: S&P peaked around 1500-1600
        base_value = 1500
        volatility = 0.015
        if current_date.month < 10:
            trend = 0.0003  # still rising
        else:
            trend = -0.0005  # starting to fall
    elif current_date.year == 2008:
        # Crisis: S&P fell from ~1400 to ~800
        base_value = 1200
        volatility = 0.025
        trend = -0.001  # strong downward trend
        # Lehman effect
        if current_date.month >= 9:
            trend = -0.002
            volatility = 0.035
    else:  # 2009
        # Recovery beginning: S&P bottomed around 700
        base_value = 800
        volatility = 0.02
        if current_date.month < 3:
            trend = -0.0005  # still falling
        else:
            trend = 0.001  # starting recovery
    
    # Generate prices with random walk
    n_days = len(date_range)
    noise = np.random.normal(0, volatility, n_days)
    trends = np.arange(n_days) * trend
    
    # Combine base, trend and noise
    closes = base_value * (1 + trends + np.cumsum(noise))
    
    # Create other price columns based on close
    opens = closes * (1 + np.random.normal(0, 0.003, n_days))
    highs = np.maximum(opens, closes) * (1 + np.abs(np.random.normal(0, 0.005, n_days)))
    lows = np.minimum(opens, closes) * (1 - np.abs(np.random.normal(0, 0.005, n_days)))
    volumes = np.random.randint(1000000, 5000000, n_days)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Open': opens,
        'High': highs,
        'Low': lows,
        'Close': closes,
        'Volume': volumes
    }, index=date_range)
    
    return df

def calculate_investment_return(amount, risk_rating, current_date):
    """
    Calculate investment returns based on risk rating and current market conditions.
    
    Parameters:
    - amount: Amount invested
    - risk_rating: Character's risk rating (1.0-10.0)
    - current_date: Current game date
    
    Returns:
    - Tuple of (new_amount, return_percentage)
    """
    # Success rate decreases as risk rating increases
    success_rate = max(20, 100 - (risk_rating - 1) * 10)
    
    # Base monthly return ranges from -8% to +12%
    base_return = random.uniform(-8, 12) / 100
    
    # Adjust returns based on key market events
    lehman_collapse = datetime.date(2008, 9, 15)
    market_peak = datetime.date(2007, 10, 9)
    bear_stearns_collapse = datetime.date(2008, 3, 14)
    
    # Check if we're near a significant market event
    if abs((current_date - lehman_collapse).days) < 60:
        # During Lehman collapse, higher chance of big losses
        base_return = random.uniform(-25, 5) / 100
    elif abs((current_date - market_peak).days) < 30:
        # Near market peak, mostly positive returns
        base_return = random.uniform(-2, 15) / 100
    elif abs((current_date - bear_stearns_collapse).days) < 45:
        # Bear Stearns collapse
        base_return = random.uniform(-15, 8) / 100
    
    # Apply risk multiplier - higher risk means higher volatility
    risk_multiplier = 0.5 + (risk_rating / 10)
    adjusted_return = base_return * risk_multiplier
    
    # Calculate new amount
    new_amount = amount * (1 + adjusted_return)
    
    return (new_amount, adjusted_return * 100)  # Return new amount and percentage

def get_market_sentiment(current_date):
    """
    Returns a description of current market sentiment based on the date.
    
    Parameters:
    - current_date: Current game date
    
    Returns:
    - String describing market sentiment
    """
    # Define key dates and periods
    housing_peak = datetime.date(2006, 4, 1)
    subprime_start = datetime.date(2007, 2, 1)
    bear_stearns = datetime.date(2008, 3, 14)
    lehman = datetime.date(2008, 9, 15)
    bottom = datetime.date(2009, 3, 9)
    
    if current_date < housing_peak:
        return "Housing market booming, confidence high"
    elif current_date < subprime_start:
        return "Housing prices leveling off, but markets strong"
    elif current_date < bear_stearns:
        return "Concerns about subprime mortgages, market volatile"
    elif current_date < lehman:
        return "Serious financial instability, Bear Stearns bailout"
    elif current_date < bottom:
        return "Financial crisis in full effect, panic in markets"
    else:
        return "Markets beginning to stabilize, signs of recovery"