from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("resources/", views.resources, name="resources"),
    path("roadmap/", views.roadmap, name="roadmap"),
    path("roadmap/complete/<int:task_id>/", views.complete_task, name="complete_task"),
    path("certificates/", views.certificates, name="certificates"),
    path("certificates/review/<int:certificate_id>/", views.review_certificate, name="review_certificate"),
    path("certificates/achievement/", views.achievement_pdf, name="achievement_pdf"),
    path("courses/", views.courses, name="courses"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
