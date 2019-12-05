from django.urls import path
from backend import views
urlpatterns = [
    path('buy/', views.buy_trade),
    path('sell/', views.sell_trade),
    path('complete_transaction/', views.complete_transaction),
    path('buy_pool/', views.buy_pool),
    path('complete_pool/', views.complete_pool),
    path('daily_stock/', views.daily_stock),
]
