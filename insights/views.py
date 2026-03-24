from django.shortcuts import render
from insights.services.engine import generate_insights
from tracker.models import Expense
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from insights.services.llm import generate_ai_response
from django.http import JsonResponse
import json

# Create your views here.
@login_required
def insights_dashboard(request):
    expenses = Expense.objects.filter(user = request.user)
    insights = generate_insights(expenses)
    return render(request , "insights/insights_dashboard.html", {"insights": insights})

@csrf_exempt
@login_required
def ai_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("question", "")

        expenses = Expense.objects.filter(user=request.user).select_related("category")
        insights = generate_insights(expenses)

        answer = generate_ai_response(question, insights, expenses)
        return JsonResponse({"answer": answer})  # this is 200 by default

    return JsonResponse({"error": "Invalid method"}, status=405)