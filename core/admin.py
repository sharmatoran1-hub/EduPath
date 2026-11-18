from django.contrib import admin
from .models import (
    StudentProfile, Resource, RoadmapTask,
    Progress, Course, Certificate, Achievement
)

admin.site.register(StudentProfile)
admin.site.register(Resource)
admin.site.register(RoadmapTask)
admin.site.register(Progress)
admin.site.register(Course)
admin.site.register(Certificate)
admin.site.register(Achievement)
