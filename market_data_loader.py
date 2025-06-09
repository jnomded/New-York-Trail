"""
Market data loader for Credit Trail game.
Provides functions to load pre-collected market data.
"""

import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console

console = Console()

def load_game_market_data():
    """Load the pre-collected game market data."""
    try:
        with open('data/game_market_data.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        console.print("[red]Game market data not found. Please run collect_data.py first.[/red]")
        return None
    except Exception as e:
        console.print(f"[red]Error loading game data: {str(e)}[/red]")
        return None

def get_market_data_for_turn(turn_number):
    """Get market data for a specific game turn."""
    game_data = load_game_market_data()
    if game_data and turn_number in game_data:
        return game_data[turn_number]
    return None

def display_market_chart_for_turn(turn_number):
    """Display market chart for a specific game turn using pre-loaded data."""
    turn_data = get_market_data_for_turn(turn_number)

    if not turn_data:
        console.print("[red]No market data available for this turn.[/red]")
        return

    market_data = turn_data['market_data']
    turn_date = turn_data['turn_date']

    # Plot the closing prices
    plt.figure(figsize=(10, 5))
    plt.plot(market_data.index, market_data["Close"], marker='o', linewidth=1, markersize=2)
    plt.title(f"S&P 500 Last 52 Weeks up to {turn_date.strftime('%Y-%m-%d')}")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Display for 25 seconds then close
    console.print("[green]Displaying market chart (closes automatically after 25 seconds)...[/green]")
    plt.show(block=False)
    plt.pause(25)
    plt.close()

def get_latest_price_for_turn(turn_number):
    """Get the latest S&P 500 price for a specific turn."""
    turn_data = get_market_data_for_turn(turn_number)
    if turn_data and 'latest_close' in turn_data:
        return turn_data['latest_close']
    return None

def is_data_available():
    """Check if market data is available."""
    return os.path.exists('data/game_market_data.pkl')
