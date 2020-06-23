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
from django.conf import settings
import os
import random
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from sendfile import sendfile
from django.db.models import Sum
from decimal import *

# (1048, "Column 'important' cannot be null")
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
    car = Car.objects.filter(id=car_id)[0]  # .dates('creation_date', 'year').distinct()
    context["Car"] = car
    if car.color is not None:
        context["color_name"] = car.color.split(";")[0]
        context["color_code"] = car.color.split(";")[1]
    else:
        context["color_name"] = "-"
        context["color_code"] = "#FFFFF"
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
def show_costs(request, car_id):
    context = {}
    action_list = Action.objects.filter(ActionTemplate__car_id=car_id).values('date__year').annotate(dcount=Sum('cost')).order_by('date__year')
    for year_obj in action_list:
        if year_obj["dcount"] is not None:
            print(year_obj)
    context["costs"] = action_list
    context["car"] = Car.objects.filter(id=car_id)[0]
    return render(request, 'costs.html', context)


@login_required
def action_list(request, car_id):
    context = {}
    context["action_list"] = Action.objects.filter(ActionTemplate__car_id=car_id).order_by('-date')
    return render(request, 'action_list.html', context)


@login_required
def action_list_by_tmpl(request, tmplaction_id):
    context = {}
    context["action_list"] = Action.objects.filter(ActionTemplate__id=tmplaction_id).order_by('-date')
    if len(context["action_list"]) != 0:
        return render(request, 'action_list.html', context)
    else:
        return HttpResponseNotFound('<h1>Brak wystąpień</h1>')


@login_required
def files(request, car_id):
    context = {}
    context["files"] = File.objects.filter(car=car_id)
    context["car"] = Car.objects.filter(id=car_id)[0]
    return render(request, 'files.html', context)


@login_required
def add_file(request, car_id):
    context = {}
    car = Car.objects.filter(id=car_id)[0]
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # saving file object in db
                new_file = File(
                    car=car,
                    name="{}{}".format(
                        random.choice(range(1, 1000)),
                        form.cleaned_data['name'].replace(" ", "_")
                    ),
                    desc=form.cleaned_data['desc']
                )
                new_file.save()

                # saving file to disc
                file_path = os.path.join(settings.DOCUMENTS_DIR, new_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in request.FILES['file'].chunks():
                        destination.write(chunk)

                return redirect('files', car_id)
            except:
                print("Error writing file {}".format(form.cleaned_data['name']))
                return redirect('files', car_id)
        else:
            return redirect('add_file', car_id)

    else:

        form = FileForm()
        context['form'] = form
        context['car_id'] = car_id
        return render(request, 'add_file.html', context)


@login_required
def get_file(request, file_id):
    file_obj = get_object_or_404(File, pk=file_id)
    if file_obj.name is not None:
        abs_filename = settings.DOCUMENTS_DIR+"/"+file_obj.name
        if os.path.isfile(abs_filename):
            return sendfile(request, abs_filename, attachment=False)
        else:

            return HttpResponseNotFound('<h1>File not found on server</h1>')
    else:
        return HttpResponseNotFound('<h1>Problem with file object</h1>')
        raise


@login_required
def todo_list(request, car_id):
    context = {}
    context["todo_list"] = Note.objects.filter(car__id=car_id).order_by('todo_priority')
    context["car"] = Car.objects.filter(id=car_id)[0]
    return render(request, 'todo.html', context)


@login_required
def items(request):
    context = {}
    context["items"] = Item.objects.filter(used=False)    
    return render(request, 'items.html', context)


@login_required
def notes_list(request, car_id):
    context = {}
    context["notes_list"] = Note.objects.filter(car__id=car_id)
    context["car"] = Car.objects.filter(id=car_id)[0]
    return render(request, 'notes.html', context)


@login_required
def note_details(request, note_id):
    context = {}
    context["note"] = Note.objects.filter(id=note_id)[0]
    return render(request, 'note_details.html', context)


@login_required
def note_status_change(request, note_id):
    context = {}
    note_tmp = Note.objects.filter(id=note_id)[0]
    note_tmp.todo_done = True
    note_tmp.save()
    return redirect('todo_list', car_id=note_tmp.car.id)



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
    last_milage=Milage.objects.filter(car__id=car_id).order_by('-milage')[0].milage
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            new_action = Action(
                ActionTemplate=ActionTemplate.objects.filter(id=form['ActionTemplate'].value())[0],
                date=form['date'].value(),
                comment=form['comment'].value(),
                show_on_list=form['show_on_list'].value()
            )

            if form['milage'].value() :
                new_milage = Milage(
                    car=car,
                    milage=form['milage'].value(),
                    date=form['date'].value()
                )
                new_milage.save()
                new_action.milage = new_milage

            if form['file'].value() :
                new_action.file=File.objects.filter(id=form['file'].value())[0]
            if form['cost'].value() :
                new_action.cost = form['cost'].value()

            new_action.save()
            return redirect('add_action_item', new_action.id)
        else:
            print(form.errors)
            print("NOT VALID")
            return redirect('add_action', car_id)
    else:
        form = ActionForm()
        form.fields['ActionTemplate'] = forms.ModelChoiceField(queryset=ActionTemplate.objects.filter(car=car), label="Akcja predefiniowana")
        form.fields['file'] = forms.ModelChoiceField(queryset=File.objects.filter(car=car), label="Dokument (fv, paragon)",required=False)
        form.fields['milage'] = forms.DecimalField(
            min_value=last_milage+1,
            initial=last_milage+1,
            label="Przebieg",
            required=False
        )
        context['form'] = form
        context['car_id'] = car_id
        return render(request, 'add_action.html', context)


@login_required
def add_action_item(request, action_id):
    context = {}
    action = Action.objects.filter(id=action_id)[0]    
    if request.method == "POST":
        form = ItemToActionForm(request.POST)
        if form.is_valid():
            #odejmij uqntity , jesli wieksze od zero -> zrob pustą kopię
            product = form['product'].value()
            used_quantity = Decimal(form['quantity'].value())

            item_found = Item.objects.filter(id=product)[0]

            left_quantity = item_found.quantity - used_quantity
            print(used_quantity,left_quantity)
            if left_quantity > 0:              
                # robimy kopie itema z pozostałą ilością quantity bez przypisanej action
                item_new = Item.objects.filter(id=product)[0]
                item_new.id = None
                item_new.pk = None
                item_new.description = f"Oryginalny koszt ilośći {item_new.quantity}: {item_new.cost} #### {item_new.description}"

                item_new.quantity=left_quantity
                item_new.used = False                
                item_new.cost = 0
                
                print(item_new)
                item_new.save()
            
                # przypisujemy action do starego item oraz uzytą quantity
                item_found.action = action
                item_found.quantity = used_quantity
                item_found.used = True
                item_found.save()

            elif left_quantity == 0:
                # tylko przypisujemy action do item oraz użytą quantity
                item_found.action = action
                item_found.quantity = used_quantity
                item_found.used = True
                item_found.save()
            elif left_quantity < 0:               
                # Return a 'disabled account' error message
                form = ItemToActionForm()
                context['form'] = form
                context['action'] = action
                messages.error(request, f"Zbyt mała ilość {item_found}")
                return render(request, 'add_action_item.html', context) 
   
        
          
            # dodaj id action do itemu
           
            messages.info(request, f"Dodano produkt {item_found} do akcji")
            return redirect('add_action_item', action_id)
        else:
            print(form.errors)
            print("NOT VALID")
            return redirect('add_action_item', action_id)
    else:
        form = ItemToActionForm()        
        context['form'] = form
        context['action'] = action
        return render(request, 'add_action_item.html', context)


@login_required
def action(request, action_id):
    context = {}
    context["action"] = Action.objects.filter(id=action_id)[0]
    context["products"] = Item.objects.filter(action=action_id)
    context["sum_cost"] = extras.get_full_action_cost(action_id)
    return render(request, 'action.html', context)


@csrf_exempt
def send_notifications(request):
    '''
    how to call:
    curl -d "username=xxx&password=xxx&check_important=1" -X POST http://127.0.0.1:8000/notify
    curl -d "username=xxx&password=xxx&check_important=0" -X POST http://127.0.0.1:8000/notify
    '''

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
                                msg = extras.send_notifications(important_only=True)
                            except:
                                status = "-1"
                                msg = "Unknown error in extras.send_notifications()"
                                raise
                        else:
                            try:
                                status = "0"
                                msg = extras.send_notifications(important_only=False)
                            except:
                                status = "-1"
                                msg = "Unknown error in extras.send_notifications()"
                                raise
                    else:
                        status = "-1"
                        msg = "Please call me with check_important parameter (0 or 1 value)"

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


@csrf_exempt
def TestConnection(request):
    try:
        Car.objects.count()
        return JsonResponse({'status': "database connection ok"})
    except:
        print("Błąd połączenia z bazą danych")
        return JsonResponse({'status': "database connection error"})