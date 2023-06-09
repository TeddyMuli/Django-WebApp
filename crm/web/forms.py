from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Record, Sale, Debt, Route, Product, Expense, Message

class RecordForm(forms.ModelForm):
    f_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
    l_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
    phone_no = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone Number", "class":"form-control"}), label="")
    route = forms.ModelChoiceField(queryset=Route.objects.all(), empty_label="Route",widget=forms.Select(attrs={'style': 'background-color: #f2f2f2; border: 1px solid #ccc; padding: 5px 10px;'}))

    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)

        choices = Route.objects.values_list('id', 'route')  # Replace 'name' with the appropriate field name from the related model
        self.fields['route'].choices = [('', 'Route')] + list(choices)
        self.fields['route'].label = False
    class Meta:
        model = Record
        exclude = ("user", )


class SaleForm(forms.ModelForm):
    quantity = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Quantity", "class":"form-control"}), label="")
    paid = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Paid", "class":"form-control"}), label="")
    client = forms.ModelChoiceField(queryset=Record.objects.all(), empty_label="Client",widget=forms.Select(attrs={'style': 'background-color: #f2f2f2; border: 1px solid #ccc; padding: 5px 10px;'}))
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Product",widget=forms.Select(attrs={'style': 'background-color: #f2f2f2; border: 1px solid #ccc; padding: 5px 10px;'}))
    pay = forms.ChoiceField(widget=forms.Select(attrs={'style': 'background-color: #f2f2f2; border: 1px solid #ccc; padding: 5px 10px;'}))
    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        # Clients
        clients = Record.objects.values_list('phone_no', 'f_name', 'l_name')
        choice_tuples = [(phone_no, f'{f_name} {l_name}') for phone_no, f_name, l_name in clients]
        self.fields['client'].choices = [('', 'Client')] + list(choice_tuples)
        self.fields['client'].label = False
        
		#Products
        products = Product.objects.values_list('id', 'product')
        self.fields['product'].choices = [('', 'Product')] + list(products)
        self.fields['product'].label = False
		#Pay
		
        pays = Sale.objects.order_by('pay').values_list('pay', 'pay').distinct()
        self.fields['pay'].label = False
        self.fields['pay'].choices = [('', 'Payment Method')] + list(pays)

    class Meta:
        model = Sale
        exclude = ("served_by", )

class DebtForm(forms.ModelForm):
    paid = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Pay Debt", "class":"form-control"}), label="")
    class Meta:
         model = Debt
         exclude = ('client','user',)

class MessageForm(forms.ModelForm):
     message = forms.CharField(
          required=True, 
          widget=forms.widgets.Textarea(attrs={"placeholder":"Enter Message","class":"form-control"}), 
          label=""
          )
     class Meta:
          model = Message
          exclude = ('user',)


class ExpenseForm(forms.ModelForm):
     name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Name", "class":"form-control"}), label="")
     amount = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Amount", "class":"form-control"}), label="")

     class Meta:
          model = Expense
          exclude = ('user',)
         
class SignUpForm(UserCreationForm):
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	