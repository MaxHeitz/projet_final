from import_export import resources
from .models import Project, Status, Task, Journal


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project


class StatusResource(resources.ModelResource):
    class Meta:
        model = Status


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task


class JournalResource(resources.ModelResource):
    class Meta:
        model = Journal