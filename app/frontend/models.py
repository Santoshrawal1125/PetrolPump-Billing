from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from app.account.models import User
from phonenumber_field.modelfields import PhoneNumberField

class OrganizationSetting(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=False, null=False)
    phone = models.IntegerField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    pan_vat = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.company_name

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_invoice = Invoice.objects.order_by('-id').first()
            if last_invoice:
                last_number = int(last_invoice.invoice_number.replace("SL", ""))
                new_number = f"SL{last_number + 1:04d}"
            else:
                new_number = "SL0001"
            self.invoice_number = new_number
        super().save(*args, **kwargs)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(region='NP', null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_by = models.ForeignKey(User, related_name='customers_created', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='expenses_category_created', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, null=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    category = models.ForeignKey('ExpenseCategory', on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    reference_no = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_expenses', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f"Expense {self.reference_no} (Amount: {self.amount})"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='itemCategory_created', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    created_by = models.ForeignKey(User, related_name='item_created', on_delete=models.CASCADE, null=True)
    item_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    discount_type = models.CharField(max_length=50, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed')], blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, null=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('pending', 'Pending'),
        ('ordered', 'Ordered'),
    ]

    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True)
    purchase_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reference_no = models.CharField(max_length=50, unique=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, null=True)

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_tax(self):
        return sum(item.tax_amount for item in self.items.all())

    @property
    def grand_total(self):
        return self.subtotal + self.total_tax

    def __str__(self):
        return f"Purchase {self.reference_no} (Supplier: {self.supplier.name})"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey('Purchase', on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self.item and self.category:
            if self.item.category != self.category:
                raise ValidationError(
                    f"The item '{self.item.name}' does not belong to the selected category '{self.category.name}'."
                )
        self.tax_amount = (
            (self.price_per_unit * self.quantity * self.tax_percentage / 100) if self.tax_percentage else 0.0
        )
        self.total_price = (self.price_per_unit * self.quantity) + self.tax_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Item {self.item.name} (Quantity: {self.quantity})"

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(region='NP', null=True)
    email = models.EmailField(blank=True, null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tax_no = models.CharField(max_length=100, blank=True, null=True)
    gst_no = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=[('paid', 'Paid'), ('pending', 'Pending'), ('partial', 'Partial')], default='pending'
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, null=True)
    created_by = models.ForeignKey(User, related_name='supplier_created', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Sale(models.Model):
    created_by = models.ForeignKey(
        User,
        related_name='frontend_sale_created',  # Unique related_name
        on_delete=models.CASCADE,
        null=True
    )
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Sale #{self.id} (Customer: {self.customer_name})"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, default="Unknown Item")  
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add a default value

    def save(self, *args, **kwargs):
        # Calculate subtotal before saving
        self.subtotal = (self.price * self.quantity) - self.discount + self.tax
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_name} (Qty: {self.quantity}, Subtotal: {self.subtotal})"
