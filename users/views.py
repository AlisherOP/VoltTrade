from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm


def register(request):
    if request.method == "POST":  # when the username is posted
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # saving the new account
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"Welcome {username}, you are currently logged in")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {'form': form})
# Create your views here.
