from django.db import models
from django.db.models import Sum
from simple_history.models import HistoricalRecords
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.name
    
class Admin(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)    

class Invoice(models.Model):
    customer_name = models.CharField(max_length=200)
    address_line1 = models.CharField(max_length=200, null=True)
    address_line2 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    country = CountryField(default='IN')

    gst = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    amount_paid = models.DecimalField(max_digits=20, decimal_places=2)
    amount_due = models.DecimalField(max_digits=20, decimal_places=2, editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, editable=False, null=True)
    gst_rate = models.DecimalField(max_digits=20, decimal_places=2, editable=False, null=True)
    all_total = models.DecimalField(max_digits=20, decimal_places=2, editable=False, null=True)
    note = models.TextField(null=True, blank=True)
    history = HistoricalRecords(user_model=User)
    email = models.CharField(max_length=100, null=True)

    gst_no = models.CharField(max_length=50, null=True)
    hsn_no = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)  # Save the Invoice instance first
        # Calculate subtotal based on the sum of total fields of related items
        self.subtotal = self.items.aggregate(total=Sum('total'))['total'] or 0
        self.gst_rate = (self.gst / 100) * self.subtotal  # Update gst_rate based on gst and subtotal
        self.all_total = self.subtotal + self.gst_rate  # Update all_total based on subtotal and gst_rate
        self.amount_due = self.all_total - self.amount_paid
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return "invoice" + "(" + str(self.id) + ")"

class Item(models.Model):
    item_no = models.CharField(max_length=50)
    item_name = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    remove = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=User)

    def save(self, *args, **kwargs):
        # Calculate total based on quantity and price
        self.total = self.quantity * self.price
        super(Item, self).save(*args, **kwargs)

class Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    address_line1 = models.CharField(max_length=200, null=True)
    address_line2 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    country = CountryField(default='IN')
    gst_no = models.CharField(max_length=50, null=True)
    hsn_no = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.customer_name + " ( " + self.email + " ) "
    
@receiver(post_save, sender=Invoice)
def create_customer_from_invoice(sender, instance, created, **kwargs):
    if created:
        # Check if a Customer with the same data already exists
        existing_customer = Customer.objects.filter(
            customer_name=instance.customer_name,
            address_line1=instance.address_line1,
            address_line2=instance.address_line2,
            city=instance.city,
            state=instance.state,
            zip_code=instance.zip_code,
            country=instance.country,
            gst_no=instance.gst_no,
            hsn_no=instance.hsn_no,
            email=instance.email,
            created_by=instance.created_by
        ).first()

        # If no matching Customer is found, create a new one
        if not existing_customer:
            Customer.objects.create(
                customer_name=instance.customer_name,
                address_line1=instance.address_line1,
                address_line2=instance.address_line2,
                city=instance.city,
                state=instance.state,
                zip_code=instance.zip_code,
                country=instance.country,
                gst_no=instance.gst_no,
                hsn_no=instance.hsn_no,
                email=instance.email,
                created_by=instance.created_by
            )