from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100, blank=True)
    year = models.PositiveSmallIntegerField(default=1)
    interest = models.CharField(max_length=100, default="Python")
    career_goal = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.user.username

class Resource(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    semester = models.PositiveSmallIntegerField(default=1)
    category = models.CharField(max_length=30, choices=[
        ("Notes", "Notes"), ("PYQ", "Previous Year Paper")
    ])
    file = models.FileField(upload_to="resources/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class RoadmapTask(models.Model):
    skill = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["year", "order"]

    def __str__(self):
        return self.title

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(RoadmapTask, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "task"],
                name="unique_user_task"
            )
        ]

class Course(models.Model):
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=100, default="NPTEL")
    skill = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200)
    provider = models.CharField(max_length=100)
    file = models.FileField(upload_to="certificates/")
    extracted_text = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        default="Pending",
        choices=[
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Rejected", "Rejected")
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    certificate_id = models.CharField(max_length=40, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
