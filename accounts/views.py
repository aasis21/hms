from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout, update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm, PasswordChangeForm)
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string


from . import models
from . import forms
from .tokens import account_activation_token

def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('accounts:profile'))
                else:
                    messages.error(
                        request,
                        "That user account is not active."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    form.fields['username'].help_text = "This should be your IITK email ID"
    form.fields['password1'].help_text = ""
    form.fields['password2'].help_text = ""
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email = user.username + "@iitk.ac.in"
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Hall12 HMS Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            new_form = UserCreationForm()
            new_form.fields['username'].help_text = "This should be your IITK email ID"
            new_form.fields['password1'].help_text = ""
            new_form.fields['password2'].help_text = ""

            return render(request, 'accounts/sign_up.html', {'form' : new_form, 'message' : "An activation link has been sent to " + user.email })

    return render(request, 'accounts/sign_up.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(
            request,
            "You're now a user! You've been signed in, too."
        )
        return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        new_form = UserCreationForm()
        new_form.fields['username'].help_text = "This should be your IITK email ID"
        new_form.fields['password1'].help_text = ""
        new_form.fields['password2'].help_text = ""

        return render(request, 'accounts/sign_up.html', {'form' : new_form, 'message' : "Invalid Activation Link" })

def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('accounts:sign_in'))


@login_required
def profile(request):
    """Display User Profile"""
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {
        'profile': profile
    })

