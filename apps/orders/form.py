from django import forms
from .models import PaymentType
 
#  Chice_Payment_type = ((1,'درگاه بانکی '), (2,'پرداخت در محل'),(3,'فیش بانکی '))
class OrderForm(forms.Form):
    name = forms.CharField(label="", 
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'نام'}),
                        error_messages={'required': ' این فیلد نباید خالی بماند'})
    family = forms.CharField(label="", 
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'خانوادگی '}),
                        error_messages={'required': 'این فیلد نباید خالی بماند'})
    email = forms.CharField(label="", 
                        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder' :'ایمیل'}),
                        required=False)
    
    phone_number = forms.CharField(label="", 
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'تلفن'}),
                        required=False)
    
    address = forms.CharField(label="", 
                        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' :'آدرس', 'rows':'3'}),
                        error_messages={'required': 'این فیلد نباید خالی بماند'})
    
    description = forms.CharField(label="", 
                        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' :'توضیحات ','rows':'5'}),
                        required=False)
    # payment_type = forms.ChoiceField(label='',
    #                                 choices=[(item.pk,item) for item in PaymentType.objects.all()],
    #                                 widget=forms.RadioSelect() )
    