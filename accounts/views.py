from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'
    redirect_authenticated_user =True
    
    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        else:
            return reverse('ttgen:dashboard')
    

class LogoutView(LogoutView):
    template_name = 'account/logout.html'
