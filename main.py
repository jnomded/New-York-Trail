#!/usr/bin/env python3
"""
Credit Trail - A financial simulator game set during the 2008 financial crisis
"""

import sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.text import Text

from characters import Hudson, Jane
from game import Game

console = Console()

def display_intro():
    """Display the game introduction and rules."""
    title = Text("CREDIT TRAIL", style="bold cyan")
    subtitle = Text("Navigate the Financial Crisis of 2008", style="italic yellow")
    
    console.print(Panel.fit(
        f"{title}\n{subtitle}\n\n"
        "June 2005 - June 2009: Make financial decisions as you navigate\n"
        "through one of the most turbulent economic periods in history.\n"
        "Can you survive the financial crisis and come out ahead?",
        border_style="bright_blue"
    ))
    
    console.print("\nHow to play:", style="bold green")
    console.print("- Each turn represents one month")
    console.print("- Make decisions to work, invest, pay debts, or relax")
    console.print("- Watch the market for signs of trouble")
    console.print("- Manage your finances and personal well-being")
    console.print("- Survive until June 2009 with positive net worth to win\n")

def select_character():
    """Let the player select a character."""
    console.print(Panel("Choose Your Character", style="bold magenta"))
    
    console.print(Panel.fit(
        "[1] Hudson\n"
        "   - Savings: $6,500\n"
        "   - Income: $62,000 per year\n"
        "   - Risk Rating: 5.5 (moderate risk taker)\n",
        title="Hudson", 
        border_style="blue"
    ))
    
    console.print(Panel.fit(
        "[2] Jane\n"
        "   - Debt: $8,000\n"
        "   - Income: $80,000 per year\n"
        "   - Risk Rating: 2.0 (conservative)\n",
        title="Jane",
        border_style="green"
    ))
    
    choice = IntPrompt.ask("Enter your choice (1-2)", choices=["1", "2"])
    
    if choice == 1:
        return Hudson()
    else:
        return Jane()

def main():
    """Main function to run the game."""
    try:
        console.clear()
        display_intro()
        
        if Prompt.ask("\nReady to begin? (Y/N)", choices=["Y", "N"], default="Y") == "N":
            console.print("Maybe next time. Goodbye!")
            sys.exit(0)
        
        character = select_character()
        console.print(f"\nYou selected [bold]{character.name}[/bold]!")
        
        # Initialize and start the game
        game = Game(character)
        game.start()
        
    except KeyboardInterrupt:
        console.print("\nGame terminated by user. Goodbye!")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
