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
        self.process_expenses()

        # Volunteer bonus: increases chance of positive event
        volunteer_bonus = getattr(self.character, "volunteer_bonus", 0)

        # Calculate random event chance (20% base, up to 60% if high stress/low health)
        stress_factor = max(0, (self.character.stress - 40) / 60)  # 0 to 1
        health_factor = max(0, (80 - self.character.health) / 80)  # 0 to 1
        base_chance = 0.2 + 0.4 * max(stress_factor, health_factor)
        base_chance += volunteer_bonus  # Volunteer increases chance of positive event
        if base_chance > 0.6:
            base_chance = 0.6

        # Random event: multiple actions allowed
        allow_multiple_actions = False
        if random.random() < base_chance:
            allow_multiple_actions = True
            console.print(Panel(
                "[bold yellow]You feel a surge of energy and opportunity this month![/bold yellow]\n"
                "You may take multiple main actions this turn.",
                title="Special Opportunity!",
                border_style="yellow"
            ))

        # Player actions
        self.process_player_actions(allow_multiple_actions)

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
            # Track shortfall but don't immediately add to debt
            shortfall = self.monthly_expenses - self.character.savings
            self.character.savings = 0
            self.character.pending_debt = shortfall  # Track pending debt
            console.print(f"[bold red]Warning:[/bold red] You didn't have enough savings to cover expenses. ${shortfall:.2f} will be added to debt at the end of the turn.")
    
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

    def process_player_actions(self, allow_multiple_actions=False):
        """
        Process player actions for the turn.
        allow_multiple_actions: if True, allow up to 2 main actions this turn.
        """
        main_actions = [
            "Work (earn income)",
            "Relax (reduce stress)",
            "Volunteer (help others, reduce expenses/risk)"
        ]
        non_actions = [
            "Pay debt",
            "Invest in market",
            "Check market trends",
            "End turn"
        ]
        main_actions_taken = set()
        main_actions_limit = 2 if allow_multiple_actions else 1
        while True:
            console.print("\n[bold]Available Actions:[/bold]")
            idx = 1
            action_map = {}
            for i, action in enumerate(main_actions, 1):
                if action not in main_actions_taken:
                    console.print(f"{idx}. {action}")
                    action_map[str(idx)] = ("main", i-1)
                    idx += 1
            for j, action in enumerate(non_actions, 1):
                console.print(f"{idx}. {action}")
                action_map[str(idx)] = ("non", j-1)
                idx += 1

            # If player has taken the max allowed main actions, force end of turn
            if len(main_actions_taken) >= main_actions_limit:
                console.print("[green]You've taken the maximum main actions allowed this turn.[/green]")
                break

            choice = Prompt.ask("Choose an action (1 - 3) to end turn.", choices=list(action_map.keys()))
            action_type, action_idx = action_map[choice]

            if action_type == "main":
                if action_idx == 0:
                    self.action_work()
                elif action_idx == 1:
                    self.action_relax()
                elif action_idx == 2:
                    self.action_volunteer()
                main_actions_taken.add(main_actions[action_idx])
                # If reached main actions limit, end turn
                if len(main_actions_taken) >= main_actions_limit:
                    console.print("[green]You've taken the maximum main actions allowed this turn.[/green]")
                    break
            else:
                if action_idx == 0:
                    self.action_pay_debt()
                elif action_idx == 1:
                    self.action_invest()
                elif action_idx == 2:
                    self.action_check_market()
                elif action_idx == 3:
                    break  # End turn

    def action_volunteer(self):
        """Volunteer: reduce expenses, risk, and increase chance of positive event."""
        expense_reduction = self.monthly_expenses * 0.1
        self.monthly_expenses -= expense_reduction
        if self.monthly_expenses < 0:
            self.monthly_expenses = 0
        self.character.risk_rating -= 0.5
        if self.character.risk_rating < 1:
            self.character.risk_rating = 1
        # Set a bonus for next turn's event chance
        self.character.volunteer_bonus = 0.1
        console.print(
            f"[cyan]You volunteered this month![/cyan]\n"
            f"Monthly expenses reduced by ${expense_reduction:.2f}.\n"
            f"Risk rating decreased to {self.character.risk_rating:.1f}/10.\n"
            f"You're more likely to encounter a positive event next month."
        )

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
        """Invest money in the market with risk options and secret casino."""
        while True:
            invest_types = [
                ("Sell shares (convert shares to cash)", 0),
                ("Purchase shares (lower risk, -1 risk rating)", -1),
                ("Day trading (higher risk, +2 risk rating)", 2),
                ("Option day trading (very high risk, +4 risk rating)", 4),
                ("Short the market (+3 risk rating)", 3)
            ]
            show_casino = self.character.risk_rating > 7 and self.character.debt > 10000
            if show_casino:
                invest_types.append(("Secret: Go to the casino (50/50 double or lose all)", "casino"))
            invest_types.append(("Go back", "back"))

            console.print(f"You have ${self.character.savings:.2f} available to invest.")
            console.print(f"Your risk rating is {self.character.risk_rating}/10 (higher = more volatile returns)")

            for idx, (desc, _) in enumerate(invest_types, 1):
                console.print(f"{idx}. {desc}")

            choices = [str(i) for i in range(1, len(invest_types) + 1)]
            invest_choice = IntPrompt.ask("Choose investment type", choices=choices)
            invest_type, risk_change = invest_types[invest_choice - 1]

            # --- New logic for "Purchase shares" ---
            if invest_type.startswith("Purchase shares"):
                # Example market prices (replace with your actual market data)
                market_prices = {'stocks': 100.0, 'bonds': 95.0}
                investment_options = list(market_prices.keys())
                console.print("Which investment would you like to purchase?")
                for idx, inv in enumerate(investment_options):
                    console.print(f"{idx + 1}. {inv} (Current price: ${market_prices[inv]:.2f})")
                choice = IntPrompt.ask("Enter the number of your choice",
                                       choices=[str(i + 1) for i in range(len(investment_options))])
                investment_type = investment_options[choice - 1]

                max_shares = int(self.character.savings // market_prices[investment_type])
                if max_shares == 0:
                    console.print("[yellow]You don't have enough savings to buy any shares.[/yellow]")
                    return

                num_shares = IntPrompt.ask(
                    f"How many shares of {investment_type} would you like to buy? (1-{max_shares})",
                    choices=[str(i) for i in range(1, max_shares + 1)]
                )
                price = market_prices[investment_type]

                success = self.character.buy_shares(investment_type, num_shares, price)
                if success:
                    console.print(
                        f"Successfully purchased {num_shares} shares of {investment_type} at ${price:.2f} each.")
                else:
                    console.print("[red]Purchase failed. Not enough savings.[/red]")
                return  # End after purchase
            # --- End of new logic for "Purchase shares" ---

            # ...inside action_invest...
            if invest_type.startswith("Sell shares"):
                market_prices = {'stocks': 100.0, 'bonds': 95.0}
                holdings = self.character.investments_dict
                owned_types = [k for k, v in holdings.items() if v > 0]
                if not owned_types:
                    console.print("[yellow]You don't own any shares to sell.[/yellow]")
                    return

                console.print("Your current holdings:")
                for idx, inv in enumerate(owned_types):
                    num = holdings[inv]
                    price = market_prices.get(inv, 0)
                    console.print(f"{idx+1}. {inv}: {num} shares (Current price: ${price:.2f})")

                choice = IntPrompt.ask("Enter the number of the investment to sell", choices=[str(i+1) for i in range(len(owned_types))])
                investment_type = owned_types[choice - 1]
                max_shares = holdings[investment_type]
                price = market_prices[investment_type]

                num_shares = IntPrompt.ask(
                    f"How many shares of {investment_type} would you like to sell? (1-{max_shares})",
                    choices=[str(i) for i in range(1, max_shares+1)]
                )

                sold, proceeds = self.character.sell_shares(investment_type, num_shares, price)
                if sold > 0:
                    console.print(f"Sold {sold} shares of {investment_type} at ${price:.2f} each for ${proceeds:.2f}.")
                else:
                    console.print("[red]Sale failed. You don't own enough shares.[/red]")
                return
            
            # Handle risk change options

            if risk_change == "back":
                # Return to main action menu
                return

            if risk_change == "casino":
                # Casino logic
                if self.character.savings <= 0:
                    console.print("[yellow]You don't have any savings to bet at the casino.[/yellow]")
                    continue
                amount = IntPrompt.ask(
                    f"How much would you like to bet at the casino? (0-{int(self.character.savings)})",
                    default=int(self.character.savings)
                )
                amount = min(amount, self.character.savings)
                if amount <= 0:
                    console.print("No bet made.")
                    continue
                self.character.savings -= amount
                win = random.choice([True, False])
                if win:
                    winnings = amount * 2
                    self.character.savings += winnings
                    console.print(f"[bold magenta]You WON at the casino! Your bet is now ${winnings:.2f}.[/bold magenta]")
                else:
                    console.print(f"[bold red]You lost your bet at the casino. ${amount:.2f} is gone.[/bold red]")
                # Casino does not affect risk rating
                return

            # Standard investment
            if self.character.savings <= 0:
                console.print("[yellow]You don't have any savings to invest.[/yellow]")
                continue
            amount = IntPrompt.ask(
                f"How much would you like to invest? (0-{int(self.character.savings)})",
                default=int(self.character.savings / 2)
            )
            amount = min(amount, self.character.savings)
            if amount <= 0:
                console.print("No investment made.")
                continue

            self.character.invest(amount)
            # Adjust risk rating, clamp between 1 and 10
            self.character.risk_rating += risk_change
            if self.character.risk_rating < 1:
                self.character.risk_rating = 1
            if self.character.risk_rating > 10:
                self.character.risk_rating = 10

            console.print(f"You've invested [green]${amount:.2f}[/green] in the market via [bold]{invest_type.split('(')[0].strip()}[/bold].")
            if isinstance(risk_change, int):
                if risk_change < 0:
                    console.print(f"[cyan]Your risk rating decreased to {self.character.risk_rating}/10.[/cyan]")
                elif risk_change > 0:
                    console.print(f"[red]Your risk rating increased to {self.character.risk_rating}/10.[/red]")
            return

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
        # Add pending debt to total debt
        if hasattr(self.character, "pending_debt") and self.character.pending_debt > 0:
            self.character.debt += self.character.pending_debt
            console.print(f"[bold red]Pending debt of ${self.character.pending_debt:.2f} added to total debt.[/bold red]")
            self.character.pending_debt = 0  # Reset pending debt

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