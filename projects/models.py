from datetime import date

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from teams.models import Team


class Project(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    technologies_used = models.CharField(max_length=100, blank=True, null=True)
    project_progress = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    plagiarism_score = models.FloatField(null=True, blank=True)  # Score in percentage
    most_similar_project = models.CharField(max_length=255, null=True, blank=True)  # Name of the most similar project
    
    uploaded_zip = models.FileField(upload_to='uploads/code_zips/', null=True, blank=True)  # ZIP for code
    uploaded_report = models.FileField(upload_to='uploads/reports/', null=True, blank=True)  # Report file
    
    plagiarism_score_code = models.FloatField(default=0)  # Plagiarism score for code
    plagiarism_score_report = models.FloatField(default=0)  # Plagiarism score for report
    most_similar_code_project = models.CharField(max_length=255, null=True, blank=True)  # Most similar project for code
    most_similar_report_project = models.CharField(max_length=255, null=True, blank=True)  # Most similar project for report

    report_text = models.TextField(blank=True, null=True)  # Store processed report text
    code_text = models.TextField(blank=True, null=True)  # Store processed code text

    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_projects",
    )  # Set to current user on form validations
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="modified_projects",
    )  # Set to current user on form validation
    date_due = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)
    completed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="completed_projects",
    )  # Set to current user on form validation

    @property
    def days_till_due(self):
        if self.date_due:
            difference = self.date_due - date.today()
            return difference.days
        return None

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk})

    # Authorization methods
    def team_has_member(self, user):
        return user in self.team.members.all()

    def leader_is(self, user):
        return user == self.team.leader

    def was_created_by(self, user):
        return user == self.created_by
