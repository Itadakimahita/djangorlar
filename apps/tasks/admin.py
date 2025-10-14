# Python modules
from typing import Optional, Sequence

# Django modules
from django.contrib.admin import ModelAdmin, register
from django.core.handlers.wsgi import WSGIRequest

# Project modules
from apps.tasks.models import (
    Project,
    Task,
    UserTask,
    Milestone,
    Comment,
    Label,
)


@register(Project)
class ProjectAdmin(ModelAdmin):
    """
    Project admin configuration class.
    """

    list_display = (
        "id",
        "name",
        "author",
        "created_at",
    )
    list_display_links = ("id",)
    list_per_page = 50
    search_fields = ("id", "name",)
    ordering = ("-updated_at",)
    list_filter = ("updated_at",)
    readonly_fields = ("created_at", "updated_at", "deleted_at",)
    filter_horizontal = ("users",)
    save_on_top = True

    fieldsets = (
        (
            "Project Information",
            {"fields": ("name", "author", "users",)},
        ),
        (
            "Date and Time Information",
            {"fields": ("created_at", "updated_at", "deleted_at",)},
        ),
    )

    def has_add_permission(self, request: WSGIRequest) -> bool:
        """Disable add permission."""
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: Optional[Project] = None) -> bool:
        """Disable delete permission."""
        return False

    def has_change_permission(self, request: WSGIRequest, obj: Optional[Project] = None) -> bool:
        """Disable change permission."""
        return False

@register(Task)
class TaskAdmin(ModelAdmin):
    """
    Task admin configuration class.
    """

    list_display = (
        "id",
        "name",
        "project",
        "status",
        "due_date",
        "display_assignees",
        "created_at",
    )
    list_display_links = ("id",)
    list_per_page = 50
    search_fields = ("id", "name", "project__name",)
    ordering = ("-updated_at",)
    list_filter = ("status", "project", "updated_at",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
        "display_assignees",
    )
    save_on_top = True

    fieldsets = (
        (
            "Task Information",
            {
                "fields": (
                    "name",
                    "project",
                    "status",
                    "parent",
                    "due_date",
                    "description",
                    "display_assignees",
                )
            },
        ),
        (
            "Date and Time Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            },
        ),
    )

    def display_assignees(self, obj: Task) -> str:
        """Display assigned users (read-only)."""
        return ", ".join([user.username for user in obj.assignees.all()])

    display_assignees.short_description = "Assignees"



@register(UserTask)
class UserTaskAdmin(ModelAdmin):
    """
    UserTask admin configuration class.
    """

    list_display = (
        "id",
        "task",
        "user",
        "created_at",
    )
    list_display_links = ("id",)
    list_per_page = 50
    search_fields = ("task__name", "user__username",)
    ordering = ("-updated_at",)
    list_filter = ("user", "task__project", "updated_at",)
    readonly_fields = ("created_at", "updated_at", "deleted_at",)
    save_on_top = True

    fieldsets = (
        (
            "UserTask Information",
            {"fields": ("task", "user",)},
        ),
        (
            "Date and Time Information",
            {"fields": ("created_at", "updated_at", "deleted_at",)},
        ),
    )


@register(Milestone)
class MilestoneAdmin(ModelAdmin):
    """
    Milestone admin configuration class.
    """

    list_display = (
        "id",
        "title",
        "project",
        "start_date",
        "end_date",
        "created_at",
    )
    list_display_links = ("id",)
    list_per_page = 50
    search_fields = ("id", "title", "project__name",)
    ordering = ("-updated_at",)
    list_filter = ("project", "start_date", "end_date",)
    readonly_fields = ("created_at", "updated_at", "deleted_at",)
    save_on_top = True

    fieldsets = (
        (
            "Milestone Information",
            {"fields": ("title", "project", "start_date", "end_date",)},
        ),
        (
            "Date and Time Information",
            {"fields": ("created_at", "updated_at", "deleted_at",)},
        ),
    )


@register(Comment)
class CommentAdmin(ModelAdmin):
    """
    Comment admin configuration class.
    """

    list_display = (
        "id",
        "user",
        "task",
        "created_at",
    )
    list_display_links = ("id",)
    list_per_page = 50
    search_fields = ("text", "task__name", "user__username",)
    ordering = ("-updated_at",)
    list_filter = ("user", "task__project",)
    readonly_fields = ("created_at", "updated_at", "deleted_at",)
    save_on_top = True

    fieldsets = (
        (
            "Comment Information",
            {"fields": ("user", "task", "text", "created_by",)},
        ),
        (
            "Date and Time Information",
            {"fields": ("created_at", "updated_at", "deleted_at",)},
        ),
    )


@register(Label)
class LabelAdmin(ModelAdmin):
    """
    Label admin configuration class.
    """

    list_display = (
        "id",
        "name",
        "color",
        "created_at",
    )
    list_display_links = ("id",)
    list_per_page = 50
    search_fields = ("id", "name",)
    ordering = ("-updated_at",)
    list_filter = ("updated_at",)
    readonly_fields = ("created_at", "updated_at", "deleted_at",)
    filter_horizontal = ("tasks",)
    save_on_top = True

    fieldsets = (
        (
            "Label Information",
            {"fields": ("name", "color", "tasks",)},
        ),
        (
            "Date and Time Information",
            {"fields": ("created_at", "updated_at", "deleted_at",)},
        ),
    )
