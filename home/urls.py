from django.urls import path
from .views import LoginView, HomeView, LogoutView, SubDepartmentView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('departments/<str:slug>/', SubDepartmentView.as_view(), name='subdepartment'),
]