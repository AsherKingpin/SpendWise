from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name
    

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # add date and time only once (at creation).

    def __str__(self):
        return f"{self.category.name} - {self.amount}"