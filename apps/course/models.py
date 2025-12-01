from django.db import models

from apps.abstract.models import AbstractBaseModel
from apps.course.validators import validate_indentation
from apps.user.models import CustomUser

# Create your models here.
class Course(AbstractBaseModel):
    """Model representing a course."""
    TITLE_MAX_LENGTH = 255
    
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_courses')
    

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['title']

    def __str__(self):
        return self.title
    
    
class Lessons(AbstractBaseModel):
    """Model representing a lesson within a course."""
    TITLE_MAX_LENGTH = 255
    
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    order = models.DecimalField(max_digits=5, decimal_places=2)
    indentation = models.PositiveIntegerField(default=0)
    
    is_published = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['order']

    def clean(self) -> None:
        """Custom validation logic to validate indentation level from 0 to 5."""
        validate_indentation(self.indentation)
        return super().clean()

    def __str__(self):
        return self.title