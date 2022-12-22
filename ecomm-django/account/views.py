from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def login(request):
    return render(request, 'registration/login.html')


class UserRegisterView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('account:login')

@login_required(login_url='account:login')
def Profile(request):
    return render(request, 'registration/profile.html')




def contact(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        user_subject = request.POST['user_subject']
        user_message = request.POST['user_message']

        contact_user = Contact.objects.create(
            user=request.user,
            user_name = user_name,
            email = user_email,
            subject = user_subject,
            message = user_message
        )
        contact_user.save()
        messages.info(request, f"Hey, {user_name} Thanks for being awesome! We have received your message and would like to thank you for writing to us. ...")

        send_mail(
            user_subject,
            f"Hey {user_name} we have received your mail, we will get beck in touch with you as soon as possible. Thanks for contacting us",
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )


        return redirect('account:contact')

    return render(request, 'registration/contact.html')
