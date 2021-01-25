from django.contrib import messages
from django.shortcuts import render, redirect
from litLogin.form import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout


def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'you account is saved')
            return redirect('login_blog')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, "registration.html", context)


def login_blog(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('flux')
        else:
            messages.info(request, 'Username Or email are incorrect')

    form = LoginForm()
    context = {'form': form}
    return render(request, "connexion.html", context)


def logout_blog(request):
    logout(request)
    return redirect('login_blog')



