from django.urls import path
from .views import account_register

app_name = 'account'

urlpatterns = [
    path('', account_register, name = 'register')
]
