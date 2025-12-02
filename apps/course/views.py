# Python modules
from typing import Any

# Django modules
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet, Count
from django.db import models

# Django REST Framework
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.decorators import action

from apps.course.models import Course, Lessons
from apps.user.models import CustomUser
from apps.course.serializers import (
    CourseSerializer,
    CourseListSerializer,
    CourseCreateSerializer,   
    CourseUpdateSerializer,
    LessonSerializer,
)
from apps.course.permission import IsOwner

class CourseViewSet(ViewSet):
    """
    ViewSet for handling Course-related endpoints.
    """

    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    serializer_class = CourseSerializer

    # ---------------------- Helpers ----------------------
    def get_course(self, id):
        return get_object_or_404(
            Course.objects.annotate(
                lessons_count=models.Count("lessons")
            ).prefetch_related("lessons"),
            id=id
        )

    def get_permissions(self):
        """Extra owner check for update, delete, activate, deactivate"""
        if self.action in ["update", "destroy", "activate", "deactivate"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]
    


    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle GET requests to list Courses.

        Parameters:
            request: DRFRequest
                The request object.
            *args: list
                Additional positional arguments.
                Additional positional arguments.
            **kwargs: dict
                Additional keyword arguments.
        
        Returns:
            DRFResponse
                A response containing list of Courses.
        """

        all_Courses: QuerySet[Course] = Course.objects.select_related("owned_courses").annotate(
            users_count=Count("users", distinct=True)
        ).all()

        serializer: CourseListSerializer = CourseListSerializer(
            all_Courses,
            many=True
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to create a new Course.

        Parameters:
            request: DRFRequest
                The request object.
            *args: list
                Additional positional arguments.
            **kwargs: dict
                Additional keyword arguments.
        
        Returns:
            DRFResponse
                A response indicating the result of the creation operation.
        """
        serializer: CourseCreateSerializer = CourseCreateSerializer(
            data=request.data
        )
        
        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )
        
        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )

    def partial_update(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle PATCH requests to partially update a Course.

        Parameters:
            request: DRFRequest
                The request object.
            *args: list
                Additional positional arguments.
            **kwargs: dict
                Additional keyword arguments.
        
        Returns:
            DRFResponse
                A response indicating the result of the update operation.
        """
        try:
            course: Course = Course.objects.get(id=kwargs["pk"])
        except course.DoesNotExist:
            return DRFResponse(
                data={
                    "pk": [f"Course with id={kwargs['pk']} does not exist."]
                },
                status=HTTP_404_NOT_FOUND
            )

        serializer: CourseUpdateSerializer = CourseUpdateSerializer(
            data=request.data,
            instance=course,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    def destroy(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle DELETE requests to delete a Course.

        Parameters:
            request: DRFRequest
                The request object.
            *args: list
                Additional positional arguments.
            **kwargs: dict
                Additional keyword arguments.
        
        Returns:
            DRFResponse
                A response indicating the result of the deletion operation.
        """
        try:
            course: Course = Course.objects.get(id=kwargs["pk"])
        except course.DoesNotExist:
            return DRFResponse(
                data={
                    "pk": [f"Course with id={kwargs['pk']} does not exist."]
                },
                status=HTTP_404_NOT_FOUND
            )

        course.delete()

        return DRFResponse(
            status=HTTP_204_NO_CONTENT
        )

    @action(
        methods=("GET",),
        detail=True,
        url_name="Lists",
        url_path="Lists",
        permission_classes=(IsAuthenticated,)
    )
    def get_Lists(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle GET requests to retrieve Lists for a specific Course.

        Parameters:
            request: DRFRequest
                The request object.
            *args: list
                Additional positional arguments.
            **kwargs: dict
                Additional keyword arguments.
        Returns:
            DRFResponse
                A response containing list of Lists for the specified Course.
        """
        try:
            Course: Course = Course.objects.get(id=kwargs["pk"])
        except Course.DoesNotExist:
            return DRFResponse(
                data={
                    "id": [f"Course with id={kwargs['pk']} does not exist."]
                },
                status=HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request=request, obj=Course)

        return DRFResponse(
            data=CourseListSerializer(
                Course.Lists.prefetch_related("owner").all(),
                many=True,
            ).data,
            status=HTTP_200_OK
        )

    @action(
        detail=True, 
        methods=["POST"],
        url_path="activate",
        url_name="activate_course",
    )
    def activate(self, request: DRFRequest, id=None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to activate a Course.
        
        Parameters:
            request: DRFRequest
                The request object.
            id: int
                The ID of the Course to activate.
            
        Returns:
            DRFResponse
                A response indicating the result of the activation operation, with course data
        """
        course: Course = self.get_course(id)
        self.check_object_permissions(request, course)

        if course.is_active:
            return DRFResponse({"detail": "Course already active"}, status=HTTP_400_BAD_REQUEST)

        course.is_active = True
        course.save()
        return DRFResponse(CourseSerializer(course).data)


    @action(
        detail=True, 
        methods=["POST"], 
        url_path="deactivate",
        url_name="deactivate_course",
    )
    def deactivate(self, request, id=None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to deactivate a Course.
        
        Parameters:
            request: DRFRequest
                The request object.
            id: int
                The ID of the Course to deactivate.
        
        Returns:
            DRFResponse
                A response indicating the result of the deactivation operation, with course data
        """
        
        course = self.get_course(id)
        self.check_object_permissions(request, course)

        if not course.is_active:
            return DRFResponse({"detail": "Course already inactive"}, status=HTTP_400_BAD_REQUEST)

        course.is_active = False
        course.save()
        return DRFResponse(CourseSerializer(course).data)


    @action(
        detail=True, 
        methods=["get"], 
        url_path="lessons",
        url_name="course_lessons",
    )
    def list_lessons(self, request, id=None):
        course = self.get_course(id)

        lessons = course.lessons.filter(deleted_at__isnull=True)
        serializer = LessonSerializer(lessons, many=True)
        return DRFResponse(serializer.data)