from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff True')
        
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser True')
        
        return self.create_user(email, user_name, password, **kwargs)

    def create_user(self, email, user_name, password, **kwargs):
        if not email:
            raise ValueError('Required Email')
        email = self.normalize_email(email)
        user = self.model(email = email, user_name = user_name, **kwargs)
        user.set_password(password)
        user.save()
        return user
        

# Create your models here.
class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField("email_address", max_length=254, unique = True)
    user_name = models.CharField(max_length = 150, unique = True)
    first_name = models.CharField(max_length = 150, blank = True)
    about = models.TextField('about', max_length = 500, blank = True)
    country = CountryField()
    phone_number = models.CharField(max_length = 20, blank = True)
    postcode = models.CharField(max_length=150, blank = True)
    address_1 = models.CharField(max_length = 150, blank = True)
    address_2 = models.CharField(max_length = 150, blank = True)
    town_city = models.CharField(max_length = 150, blank = True)

    is_active = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return str(self.user_name)
    
    def clean_username(self):
        username = self.cleaned_data['user_name'].lower()
        r = Account.objects.filter(user_name = username)
        if r.count():
            raise ValueError('User already exists')
        return username
    
    def clean_password(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise ValueError('Password do not match!')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email = email).exists():
            raise forms.ValidationError('Email already exists')
        return email