# Django modules
from django.contrib import admin
from django.urls import path

# Project modules
from apps.views import hello_view, users_info, city_time, counter

urlpatterns = [
    path('admin/', admin.site.urls),
    path(route="", view=hello_view, name="hello-view"),
    path(route="users/", view=users_info, name="users"),
    path(route="cities/", view=city_time, name="city-time"),
    path(route="counter/", view=counter, name="counter"),
]
