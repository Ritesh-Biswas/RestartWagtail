from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import FormView, TemplateView, DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from wagtail.models import Page
from .models import DepartmentPage, SubDepartmentPage, AnnouncementPage, FAQPage
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

class SubDepartmentView(LoginRequiredMixin, DetailView):
    model = SubDepartmentPage
    template_name = 'home/sub_department_page.html'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subdepartment = self.object
        # print("Announcments data:-",AnnouncementPage.objects.child_of(subdepartment).live().specific("Announcement"))
        
       
        context['announcements'] = AnnouncementPage.objects.child_of(subdepartment).live().specific("Announcement").order_by('-date_posted')
        
     
        context['faqs'] = FAQPage.objects.child_of(subdepartment).live().specific("FAQ")
        
        return context

    def get_object(self, queryset=None):
        # Get the page by its slug
        return get_object_or_404(SubDepartmentPage, slug=self.kwargs['slug'])