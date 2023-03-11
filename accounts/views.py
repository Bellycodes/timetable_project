from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import EmailAuthenticationForm
import pdb

class LoginWithEmailView(LoginView):
    template_name = 'account/login.html'
    authentication_form = EmailAuthenticationForm
    success_url = reverse_lazy('ttgen:dashboard')

    def get_success_url(self):
        pdb.set_trace()
        return super().get_success_url()
    

class LogoutView(LogoutView):
    template_name = 'account/logout.html'
