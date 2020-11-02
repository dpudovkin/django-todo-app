import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"New account created: {username}.")
            login(request, user)
            return redirect("/")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(
                request=request,
                template_name="main/register.html",
                context={"form": form}
            )

    form = UserCreationForm
    return render(
        request=request,
        template_name="main/register.html",
        context={"form": form}
    )


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                if request.POST.get('next') == '':
                    return redirect('/')
                else:
                    return redirect(request.POST.get('next', '/'))
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm
    return render(
        request=request,
        template_name="main/login.html",
        context={"form": form}
    )

def signout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/login")