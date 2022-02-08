from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(StaffModel)
admin.site.register(DealerModel)
admin.site.register(VehicleModel)
admin.site.register(CustomerModel)
admin.site.register(OrderModel)
