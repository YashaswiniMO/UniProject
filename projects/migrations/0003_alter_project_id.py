# Generated by Django 4.2.7 on 2024-11-21 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0002_remove_project_plagiarism_report_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
