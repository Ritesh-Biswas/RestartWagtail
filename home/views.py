from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from wagtail.models import Page
from .models import DepartmentPage
# from wagtail.admin.auth import logout

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all department pages
        context['departments'] = DepartmentPage.objects.live().specific()
        return context

class LoginView(FormView):
    template_name = 'home/login.html'
    form_class = AuthenticationForm
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(self.request, user)
            return redirect('home:home')
        else:
            messages.error(self.request, "Invalid username or password or insufficient permissions.")
            return self.form_invalid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:login')