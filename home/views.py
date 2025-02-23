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

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            context['departments'] = SubDepartmentPage.objects.live().specific()
            return context

        user_sub_departments = []
        sub_departments = SubDepartmentPage.objects.live().specific()
        for sub_department in sub_departments:
            if user in sub_department.members.all() or user in sub_department.site_admins.all():
                user_sub_departments.append(sub_department)
        context['departments'] = user_sub_departments
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
       
        announcements = AnnouncementPage.objects.child_of(subdepartment).live().specific()
        print("---->Available Annoucments:", [(announcement.id, announcement.name) for announcement in announcements])
        context['announcements'] = AnnouncementPage.objects.child_of(subdepartment).live().specific("Announcement").order_by('-date_posted')
        
        faqs = FAQPage.objects.child_of(subdepartment).live().specific()
        print("---->Available FAQs:", [(faq.id, faq.question) for faq in faqs])
        context['faqs'] = FAQPage.objects.child_of(subdepartment).live().specific("FAQ")
        
        announcement_id = self.request.GET.get('announcement_id')
        faq_id = self.request.GET.get('faq_id')
        print("Announcement id is:-",announcement_id)
        print("FAQ id is:-",faq_id)

       

        if announcement_id:
            context['selected_announcement'] = get_object_or_404(
            AnnouncementPage, 
            id=announcement_id,
            path__startswith=subdepartment.path
            
        )
        elif faq_id:
            context['selected_faq'] = get_object_or_404(
            FAQPage,
            id=faq_id,
            path__startswith=subdepartment.path
        )
             
                
        
        return context

    def get_object(self, queryset=None):
        # Get the page by its slug
        return get_object_or_404(SubDepartmentPage, slug=self.kwargs['slug'])