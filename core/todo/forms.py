from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'deadline', 'is_completed', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Force sync from status → is_completed
        if instance.status == 'completed':
            instance.is_completed = True
        else:
            instance.is_completed = False

        # Optional fallback if status wasn't set, but checkbox was toggled
        if not instance.status:
            instance.status = 'completed' if instance.is_completed else 'in progress'

        if commit:
            instance.save()
        return instance


