from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.user.username}'s Wallet"
    

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    ]
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        default='DEPOSIT',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

    running_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

class Asset(models.Model):
    COIN_CHOICES = [
        ("BITCOIN", "BTC"),
        ("ETHEREUM", "ETH"), 
        ("SOLANA", "SOL"),
        ("BINANCECOIN", "BNB"), 
        ("RIPPLE", "XRP"), 
        ("CARDANO", "ADA"),
    ]
    symbol= models.CharField(
        max_length=50,
        choices=COIN_CHOICES,
        default="bitcoin"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assets'
    )

    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0.00)

    def __str__(self):
        # Fixed: your model uses 'symbol', not 'coin_id'
        return f"{self.user.username} - {self.symbol}"
