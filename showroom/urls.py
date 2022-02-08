from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls import static
urlpatterns = [
    path('', loginview, name="loginview"),
    path('login/validate/',loginuser,name="loginuser"),
    path('home/', indexview, name="indexview"),
    path('success/', successview, name="success"),

    path('customers/', customersview, name="customersview"),
    path('addcustomer/', addcustomerview, name="addcustomerview"),
    path('editcustomer/<int:pk>/', editcustomer, name="editcustomer"),
    path('searchcustomer/', searchcustomer, name="searchcustomer"),


    path('staff/', staffview, name="staffview"),
    path('addstaff/', addstaffview, name="addstaffview"),
     path('editstaff/<int:pk>/', editstaff, name="editstaff"),

     path('orders/<int:pk>',orders,name="orders"),
      path('invoice/<int:pk>/',invoiceview,name='invoice'),


    path('vehicle/', vehicleview, name="vehicleview"),
    path('addvehicle/', addvehicleview, name="addvehicleview"),
    path('dealer/', dealerview, name="dealerview"),
    path('addealer/', addealerview, name="addealerview"),
    path('editdealer/<int:pk>/', editdealer, name="editdealer"),
    path('subscribe/',subscribe,name="subscribe"),

    
]
if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
