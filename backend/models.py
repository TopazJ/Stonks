import re
import uuid

from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employeeID = models.CharField(max_length=9, primary_key=True)
    SSN = models.IntegerField(unique=True)
    salary = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        permissions = [
            ("Employee", "Can do employee things")
        ]

    def __str__(self):
        return '%s' % self.employeeID


class EmpAddress(models.Model):
    employee = models.OneToOneField('Employee', on_delete=models.CASCADE)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('employee', 'street', 'city', 'province', 'postal_code')

    def __str__(self):
        return '%s %s %s %s' % (self.street, self.city, self.province, self.postal_code)


class EmpName(models.Model):
    employee = models.OneToOneField('Employee', on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)

    class Meta:
        unique_together = ('employee', 'fname', 'mname', 'lname')

    def __str__(self):
        return '%s %s %s' % (self.fname, self.mname, self.lname)


class Support(Employee):
    customer_rating = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        permissions = [
            ('Support', 'Can support them clients')
        ]


class Admin(Employee):
    rules = models.FileField(upload_to='uploads/%Y/%m/%d/')


class MarketMaker(Employee):
    AdminEmployeeID = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, related_name='AEmpID')

    class Meta:
        permissions = [
            ('MarketMaker', 'Can do market maker things')
        ]


class Trade(models.Model):
    exchange = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    company_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    INDIVIDUAL = 'IND'
    ETF = 'ETF'
    MUTUAL_FUND = 'MF'
    TRADE_TYPE_CHOICES = [
        (INDIVIDUAL, 'Individual'),
        (ETF, 'etf'),
        (MUTUAL_FUND, 'mutual fund'),
    ]
    trade_type = models.CharField(
        max_length=3,
        choices=TRADE_TYPE_CHOICES,
        default=INDIVIDUAL,
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    LOW_RISK = 'LOW'
    MED_RISK = 'MED'
    HIGH_RISK = 'HIG'
    RISK_CHOICES = [
        (LOW_RISK, 'Low risk'),
        (MED_RISK, 'Medium risk'),
        (HIGH_RISK, 'High risk'),
    ]
    risk = models.CharField(
        max_length=3,
        choices=RISK_CHOICES,
        default=HIGH_RISK,
    )

    class Meta:
        unique_together = ('exchange', 'symbol')

    def __str__(self):
        return '%s %s' % (self.exchange, self.symbol)


class ETF(Trade):
    index = models.CharField(max_length=50)


class MutualFund(Trade):
    manager = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=7, decimal_places=4)


class Prediction(models.Model):
    trade = models.ForeignKey('Trade', on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)
    result = models.DecimalField(max_digits=7, decimal_places=4)

    # history #not useful since we can just query the history right?
    # big SQL energy
    class Meta:
        unique_together = ('trade', 'date')

    def __str__(self):
        return str(self.trade) + ' %s' % self.result


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("Client", "Can do client things")
        ]

    def __str__(self):
        return str(self.user)


class Account(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    account_no = models.IntegerField()
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_valid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('client', 'account_no')

    def __str__(self):
        return str(self.client) + ' %s' % self.balance


class Owns(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    trade = models.ForeignKey('Trade', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('client', 'account', 'trade')


class Transaction(models.Model):
    market_maker = models.ForeignKey('MarketMaker', on_delete=models.PROTECT)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    trade = models.ForeignKey('Trade', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField()
    BUY = 'BUY'
    SELL = 'SELL'
    TYPE_CHOICES = [
        (BUY, 'buy'),
        (SELL, 'sell'),
    ]
    type = models.CharField(
        max_length=4,
        choices=TYPE_CHOICES,
        default=BUY,
    )
    complete = models.BooleanField(default=False)

    class Meta:
        unique_together = ('date', 'client', 'trade')

    def __str__(self):
        return str(self.account) + str(self.trade) + ' %s %s %s' % (self.type, self.quantity, self.date)


class Pool(Transaction):
    fraction = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return str(super(self)) + ' %s' % self.fraction


class Review(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    support = models.ForeignKey('Support', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('client', 'account', 'support')

    def __str__(self):
        return str(self.client) + str(self.support)


class Help(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    support = models.ForeignKey('Support', on_delete=models.PROTECT)
    ticket_no = models.UUIDField(primary_key=True, default=uuid.uuid4)

    def __str__(self):
        return str(self.client) + str(self.support) + ' %s' % self.ticket_no


class Enforce(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    admin = models.ForeignKey('Admin', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('client', 'admin')

    def __str__(self):
        return str(self.client) + str(self.admin)


# TODO: not sure this works
class Manage(models.Model):
    employee = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.employee)
