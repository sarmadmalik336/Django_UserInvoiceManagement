from django.contrib import admin
from .models import User, Invoice, Item, Admin, Customer
# Register your models here.
admin.site.register(User)
admin.site.register(Invoice)
admin.site.register(Item)
admin.site.register(Admin)
admin.site.register(Customer)