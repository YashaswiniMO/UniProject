from django import forms
from .models import Forum
from .models import Message


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'file']  # Allow text and file uploads
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Type your message here...',
                'rows': 3,
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,application/pdf,application/zip,application/jpeg,application/doc,application/ppt,application/msword',
            }),
        }

    def save(self, commit=True):
        message = super().save(commit=False)
        message.forum = self.instance.forum  # Ensure the forum is set on the message
        if commit:
            message.save()
        return message