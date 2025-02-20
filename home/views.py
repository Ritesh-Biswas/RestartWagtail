from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

class HomeLoginView(FormView):
    template_name = 'home/home_page.html'
    form_class = AuthenticationForm
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(self.request, user)
            return redirect(reverse('wagtailadmin_home'))
        else:
            messages.error(self.request, "Invalid username or password or insufficient permissions.")
            return self.form_invalid(form)