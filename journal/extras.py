from journal.models import *
from datetime import datetime, timedelta, timezone
from django.conf import settings


def Check_When_Do_Action(action_template_id):

    warning = False
    disaster = False
    msg = ""

    this_action_template = ActionTemplate.objects.filter(id=action_template_id)[0]
    try:
        last_action = Action.objects.filter(ActionTemplate=this_action_template).order_by('-date')[0]
    except:
        last_action = Action()
        last_action.ActionTemplate = this_action_template
        last_action.date = this_action_template.car.first_registration

        last_action.milage = Milage(
            milage=0,
            date=this_action_template.car.first_registration)
    try:
        last_milage = Milage.objects.filter(car=this_action_template.car).order_by('-milage')[0]
    except:
        last_milage = Milage(milage=0, date=this_action_template.car.first_registration)

    current_date = datetime.now(timezone.utc).date()

    if this_action_template.action_milage_period:
        milage_left = (last_action.milage.milage + this_action_template.action_milage_period) - last_milage.milage
    else:
        milage_left = None

    if this_action_template.action_days_period:     # how many days left to this action
        days_left = (last_action.date + timedelta(days=int(this_action_template.action_days_period))) - current_date
    elif this_action_template.action_end_date:  # deadline date for that action
        days_left = this_action_template.action_end_date - current_date # sometimes strict date is defined
    else:
        days_left = None

    if this_action_template.action_end_date:   # deadline date for that action
        date_left = this_action_template.action_end_date    # sometimes strict date is defined
    elif this_action_template.action_days_period: #else count it from action_days_period
        date_left = current_date + days_left
    else:
        date_left = None


    # warnings
    if milage_left is not None:
        if 0 < milage_left < 1000:
            warning = True
            msg = "Pozostało mniej niż 1000 km do wykonania serwisu!\n"
        elif milage_left < 0:
            disaster = True
            msg = "Przekroczyłeś limit km dla serwisu o {}\n".format(abs(milage_left))

    if date_left is not None:
        if 0 < (date_left - current_date).days < 7:
            warning = True
            msg = msg + "Pozostało mniej niż 7 dni do wykonania serwisu!\n"
        elif (date_left - current_date).days <= 0:
            disaster = True
            msg = msg +  "Przekroczyłeś limit dni serwisu o {} dni\n".format(abs((date_left - current_date).days))


    return {
        "milage_left": milage_left,
        "days_left": days_left,
        "date_left": date_left,
        "warning": warning,
        "disaster": disaster,
        "msg": msg
    }

def SendNotifications():
    import telegram
    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    owners = Owner.objects.all()

    for owner in owners:
        msg = ""
        cars = Car.objects.filter(owner=owner)
        for car in cars:
            action_counter = 0
            msg += "{} {}:\n".format(u'\U0001F699', car)
            actmpl = ActionTemplate.objects.filter(car=car)
            for action in actmpl:
                check = Check_When_Do_Action(action.id)
                if check["warning"] or check["disaster"]:
                    action_counter += 1
                    msg += "\t\t\t\t{} => {}\n".format(action.getName(), check["msg"])
            if action_counter > 1:
                print(msg)
                # emoji list https://apps.timwhitlock.info/emoji/tables/unicode
                bot.send_message(chat_id=str(owner.telegram_chat_id), text=msg)
            else:
                msg = ""
