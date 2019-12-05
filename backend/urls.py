from django.urls import path
from . import views
urlpatterns = [
    path('add-money/', views.add_money),
    path('create-account/', views.create_account),
    path('buy-trade/', views.buy_trade),
    path('sell-trade/', views.sell_trade),
    path('complete-transaction/', views.complete_transaction),
    path('buy-pool/', views.buy_pool),
    path('complete-pool/', views.complete_pool),
    path('buy/', views.buy_trade),
    path('sell/', views.sell_trade),
    path('complete-transaction/', views.complete_transaction),
    path('buy-pool/', views.buy_pool),
    path('complete-pool/', views.complete_pool),
    path('daily-stock/', views.daily_stock),
    path('owns/', views.owns),
    path('get-accounts/', views.get_accounts)
]
