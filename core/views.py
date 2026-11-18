import uuid
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from .models import (
    StudentProfile, Resource, RoadmapTask,
    Progress, Course, Certificate, Achievement
)
from .ai_engine import recommend_next, skill_gaps


def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Username and password are required.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            StudentProfile.objects.create(user=user)
            login(request, user)
            return redirect("dashboard")

    return render(request, "register.html")


def user_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)

    completed = Progress.objects.filter(
        user=request.user,
        completed=True
    ).select_related("task")

    titles = [p.task.title for p in completed]

    next_step = recommend_next(profile.interest, titles)
    gaps = skill_gaps(profile.interest, titles)

    total = RoadmapTask.objects.filter(skill=profile.interest).count()
    done = sum(
        1 for p in completed
        if p.task.skill == profile.interest
    )

    percent = round(done * 100 / total) if total else 0

    certificates = Certificate.objects.filter(user=request.user)

    return render(request, "dashboard.html", {
        "profile": profile,
        "completed": completed,
        "next_step": next_step,
        "gaps": gaps,
        "percent": percent,
        "certificates": certificates,
    })


@login_required
def resources(request):
    query = request.GET.get("q", "")
    items = Resource.objects.all()

    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query)
        )

    return render(request, "resources.html", {
        "items": items,
        "query": query
    })


@login_required
def roadmap(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.interest = request.POST.get("skill", "Python")
        profile.year = int(request.POST.get("year", 1))
        profile.career_goal = request.POST.get("career_goal", "")
        profile.save()
        return redirect("roadmap")

    tasks = RoadmapTask.objects.filter(skill=profile.interest)

    progress = {
        p.task_id: p.completed
        for p in Progress.objects.filter(user=request.user, task__in=tasks)
    }

    return render(request, "roadmap.html", {
        "profile": profile,
        "tasks": tasks,
        "progress": progress
    })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(RoadmapTask, id=task_id)

    if request.method == "POST":
        obj, _ = Progress.objects.get_or_create(
            user=request.user,
            task=task
        )
        obj.completed = not obj.completed
        obj.save()

    return redirect("roadmap")


@login_required
def certificates(request):
    if request.method == "POST":
        uploaded = request.FILES.get("file")

        if not uploaded or uploaded.size > 5 * 1024 * 1024:
            messages.error(request, "Choose a file smaller than 5 MB.")

        elif Path(uploaded.name).suffix.lower() not in [
            ".pdf", ".png", ".jpg", ".jpeg"
        ]:
            messages.error(request, "Only PDF and image files are allowed.")

        else:
            cert = Certificate.objects.create(
                user=request.user,
                course_name=request.POST.get("course_name", "Course"),
                provider=request.POST.get("provider", "NPTEL"),
                file=uploaded
            )

            try:
                import pytesseract
                from PIL import Image

                if cert.file.name.lower().endswith(
                    (".png", ".jpg", ".jpeg")
                ):
                    cert.extracted_text = pytesseract.image_to_string(
                        Image.open(cert.file.path)
                    )
                    cert.save()

            except Exception:
                pass

            messages.success(
                request,
                "Certificate submitted for admin review."
            )
            return redirect("certificates")

    items = Certificate.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    return render(request, "certificates.html", {"items": items})


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def review_certificate(request, certificate_id):
    cert = get_object_or_404(Certificate, id=certificate_id)

    if request.method == "POST":
        status = request.POST.get("status")

        if status in ["Approved", "Rejected"]:
            cert.status = status
            cert.save()

            if status == "Approved":
                Achievement.objects.get_or_create(
                    user=cert.user,
                    title=cert.course_name,
                    defaults={
                        "certificate_id": str(uuid.uuid4())[:12].upper()
                    }
                )

        return redirect("admin:index")

    return render(request, "review.html", {"cert": cert})


@login_required
def courses(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    items = Course.objects.filter(skill__icontains=profile.interest)

    return render(request, "courses.html", {
        "items": items,
        "skill": profile.interest
    })


@login_required
def achievement_pdf(request):
    from reportlab.pdfgen import canvas

    achievements = Achievement.objects.filter(
        user=request.user
    ).order_by("-issued_at")

    if not achievements.exists():
        messages.info(request, "No approved achievements yet.")
        return redirect("certificates")

    item = achievements.first()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="EduPath-Achievement.pdf"'
    )

    pdf = canvas.Canvas(response)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(300, 740, "EduPath Achievement Certificate")

    pdf.setFont("Helvetica", 15)
    pdf.drawCentredString(300, 670, "This recognizes the achievement of")

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(
        300, 620,
        request.user.get_full_name() or request.user.username
    )

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(300, 560, item.title)
    pdf.drawCentredString(300, 500, "Platform achievement recognition")
    pdf.drawCentredString(300, 450, "Certificate ID: " + item.certificate_id)
    pdf.drawCentredString(
        300, 420,
        item.issued_at.strftime("%d %B %Y")
    )

    pdf.save()
    return response
