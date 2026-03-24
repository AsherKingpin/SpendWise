from collections import defaultdict
from datetime import timedelta
from django.utils import timezone

def category_dominance(expenses):
    category_total = defaultdict(float)
    total_spend = 0

    for expense in expenses:
        category_total[expense.category] += float(expense.amount)
        total_spend += float(expense.amount)

    if total_spend == 0:
        return None
    
    top_category = max(category_total, key = category_total.get)
    top_amount = category_total[top_category]
    percentage = (top_amount/total_spend) * 100

    return {
        "type": "category_dominance",
        "category": top_category,
        "amount": round(top_amount,2),
        "percentage":round(percentage,1),
        "message":f"{top_category} accounts for {percentage:.1f}% of your total spend"
    }

def weekly_comparison(expenses):
    today = timezone.now().date()
    last_week_start = today - timedelta(7)
    prev_week_start = today - timedelta(14)

    last_week_total = 0
    prev_week_total = 0

    for expense in expenses:
        if last_week_start <= expense.date < today:
            last_week_total += expense.amount
        elif prev_week_start <= expense.date < last_week_start:
            prev_week_total += expense.amount
    
    if prev_week_total == 0:
        return None
    
    change = ((last_week_total - prev_week_total)/prev_week_total) * 100
    direction = "increased" if change > 0 else "decreased"
    return {
        "type":"weekly_comparison",
        "change": change,
        "direction": direction,
        "message":f"Your spending {direction} by {change:.1f}% from the previous week"
    }

def categorywise_spend(expenses):
    summary = defaultdict(float)
    for expense in expenses:
        summary[expense.category] += float(expense.amount)
    
    return {
    "type": "category_summary",
    "data": dict(summary),
    "message": "\n".join(
        [f"You spent {total} INR on {cat}" for cat, total in summary.items()]
    )
}
