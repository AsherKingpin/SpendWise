from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from tracker.models import Expense, Category


class Command(BaseCommand):
    help = "Seed dummy expenses for testing insights"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user = User.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR("No user found"))
            return

        today = timezone.now().date()

        # ✅ User-specific categories
        food, _ = Category.objects.get_or_create(user=user, name="Food")
        outing, _ = Category.objects.get_or_create(user=user, name="Outing")

        categories = [food, outing]

        # Optional: clear old data
        Expense.objects.filter(user=user).delete()

        expenses = []

        # 🔹 Previous week (low spending)
        for i in range(14, 7, -1):
            expenses.append(
                Expense(
                    user=user,
                    amount=random.randint(100, 300),
                    category=random.choice(categories),
                    date=today - timedelta(days=i),
                )
            )

        # 🔹 Last week (high spending → triggers increase + dominance)
        for i in range(7, 0, -1):
            expenses.append(
                Expense(
                    user=user,
                    amount=random.randint(500, 1000),
                    category=food,
                    date=today - timedelta(days=i),
                )
            )

        # 🔹 Spike
        expenses.append(
            Expense(
                user=user,
                amount=2500,
                category=outing,
                date=today - timedelta(days=2),
            )
        )

        Expense.objects.bulk_create(expenses)

        self.stdout.write(self.style.SUCCESS("Dummy expenses created successfully!"))