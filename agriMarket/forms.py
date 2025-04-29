from django import forms 
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from products.models import Product

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class" : "form-control"
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                "class" : "form-control"
            }
        )
    )
    
class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','role', 'lat', 'lng']
        


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'image', 'lat', 'lng']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
        }