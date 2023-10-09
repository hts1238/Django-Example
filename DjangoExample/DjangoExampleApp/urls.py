from django.urls import path

from .views import index, news, register


urlpatterns = [
    path('', index.index, name="index"),
    path('index', index.index, name="index"),
    path('news/<int:news_id>', news.view_news, name="view news"),
    path('news/<int:news_id>/edit', news.edit_news, name="view news"),
    path('news/my', news.my_news, name="my news"),
    path('news/create', news.create_news, name="create news"),
    path('register', register.register, name="register"),
]
