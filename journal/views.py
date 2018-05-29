from django.shortcuts import render
from journal.models import *
from journal import extras

def car_list(request):
    context = {}
    context["car_list"] = Car.objects.filter(owner=request.user)
    print(request.user)
    return render(request, 'car_list.html', context)


def car(request, car_id):
    context = {}
    context["Car"] = Car.objects.filter(id=car_id)[0]  # .dates('creation_date', 'year').distinct()
    try:
        context["Last_milage"] = Milage.objects.filter(car__id=car_id).order_by('-milage')[0]  # .dates('creation_date', 'year').distinct()
    except IndexError:
        context["Last_milage"] = None
    return render(request, 'car.html', context)


def milage_list(request, car_id):
    context = {}
    context["Milage"] = Milage.objects.filter(car_id=car_id).order_by('-date')
    return render(request, 'milage.html', context)


def service_plan(request, car_id):
    context = {}
    context["service_plan"] = ActionTemplate.objects.filter(car_id=car_id).order_by('action_milage_period')
    return render(request, 'service_plan.html', context)


def action_list(request, car_id):
    context = {}
    context["action_list"] = Action.objects.filter(ActionTemplate__car_id=car_id).order_by('-date')
    return render(request, 'action_list.html', context)


