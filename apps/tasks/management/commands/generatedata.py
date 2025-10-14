# Python modules
from typing import Any
from random import choice, choices, randint
from datetime import datetime, timedelta

# Django modules
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import QuerySet

# Project modules
from apps.tasks.models import (
    Task,
    Project,
    UserTask,
    Milestone,
    Comment,
    Label,
)


class Command(BaseCommand):
    """
    Generates sample data for testing the tasks app.
    """

    help = "Generate tasks data for testing purposes"

    EMAIL_DOMAINS = (
        "example.com",
        "test.com",
        "sample.org",
        "demo.net",
        "mail.com",
    )
    SOME_WORDS = (
        "lorem",
        "ipsum",
        "dolor",
        "sit",
        "amet",
        "consectetur",
        "adipiscing",
        "elit",
        "sed",
        "do",
        "eiusmod",
        "tempor",
        "incididunt",
        "ut",
        "labore",
        "et",
        "dolore",
        "magna",
        "aliqua",
    )
    STATUS_CHOICES = [1, 2, 3]

    def __generate_users(self, user_count: int = 100) -> None:
        """Generates users for testing purposes."""
        USER_PASSWORD = make_password(password="12345")
        created_users: list[User] = []
        users_before: int = User.objects.count()

        for i in range(user_count):
            username: str = f"user{i+1}"
            email: str = f"user{i+1}@{choice(self.EMAIL_DOMAINS)}"
            created_users.append(
                User(username=username, email=email, password=USER_PASSWORD)
            )

        User.objects.bulk_create(created_users, ignore_conflicts=True)
        users_after: int = User.objects.count()

        self.stdout.write(
            self.style.SUCCESS(f"Created {users_after - users_before} users.")
        )

    def __generate_projects(self, project_count: int = 50) -> None:
        """Generates projects for testing purposes."""
        created_projects: list[Project] = []
        projects_before: int = Project.objects.count()
        users: QuerySet[User] = User.objects.all()

        for i in range(project_count):
            name: str = " ".join(choices(self.SOME_WORDS, k=3)).capitalize()
            author: User = choice(users)
            created_projects.append(Project(name=name, author=author))

        Project.objects.bulk_create(created_projects, ignore_conflicts=True)

        # Add random members
        for project in Project.objects.all():
            project.users.add(*choices(users, k=randint(3, 10)))

        projects_after: int = Project.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {projects_after - projects_before} projects.")
        )

    def __generate_tasks(self, task_count: int = 500) -> None:
        """Generates tasks for projects."""
        created_tasks: list[Task] = []
        tasks_before: int = Task.objects.count()
        projects: QuerySet[Project] = Project.objects.all()
        users: QuerySet[User] = User.objects.all()

        for i in range(task_count):
            name: str = " ".join(choices(self.SOME_WORDS, k=4)).capitalize()
            project: Project = choice(projects)
            status: int = choice(self.STATUS_CHOICES)
            due_date = datetime.now().date() + timedelta(days=randint(1, 60))

            created_tasks.append(
                Task(
                    name=name,
                    project=project,
                    status=status,
                    description=" ".join(choices(self.SOME_WORDS, k=10)),
                    due_date=due_date,
                )
            )

        Task.objects.bulk_create(created_tasks, ignore_conflicts=True)

        # Assign random users to each task via UserTask
        for task in Task.objects.all():
            assigned_users = choices(users, k=randint(1, 3))
            for user in assigned_users:
                UserTask.objects.get_or_create(task=task, user=user)

        tasks_after: int = Task.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {tasks_after - tasks_before} tasks.")
        )

    def __generate_milestones(self, milestone_count: int = 100) -> None:
        """Generates milestones for projects."""
        created_milestones: list[Milestone] = []
        projects = Project.objects.all()
        milestones_before = Milestone.objects.count()

        for i in range(milestone_count):
            project = choice(projects)
            start = datetime.now().date() + timedelta(days=randint(0, 30))
            end = start + timedelta(days=randint(5, 20))
            title = f"Milestone {i+1}: {' '.join(choices(self.SOME_WORDS, k=2)).capitalize()}"
            created_milestones.append(
                Milestone(title=title, project=project, start_date=start, end_date=end)
            )

        Milestone.objects.bulk_create(created_milestones, ignore_conflicts=True)

        milestones_after = Milestone.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {milestones_after - milestones_before} milestones."
            )
        )

    def __generate_labels(self, label_count: int = 20) -> None:
        """Generates task labels."""
        colors = ["#FF5733", "#33FF57", "#3357FF", "#FFC300", "#FF33A8"]
        created_labels: list[Label] = []
        labels_before: int = Label.objects.count()

        for i in range(label_count):
            name = f"Label {i+1}"
            color = choice(colors)
            created_labels.append(Label(name=name, color=color))

        Label.objects.bulk_create(created_labels, ignore_conflicts=True)

        # Randomly tag tasks
        tasks = list(Task.objects.all())
        for label in Label.objects.all():
            label.tasks.add(*choices(tasks, k=randint(5, 20)))

        labels_after = Label.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {labels_after - labels_before} labels.")
        )

    def __generate_comments(self, comment_count: int = 500) -> None:
        """Generates comments for tasks."""
        created_comments: list[Comment] = []
        tasks: QuerySet[Task] = Task.objects.all()
        users: QuerySet[User] = User.objects.all()
        comments_before = Comment.objects.count()

        for i in range(comment_count):
            user = choice(users)
            task = choice(tasks)
            created_comments.append(
                Comment(
                    user=user,
                    task=task,
                    text=" ".join(choices(self.SOME_WORDS, k=12)),
                    created_by=user,
                )
            )

        Comment.objects.bulk_create(created_comments, ignore_conflicts=True)
        comments_after = Comment.objects.count()

        self.stdout.write(
            self.style.SUCCESS(f"Created {comments_after - comments_before} comments.")
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Command entry point."""
        start_time: datetime = datetime.now()

        self.__generate_users(user_count=200)
        self.__generate_projects(project_count=100)
        self.__generate_tasks(task_count=500)
        self.__generate_milestones(milestone_count=150)
        self.__generate_labels(label_count=30)
        self.__generate_comments(comment_count=800)

        self.stdout.write(
            self.style.SUCCESS(
                f"The whole process took {(datetime.now() - start_time).total_seconds():.2f} seconds."
            )
        )
