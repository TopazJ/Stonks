from django.urls import path
from backend import views
urlpatterns = [
    path('buy/', views.buy_trade),
    path('sell/', views.sell_trade),
    path('complete-transaction/', views.complete_transaction),
    path('buy-pool/', views.buy_pool),
    path('complete-pool/', views.complete_pool),
    path('daily-stock/', views.daily_stock),
    path('add-money/', views.add_money),
    path('create-account/', views.create_account)
    path('owns/', views.owns)
]
