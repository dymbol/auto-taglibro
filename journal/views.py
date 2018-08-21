from django.shortcuts import render
from journal.models import *
from journal.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
import datetime
from django.http import JsonResponse
from journal import extras
from django.views.decorators.csrf import csrf_exempt, csrf_protect


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                messages.info(request, "{0},\n zostałeś zalogowany".format(username))
                return redirect('car_list')
            else:
                # Return a 'disabled account' error message
                return render(request, 'login.html', {'error_message': "Konto wyłączone", })
        else:
            return render(request, 'login.html', {'error_message': "Błąd logowania", })
            # Return an 'invalid login' error message.
    else:
        return render(request, 'login.html', {})


def logoutuser(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, "Zostałeś wylogowany ")
    return redirect('login_user')


@login_required
def car_list(request):
    context = {}
    context["car_list"] = Car.objects.filter(owner=request.user)
    return render(request, 'car_list.html', context)

@login_required
def car(request, car_id):
    context = {}
    context["Car"] = Car.objects.filter(id=car_id)[0]  # .dates('creation_date', 'year').distinct()
    try:
        context["Last_milage"] = Milage.objects.filter(car__id=car_id).order_by('-milage')[0]  # .dates('creation_date', 'year').distinct()
    except IndexError:
        context["Last_milage"] = None
    return render(request, 'car.html', context)

@login_required
def milage_list(request, car_id):
    context = {}
    context["Milage"] = Milage.objects.filter(car_id=car_id).order_by('-date')
    return render(request, 'milage.html', context)

@login_required
def update_milage(request, car_id):
    context = {}
    context["car_id"] = car_id

    if request.method == "POST":
        milage = request.POST['milage']
        if milage.isdigit():
            new_milage = Milage(car_id=car_id, milage=milage, date=datetime.datetime.now())
            new_milage.save()
            messages.info(request, " Przebieg dodany")
            return redirect('car_list')
    else:
        car = Car.objects.filter(id=car_id)[0]
        context["car"] = car
        return render(request, 'update_milage.html', context)

@login_required
def service_plan(request, car_id):
    context = {}
    context["service_plan"] = ActionTemplate.objects.filter(car_id=car_id, periodic=True).order_by('action_milage_period')
    context["car_id"] = car_id
    return render(request, 'service_plan.html', context)

@login_required
def action_list(request, car_id):
    context = {}
    context["action_list"] = Action.objects.filter(ActionTemplate__car_id=car_id).order_by('-date')
    return render(request, 'action_list.html', context)


@login_required
def action_list_by_tmpl(request, tmplaction_id):
    context = {}
    context["action_list"] = Action.objects.filter(ActionTemplate__id=tmplaction_id).order_by('-date')
    return render(request, 'action_list.html', context)


@login_required
def files(request, car_id):
    context = {}
    context["files"] = File.objects.filter(car=car_id)
    context["car_id"] = car_id
    return render(request, 'files.html', context)


@login_required
def add_file(request, car_id):
    context = {}
    car = Car.objects.filter(id=car_id)[0]
    if request.method == "POST":
        form = FileForm(request.POST)

        # form
        if form.is_valid():
            new_tmpl = form.save(commit=False)
            new_tmpl.car = car
            new_tmpl.save()

            # context["TmplAction"] = ActionTemplate.objects.filter(id=car_id)[0]
            # print(context["TmplAction"])
            return redirect('index')
        else:
            return redirect('add_tmpl_action', car_id)
    else:

        form = FileForm()
        context['form'] = form
        context['car_id'] = car_id
        return render(request, 'add_file.html', context)


@login_required
def tmpl_action(request, tmplaction_id):
    context = {}
    context["TmplAction"] = ActionTemplate.objects.filter(id=tmplaction_id)[0]
    return render(request, 'template_action.html', context)


@login_required
def add_tmpl_action(request, car_id):
    context = {}
    car = Car.objects.filter(id=car_id)[0]
    if request.method == "POST":
        form = ActionTemplateForm(request.POST)

        #form
        if form.is_valid():
            new_tmpl = form.save(commit=False)
            new_tmpl.car = car
            new_tmpl.save()


        #context["TmplAction"] = ActionTemplate.objects.filter(id=car_id)[0]
        #print(context["TmplAction"])
            return redirect('index')
        else:
            return redirect('add_tmpl_action', car_id)
    else:

        form = ActionTemplateForm()
        context['form'] = form
        context['car_id'] = car_id
        return render(request, 'add_template_action.html', context)


@login_required
def add_action(request, car_id):
    context = {}
    car = Car.objects.filter(id=car_id)[0]
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            return redirect('index')
        else:
            print(form)
            print("NOT VALID")
            return redirect('add_action', car_id)
    else:

        #form = ActionForm()
        #print(form)
        #form.ActionTemplate.queryset = ActionTemplate.objects.filter(car=car)
        form = ActionForm()
        #overwriten because we want only action connected to this car
        form.fields['ActionTemplate'] = forms.ModelChoiceField(queryset=ActionTemplate.objects.filter(car=car), label="Akcja predefiniowana")
        form.fields['file'] = forms.ModelChoiceField(queryset=File.objects.filter(car=car), label="Dokument (fv, paragon)")
        print(form.fields)
        context['form'] = form
        context['car_id'] = car_id
        return render(request, 'add_action.html', context)


@csrf_exempt
def send_notifications(request):
    # how to call: curl -d "username=xxx&password=xxx" -X POST http://127.0.0.1:8000/notify
    #or
    #curl -d "username=xxx&password=xxx&check_important=1" -X POST http://127.0.0.1:8000/notify
    #curl -d "username=xxx&password=xxx&check_important=0" -X POST http://127.0.0.1:8000/notify


    status = ""
    msg = ""

    if request.method == "POST":
        if 'username' in request.POST.keys() and 'password' in request.POST.keys():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    # Let's check for very important infos in car's schedule.
                    if 'check_important' in request.POST.keys():
                        if request.POST['check_important'] == "1":
                            try:
                                status = "0"
                                msg = extras.SendNotifications(ImportantOnly=True)
                            except:
                                status = "-1"
                                msg = "Unknown error in extras.SendNotifications()"
                                raise
                        else:
                            try:
                                status = "0"
                                msg = extras.SendNotifications(ImportantOnly=False)
                            except:
                                status = "-1"
                                msg = "Unknown error in extras.SendNotifications()"
                                raise
                else:
                    # Return a 'disabled account' error message
                    status = "1"
                    msg = "Authentication problem: User not active"
            else:
                status = "2"
                msg = "Authentication problem: No user"



        else:
            status = "3"
            msg = "Provide username and password fields in POST method"
    else:
        status = "4"
        msg = "POST method required"

    return JsonResponse({'status': status, 'msg': msg})
