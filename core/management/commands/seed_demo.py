from django.core.management.base import BaseCommand
from core.models import RoadmapTask, Course

class Command(BaseCommand):
    help = "Add starter roadmap tasks and course links"

    def handle(self, *args, **kwargs):
        data = {
            "Python": [
                ("Programming fundamentals", "Variables, loops and functions."),
                ("Python OOP", "Classes, objects and inheritance."),
                ("SQL basics", "Queries and relational databases."),
                ("NumPy and Pandas", "Data analysis foundations."),
                ("Build a Python project", "Create a portfolio project."),
            ],
            "Java": [
                ("Java fundamentals", "Syntax and control flow."),
                ("Object-oriented programming", "Classes and inheritance."),
                ("Data structures", "Arrays, stacks and queues."),
                ("SQL and JDBC", "Database connectivity."),
                ("Build a Java project", "Create a portfolio project."),
            ],
            "Web Development": [
                ("HTML and CSS", "Build responsive pages."),
                ("JavaScript", "Learn DOM basics."),
                ("Django", "Build backend applications."),
                ("SQL", "Learn database design."),
                ("Deploy a project", "Publish your application."),
            ],
        }

        for skill, tasks in data.items():
            for i, (title, desc) in enumerate(tasks, 1):
                RoadmapTask.objects.get_or_create(
                    skill=skill,
                    title=title,
                    defaults={
                        "description": desc,
                        "year": min(4, (i + 1) // 2),
                        "order": i
                    }
                )

        Course.objects.get_or_create(
            title="NPTEL course catalogue",
            defaults={
                "provider": "NPTEL",
                "skill": "Python",
                "url": "https://nptel.ac.in/courses",
                "description": "Browse available courses."
            }
        )

        self.stdout.write(self.style.SUCCESS("Starter content added."))
