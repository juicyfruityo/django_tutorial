from django.shortcuts import render, redirect
from .forms import RegisterForm


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        print(form.is_valid())
        if form.is_valid():
            print(response)
            form.save()
        return redirect("/")

    else:
        form = RegisterForm()
    return render(response, "register/register.html", {"form": form})