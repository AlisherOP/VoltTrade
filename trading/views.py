from django.shortcuts import render
from django.db import transaction
from .models import Wallet, Transaction, Asset
from django.contrib.auth.models import User

from rest_framework import viewsets
from .serializers import SerialWalet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
import requests
# Create your views here.


def get_crypto_price(coin_id='bitcoin', currency='usd'):
    """
    coin_id: Use 'bitcoin', 'ethereum', 'solana', etc.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': coin_id,
        'vs_currencies': currency
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for errors
        data = response.json()
        return data[coin_id][currency]
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

# Usage
price = get_crypto_price('ethereum')
print(f"The price of ETH is ${price}")



class WalletViewSet(viewsets.ModelViewSet):
    queryset= Wallet.objects.all()
    serializer_class= SerialWalet
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def trasfer(self, request):
        # checking the ammount in wallet
        try:
            amount = Decimal(request.data.get('amount'))
            if amount <=0:
                raise ValidationError("Amount must be positive")
        except (TypeError, ValueError):
            raise ValidationError("Invalid amount format")

# from which person to which
        receiver_name= request.data.get('receiver')
        sender_name = request.user
        with transaction.atomic():
            try:
                receiver_user = User.objects.get(username=receiver_name)
            except User.DoesNotExist:
                raise ValidationError("Receiver not found")
            # dont send to yourself
            if receiver_user == sender_name:
                raise ValidationError("Cannot send the money to yourself")

            # creating order to prevent deadlock
            wallet_ids = sorted(
                [sender_name.wallet.id, receiver_user.wallet.id])

            locked_wallets= {
                w.id: w for w in Wallet.objects.select_for_update().filter(id__in= wallet_ids)
            }

            sender_wallet= locked_wallets[sender_name.wallet.id]
            receiver_wallet= locked_wallets[receiver_user.wallet.id]
            # dont send more then you have
            if sender_wallet.balance < amount:
                raise ValidationError("Insufficient balance")

            # equivalent exchange
            sender_wallet.balance -= amount
            receiver_wallet.balance +=  amount

            sender_wallet.save()
            receiver_wallet.save()
            # noting for both sides
            Transaction.objects.create(
                wallet=sender_wallet,
                transaction_type='TRANSFER',
                running_balance=sender_wallet.balance,
                amount= -amount,
            )
            Transaction.objects.create(
                wallet=receiver_wallet,
                transaction_type='TRANSFER',
                running_balance=receiver_wallet.balance,
                amount=amount,
            )
        return Response({"status": "Transfer successful",  "new_balance": sender_wallet.balance})
    

    @action(detail=False, methods=['post'])
    def buy_coin(self, request):
        coin_id = request.data.get('coin_id', 'bitcoin')

        try:
            usd_to_spend = Decimal(request.data.get('amount_usd','0'))
        except (TypeError, ValueError):
            raise ValidationError("Please provide a valid number.")

        # 1. Validation (Is usd_to_spend > 0?)
        if usd_to_spend <=0:
            raise ValidationError("Amount must be positive")


        # 2. Get Price (Outside the lock!)
        price = get_crypto_price(coin_id)
        if not price:
            return Response({"error": "Price feed unavailable"}, status=503)

        price_dec = Decimal(str(price))

        with transaction.atomic():
            # Lock Wallet and check balance
            wallet =  Wallet.objects.select_for_update().get(user=request.user)
            if wallet.balance < usd_to_spend:
                raise ValidationError("Insufficient funds")
            # Calculate coin_amount (usd_to_spend / price_dec)
            coin_amount = usd_to_spend / price_dec
            # Subtract USD and save
            wallet.balance -= usd_to_spend
            wallet.save()
            # Get_or_create Asset(if there is one get it else.. ), 
            asset, created = Asset.objects.get_or_create(
                user=request.user,
                symbol=coin_id.upper()  # Use the coin_id from the request, not just "BTC"!
            )
            asset = Asset.objects.select_for_update().get(id=asset.id)
            asset.balance+=coin_amount
            asset.save()

            # Create Transaction log(ofcause)
            Transaction.objects.create(
                wallet=wallet,
                transaction_type='WITHDRAWAL',
                running_balance=wallet.balance,
                amount=-usd_to_spend,
            )
        return Response({"status": "Success", "bought": coin_amount})
    
    @action(detail=False, methods=['post'])
    def sell_coin(self, request):
        coin_id = request.data.get('coin_id', 'bitcoin')
        try:
            coin_to_spend = Decimal(request.data.get('amount_crypto', '0'))
        except (TypeError, ValueError):
            raise ValidationError("Please provide a valid number.")
        
        if coin_to_spend <= 0:
            raise ValidationError("Amount must be positive")
        price = get_crypto_price(coin_id)

        if not price:
            return Response({"error": "Price feed unavailable"}, status=503)
        price_dec = Decimal(str(price))

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=request.user)

            asset = Asset.objects.select_for_update().filter(user=request.user,
                                                            symbol=coin_id.upper()
                                                            ).first()
            if not asset or asset.balance < coin_to_spend:
                raise ValidationError(
                    f"You don't have enough {coin_id} to sell.")
            dollar_amount = coin_to_spend*price_dec
            

            wallet.balance += dollar_amount
            wallet.save()

            
            asset = Asset.objects.select_for_update().get(id=asset.id)
            asset.balance -= coin_to_spend
            asset.save()

            Transaction.objects.create(
                wallet=wallet,
                transaction_type='DEPOSIT',
                running_balance=wallet.balance,
                amount=+dollar_amount,
            )
        return Response({
            "status": "Success",
            "sold_crypto": coin_to_spend,
            "received_usd": dollar_amount
        })












# def transfer_money(sender_username, receiver_username, amount):
#     with transaction.atomic():
#         try:
#             user_obj = User.objects.get(username=sender_username)
#             user_obj2 = User.objects.get(username=receiver_username)
#         except User.DoesNotExist:
#             raise ValueError("User not found")
        
#         wallet_ids = sorted([user_obj.wallet.id, user_obj2.wallet.id])

#         for w_id in wallet_ids:
#             Wallet.objects.select_for_update().get(id=w_id)

#         sender= user_obj.wallet
#         receiver = user_obj2.wallet

        
#         if sender.balance>=amount:
#             sender.balance -=amount
#             sender.save()
#         else:
#             raise ValueError("Insufficiant sum")

#         receiver.balance +=amount
#         receiver.save()

#         Transaction.objects.create(
#             wallet= sender,
#             transaction_type='TRANSFER',
#             running_balance=sender.balance,
#             amount=amount,
#             )
#         Transaction.objects.create(
#             wallet= receiver,
#             transaction_type= 'TRANSFER',
#             running_balance=receiver.balance,
#             amount=amount,
#             )
#     return True




