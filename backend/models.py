from django.db import models


class Employee(models.Model):
    employeeID = models.CharField(max_length=9, primary_key=True)
    SSN = models.IntegerField(unique=True)
    salary = models.DecimalField(max_digits=9, decimal_places=2)


class EmpAddress(models.Model):
    employeeID = models.ForeignKey('Employee', on_delete=models.CASCADE())
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('employeeID', 'street', 'city', 'province', 'postal_code')


class EmpName(models.Model):
    employeeID = models.ForeignKey('Employee', on_delete=models.CASCADE())
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)

    class Meta:
        unique_together = ('employeeID', 'fname', 'mname', 'lname')


class Support(Employee):
    customer_rating = models.DecimalField(max_digits=2, decimal_places=1)


class Admin(Employee):
    rules = models.FileField(upload_to='uploads/%Y/%m/%d/')


class MarketMaker(Employee):
    AdminEmployeeID = models.ForeignKey('Employee', on_delete=models.SET_NULL())


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


class ETF(Trade):
    index = models.CharField(max_length=50)


class MutualFund(Trade):
    manager = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=7, decimal_places=4)


class Prediction(models.Model):
    trade = models.ForeignKey('Trade', on_delete=models.PROTECT())
    date = models.DateField(auto_now=True)
    result = models.DecimalField(max_digits=7, decimal_places=4)

    # history #not useful since we can just query the history right?
    # big SQL energy
    class Meta:
        unique_together = ('trade', 'date')


class Client(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    is_banned = models.BooleanField(default=False)

    class Meta:
        unique_together = ('username', 'password')


class Account(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE())
    accountID = models.AutoField()
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    is_valid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('client', 'accoutnID')


class Owns(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE())
    account = models.ForeignKey('Account', on_delete=models.CASCADE())
    trade = models.ForeignKey('Trade', on_delete=models.CASCADE())
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('client', 'account', 'trade')


class Transaction(models.model):
    market_maker = models.ForeignKey('MarketMaker', on_delete=models.PROTECT())
    client = models.ForeignKey('Client', on_delete=models.CASCADE())
    account = models.ForeignKey('Account', on_delete=models.CASCADE())
    trade = models.ForeignKey('Trade', on_delete=models.CASCADE())
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('client', 'account', 'trade', 'market_maker')


class Pool(Transaction):
    fraction = models.DecimalField(max_digits=3, decimal_places=2)


class Review(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE())
    account = models.ForeignKey('Account', on_delete=models.CASCADE())
    support = models.ForeignKey('Support', on_delete=models.PROTECT())

    class Meta:
        unique_together = ('client', 'account', 'support')


class Help(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE())
    support = models.ForeignKey('Support', on_delete=models.PROTECT())
    ticket_no = models.IntegerField()

    class Meta:
        unique_together = ('client', 'support')


class Enforce(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE())
    admin = models.ForeignKey('Admin', on_delete=models.PROTECT())

    class Meta:
        unique_together = ('client', 'admin')


class Manage(models.Model):
    employeeID = models.ForeignKey('self', on_delete=models.CASCADE)
