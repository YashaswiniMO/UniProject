# Generated by Django 4.2.7 on 2024-11-21 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("teams", "__first__"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                (
                    "technologies_used",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "project_progress",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("plagiarism_score", models.FloatField(blank=True, null=True)),
                ("plagiarism_report", models.TextField(blank=True, null=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("date_due", models.DateField(blank=True, null=True)),
                ("completed", models.BooleanField(default=False)),
                ("date_completed", models.DateField(blank=True, null=True)),
                (
                    "completed_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="completed_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="modified_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="teams.team"
                    ),
                ),
            ],
        ),
    ]
