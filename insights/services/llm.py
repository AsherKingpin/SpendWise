import requests
import os
from dotenv import load_dotenv


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def format_expenses(expenses):
    """
    Convert queryset into readable text for LLM
    """
    lines = []

    for exp in expenses:
        lines.append(
            f"{exp.date} | {exp.category.name} | ₹{exp.amount}"
        )

    return "\n".join(lines)


def generate_ai_response(question, insights, expenses):
    insights_text = "\n".join([
        f"- {i['type']}: {i['message']}"
        for i in insights
    ])
    expenses = expenses.order_by('-date')[:15]
    expenses_text = format_expenses(expenses)

    prompt = f"""
You are a personal finance assistant.

User financial insights:
{insights_text}

Detailed expenses:
{expenses_text}

User question:
{question}

Instructions:
- Answer using the provided data only
- Be specific and data-driven
- Mention exact categories and amounts when relevant
- If a trend exists, explain it
- If overspending is detected, warn clearly
- Give 1 actionable suggestion

Answer:
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a smart financial assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]

    return "Error generating response"