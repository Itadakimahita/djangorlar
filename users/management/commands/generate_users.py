# Python modules
from typing import Any
from random import choice, choices
from datetime import datetime
from random import randint
from faker import Faker

# Django modules
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet

# Project modules
from users.models import CustomUser


class Command(BaseCommand):
    help = "Generate tasks data for testing purposes"

    faker = Faker()

    def __generate_users(self, user_count: int = 100) -> None:
        """
        Generates users for testing purposes.
        """

        DEPARTAMENTS = (
            "IT",
            "HR",
            "SALES",
            "FINANCE",
            "MARKETING"
        )
        ROLES = (
            "admin",
            "manager",
            "employee"
        )

        USER_PASSWORD = make_password(password="12345")
        created_users: list[CustomUser] = []
        users_before: int = CustomUser.objects.count()
        i: int
        for i in range(user_count):
            username: str = self.faker.user_name()
            email: str = self.faker.email()
            first_name: str = self.faker.first_name()
            last_name: str = self.faker.last_name()
            phone: str = self.faker.phone_number()
            city: str = self.faker.city()
            country: str = self.faker.country()
            department: str = choice(DEPARTAMENTS)
            role: str = choice(ROLES)
            bday: datetime = self.faker.date_of_birth(minimum_age=10)
            salary: int = randint(1, 99) * 10000
            bool_rand_cond: int = randint(1, 3)
            is_active: bool = True if bool_rand_cond == 1 or bool_rand_cond == 3 else False
            is_staff: bool = True if bool_rand_cond == 2 or bool_rand_cond == 3 else False

            created_users.append(
                CustomUser(
                    username=username,
                    email=email,
                    password=USER_PASSWORD,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    city=city,
                    country=country,
                    department=department,
                    role=role,
                    birth_date=bday,
                    salary=salary,
                    is_staff=is_staff,
                    is_active=is_active
                )
            )

        CustomUser.objects.bulk_create(created_users, ignore_conflicts=True, batch_size=1000)
        users_after: int = CustomUser.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {users_after - users_before} users."
            )
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Command entry point."""

        start_time: datetime = datetime.now()

        self.__generate_users(user_count=10000)

        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                (datetime.now() - start_time).total_seconds()
            )
        )

