from django.urls import path
from .views import add_expense, dashboard, update_expense, delete_expense

urlpatterns = [
    path('add/', add_expense, name="add_expense"),
    path('', dashboard, name = 'dashboard'),
    path('delete/<int:id>/', delete_expense, name = 'delete_expense'),
    path('update/<int:id>/', update_expense, name = 'update_expense')
]