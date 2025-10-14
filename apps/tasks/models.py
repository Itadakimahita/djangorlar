# Django modules
from django.db.models import (
    CharField,
    TextField,
    IntegerField,
    DateField,
    ForeignKey,
    ManyToManyField,
    UniqueConstraint,
    PROTECT,
    CASCADE,
)
from django.contrib.auth.models import User

# Project modules
from apps.abstract.models import AbstractSoftDeletableModel


class Project(AbstractSoftDeletableModel):
    """Project model."""

    NAME_MAX_LEN = 100

    name = CharField(max_length=NAME_MAX_LEN)
    author = ForeignKey(User, on_delete=PROTECT, related_name="owned_projects")
    users = ManyToManyField(User, blank=True, related_name="joined_projects")

    def __repr__(self):
        return f"Project(id={self.id}, name={self.name})"

    def __str__(self):
        return self.name


class Task(AbstractSoftDeletableModel):
    """Task model."""

    NAME_MAX_LEN = 200
    STATUS_CHOICES = [
        (1, "To Do"),
        (2, "In Progress"),
        (3, "Done"),
    ]

    name = CharField(max_length=NAME_MAX_LEN, db_index=True)
    description = TextField(blank=True, default="")
    status = IntegerField(default=1, choices=STATUS_CHOICES)
    parent = ForeignKey("self", on_delete=CASCADE, null=True, blank=True)
    project = ForeignKey(Project, on_delete=CASCADE)
    assignees = ManyToManyField(User, through="UserTask", blank=True)
    due_date = DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"


class UserTask(AbstractSoftDeletableModel):
    """Links users to tasks."""

    task = ForeignKey(Task, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["task", "user"], name="unique_task_user"),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.task.name}"


class Milestone(AbstractSoftDeletableModel):
    """Represents major checkpoints in a project."""

    title = CharField(max_length=100)
    project = ForeignKey(Project, on_delete=CASCADE, related_name="milestones")
    start_date = DateField()
    end_date = DateField()

    def __str__(self):
        return f"{self.title} ({self.project.name})"


class Comment(AbstractSoftDeletableModel):
    """User comments on tasks."""

    user = ForeignKey(User, on_delete=CASCADE)
    task = ForeignKey(Task, on_delete=CASCADE, related_name="comments")
    text = TextField()
    created_by = ForeignKey(User, on_delete=PROTECT, related_name="created_comments")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.name}"


class Label(AbstractSoftDeletableModel):
    """Labels for categorizing tasks."""

    name = CharField(max_length=50, unique=True)
    color = CharField(max_length=7, default="#FFFFFF")  # Hex color
    tasks = ManyToManyField(Task, blank=True, related_name="labels")

    def __str__(self):
        return self.name
