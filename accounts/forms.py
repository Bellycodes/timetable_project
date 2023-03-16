from django import forms
from allauth.account.forms import LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import User

class LoginForm(LoginForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'required': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'password',
            Submit('submit', 'Login', css_class='col-md-12 justify-content-center')
        )
    
    class Meta:
        model = User
        fields = ('email', 'password')
        

