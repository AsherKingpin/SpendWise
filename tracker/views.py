from django.shortcuts import render, redirect
from django.db.models import Sum
from .forms import ExpenseForm
from .models import Expense
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('/')
    else:
        form = ExpenseForm()
    
    return render(request, 'tracker/add_expense.html', {'form':form})

@login_required
def update_expense(request, id):
    expense = Expense.objects.get(user=request.user, id = id)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance = expense)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ExpenseForm(instance = expense)
    
    return render(request, 'tracker/add_expense.html', {"form":form})


@login_required
def delete_expense(request, id):
    expense = Expense.objects.get(user = request.user, id = id)
    expense.delete()
    return redirect('/')


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user = request.user).order_by('-date')

    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    category_summary = (
        expenses.values('category__name')
        .annotate(total = Sum('amount'))
        .order_by('-total')
    )

    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'category_summary': category_summary
    }

    return render(request, 'tracker/dashboard.html', context)

