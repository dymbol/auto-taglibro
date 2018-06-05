from django.shortcuts import render
from journal.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
import datetime
from journal import extras


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
        return render(request, 'update_milage.html', context)

@login_required
def service_plan(request, car_id):
    context = {}
    context["service_plan"] = ActionTemplate.objects.filter(car_id=car_id).order_by('action_milage_period')
    return render(request, 'service_plan.html', context)

@login_required
def action_list(request, car_id):
    context = {}
    context["action_list"] = Action.objects.filter(ActionTemplate__car_id=car_id).order_by('-date')
    return render(request, 'action_list.html', context)


