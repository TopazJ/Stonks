from django.urls import path
from authentication import views
urlpatterns = [
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('status/', views.status),
]
