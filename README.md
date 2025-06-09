# Credit Trail

A terminal-based financial simulator game set during the 2008 financial crisis.

## Overview

Credit Trail is an interactive, turn-based financial simulator where you navigate the economic landscape from June 2005 to June 2009. Make critical financial decisions, manage your investments, and try to survive one of the most turbulent economic periods in modern history.

## Features

- Choose between two characters with different financial starting points
- Make monthly decisions about work, investments, debt management, and personal well-being
- Experience real historical market events like the Lehman Brothers collapse
- View real S&P 500 market data visualizations for any point in the timeline
- Manage both financial metrics (savings, debt, investments) and life variables (stress, health, reputation)
- Random events that can help or hinder your progress

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Game

1. First, collect the market data (only needed once):
2. Take the files in data_collection out of their directory before running them.
3. Run collect_data.py to gather historical market data:
4. Run generate plots to create visualizations of the S&P 500 data:
```bash
python collect_data.py
python generate_plots.py
```

2. Start the game:
```bash
python main.py
```

## Gameplay

- Each turn represents one month from June 2005 to June 2009
- On each turn, you can choose one action:
  - Work to earn income
  - Pay down debt
  - Invest in the market
  - Relax to reduce stress
  - Check market trends

- Random events may occur that affect your financial situation or personal well-being
- Key historical events will impact the market at specific dates
- The game ends when you reach June 2009 or meet certain failure conditions

## Characters

### Hudson
- Starting savings: $6,500
- Annual income: $62,000
- Risk rating: 5.5 (moderate risk)

### Jane
- Starting debt: $8,000
- Annual income: $80,000
- Risk rating: 2.0 (conservative)

## Win Conditions

- Survive until June 2009 with a positive net worth

## License

This project is for educational purposes only.
