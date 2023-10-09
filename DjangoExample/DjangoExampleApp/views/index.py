from django.shortcuts import render
from django.core.paginator import Paginator

from ..objects.menuitem import MenuItem
from ..models import News


def index(request):
    news_list = News.objects.filter(hidden=False).order_by("-created_at")
    paginator = Paginator(news_list, 5)
    page = request.GET.get("page") if "page" in request.GET else 1

    menu_items = []
    if request.user.is_authenticated:
        if request.user.profile.roles.filter(name="writer").exists():
            menu_items.append(MenuItem(
                "/news/my",
                "My news"
            ))

        if request.user.is_superuser:
            menu_items.append(MenuItem(
                "/admin",
                "Admin"
            ))

        menu_items.append(MenuItem(
            "/accounts/logout",
            "Log out"
        ))
    else:
        menu_items.extend((
            MenuItem(
                "/accounts/login",
                "Log in"
            ),
            MenuItem(
                "/register",
                "Register"
            )
        ))

    context = {
        "title": "Latest news",
        "news_list": paginator.get_page(page),
        "menu_items": menu_items,
    }

    return render(request, "index.html", context)
