from django.urls import path
from .views import HomeLoginView

app_name = 'home'

urlpatterns = [
    path('', HomeLoginView.as_view(), name='home'),
]