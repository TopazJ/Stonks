"""Stonks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from backend import views

# Wire up our API using automatic URL routing.
router = routers.DefaultRouter()
"""
router.register(r'm_employee', views.EmployeeViewSet)
router.register(r'm_emp_address', views.EmpAddressViewSet)
router.register(r'm_emp_name', views.EmpNameViewSet)
router.register(r'm_support', views.SupportViewSet)
router.register(r'm_admin', views.AdminViewSet)
router.register(r'm_market_maker', views.MarketMakerViewSet)
router.register(r'm_trade', views.TradeViewSet)
router.register(r'm_etf', views.ETFViewSet)
router.register(r'm_mutual_fund', views.MutualFundViewSet)
router.register(r'm_prediction', views.PredictionViewSet)
router.register(r'm_client', views.ClientViewSet)
router.register(r'm_account', views.AccountViewSet)
router.register(r'm_owns', views.OwnsViewSet)
router.register(r'm_transaction', views.TransactionViewSet)
router.register(r'm_pool', views.PoolViewSet)
router.register(r'm_review', views.ReviewViewSet)
router.register(r'm_help', views.HelpViewSet)
router.register(r'm_enforce', views.EnforceViewSet)
router.register(r'm_manage', views.ManageViewSet)
"""
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('authentication.urls')),
    path('', include('frontend.urls')),
]
