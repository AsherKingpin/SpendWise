from .rules import category_dominance, weekly_comparison, categorywise_spend

def generate_insights(expenses):
    insights = []
    rules = [category_dominance, weekly_comparison, categorywise_spend]

    for rule in rules:
        result = rule(expenses)

        if result:
            insights.append(result)

    return insights