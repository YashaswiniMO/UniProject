from datetime import date
from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.views import View, generic
from comments import forms as comment_forms
from comments import views as comment_views
from tasks.views import TaskCreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from .models import Project
import requests 
from django.contrib import messages
from projects.utils import calculate_cosine_similarity
import tempfile


class ProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of all user projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.all()


class ActiveProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of users active projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(team__members=self.request.user).filter(
            completed=False
        )


class CompletedProjectListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of users completed projects"""

    model = Project

    def get_queryset(self):
        return Project.objects.filter(team__members=self.request.user).filter(
            completed=True
        )


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get(self, request, *args, **kwargs):
        view = ProjectDetailDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = comment_views.PostProjectComment.as_view()
        return view(request, *args, **kwargs)
    
class ProjectDetailDisplay(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = comment_forms.ProjectCommentForm(
            user=self.request.user
        )
        return context
    



class ProjectCreateView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.CreateView,
):
    model = Project
    form_class = forms.ProjectForm
    success_message = "Project #%(id)s was created successfully"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
    # Assign user-related metadata
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        form.instance.technologies_used = form.cleaned_data["technologies_used"]

    # Perform plagiarism check
        new_project_description = form.cleaned_data.get('description')
        existing_projects = Project.objects.exclude(pk=form.instance.pk)  # Exclude the current project if updating

        try:
            similarity, most_similar = calculate_cosine_similarity(new_project_description, existing_projects)
        
        # Save plagiarism results to the instance
            form.instance.plagiarism_score = similarity
            form.instance.most_similar_project = most_similar

            # Log an informational message if no similar projects are found
            if most_similar is None:
                messages.info(self.request, "No similar projects found.")
        except ValueError as e:
        # Handle specific errors from the similarity calculation
            messages.error(self.request, f"Error during plagiarism check: {str(e)}")

    # Save the project and return the response
        return super().form_valid(form)


    

class ProjectUpdateView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = Project
    form_class = forms.ProjectForm
    success_message = "Project #%(id)s was updated successfully"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.technologies_used = form.cleaned_data["technologies_used"]
        form.instance.project_progress = form.cleaned_data["project_progress"]
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        user = self.request.user

        if project.was_created_by(user):
            return True
        return project.leader_is(user)


class ProjectCompleteView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = Project
    form_class = forms.CompleteProjectForm
    initial = {
        "date_completed": date.today(),
    }
    success_message = "Project #%(id)s completed"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.completed = True
        form.instance.completed_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        user = self.request.user

        if project.was_created_by(user):
            return True
        return project.leader_is(user)


class ProjectDeleteView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView,
):
    model = Project
    success_url = "/projects"

    def test_func(self):
        project = self.get_object()
        user = self.request.user

        if user.profile.is_demo_user:
            return False
        if project.was_created_by(user):
            return True
        return project.leader_is(user)


class ProjectAddTaskView(TaskCreateView):
    success_message = (
        "Task #{task_id} was successfully added to project #{project_id}."
    )

    def get_initial(self):
        initial = super().get_initial()

        project_pk = self.kwargs["pk"]
        # project = Project.objects.get(pk=project_pk)

        initial["project"] = project_pk
        return initial

    def get_success_message(self, cleaned_data):
        return self.success_message.format(
            task_id=self.object.id, project_id=self.kwargs["pk"]
        )

def check_plagiarism(text):
    # Replace with actual API call or library for plagiarism detection
    # Example for Copyscape API (pseudo-code):
    api_url = "https://plagiarism-check-api.com/check"
    response = requests.post(api_url, data={"text": text})
    if response.status_code == 200:
        result = response.json()
        return result['similarity'], result.get('report_url', '')
    return None, None

def form_valid(self, form):
    # Debugging: Check if files are being received
    print("Uploaded ZIP file:", self.request.FILES.get('uploaded_zip'))
    print("Uploaded Report file:", self.request.FILES.get('uploaded_report'))

    form.instance.created_by = self.request.user
    form.instance.modified_by = self.request.user

    # Debugging: Check instance files
    print("Before saving: ZIP -", form.instance.uploaded_zip)
    print("Before saving: Report -", form.instance.uploaded_report)

    return super().form_valid(form)
