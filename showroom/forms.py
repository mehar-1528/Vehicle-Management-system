from django import forms
from django.db.models import fields
from django.forms import ModelForm,widgets
from django.utils.safestring import mark_safe
from django.forms.widgets import DateInput
import datetime
from django.core.exceptions import ValidationError


from .models import *


class Customer(ModelForm):
    class Meta:
        model = CustomerModel
        fields='__all__'
        labels ={
            'fname':'First Name',
            'lname':'Last Name',
            'contact':'Contact Number',
            'cemail':'Email ID',
            'caddress':'Address',
            'staff_id':'Staff Name',
           

        }

class Staff(ModelForm):
    class Meta:
        model = StaffModel
        fields='__all__'
        labels ={
            'sname':'Name',
            'scontact':'Contact Number',
            'semail':'Email ID',
            'saddress':'Address',
            'status':'Current Status',
           

        }

class Dealer(ModelForm):
    class Meta:
        model = DealerModel
        fields='__all__'
        labels ={
            'dname':'Name',
            'dcontact':'Contact Number',
            'demail':'Email ID',
            'daddress':'Address',
            'dcompany':'Company Name',
            'staff_id':'Staff Name',

        }

class Vehicle(ModelForm):
     class Meta:
        model = VehicleModel
        fields='__all__'
        labels ={
            'vname':'Name',
            'vmodel':'Vehicle Model',
            'vtype':'Select Vehicle Type',
            'vprice':'Price',
            'vimage':'Select Image',
            'vdescription':'Write Description',
            'v_dealer':'Select Dealer',

        }

class OrderForm(ModelForm):
    class Meta:
        model =OrderModel
        fields ='__all__'
        labels = {
            'v_id':'Vehicle Name',

        }
        widgets ={
            'order_date': forms.DateInput(),
            'delivery_date':forms.DateInput(),
        }
        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get("order_date")
            end_date = cleaned_data.get("delivery_date")
            if end_date < start_date:
                raise forms.ValidationError("End date should be greater than start date.")
        
class SubscribeForm(forms.Form):
    email = forms.EmailField()
    