from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from .models import Record, Sale, Route, Product, Debt
from .forms import RecordForm, SaleForm, SignUpForm, DebtForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum

def home(request):
    records = Record.objects.all()
    #Check if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
            # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})

def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')
 
def customer_record(request):
    if request.user.is_authenticated:
        customer_record = Record.objects.all().order_by('-created_at')
        return render(request, 'customer_record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You have to be logged in!")

def sale_record(request):
    if request.user.is_authenticated:
        sale_record = Sale.objects.all().order_by('-date')
        context = {
        'sale_record':sale_record,
        }
        return render(request, 'sale_record.html', context)
    else:
        messages.success(request, "You have to be logged in!")


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
        
    return render(request, 'register.html', {'form':form})

def customer(request, customer):
    customer = customer
    if request.user.is_authenticated:
        customer_r = Record.objects.filter(phone_no = customer)
        sales = Sale.objects.filter(client = customer).order_by('-date')
        customer_rec = Record.objects.get(phone_no = customer)
        tot_paid = Sale.objects.filter(client = customer).aggregate(total=Sum('paid'))
        total = tot_paid['total']
        tot_debt = 0
        for i in sales:
            tot_debt += i.debt

        debt_payments = Debt.objects.filter(client=customer_rec)
        for payment in debt_payments:
            tot_debt -= payment.paid
    

        total += debt_payments.aggregate(total=Sum('paid'))['total']

        context = {
            'customer_rec': customer_rec,
            'sales': sales,
            #total paid
            'total' : total,
            'tot_debt' : tot_debt,
            'customer_r' : customer_r,
        }
        return render(request, 'customer.html', context)
    else:
        messages.success(request, "You have to be logged in!")


def delete_record(request, customer):
    customer = customer

    if request.user.is_authenticated:
        delete_c = Record.objects.filter(phone_no = customer)
        delete_s = Sale.objects.filter(client = customer)
        delete_c.delete()
        delete_s.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('customer_record')
    else:
        messages.success(request, "You Must Be Logged In To Delete...")
        return redirect('home')

def update(request, customer):
    #customer = customer
    if request.user.is_authenticated:
        current_record = Record.objects.get(phone_no = customer)
        form = RecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated...")
            return redirect('customer_record')
        return render(request, 'update.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In To Update...")
        return redirect('home')
    
@login_required
def cust_entry(request):
    form = RecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user
                record.save()
                cust_entry = form.save()
                messages.success(request, "Record Added...")
                return redirect('customer_record')
        return render(request, 'cust_entry.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
    

@login_required
def sale_entry(request):
    form = SaleForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                sale = form.save(commit=False)
                sale.served_by = request.user
                sale.save()
                sale_entry = form.save()
                messages.success(request, "Record Added...")
                return redirect('sale_record')
        return render(request, 'sale.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

@login_required
def debt(request, customer):
    customer = customer
    if request.user.is_authenticated:
        debt_form = DebtForm(request.POST or None)
        customer_r = Record.objects.filter(phone_no = customer)
        sales = Sale.objects.filter(client = customer).order_by('-date')
        customer_rec = Record.objects.get(phone_no = customer)
        debt = Debt.objects.filter(client = customer)
                
        if request.method == "POST":
            if debt_form.is_valid():
                debt = debt_form.save(commit=False)
                debt.client = customer_rec
                debt_form.save()
                messages.success(request, "Payment Recorded")
                return redirect('customer', customer=customer_rec.phone_no)

        tot_debt = 0
        for i in sales:
            tot_debt += i.debt

        for j in debt:
            tot_debt = tot_debt - j.paid

        context = {
            'customer_rec': customer_rec,
            'sales': sales,
            #total paid
            'tot_debt' : tot_debt,
            'customer_r' : customer_r,
            'debt_form' : debt_form,
        }
        return render(request, 'pay_debt.html', context)
    else:
        messages.success(request, "You have to be logged in!")
