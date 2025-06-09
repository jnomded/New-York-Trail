"""
Events system for Credit Trail game.
"""

import random
import datetime

class Event:
    """Base class for game events."""
    
    def __init__(self, title, description, effect_description):
        """
        Initialize an event.
        
        Parameters:
        - title: Event title
        - description: Event description
        - effect_description: Description of the event's effects
        """
        self.title = title
        self.description = description
        self.effect_description = effect_description
    
    def apply(self, character):
        """
        Apply the event's effects to the character.
        
        Parameters:
        - character: The character to apply effects to
        
        Returns:
        - Dictionary containing the effects applied
        """
        # This method should be overridden by subclasses
        return {}


class FinancialEvent(Event):
    """Events that impact financial status."""
    
    def __init__(self, title, description, effect_description, 
                 savings_change=0, debt_change=0, income_change=0, 
                 investment_change=0, credit_score_change=0,
                 stress_change=0, health_change=0, reputation_change=0):
        """
        Initialize a financial event.
        
        Parameters:
        - title: Event title
        - description: Event description
        - effect_description: Description of the event's effects
        - savings_change: Change to savings (can be absolute or percentage)
        - debt_change: Change to debt (can be absolute or percentage)
        - income_change: Change to income (can be absolute or percentage)
        - investment_change: Change to investments (can be absolute or percentage)
        - credit_score_change: Change to credit score (absolute)
        - stress_change: Change to stress level (absolute)
        - health_change: Change to health (absolute)
        - reputation_change: Change to reputation (absolute)
        """
        super().__init__(title, description, effect_description)
        self.savings_change = savings_change
        self.debt_change = debt_change
        self.income_change = income_change
        self.investment_change = investment_change
        self.credit_score_change = credit_score_change
        self.stress_change = stress_change
        self.health_change = health_change
        self.reputation_change = reputation_change
    
    def apply(self, character):
        """Apply financial effects to the character."""
        effects = {}
        
        # Apply savings change
        if isinstance(self.savings_change, float) and -1 < self.savings_change < 1:
            # Percentage change
            change = character.savings * self.savings_change
            effects['savings'] = change
            character.savings += change
        else:
            # Absolute change
            effects['savings'] = self.savings_change
            character.savings += self.savings_change
        
        # Apply debt change
        if isinstance(self.debt_change, float) and -1 < self.debt_change < 1:
            # Percentage change
            change = character.debt * self.debt_change
            effects['debt'] = change
            character.debt += change
        else:
            # Absolute change
            effects['debt'] = self.debt_change
            character.debt += self.debt_change
        
        # Apply income change
        if isinstance(self.income_change, float) and -1 < self.income_change < 1:
            # Percentage change
            change = character.income * self.income_change
            effects['income'] = change
            character.income += change
        else:
            # Absolute change
            effects['income'] = self.income_change
            character.income += self.income_change
        
        # Apply investment change
        if isinstance(self.investment_change, float) and -1 < self.investment_change < 1:
            # Percentage change
            change = character.investments * self.investment_change
            effects['investments'] = change
            character.investments += change
        else:
            # Absolute change
            effects['investments'] = self.investment_change
            character.investments += self.investment_change
        
        # Apply credit score change
        effects['credit_score'] = self.credit_score_change
        character.credit_score += self.credit_score_change
        if character.credit_score > 850:
            character.credit_score = 850
        elif character.credit_score < 300:
            character.credit_score = 300
        
        # Apply stress change
        if self.stress_change != 0:
            effects['stress'] = self.stress_change
            character.stress += self.stress_change
            if character.stress > 100:
                character.stress = 100
            elif character.stress < 0:
                character.stress = 0
        
        # Apply health change
        if self.health_change != 0:
            effects['health'] = self.health_change
            character.health += self.health_change
            if character.health > 100:
                character.health = 100
            elif character.health < 0:
                character.health = 0
        
        # Apply reputation change
        if self.reputation_change != 0:
            effects['reputation'] = self.reputation_change
            character.reputation += self.reputation_change
            if character.reputation > 100:
                character.reputation = 100
            elif character.reputation < 0:
                character.reputation = 0
        
        return effects


class LifeEvent(Event):
    """Events that impact life variables."""
    
    def __init__(self, title, description, effect_description, 
                 stress_change=0, health_change=0, reputation_change=0,
                 savings_change=0, debt_change=0, income_change=0,
                 investment_change=0, credit_score_change=0):
        """
        Initialize a life event.
        
        Parameters:
        - title: Event title
        - description: Event description
        - effect_description: Description of the event's effects
        - stress_change: Change to stress level (absolute)
        - health_change: Change to health (absolute)
        - reputation_change: Change to reputation (absolute)
        - savings_change: Change to savings (can be absolute or percentage)
        - debt_change: Change to debt (can be absolute or percentage)
        - income_change: Change to income (can be absolute or percentage)
        - investment_change: Change to investments (can be absolute or percentage)
        - credit_score_change: Change to credit score (absolute)
        """
        super().__init__(title, description, effect_description)
        self.stress_change = stress_change
        self.health_change = health_change
        self.reputation_change = reputation_change
        self.savings_change = savings_change
        self.debt_change = debt_change
        self.income_change = income_change
        self.investment_change = investment_change
        self.credit_score_change = credit_score_change
    
    def apply(self, character):
        """Apply life effects to the character."""
        effects = {}
        
        # Apply stress change
        effects['stress'] = self.stress_change
        character.stress += self.stress_change
        if character.stress > 100:
            character.stress = 100
        elif character.stress < 0:
            character.stress = 0
        
        # Apply health change
        effects['health'] = self.health_change
        character.health += self.health_change
        if character.health > 100:
            character.health = 100
        elif character.health < 0:
            character.health = 0
        
        # Apply reputation change
        effects['reputation'] = self.reputation_change
        character.reputation += self.reputation_change
        if character.reputation > 100:
            character.reputation = 100
        elif character.reputation < 0:
            character.reputation = 0
        
        # Apply savings change
        if isinstance(self.savings_change, float) and -1 < self.savings_change < 1:
            # Percentage change
            change = character.savings * self.savings_change
            effects['savings'] = change
            character.savings += change
        else:
            # Absolute change
            effects['savings'] = self.savings_change
            character.savings += self.savings_change
        
        # Apply debt change
        if isinstance(self.debt_change, float) and -1 < self.debt_change < 1:
            # Percentage change
            change = character.debt * self.debt_change
            effects['debt'] = change
            character.debt += change
        else:
            # Absolute change
            effects['debt'] = self.debt_change
            character.debt += self.debt_change
        
        # Apply income change
        if isinstance(self.income_change, float) and -1 < self.income_change < 1:
            # Percentage change
            change = character.income * self.income_change
            effects['income'] = change
            character.income += change
        else:
            # Absolute change
            effects['income'] = self.income_change
            character.income += self.income_change
        
        # Apply investment change
        if isinstance(self.investment_change, float) and -1 < self.investment_change < 1:
            # Percentage change
            change = character.investments * self.investment_change
            effects['investments'] = change
            character.investments += change
        else:
            # Absolute change
            effects['investments'] = self.investment_change
            character.investments += self.investment_change
        
        # Apply credit score change
        if self.credit_score_change != 0:
            effects['credit_score'] = self.credit_score_change
            character.credit_score += self.credit_score_change
            if character.credit_score > 850:
                character.credit_score = 850
            elif character.credit_score < 300:
                character.credit_score = 300
        
        return effects


def get_random_event(current_date, character):
    """
    Get a random event based on the current date and character state.
    
    Parameters:
    - current_date: Current game date
    - character: Current character
    
    Returns:
    - An Event object or None if no event occurs
    """
    # Define event probability (30% chance of an event per turn)
    if random.random() > 0.3:
        return None
    
    # Check for historical events based on date
    historical_event = get_historical_event(current_date)
    if historical_event:
        return historical_event
    
    # Define possible random events
    financial_events = [
        FinancialEvent(
            "Car Repair", 
            "Your car broke down and needs repairs.",
            "You had to pay for expensive car repairs.",
            savings_change=-500
        ),
        FinancialEvent(
            "Bonus at Work", 
            "You received a bonus for your hard work!",
            "Extra cash has been added to your savings.",
            savings_change=1000
        ),
        FinancialEvent(
            "Medical Expense", 
            "You had an unexpected medical expense.",
            "Your savings have been reduced to cover medical bills.",
            savings_change=-800
        ),
        FinancialEvent(
            "Tax Refund", 
            "You received a tax refund!",
            "The refund has been added to your savings.",
            savings_change=600
        ),
        FinancialEvent(
            "Credit Card Fee", 
            "Your credit card company raised their fees.",
            "You've incurred additional debt from fees.",
            debt_change=200
        )
    ]
    
    # Add the Promotion event
    promotion_event = FinancialEvent(
        "Promotion",
        "You received a promotion at work!",
        "Your monthly income has increased by 10%.",
        income_change=0.10  # 10% increase in income
    )
    
    # Adjust probability of promotion based on reputation
    if character.reputation > 75:
        # High reputation increases the chance of a promotion
        financial_events.extend([promotion_event] * 3)  # Add promotion event multiple times
    elif character.reputation > 50:
        # Moderate reputation gives a smaller chance
        financial_events.append(promotion_event)
    
    life_events = [
        LifeEvent(
            "Vacation", 
            "You took a short vacation to relax.",
            "Your stress level has decreased, but it cost you some money.",
            stress_change=-20,
            savings_change=-300
        ),
        LifeEvent(
            "Flu Season", 
            "You caught the seasonal flu and had to rest.",
            "Your health and productivity suffered.",
            health_change=-15,
            stress_change=10
        ),
        LifeEvent(
            "Networking Event", 
            "You attended a valuable networking event.",
            "Your professional reputation has improved.",
            reputation_change=10
        ),
        LifeEvent(
            "Argument at Work", 
            "You had a disagreement with a colleague.",
            "Your stress increased and reputation slightly decreased.",
            stress_change=15,
            reputation_change=-5
        )
    ]
    
    # Choose random event type (60% financial, 40% life)
    if random.random() < 0.6:
        return random.choice(financial_events)
    else:
        return random.choice(life_events)


def get_historical_event(current_date):
    """
    Return a specific historical event if the date matches.
    
    Parameters:
    - current_date: Current game date
    
    Returns:
    - An Event object or None if no historical event on this date
    """
    # Key historical events
    historical_events = {
        datetime.date(2007, 2, 27): FinancialEvent(
            "Stock Market Dip",
            "The Dow Jones dropped 416 points as subprime concerns grow.",
            "Market instability has affected your investments negatively.",
            investment_change=-0.05
        ),
        datetime.date(2007, 8, 9): FinancialEvent(
            "BNP Paribas Freezes Funds",
            "BNP Paribas freezes $2.2 billion in funds, citing subprime problems.",
            "Financial markets are becoming more unstable.",
            investment_change=-0.07
        ),
        datetime.date(2008, 3, 14): FinancialEvent(
            "Bear Stearns Collapse",
            "Bear Stearns collapses and is acquired by JPMorgan Chase.",
            "The financial crisis is deepening, severely impacting investments.",
            investment_change=-0.15,
            stress_change=20
        ),
        datetime.date(2008, 9, 15): FinancialEvent(
            "Lehman Brothers Bankruptcy",
            "Lehman Brothers files for bankruptcy, sending shockwaves through the global financial system.",
            "Market panic has caused severe losses to investments and increased stress.",
            investment_change=-0.25,
            stress_change=30
        ),
        datetime.date(2008, 10, 3): FinancialEvent(
            "Emergency Economic Stabilization Act",
            "Congress passes a $700 billion bailout package for the financial industry.",
            "Government intervention provides some market stability.",
            investment_change=0.05
        ),
        datetime.date(2009, 3, 9): FinancialEvent(
            "Market Bottom",
            "The S&P 500 reaches its lowest point during the crisis.",
            "Market sentiment is beginning to improve from rock bottom.",
            investment_change=0.08
        )
    }
    
    # Check if current date is a historical event date
    for event_date, event in historical_events.items():
        if current_date.year == event_date.year and current_date.month == event_date.month:
            return event
    
    return None