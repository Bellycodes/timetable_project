from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
import pdb

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'
    

class LogoutView(LogoutView):
    template_name = 'account/logout.html'
