"""
Core game logic for Credit Trail.
"""

import datetime
import time
import random
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from market import display_sp500, calculate_investment_return, get_market_sentiment
from events import get_random_event

console = Console()

class Game:
    """Main game class that manages the game state and logic."""
    
    def __init__(self, character):
        """
        Initialize the game with a character.
        
        Parameters:
        - character: The character object to use for the game
        """
        self.character = character
        self.start_date = datetime.date(2005, 6, 1)
        self.end_date = datetime.date(2009, 6, 1)
        self.current_date = self.start_date
        self.turn = 1
        self.max_turns = 48  # 4 years * 12 months
        self.game_over = False
        self.monthly_expenses = character.monthly_expenses
    
    def start(self):
        """Start the game and run the main game loop."""
        console.clear()
        console.print(Panel(f"[bold green]Credit Trail[/bold green] - Starting on {self.start_date.strftime('%B %d, %Y')}"))
        console.print(f"Welcome, [bold]{self.character.name}[/bold]! Your journey begins...\n")
        
        # Main game loop
        while not self.game_over and self.turn <= self.max_turns:
            self.play_turn()
            
            # Check if game should end
            if self.character.health <= 0:
                self.end_game("Your health deteriorated to a critical level. Game over!")
            elif self.character.debt > 50000 and self.character.credit_score < 500:
                self.end_game("Your debt spiraled out of control. You've gone bankrupt!")
            
            # Advance to next turn if game isn't over
            if not self.game_over:
                self.advance_turn()
        
        # Game completed - check win condition
        if not self.game_over:
            if self.character.get_net_worth() > 0:
                console.print(Panel(
                    f"[bold green]Congratulations![/bold green] You've survived the financial crisis!\n"
                    f"Final net worth: ${self.character.get_net_worth():.2f}",
                    border_style="green"
                ))
            else:
                console.print(Panel(
                    f"[bold yellow]You survived, but at what cost?[/bold yellow]\n"
                    f"You made it through the financial crisis, but ended with a negative net worth of ${self.character.get_net_worth():.2f}",
                    border_style="yellow"
                ))
    
    def play_turn(self):
        """Play a single turn of the game."""
        self.display_status()
        
        # Process monthly expenses
        self.process_expenses()
        
        # Check for random events
        event = get_random_event(self.current_date, self.character)
        if event:
            self.process_event(event)
        
        # Player actions
        self.process_player_actions()
    
    def display_status(self):
        """Display the current game status."""
        console.print(f"\n[bold cyan]== TURN {self.turn}/{self.max_turns} - {self.current_date.strftime('%B %Y')} ==[/bold cyan]")
        
        # Financial status
        financial_table = Table(title="Financial Status")
        financial_table.add_column("Metric", style="cyan")
        financial_table.add_column("Value", style="green")
        
        financial_table.add_row("Savings", f"${self.character.savings:.2f}")
        financial_table.add_row("Debt", f"${self.character.debt:.2f}")
        financial_table.add_row("Investments", f"${self.character.investments:.2f}")
        financial_table.add_row("Monthly Income", f"${self.character.get_monthly_income():.2f}")
        financial_table.add_row("Monthly Expenses", f"${self.monthly_expenses:.2f}")
        financial_table.add_row("Credit Score", f"{int(self.character.credit_score)}")
        financial_table.add_row("Net Worth", f"${self.character.get_net_worth():.2f}")
        
        # Personal status
        personal_table = Table(title="Personal Status")
        personal_table.add_column("Metric", style="magenta")
        personal_table.add_column("Value", style="yellow")
        
        personal_table.add_row("Stress", f"{self.character.stress}/100")
        personal_table.add_row("Health", f"{self.character.health}/100")
        personal_table.add_row("Reputation", f"{self.character.reputation}/100")
        
        # Display both tables side by side
        console.print(financial_table)
        console.print(personal_table)
        
        # Market sentiment
        sentiment = get_market_sentiment(self.current_date)
        console.print(f"\n[italic]Market Sentiment:[/italic] {sentiment}")
    
    def process_expenses(self):
        """Process monthly expenses."""
        if self.character.savings >= self.monthly_expenses:
            self.character.savings -= self.monthly_expenses
        else:
            # Not enough savings, go into debt
            shortfall = self.monthly_expenses - self.character.savings
            self.character.savings = 0
            self.character.debt += shortfall
            self.character.credit_score -= 10  # Credit score penalty
            
            console.print(f"[bold red]Warning:[/bold red] You didn't have enough savings to cover expenses. ${shortfall:.2f} added to debt.")
    
    def process_event(self, event):
        """Process a random event."""
        console.print(Panel(
            f"[bold]{event.title}[/bold]\n\n{event.description}",
            title="Event!",
            border_style="yellow"
        ))
        
        # Apply event effects
        effects = event.apply(self.character)
        
        console.print(f"[italic]{event.effect_description}[/italic]")
        
        # Display effects if any
        if effects:
            effect_lines = []
            for key, value in effects.items():
                if abs(value) > 0:
                    sign = "+" if value > 0 else ""
                    if key in ['savings', 'debt', 'income', 'investments']:
                        effect_lines.append(f"{key.capitalize()}: {sign}${value:.2f}")
                    else:
                        effect_lines.append(f"{key.capitalize()}: {sign}{value}")
            
            if effect_lines:
                console.print("Effects:", style="bold")
                for line in effect_lines:
                    console.print(f"  {line}")
        
        console.print()  # Empty line for spacing
        time.sleep(2)  # Pause to read the event
    
    def process_player_actions(self):
        """Process player actions for the turn."""
        actions = [
            "Work (earn income)",
            "Pay debt",
            "Invest in market",
            "Relax (reduce stress)",
            "Check market trends"
        ]
        
        while True:
            console.print("\n[bold]Available Actions:[/bold]")
            for i, action in enumerate(actions, 1):
                console.print(f"{i}. {action}")
            
            choice = IntPrompt.ask("Choose an action (1-5)", choices=[str(i) for i in range(1, 6)])
            
            if choice == 1:
                self.action_work()
            elif choice == 2:
                self.action_pay_debt()
            elif choice == 3:
                self.action_invest()
            elif choice == 4:
                self.action_relax()
            elif choice == 5:
                self.action_check_market()
                continue  # Don't end turn after checking market
            
            break  # End turn after taking an action
    
    def action_work(self):
        """Work action to earn income."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            work_task = progress.add_task("[green]Working...", total=100)
            
            # Simulate work
            while not progress.finished:
                progress.update(work_task, advance=random.randint(5, 15))
                time.sleep(0.2)
        
        income = self.character.work()
        console.print(f"You worked for the month and earned [green]${income:.2f}[/green]")
        console.print(f"Stress increased by 10 points to {self.character.stress}/100")
    
    def action_pay_debt(self):
        """Pay down debt."""
        if self.character.debt <= 0:
            console.print("[yellow]You don't have any debt to pay off.[/yellow]")
            return
        
        console.print(f"You have ${self.character.savings:.2f} in savings and ${self.character.debt:.2f} in debt.")
        max_payment = min(self.character.savings, self.character.debt)
        
        if max_payment <= 0:
            console.print("[red]You don't have any savings to pay down debt.[/red]")
            return
        
        payment = IntPrompt.ask(
            f"How much would you like to pay? (0-{int(max_payment)})",
            default=int(max_payment)
        )
        
        payment = min(payment, max_payment)
        if payment <= 0:
            console.print("No payment made.")
            return
        
        actual_payment = self.character.pay_debt(payment)
        console.print(f"You paid [green]${actual_payment:.2f}[/green] toward your debt.")
        console.print(f"Remaining debt: [{'green' if self.character.debt == 0 else 'red'}]${self.character.debt:.2f}[/{'green' if self.character.debt == 0 else 'red'}]")
        console.print(f"Credit score improved to {int(self.character.credit_score)}")
    
    def action_invest(self):
        """Invest money in the market."""
        if self.character.savings <= 0:
            console.print("[yellow]You don't have any savings to invest.[/yellow]")
            return
        
        console.print(f"You have ${self.character.savings:.2f} available to invest.")
        console.print(f"Your risk rating is {self.character.risk_rating}/10 (higher = more volatile returns)")
        
        amount = IntPrompt.ask(
            f"How much would you like to invest? (0-{int(self.character.savings)})",
            default=int(self.character.savings / 2)
        )
        
        amount = min(amount, self.character.savings)
        if amount <= 0:
            console.print("No investment made.")
            return
        
        self.character.invest(amount)
        console.print(f"You've invested [green]${amount:.2f}[/green] in the market.")
    
    def action_relax(self):
        """Relax to reduce stress."""
        if self.character.stress <= 10:
            console.print("[yellow]You're already quite relaxed.[/yellow]")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            relax_task = progress.add_task("[cyan]Relaxing...", total=100)
            
            # Simulate relaxation
            while not progress.finished:
                progress.update(relax_task, advance=random.randint(5, 15))
                time.sleep(0.2)
        
        stress_reduction = self.character.relax()
        console.print(f"You took time to relax. Stress reduced by [cyan]{stress_reduction}[/cyan] points.")
        console.print(f"Current stress level: {self.character.stress}/100")
        console.print(f"Health improved to {self.character.health}/100")
    
    def action_check_market(self):
        """Check the current market trends."""
        console.print("Displaying S&P 500 market data for the past year...")
        display_sp500(self.current_date)
    
    def advance_turn(self):
        """Advance to the next turn."""
        # Update investments
        if self.character.investments > 0:
            new_amount, return_percent = calculate_investment_return(
                self.character.investments, 
                self.character.risk_rating,
                self.current_date
            )
            
            gain_or_loss = new_amount - self.character.investments
            self.character.investments = new_amount
            
            sign = "+" if gain_or_loss >= 0 else ""
            console.print(f"Your investments changed by [{'green' if gain_or_loss >= 0 else 'red'}]{sign}{return_percent:.1f}%[/{'green' if gain_or_loss >= 0 else 'red'}] (${gain_or_loss:.2f})")
        
        # Apply interest on debt (assume 1.5% monthly interest)
        if self.character.debt > 0:
            interest = self.character.debt * 0.015
            self.character.debt += interest
            console.print(f"Interest added to debt: [red]${interest:.2f}[/red]")
        
        # Update date and turn counter
        self.current_date = add_one_month(self.current_date)
        self.turn += 1
        
        # Press enter to continue
        Prompt.ask("\nPress Enter to continue to next month", default="")
        console.clear()
    
    def end_game(self, message):
        """End the game with a specific message."""
        self.game_over = True
        console.print(Panel(f"[bold red]GAME OVER[/bold red]\n\n{message}", border_style="red"))
        
        # Display final statistics
        console.print("\n[bold]Final Statistics:[/bold]")
        console.print(f"Character: {self.character.name}")
        console.print(f"Survived until: {self.current_date.strftime('%B %Y')}")
        console.print(f"Final net worth: ${self.character.get_net_worth():.2f}")
        console.print(f"Savings: ${self.character.savings:.2f}")
        console.print(f"Debt: ${self.character.debt:.2f}")
        console.print(f"Investments: ${self.character.investments:.2f}")

def add_one_month(date):
    """
    Add one month to a date.
    
    Parameters:
    - date: Original date
    
    Returns:
    - New date one month later
    """
    month = date.month
    year = date.year
    
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    
    # Handle cases where the day might be invalid in the next month
    day = min(date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    
    return datetime.date(year, month, day)
