from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from taskmanager.models import Project, Task, Journal, Status
from taskmanager.forms import NewTaskForm, NewJournalForm, NewProjectForm
from django.http import HttpResponse
from .resources import ProjectResource, StatusResource, TaskResource, JournalResource


# Create your views here.


def projectprogress(project):
    list_tasks = Task.objects.filter(project=project)
    i = 0
    progress = 0
    for task in list_tasks:
        i += 1
        progress += task.progress
    if i == 0:
        i = 1
    return (int(progress / i))


# View for the list of projects
@login_required
def projects(request):
    user = request.user
    projects=Project.objects.filter(members=user)
    list_projects = []  # Each cell of list_projects will contains information about a project
    infos = []  # the info cell of a project
    count = 0
    for project in Project.objects.filter(members=user):
        infos.append(
            list(Project.objects.filter(members=user))[count])  # 1st cell of infos contains the members of the project
        infos.append(Task.objects.filter(project=project))  # 2nd cell of infos contains the tasks of the project
        infos.append(Task.objects.filter(project=project).order_by(
            "due_date"))  # 3rd cell of infos contains the tasks of the project ordered by due_date
        infos.append(projectprogress(project))
        list_projects.append(infos)  # add the infos cells in the list of projects
        infos = []
        count += 1
    return render(request, 'list_projects.html', locals())


# View for the display of a project and its details
@login_required
def project(request, id_project):
    user = request.user
    projects=Project.objects.filter(members=user)
    project = Project.objects.get(id=id_project)
    list_tasks = Task.objects.filter(project=project)  # List of the tasks of this project
    progress = projectprogress(project)
    members=project.members.all()

    # # Now we apply more filters if the user requested some...

    list_tasks, status_q_list, query_list, date1, date2, date3, date4, project_query = filters(request, list_tasks)
    list_tasks = ordering(request, list_tasks)
    # Needed for the template and form...
    Status_all = Status.objects.all()
    return render(request, 'project.html', locals())


# View for the display of a task and its details
@login_required
def task(request, id_task):
    user = request.user
    projects=Project.objects.filter(members=user)
    task = Task.objects.get(id=id_task)
    project = Project.objects.get(id=task.project.id)
    list_journals = Journal.objects.filter(task=task)  # List of the Journal entries of this task
    if request.method == "POST":
        message = request.POST["message"]
        user = request.user
        task = Task.objects.get(id=id_task)
        date = datetime.now()
        comment = Journal.objects.create(entry=message, author=user,date=date, task=task)
        comment.save()
        return redirect('/task/'+str(task.id))
    return render(request, 'task.html', locals())


# View to fill a form to create a task and add it to the database
@login_required
def newtask(request):
    projects=Project.objects.filter(members=request.user)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTaskForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            project = form['project'].value()
            return redirect('/task/'+str(form.instance.id))  # if the form is valid, save it in database and display the new task
        else:  # if not, initialize the form and display the form
            form = NewTaskForm()
            list_projects = Project.objects.all()
            list_users = User.objects.all()
            list_status = Status.objects.all()
            return render(request, 'newtask.html', locals())

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTaskForm()
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'newtask.html', locals())


# View to update a task
@login_required
def updatetask(request, id_task):
    projects=Project.objects.filter(members=request.user)
    utask = Task.objects.get(id=id_task)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTaskForm(request.POST, instance=utask)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            # Get the data from the form
            utask.project = form.cleaned_data['project']
            utask.name = form.cleaned_data['name']
            utask.description = form.cleaned_data['description']
            utask.assignee = form.cleaned_data['assignee']
            utask.due_date = form.cleaned_data['due_date']
            utask.start_date = form.cleaned_data['start_date']
            utask.priority = form.cleaned_data['priority']
            utask.status = form.cleaned_data['status']
            utask.save()  # Update data in database

            project = form['project'].value()

            return redirect('/task/'+str(utask.id))  # Display the updated task

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTaskForm(request.POST, instance=utask)
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'updatetask.html', locals())


# View to add a new journal entry
@login_required
def newjournal(request, id_task):
    projects=Project.objects.filter(members=request.user)
    jtask = Task.objects.get(id=id_task)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewJournalForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # save
            # redirect to a new URL:
            form.save()
            return redirect('/task/'+str(jtask.id))
        else:
            form = NewJournalForm()
            list_projects = Project.objects.all()
            list_users = User.objects.all()
            list_status = Status.objects.all()

        return render(request, 'newjournal.html', locals())

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewJournalForm()
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'newjournal.html', locals())




@login_required
def mytasks(request):
    projects=Project.objects.filter(members=request.user)
    user = request.user
    list_tasks = Task.objects.filter(assignee=user)
    list_projects = Project.objects.filter(members=user)
    chart_data = []
    for project in list_projects:
        chart_data.append(Task.objects.filter(assignee=user, project=project).count())
    return (render(request, 'mytasks.html', locals()))

@login_required
def search(request):
    members = User.objects.all()
    projects=Project.objects.filter(members=request.user)
    # First we check if a search was made, i.e if the Get request contains a "query" element
    if (request.method == "GET") and ("query" in request.GET):
        bool = True
        query = request.GET["query"]
        query_list = query.split()
        user = request.user
        list_tasks = Task.objects.filter(name__contains=query)
    # Else we just show the user all of HIS tasks
    else:
        bool= False
        user = request.user
        list_tasks = Task.objects.filter(assignee=user)
        list_projects = Project.objects.filter(members=user)
        chart_data = []
        for project in list_projects:
            chart_data.append(Task.objects.filter(assignee=user, project=project).count())
    list_tasks, status_q_list, query_list, date1, date2, date3, date4, project_query = filters(request, list_tasks)

    list_tasks = ordering(request,list_tasks)
    # Needed for the template and form...
    Status_all = Status.objects.all()
    return render(request, 'search.html', locals())

@login_required
def donetasks(request):
    projects=Project.objects.filter(members=request.user)
    user = request.user
    done_status = Status.objects.get(name="Terminée")
    list_tasks = Task.objects.filter(assignee=user, status=done_status)
    return (render(request, 'donetasks.html', locals()))


@login_required
def activity(request, id_project):
    projects=Project.objects.filter(members=request.user)
    user = request.user
    project = Project.objects.get(id=id_project)
    list_journals = Journal.objects.filter(task__project=project).order_by('-date')
    list_members = Project.objects.get(id=id_project).members.all()
    contributions = []
    for member in list_members:
        contributions.append(
            nb_contribution(User.objects.get(username=member.username), Project.objects.get(id=id_project)))

    return (render(request, 'activity.html', locals()))


@login_required
def gantt(request, id_project):
    list_members = Project.objects.get(id=id_project).members.all()
    contributions = []
    for member in list_members:
        contributions.append(
            nb_contribution(User.objects.get(username=member.username), Project.objects.get(id=id_project)))
    return (render(request, 'gantt.html', locals()))


def nb_contribution(user, project):
    n = Journal.objects.filter(task__project=project, author=user).count()
    return (n)


@login_required
def export(request):
    projects=Project.objects.filter(members=request.user)
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        dataset_p = ProjectResource().export()
        dataset_s = StatusResource().export()
        dataset_t = TaskResource().export()
        dataset_j = JournalResource().export()
        if file_format == 'CSV':
            response = HttpResponse({dataset_p.csv, dataset_s.csv, dataset_t.csv, dataset_j.csv},
                                    content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse({dataset_p.json, dataset_s.json, dataset_t.json, dataset_j.json},
                                    content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse({dataset_p.xls, dataset_s.xls, dataset_t.xls, dataset_j.xls},
                                    content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response
        elif file_format == 'HTML':
            response = HttpResponse({dataset_p.html, dataset_s.html, dataset_t.html, dataset_j.html},
                                    content_type='text/html')
            response['Content-Disposition'] = 'attachment; filename="exported_data.html"'
            return response
    return render(request, 'export.html',locals())


@login_required
def removetask(request, id_task):
    projects=Project.objects.filter(members=request.user)
    dtask = Task.objects.get(id=id_task)
    dtask.delete()
    return redirect('/project/'+str(dtask.project.id))


# View to fill a form to create a task and add it to the database
@login_required
def newproject(request):
    projects=Project.objects.filter(members=request.user)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewProjectForm(request.POST)
        print(form['members'].value())

        # check whether it's valid:
        if form.is_valid():
            form.save()
            id_project=form['id'].value()

            return redirect('/project/'+str(id_project))  # if the form is valid, save it in database and display the new project

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewProjectForm()
        list_members=User.objects.all()
        print(form['members'].value())

    return render(request, 'newproject.html', locals())

########Analog function for better readability, used for filtering queries #####------Ne fonctionne pas encore
def ordering(request, list_tasks):
    if (request.method == "GET") and ('sort' in request.GET):
        query = request.GET["sort"]
        q = query.split()
        if q[1] == "up":
            list_tasks = list_tasks.filter().order_by(q[0])
        else:
            list_tasks =list_tasks.order_by('-' + q[0])
    return list_tasks


def filters(request, list_tasks):
    # Initialisation des variables pour pouvoir return une liste vide si on a pas les methodes get necessaires..
    status_q_list = []
    project_q_list = []
    query_list = []

    date1 = datetime.today().date()
    date2 = datetime.today().date()
    date3 = datetime.today().date()
    date4 = datetime.today().date()

    # cette partie sert simplement a convertir les placehholder dans le bon format pour django
    date1 = date1.isoformat()
    date2 = date2.isoformat()
    date3 = date3.isoformat()
    date4 = date4.isoformat()

    # On verifie si l'utilisateur a voulu filtrer selon le status ou pas
    if (request.method == "GET") and ('status' in request.GET):
        status_q = request.GET.getlist("status")
        status_q_list = [Status.objects.all().get(name=s) for s in status_q]
        list_tasks = list_tasks.filter(status__in=status_q_list)
    # On verifier si l'utilisateur a voulu filtrer selon le projet
    if (request.method == "GET") and ('project' in request.GET):
        project_q = request.GET.getlist("project")
        project_q_list = [Project.objects.all().get(name=s) for s in project_q]
        list_tasks = list_tasks.filter(project__in=project_q_list)
    # On verifie si l'utilisateur a voulu filtrer selon les membres ou pas
    if (request.method == "GET") and ('member' in request.GET):
        query = request.GET.getlist("member")
        query_list = [User.objects.all().get(username=m) for m in query]
        list_tasks = list_tasks.filter(assignee__in=query_list)
    # On verifie si l'utilisateur a voulu filtrer selon les dates, je verifie donc si "date1" est incluse, et je receuille quand meme les autres, ou pas
    if (request.method=="GET" and ('date1' in request.GET)):
        date1 = request.GET["date1"]
        date2 = request.GET["date2"]
        date3 = request.GET["date3"]
        date4 = request.GET["date4"]
        #Rmq: comme la requete "date" est toujurs presente si on submit une recherche, je ne filtre que sur celles qui sont non nulles....
        if date1 != '':
            list_tasks = list_tasks.filter(start_date__gte=date1)
        if date2 != '':
            list_tasks = list_tasks.filter(start_date__lte=date2)
        if date3 != '':
            list_tasks = list_tasks.filter(due_date__gte=date3)
        if date4 != '':
            list_tasks = list_tasks.filter(due_date__lte=date4)
    if (request.method == "GET" and (('maxProgress' in request.GET) or ('minProgress' in request.GET))):
        max = request.GET['maxProgress']
        min = request.GET['minProgress']
        list_tasks = list_tasks.filter(progress__range=[int(min[:-3]),int(max[:-3])])
    # Enfin ces retours sont utilisés pour le template, pour une meilleure ergonomie je garde affichée les parametres de la recherche precendete.

    return (list_tasks, status_q_list, query_list, date1, date2, date3, date4, project_q_list)

