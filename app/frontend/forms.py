from django import forms



#local import
from django import forms
from app.frontend.models import Customer
from app.frontend.models import Purchase, PurchaseItem,Category, Item
from app.frontend.models import Expense,ExpenseCategory
from app.frontend.models import OrganizationSetting




class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email', 'shipping_address']

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': "Enter the customer's full name"})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': "Enter a valid phone number"})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': "Enter a valid email address"})
        self.fields['shipping_address'].widget.attrs.update({'class': 'form-control', 'rows': 4, 'placeholder': "Enter the full shipping address"})





class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'purchase_date', 'status', 'reference_no', 'notes']
    
    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})
        self.fields['purchase_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['reference_no'].widget.attrs.update({'class': 'form-control'})
        self.fields['notes'].widget.attrs.update({'class': 'form-control'})

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['purchase', 'item', 'category', 'quantity', 'price_per_unit', 'tax_percentage']
    
    def __init__(self, *args, **kwargs):
        super(PurchaseItemForm, self).__init__(*args, **kwargs)
        self.fields['purchase'].widget.attrs.update({'class': 'form-control'})
        self.fields['item'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'type': 'number'})
        self.fields['price_per_unit'].widget.attrs.update({'class': 'form-control', 'type': 'number'})
        self.fields['tax_percentage'].widget.attrs.update({'class': 'form-control', 'type': 'number'})
     


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_code', 'name', 'brand', 'category', 'quantity', 'description', 'image', 'price', 'cost_price', 'discount_type', 'discount', 'tax_percentage']
        widgets = {
            'item_code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_type': forms.Select(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        
        # Add CSS classes to form fields
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['reference_no'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Reference No'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Amount'})
        self.fields['notes'].widget.attrs.update({'class': 'form-control', 'rows': 4, 'placeholder': 'Additional notes'})

    date = forms.DateField(
        input_formats=["%Y-%m-%d"],  # Ensure format is consistent
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})  # Ensures a date picker
    )

    class Meta:
        model = Expense
        fields = ['category', 'date', 'reference_no', 'amount', 'notes']

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }



class OrganizationSettingForm(forms.ModelForm):
    class Meta:
        model = OrganizationSetting
        fields = ['company_name', 'logo', 'phone', 'telephone', 'location', 'pan_vat', 'email']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Telephone'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            'pan_vat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter PAN/VAT'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
