from backend.models import *
from rest_framework import serializers


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ['employeeID', 'SSN', 'salary']


class EmpAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmpAddress
        fields = ['employee', 'street', 'city', 'province', 'postal_code']


class EmpNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmpAddress
        fields = ['employeeI', 'fname', 'mname', 'lname']


class SupportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Support
        fields = ['employeeID', 'SSN', 'salary', 'customer_rating']


class AdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Admin
        fields = ['employeeID', 'SSN', 'salary', 'rules']


class MarketMakerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MarketMaker
        fields = ['employeeID', 'SSN', 'salary', 'AdminEmployeeID']


class TradeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trade
        fields = [
            'exchange', 'symbol',
            'company_name', 'price',
            'trade_type', 'rating',
            'risk']


class ETFSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ETF
        fields = [
            'exchange', 'symbol',
            'company_name', 'price',
            'trade_type', 'rating',
            'risk', 'index']


class MutualFundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MutualFund
        fields = [
            'exchange', 'symbol',
            'company_name', 'price',
            'trade_type', 'rating',
            'risk', 'manager', 'fee']


class PredictionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prediction
        fields = [
            'trade', 'date',
            'result']


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = [
            'username', 'password',
            'is_banned']


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = [
            'client', 'accountID',
            'balance', 'is_valid']


class OwnsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owns
        fields = [
            'client', 'account',
            'trade', 'quantity']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owns
        fields = [
            'client', 'account',
            'trade', 'quantity', 'market_maker']


class PoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owns
        fields = [
            'client', 'account',
            'trade', 'quantity', 'market_maker', 'fraction']


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = [
            'client', 'account',
            'support']


class HelpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Help
        fields = [
            'client', 'support',
            'ticket_no']


class EnforceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Enforce
        fields = [
            'client', 'admin']


class ManageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manage
        fields = [
            'employee']
