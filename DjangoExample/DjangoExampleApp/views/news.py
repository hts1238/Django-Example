from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

from ..objects.menuitem import MenuItem
from ..models import News


def view_news(request, news_id: int):
    try:
        news = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        raise Http404("This news does not exist")
    
    menu_items = []
    if request.user.is_authenticated:
        if news.author == request.user.profile:
            menu_items.append(MenuItem(
                f'/news/{ news.id }/edit',
                "Edit"
            ))

        if request.user.profile.roles.filter(name="writer").exists():
            menu_items.append(MenuItem(
                "/news/my",
                "My news"
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
        "news": news,
        "menu_items": menu_items,
    }

    return render(request, "view_news.html", context)


@login_required(login_url="/accounts/login/")
def my_news(request):
    user = request.user
    profile = user.profile

    if not profile.roles.filter(name="writer").exists():
        return redirect("/")

    news_list = News.objects.filter(author=profile).order_by("-created_at")

    context = {
        "title": "My news",
        "news_list": news_list,
        "menu_items": [
            MenuItem(
                "/news/create",
                "Create news"
            ),
            MenuItem(
                "/accounts/logout",
                "Log out"
            )
        ]
    }

    return render(request, "my_news.html", context)


@login_required(login_url="/accounts/login/")
def create_news(request):
    user = request.user
    profile = user.profile

    if not profile.roles.filter(name="writer").exists():
        return redirect("/")

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        hidden = "hidden" in request.POST

        news = News(title=title, content=content, hidden=hidden)
        news.author = profile
        news.save()

        return redirect("/news/my")
    else:
        context = {
            "title": "Create news",
            "menu_items": [
                MenuItem(
                    "/news/my",
                    "My news"
                ),
                MenuItem(
                    "/accounts/logout",
                    "Log out"
                )
            ]
        }

        return render(request, "create_news.html", context)
    

@login_required(login_url="/accounts/login/")
def edit_news(request, news_id):
    try:
        news = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        raise Http404("This news does not exist")
    
    user = request.user
    profile = user.profile

    if news.author != profile:
        return redirect(f'/news/{news_id}')

    if request.method == "POST":
        news.title = request.POST["title"]
        news.content = request.POST["content"]
        news.hidden = "hidden" in request.POST
        news.save()

        return redirect(f'/news/{news_id}')
    else:
        context = {
            "title": "Edit news",
            "news": news,
            "menu_items": [
                MenuItem(
                    "/news/my",
                    "My news"
                ),
                MenuItem(
                    "/accounts/logout",
                    "Log out"
                )
            ]
        }

        return render(request, "edit_news.html", context)
