from rest_framework import serializers
from .models import Wallet, Transaction, Asset

class SerialTransaction(serializers.ModelSerializer):
    class Meta:
        model= Transaction
        fields= ["id", "wallet", "transaction_type", "timestamp", "running_balance", "amount"]

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Asset
        fields= ["id", "symbol", "balance"]

class SerialWalet(serializers.ModelSerializer):
    """
    many=true means it is not just an obj but a list
    read_only=field will be included when you send data to the user, prevents users from overwriting sensitive data
    """
    transactions= SerialTransaction(many= True)
    assets= AssetSerializer(many=True, read_only=True, source='user.assets')
    user= serializers.StringRelatedField(read_only= True)
    class Meta:
        model= Wallet
        fields= ["id", "user", "transactions", "balance", "assets"]
        read_only_fields = ['user', "balance"]



