from django.db import models

# Create your models here.
class Course(models.Model):
    """Model representing a course."""
    
    title = models.CharField(max_length=255)
    description = models.TextField(nullable=True, blank=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='owned_courses')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class Lessons(models.Model):
    """Model representing a lesson within a course."""
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    order = models.DecimalField(max_digits=5, decimal_places=2)
    indentation = models.PositiveIntegerField(default=0)
    
    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title