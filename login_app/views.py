from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("view_blog", 25)
        else:
            messages.success(request,("There was an error login in"))
            return render(request, "authentication/login.html", {})
    else:
        return render(request, "authentication/login.html", {})


def logout_user(request):
    logout(request)
    return redirect("home")