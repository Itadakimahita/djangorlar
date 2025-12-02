# Django modules
from django.urls import include, path

# Django Rest Framework modules
from rest_framework.routers import DefaultRouter

# Project modules
from apps.course.views import CourseViewSet
from apps.course.lesson_views import LessonsViewSet


router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)
lessons_router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)

router.register(
    prefix="courses",
    viewset=CourseViewSet,
    basename="course",
)
lessons_router.register(
    prefix="lessons",
    viewset=LessonsViewSet,
    basename="lesson",
)


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include(lessons_router.urls)),
]