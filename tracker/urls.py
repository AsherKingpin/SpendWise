from django.urls import path
from .views import add_expense, dashboard

urlpatterns = [
    path('add/', add_expense, name="add_expense"),
    path('', dashboard, name = 'dashboard')
]