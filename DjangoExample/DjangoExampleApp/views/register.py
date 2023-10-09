from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User

from ..objects.menuitem import MenuItem
from ..models import News, Profile, Role


def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        confirm = request.POST["confirm"]

        if password != confirm:
            raise Exception("Passwords is different")

        if User.objects.filter(username=username).exists():
            raise Exception("The user with this username alredy exists, try another or log in")

        if User.objects.filter(email=email).exists():
            raise Exception("The user with this email alredy exists, try another or log in")

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        if Role.objects.filter(name="user").exists():
            role = Role.objects.get(name="user")
        else:
            role = Role()
            role.name = "user"
            role.save()

        profile = Profile()
        profile.user = user
        profile.save()
        profile.roles.add(role)
        profile.save()

        login(request, user)

        return redirect("/")
    else:
        context = {
            "title": "Register",
            "menu_items": [
                MenuItem(
                    "/accounts/login",
                    "Log in"
                )
            ]
        }

        return render(request, "register.html", context)
