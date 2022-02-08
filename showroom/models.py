from re import M, T
from django.db import models
from django.db.models.fields.related import ForeignKey
from datetime import date
from django.db.models.deletion import CASCADE
from django.core.validators import RegexValidator
import datetime
from django.core.exceptions import ValidationError



# Create your models here.


class StaffModel(models.Model):
    STATUS =(
        ('Active','Active'),
        ('Inactive','Inactive'),
    )
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Please Enter Valid Name')
    phone = RegexValidator(r'^[0-9]{10}$', 'Please Enter Valid Mobile Number')
    sname = models.CharField(max_length=50 ,validators=[alpha])
    semail = models.EmailField()
    scontact = models.CharField(max_length=10 , null=True,blank=True,validators=[phone])
    saddress = models.TextField()
    status = models.CharField(max_length=100,null=True,choices=STATUS)

    def __str__(self):
        return self.sname

class DealerModel(models.Model):
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Please Enter Valid Name')
    phone = RegexValidator(r'^[0-9]{10}$', 'Please Enter Valid Mobile Number')
    dname = models.CharField(max_length=50,validators=[alpha])
    demail = models.EmailField()
    dcontact = models.CharField(max_length=10 , null=True,blank=True ,validators=[phone])
    daddress = models.TextField()
    dcompany = models.CharField(max_length=50)
    staff_name = ForeignKey(StaffModel,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.dname

class VehicleModel(models.Model):
    TYPE =(
        ('Two Wheeler','Two Wheeler'),
        ('Four Wheeler','Four Wheeler'),
    )
    vname =  models.CharField(max_length=50)
    vmodel = models.CharField(max_length=50)
    vtype =models.CharField(max_length=100,null=True,choices=TYPE)
    vprice= models.FloatField()
    vdescription = models.TextField()
    vimage = models.FileField(upload_to="image/",null=True, blank=True)
    v_dealer = ForeignKey(DealerModel,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.vname

class CustomerModel(models.Model):
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Please Enter Valid Name')
    phone = RegexValidator(r'^[0-9]{10}$', 'Please Enter Valid Mobile Number')
    fname = models.CharField(max_length=50 ,validators=[alpha])
    lname = models.CharField(max_length=50,null=True,blank=True ,validators=[alpha])
    contact =models.CharField(max_length=10 , null=True,blank=True ,validators=[phone])
    cemail =models.EmailField()
    caddress = models.TextField()
    staff_id =ForeignKey(StaffModel,on_delete=models.CASCADE,null=True,blank=True)



class OrderModel(models.Model):
    
    MODE =(
        ('Cheque','Cheque'),
        ('Cash','Cash'),
        ('Net Banking','Net Banking')
    )
    cust_id = models.ForeignKey(CustomerModel,on_delete=models.CASCADE,null=True,blank=True)
    vehicle_name = models.ForeignKey(VehicleModel,on_delete=models.CASCADE,null=True,blank=True)
    order_date = models.DateField(default=date.today)
    delivery_date = models.DateField(default=date.today)
    tax = models.FloatField()
    payment_mode = models.CharField(max_length= 60, choices=MODE,null=True,blank=True)
    def save(self, *args, **kwargs):
        if self.order_date < datetime.date.today() or self.delivery_date < self.order_date:
            raise ValidationError("Invalid delivery date or order date!")
        super(OrderModel, self).save(*args, **kwargs)


    


    
