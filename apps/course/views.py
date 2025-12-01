# Python modules
from typing import Any

# Django modules
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet, Count

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
from apps.course.serializers import (
    CourseBaseSerializer,
    CourseListSerializer,
    CourseCreateSerializer,   
    CourseUpdateSerializer,
    ListListSerializer,
    ListCreateSerializer,
)

class CourseViewSet(ViewSet):
    """
    ViewSet for handling Course-related endpoints.
    """

    # permission_classes = (IsAuthenticated,)
    serializer_class = CourseBaseSerializer


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
            Course: Course = Course.objects.get(id=kwargs["pk"])
        except Course.DoesNotExist:
            return DRFResponse(
                data={
                    "pk": [f"Course with id={kwargs['pk']} does not exist."]
                },
                status=HTTP_404_NOT_FOUND
            )

        serializer: CourseUpdateSerializer = CourseUpdateSerializer(
            data=request.data,
            instance=Course,
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
            Course: Course = Course.objects.get(id=kwargs["pk"])
        except Course.DoesNotExist:
            return DRFResponse(
                data={
                    "pk": [f"Course with id={kwargs['pk']} does not exist."]
                },
                status=HTTP_404_NOT_FOUND
            )

        Course.delete()

        return DRFResponse(
            status=HTTP_204_NO_CONTENT
        )

    @action(
        methods=("GET",),
        detail=True,
        url_name="Lists",
        url_path="Lists",
        # permission_classes=(IsAuthenticated, IsUserInCourse,)
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
            data=ListListSerializer(
                Course.Lists.prefetch_related("owner").all(),
                many=True,
            ).data,
            status=HTTP_200_OK
        )

    @action(
        methods=("POST",),
        detail=True,
        url_name="create_List",
        url_path="create-List",
        permission_classes=(IsAuthenticated,),
    )
    def create_List(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to create a new List for a specific Course.

        Parameters:
            request: DRFRequest
                The request object.
            *args: list
                Additional positional arguments.
            **kwargs: dict
                Additional keyword arguments.
        Returns:
            DRFResponse
                A response indicating the result of the List creation operation.
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


        serializer: ListCreateSerializer = ListCreateSerializer(
            data=request.data,
            context={
                "pk": kwargs["pk"],
                "request": request,
            }
        )

        serializer.is_valid(raise_exception=True)

        List: List = serializer.save()
        UserList.objects.create(
            List_id=List.id,
            user_id=request.user.id,
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )