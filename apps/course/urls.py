# Django modules
from django.urls import include, path

# Django Rest Framework modules
from rest_framework.routers import DefaultRouter

# Project modules
from apps.course.views import CourseViewSet


router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)

router.register(
    prefix="courses",
    viewset=CourseViewSet,
    basename="course",
)

urlpatterns = [
    path("v1/", include(router.urls)),
]