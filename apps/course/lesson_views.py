from typing import Any

# Django modules
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, DRFHttpResponse
from django.db.models import QuerySet, Count
from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import DRFResponse as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN
)
from rest_framework.decorators import action


from apps.course.models import Course, Lessons
from apps.course.permission import IsCourseOwner
from apps.course.serializers import LessonSerializer, LessonCreateSerializer


class LessonViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def get_lesson(self, id):
        return get_object_or_404(Lessons.objects.select_related("course"), id=id)

    def ensure_owner(self, request: DRFRequest, lesson: Lessons):
        if lesson.course.owner != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not the owner of this course.")


    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle creating a new lesson at the beginning of the course.
        
        Parameters:
            - request: DRF Request object containing lesson data.
            
        Returns:
            - DRFResponse with the created lesson data or error message.
        """
        course_id = request.data.get("course_id")
        if not course_id:
            return DRFResponse({"detail": "course_id is required"}, status=HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)

        if course.owner != request.user:
            return DRFResponse({"detail": "You are not the owner"}, status=HTTP_403_FORBIDDEN)

        Lessons.objects.filter(course=course).update(order=models.F("order") + 1)

        serializer = LessonCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson = Lessons.objects.create(
            course=course,
            title=serializer.validated_data["title"],
            content=serializer.validated_data["content"],
            order=0,         
            indentation=0,   
        )

        return DRFResponse(LessonSerializer(lesson).data, status=HTTP_201_CREATED)


    @action(
        detail=True, 
        methods=["put"], 
        url_path="move",
        url_name="move_lesson"
        )
    def move(self, request: DRFRequest, id: int=None) -> DRFResponse:
        """
        Handle PUT moving a lesson to a new position within its course.
        
        Parameters:
            - request: DRF Request object containing the new position data.
            - id: int - The ID of the lesson to move.
        
        Returns:
            - DRFResponse with the new order of the lesson.
        """
        lesson = self.get_lesson(id)
        self.ensure_owner(request, lesson)

        before_id = request.data.get("before_lesson_id")

        lessons = Lessons.objects.filter(course=lesson.course).order_by("order")

        if before_id is None:
            last_order = lessons.last().order if lessons.exists() else 0
            lesson.order = last_order + 1
        else:
            before_lesson = get_object_or_404(Lessons, id=before_id, course=lesson.course)
            new_order = before_lesson.order

            for l in lessons:
                if l.order >= new_order:
                    l.order += 1
                    l.save()

            lesson.order = new_order

        prev = (
            Lessons.objects
            .filter(course=lesson.course, order__lt=lesson.order)
            .order_by("-order")
            .first()
        )
        lesson.indentation = prev.indentation if prev else 0

        lesson.save()

        return DRFResponse({"new_order": lesson.order})


    def destroy(self, request: DRFRequest, id: int=None) -> DRFResponse:
        """
        Handle DELETE requests to delete a Lesson.
        
        Parameters:
            request: DRFRequest
                The request object.
            id: int
                The ID of the Lesson to delete.
        
        Returns:
            DRFResponse
                A response indicating the result of the deletion operation.
        """
        lesson = self.get_lesson(id)
        self.ensure_owner(request, lesson)

        lesson.delete()
        return DRFResponse(status=HTTP_204_NO_CONTENT)

    @action(
        detail=True, 
        methods=["post"], 
        url_path="publish",
        url_name="publish_lesson"
        )
    def publish(self, request: DRFRequest, id: int=None) -> DRFResponse:
        """
        Handle POST requests to publish a Lesson.
        
        Parameters:
            request: DRFRequest
                The request object.
            id: int
                The ID of the Lesson to publish.
        
        Returns:
            DRFResponse
                A response indicating the result of the publish operation, with lesson data
        """
        lesson = self.get_lesson(id)
        self.ensure_owner(request, lesson)

        lesson.is_published = True
        lesson.save()
        return DRFResponse(LessonSerializer(lesson).data)


    @action(detail=True, 
            methods=["post"], 
            url_path="unpublish",
            url_name="unpublish_lesson"
            )
    def unpublish(self, request: DRFRequest, id: int=None) -> DRFResponse:
        """
        Handle POST requests to unpublish a Lesson.
        
        Parameters:
            request: DRFRequest
                The request object.
            id: int
                The ID of the Lesson to unpublish.
                
        Returns:
            DRFResponse
                A response indicating the result of the unpublish operation, with lesson data
        """
        lesson = self.get_lesson(id)
        self.ensure_owner(request, lesson)

        lesson.is_published = False
        lesson.save()
        return DRFResponse(LessonSerializer(lesson).data)
