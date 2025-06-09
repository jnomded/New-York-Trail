"""
Character classes for Credit Trail game.
"""

class Character:
    """Base character class with financial and life attributes."""
    
    def __init__(self, name, savings=0, debt=0, income=0, risk_rating=5.0):
        """
        Initialize a character with financial and personal attributes.
        
        Parameters:
        - name: Character name
        - savings: Starting savings amount in dollars
        - debt: Starting debt amount in dollars
        - income: Annual income in dollars
        - risk_rating: Risk rating from 1.0 (low risk) to 10.0 (high risk)
        """
        self.name = name
        self.savings = savings
        self.debt = debt
        self.income = income
        self.risk_rating = risk_rating
        
        # Financial attributes
        self.investments = 0
        self.credit_score = 700  # Starting credit score (average)
        self.monthly_expenses = income / 24  # Assume monthly expenses are 1/2 of monthly income
        
        # Life attributes
        self.stress = 50  # Scale 0-100
        self.health = 80  # Scale 0-100
        self.reputation = 70  # Scale 0-100
        
    def get_monthly_income(self):
        """Calculate monthly income from annual income."""
        return self.income / 12
    
    def get_net_worth(self):
        """Calculate net worth (savings + investments - debt)."""
        return self.savings + self.investments - self.debt
    
    def work(self):
        """Perform work action to earn income and increase stress."""
        earned = self.get_monthly_income()
        self.savings += earned
        self.stress += 10
        if self.stress > 100:
            self.stress = 100
            self.health -= 25
        return earned
    
    def relax(self):
        """Perform relax action to reduce stress and improve health."""
        stress_reduction = min(25, self.stress)
        self.stress -= stress_reduction
        self.health += 5
        if self.health > 100:
            self.health = 100
        return stress_reduction
    
    def pay_debt(self, amount):
        """Pay off some debt."""
        payment = min(amount, self.debt)
        if payment > self.savings:
            payment = self.savings
        
        self.savings -= payment
        self.debt -= payment
        
        # Improve credit score when paying debt
        self.credit_score += payment / 1000
        if self.credit_score > 850:
            self.credit_score = 850
            
        return payment
    
    def invest(self, amount):
        """Invest money from savings."""
        if amount > self.savings:
            amount = self.savings
        
        self.savings -= amount
        self.investments += amount
        return amount


class Hudson(Character):
    """Hudson character with pre-defined starting attributes."""
    
    def __init__(self):
        """Initialize Hudson with his specific attributes."""
        super().__init__(
            name="Hudson",
            savings=6500,
            debt=0,
            income=62000,
            risk_rating=5.5
        )
        # Custom attributes for Hudson
        self.credit_score = 720
        self.stress = 45


class Jane(Character):
    """Jane character with pre-defined starting attributes."""
    
    def __init__(self):
        """Initialize Jane with her specific attributes."""
        super().__init__(
            name="Jane",
            savings=0,
            debt=8000,
            income=80000,
            risk_rating=2.0
        )
        # Custom attributes for Jane
        self.credit_score = 680
        self.stress = 60
        self.savings = 2000  # Give her some initial savings to work with
