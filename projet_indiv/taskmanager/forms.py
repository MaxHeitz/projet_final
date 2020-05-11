from django.forms import forms, ModelForm

from taskmanager.models import Task, Journal, Project


# Different forms

# A form based on the Task model
class NewTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'


# A form based on the Journal model
class NewJournalForm(ModelForm):
    class Meta:
        model = Journal
        exclude = ('date',)  # Date/time auto-filled with the current date/time

#A form based on the Project model
class NewProjectForm(ModelForm):
    class Meta:
        model= Project
        fields = '__all__'
