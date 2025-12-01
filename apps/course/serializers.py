# Django REST Framework modules
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    IntegerField,
    Field
)

# Project modules
from apps.course.models import Course, Lessons
from apps.abstract.serializers import CustomUserForeignSerializer


class CurrentPKURLDefault:
    """Default value for the primary key URL field in serializers."""

    requires_context = True

    def __call__(self, serializer_field: Field) -> int:
        """Get the current primary key from the request."""
        assert "pk" in serializer_field.context, (
            "CurrentPKURLDefault requires 'pk' in the serializer context."
        )
        return int(serializer_field.context["pk"])

    def __repr__(self) -> str:
        """Return a string representation of the default."""
        return "%s()" % self.__class__.__name__


class CourseBaseSerializer(ModelSerializer):
    """
    Base serializer for Course instances.
    """

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Course
        fields = "__all__"


class CourseListSerializer(CourseBaseSerializer):
    """
    Serializer for listing Course instances.
    """

    users_count = SerializerMethodField(
        method_name="get_users_count",
    )
    owner = CustomUserForeignSerializer()

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Course
        fields = (
            "id",
            "title",
            "owner",
            "users_count",
        )

    def get_users_count(self, obj: Course) -> int:
        """
        Get the count of users associated with the course.

        Parameters:
            obj: Course
                The Project instance.

        Returns:
            int
                The count of users.
        """
        return getattr(obj, "users_count", 0)


class CourseCreateSerializer(CourseBaseSerializer):
    """
    Serializer for creating Course instances.
    """

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "owner",
        )


class CourseUpdateSerializer(CourseBaseSerializer):
    """
    Serializer for updating Course instances.
    """

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Course
        fields = (
            "name",
        )


class LessonsBaseSerializer(ModelSerializer):
    """
    Base serializer for Lessons instances.
    """

    status = SerializerMethodField(read_only=True)

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Lessons
        fields = "__all__"

    def get_status(self, obj: Lessons) -> dict[str, int | str]:
        """
        Get the status of the Lessons as a dictionary.

        Parameters:
            obj: Lessons
                The Lessons instance. 
        Returns:
            dict
                A dictionary containing the status id and label.
        """
        return obj.get_status_as_dict()


class LessonsListSerializer(LessonsBaseSerializer):
    """
    Serializer for listing Lessons instances.
    """

    course = CustomUserForeignSerializer(many=True)

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Lessons
        fields = (
            "id",
            "title",
            "content",
            "order",
            "indentation",
            "course",
        )


class LessonsCreateSerializer(LessonsBaseSerializer):
    """
    Serializer for creating Lessons instances.
    """

    course = IntegerField(
        source="course_id",
        default=CurrentPKURLDefault(),
        required=False,
    )

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Lessons
        fields = (
            "id",
            "title",
            "content",
            "order",
            "indentation",
            "course",
            "is_published",
        )
        read_only_fields = (
            "id",
            "course",
        )