from decimal import Context
from django import http
from django.db.models.aggregates import Count
from django.db.models.fields import NullBooleanField
from django.http import request
from .models import *
from django.shortcuts import redirect, render
from .forms import *
from django.db.models.functions import Lower
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.db.models import Sum,F
from datetime import date
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.views.generic.list import ListView
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
def loginview(request):
    return render(request,"login.html")

def loginuser(request):
   # user=User.objects.create_user('Rehan','rehan123').save()
    username=request.POST['username']
    password=request.POST['password']
   
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request,user)
        return redirect("indexview")
    else:
       
        messages.add_message(request, messages.INFO, 'Invalid Login. Username or password incorrect')
        return redirect(request.META['HTTP_REFERER'])

def indexview(request):
    order = OrderModel.objects.filter(order_date=date.today()).count()
    cust=CustomerModel.objects.count()
    total_orders=OrderModel.objects.count()
    params ={'order':order,'cust':cust,'total_orders':total_orders}
    return render(request,"index.html",params)

def successview(request):
    return render(request,"success.html")

def customersview(request):
    customers= CustomerModel.objects.all().order_by(Lower('fname'))
    context ={'customers':customers}
    return render(request,"customers.html" ,context)

def addcustomerview(request):
    form = Customer()
    if request.method == 'POST':
        form=Customer(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])

    context ={'form':form}
    return render(request,"addcustomer.html",context)


def searchcustomer(request):
    query = request.GET['query']
    allcustomers = CustomerModel.objects.filter(fname__icontains=query)
    params ={'allcustomers':allcustomers,'query':query}
    return render(request,"searchcustomer.html",params)
   # return render(request,"searchcustomers.html")

def editcustomer(request,pk):
    customer =CustomerModel.objects.get(id=pk)
    form = Customer(instance=customer)
    if request.method == 'POST':
        form=Customer(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return render(request,'success.html')

    context = {'form':form}
    return render(request,"addcustomer.html",context)


def staffview(request):
    staffs= StaffModel.objects.all().order_by(Lower('sname'))
    context ={'staffs':staffs}
    return render(request,"staff.html" ,context)

def addstaffview(request):
    form = Staff()
    if request.method == 'POST':
        form=Staff(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])

    context ={'form':form}
    return render(request,"addstaff.html",context)

def editstaff(request,pk):
    staff =StaffModel.objects.get(id=pk)
    form = Staff(instance=staff)
    if request.method == 'POST':
        form=Staff(request.POST,instance=staff)
        if form.is_valid():
            form.save()
            return render(request,'success.html')

    context = {'form':form}
    return render(request,"addstaff.html",context)

def vehicleview(request):
    vehicles = VehicleModel.objects.all()
    context ={'vehicles':vehicles}
    return render(request,"vehicle.html" ,context)

def dealerview(request):
    dealers= DealerModel.objects.all().order_by(Lower('dname'))
    context ={'dealers':dealers}
    return render(request,"dealer.html" ,context)

def addealerview(request):
    form = Dealer()
    if request.method == 'POST':
        form=Dealer(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])

    context ={'form':form}
    return render(request,"addDealer.html",context)

def editdealer(request,pk):
    dealer =DealerModel.objects.get(id=pk)
    form =Dealer(instance=dealer)
    if request.method == 'POST':
        form=Dealer(request.POST,instance=dealer)
        if form.is_valid():
            form.save()
            return render(request,'success.html')

    context = {'form':form}
    return render(request,"addDealer.html",context)

def addvehicleview(request):
    form = Vehicle()
    if request.method == 'POST':
        form=Vehicle(request.POST,request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])

    context ={'form':form}
    return render(request,"addvehicle.html",context)

def orders(request,pk):
    OrderFormSet = inlineformset_factory(CustomerModel,OrderModel,fields=('vehicle_name','order_date','delivery_date','tax','payment_mode'),extra=1)
    customer = CustomerModel.objects.get(id=pk)
    custom =CustomerModel.objects.filter(pk=pk)
    formset = OrderFormSet(queryset=OrderModel.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect(request.META['HTTP_REFERER'])

    orders = OrderModel.objects.filter(cust_id=pk)
    params ={'formset':formset,'custom':custom,'orders':orders}

    return render(request,"orders.html",params)

def invoiceview(request,pk):
    order=OrderModel.objects.get(id=pk)
    # customer = CustomerModel.objects.filter(pk=pk)
    amount=OrderModel.objects.filter(id=pk).aggregate(the_sum = Sum(F('tax')+F('vehicle_name__vprice')))
    
    
    params={'order':order,'amount':amount}
    return render(request,"invoice.html",params)

def subscribe(request):
    form = SubscribeForm()
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subject = 'Reminder for payment'
            message = 'Dear customer please pay the installment due of your vehicle. Thank you!'
            recipient = form.cleaned_data.get('email')
            send_mail(subject, 
              message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            messages.success(request, 'Success!')
            return redirect('subscribe')
    return render(request, 'subscribe.html', {'form': form})