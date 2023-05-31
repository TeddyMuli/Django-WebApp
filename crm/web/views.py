from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Record, Sale, Route, Product, Debt, Expense, Message
from .forms import RecordForm, SaleForm, SignUpForm, DebtForm, ExpenseForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
import datetime, calendar, requests, json
from datetime import date, timedelta
from django.db.models import Q

def home(request):
    records = Record.objects.all()
    #Check if logging in
    return render(request, 'home.html', {})

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

def search_customer(request):
    query = request.GET.get('query')
    customer_record = Record.objects.filter(Q(f_name__icontains=query) | Q(l_name__icontains=query) | Q(phone_no__icontains=query)).order_by('-created_at')
    return render(request, 'customer_record.html', {'customer_record': customer_record})


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

        payment_total = debt_payments.aggregate(total=Sum('paid'))['total']
        if payment_total is not None:
            total += payment_total

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
        user_r = None
        if request.method == "POST":
            if debt_form.is_valid():
                debt = debt_form.save(commit=False)
                debt.client = customer_rec
                user_r = debt_form.save(commit=False)
                user_r.user = request.user
                user_r.save()
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
            'user_r':user_r,

        }
        return render(request, 'pay_debt.html', context)
    else:
        messages.success(request, "You have to be logged in!")

@login_required
def debt_record(request):
    if request.user.is_authenticated:
        debt_record = Debt.objects.all().order_by('-date')
        context = {
        'debt_record':debt_record,
        }
        return render(request, 'debt_record.html', context)
    else:
        messages.success(request, "You have to be logged in!")

@login_required
def financials(request):
    time_frame = request.GET.get('time_frame', 'month')
# Set default values for year, quarter, and month
    year = date.today().year
    quarter = (date.today().month - 1) // 3 + 1
    month = date.today().month

    if time_frame == 'quarter':
        quarter = int(request.GET.get('quarter', quarter))
    elif time_frame == 'month':
        month = int(request.GET.get('month', month))
    else:
        year = int(request.GET.get('year', year))

    start_date, end_date = get_date_range(time_frame, year, quarter, month)

    sales_amount = Sale.objects.filter(date__range=(start_date, end_date)).aggregate(total=Sum('paid'))['total']
    sales_amount = sales_amount or 0

    debt_paid = Debt.objects.filter(date__range=(start_date, end_date)).aggregate(total=Sum('paid'))['total']
    debt_paid = debt_paid or 0

    revenue = sales_amount + debt_paid

    expense_total = Expense.objects.filter(date__range=(start_date, end_date)).aggregate(total=Sum('amount'))['total']
    expense_total = expense_total or 0

    profit = revenue - expense_total

# Prepare data for the chart
    if time_frame == 'year':
        labels = [date(year, month_num, 1).strftime("%b") for month_num in range(1, 13)]
        profit_data = [calculate_monthly_profit(year, month_num) for month_num in range(1, 13)]
    elif time_frame == 'quarter':
        labels = ['Q{}'.format(quarter_num) for quarter_num in range(1, 5)]
        profit_data = [calculate_quarterly_profit(year, quarter_num) for quarter_num in range(1, 5)]
    elif time_frame == 'month':
        num_weeks = (end_date - start_date).days // 7 + 1
        labels = ['Week {}'.format(week_num) for week_num in range(1, num_weeks + 1)]
        profit_data = [calculate_weekly_profit(start_date + timedelta(weeks=week_num-1)) for week_num in range(1, num_weeks + 1)]


    return render(request, 'financials.html', {
        'time_frame': time_frame,
        'sales_amount': sales_amount,
        'debt_paid': debt_paid,
        'revenue':revenue,
        'expense_total':expense_total,
        'profit':profit,
        'year':year,
        'quarter':quarter,
        'month':month,
        'profit_labels': json.dumps(labels),
        'profit_data': json.dumps(profit_data),
        })

def get_date_range(time_frame, year, quarter, month):
    if time_frame == 'quarter':
        start_month = (quarter - 1) * 3 + 1
        end_month = start_month + 2
        start_date = date(year, start_month, 1)
        end_date = date(year, end_month, calendar.monthrange(year, end_month)[1])
    elif time_frame == 'month':
        start_date = date(year, month, 1)
        end_date = date(year, month, calendar.monthrange(year, month)[1])
    else:
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
    return start_date, end_date
def expense(request):
    form = ExpenseForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                user_r = form.save(commit=False)
                user_r.user = request.user
                user_r.save()
                form.save()
                messages.success(request, "Record Added...")
                return redirect('expense')
        return render(request, 'expense.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
    
def expense_record(request):
    if request.user.is_authenticated:
        expenses = Expense.objects.all().order_by('-date')
        return render(request, 'expense_record.html', {'expenses':expenses})
    else:
        messages.success(request, "You Must Be Logged In!")
        return redirect('home')

def calculate_monthly_profit(year, month):
    start_date, end_date = get_date_range('month', year, None, month)
    sales_amount = Sale.objects.filter(date__range=(start_date, end_date)).aggregate(total=Sum('paid'))['total']
    sales_amount = sales_amount or 0

    debt_paid = Debt.objects.filter(date__range=(start_date, end_date)).aggregate(total=Sum('paid'))['total']
    debt_paid = debt_paid or 0

    revenue = sales_amount + debt_paid

    expense_total = Expense.objects.filter(date__range=(start_date, end_date)).aggregate(total=Sum('amount'))['total']
    expense_total = expense_total or 0

    profit = revenue - expense_total

    return profit


def calculate_quarterly_profit(year, quarter):
    start_date, end_date = get_date_range('quarter', year, quarter, None)
    sales_amount = Sale.objects.filter(date__range=(start_date, end_date)).aggregate(total=Sum('paid'))['total']
    sales_amount = sales_amount or 0

    debt_paid = Debt.objects.filter(date__range=(start_date, end_date)).aggregate(total=Sum('paid'))['total']
    debt_paid = debt_paid or 0

    revenue = sales_amount + debt_paid

    expense_total = Expense.objects.filter(date__range=(start_date, end_date)).aggregate(total=Sum('amount'))['total']
    expense_total = expense_total or 0

    profit = revenue - expense_total

    return profit


def calculate_weekly_profit(week_start_date):
    week_end_date = week_start_date + timedelta(days=6)
    sales_amount = Sale.objects.filter(date__range=(week_start_date, week_end_date)).aggregate(total=Sum('paid'))['total']
    sales_amount = sales_amount or 0

    debt_paid = Debt.objects.filter(date__range=(week_start_date, week_end_date)).aggregate(total=Sum('paid'))['total']
    debt_paid = debt_paid or 0

    revenue = sales_amount + debt_paid

    expense_total = Expense.objects.filter(date__range=(week_start_date, week_end_date)).aggregate(total=Sum('amount'))['total']
    expense_total = expense_total or 0

    profit = revenue - expense_total

    return profit


def login_n(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                messages.success(request, "You have been logged in!")
                return redirect('home')
        else:
            messages.error(request, "There was an error logging in. Please try again.")
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'success': False})
            else:
                return redirect('home')
    else:
        return render(request, 'login.html', {})


#Authenticate sms
def authenticate_sms_api():
    url = "https://sms.textsms.co.ke/auth/login"
    headers = {"Content-Type": "application/json"}
    payload = {
        "secret": "u4wwe4",
        "username": "tedmuli",
        "pass_type": "plain"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # Handle the authentication response as needed
    if response.status_code == 200:
        send_bulk_sms()  # Call the function to send bulk SMS


#Send bulk sms
def send_bulk_sms(request):
    form = MessageForm(request.POST or None)
    if request.method == 'POST':
        phone_numbers = Record.objects.values_list('phone_no', flat=True)
        # Create a list to store SMS objects
        sms_list = []
        if form.is_valid():
        # Iterate over phone numbers
            for phone_number in phone_numbers:
                sms_object = {
                    "partnerID": "7600",
                    "apikey": "855c1e3f795bc89683bea4c4b7a0aac6",
                    "pass_type": "plain",
                    "clientsmsid": 1234,
                    "mobile": phone_number,
                    "message": form.cleaned_data['message'],
                    "shortcode": "TextSMS"
                }
                sms_list.append(sms_object)
                # Create the payload for sending bulk SMS
            payload = {
                "count": len(sms_list),
                "smslist": sms_list
            }
            url = "https://sms.textsms.co.ke/api/services/sendbulk/"
            headers = {"Content-Type": "application/json"}

            response = requests.post(url, headers=headers, data=json.dumps(payload))
            # Handle the bulk SMS response as needed
            if response.status_code == 200:
            # Save the message to the database
                form.save()
                messages.success(request, "Message sent successfully!.")
                return redirect('send_bulk_sms')
            else:
                messages.success(request,"Failed to send bulk SMS.")
    return render(request, 'message.html', {'form':form})
