from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .token import token_generator

# Create your views here.
from .forms import RegistrationForm

def account_register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    form = RegistrationForm()
    if request.method == 'POST':
        registration_form  = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save(commit = False)
            user.email = registration_form.cleaned_data['email']
            user.password = registration_form.cleaned_data['password']
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string(
                'account/registration/account_activation_email.html',
                {
                    'user' : user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_decode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user)
                }
            )
            user.email_user(subject=subject, message = message)
            return 
    return render(request, 'account/registration/register.html', {'form': form})