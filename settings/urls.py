# Django modules
from django.contrib import admin
from django.urls import path

# Project modules
from apps.views import hello_view, users_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path(route="hello/", view=hello_view, name="hello-view"),
    path(route="users/", view=users_info, name="users")
]
