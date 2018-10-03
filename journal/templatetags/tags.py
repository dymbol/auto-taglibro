from journal import extras
from django import template
register = template.Library()

@register.filter
def action_extra_data_days_left(act_tmpl_id):
    if extras.check_when_do_action(act_tmpl_id)["days_left"] is not None:
        return extras.check_when_do_action(act_tmpl_id)["days_left"].days
    else:
        return "-"

@register.filter
def action_extra_data_date_left(act_tmpl_id):
    return extras.check_when_do_action(act_tmpl_id)["date_left"]

@register.filter
def action_extra_data_milage_left(act_tmpl_id):
    return extras.check_when_do_action(act_tmpl_id)["milage_left"]

@register.filter
def action_extra_info(act_tmpl_id):
    if extras.check_when_do_action(act_tmpl_id)["disaster"] is True:
        return "KATASTROFA"
    elif extras.check_when_do_action(act_tmpl_id)["warning"] is True:
        return "UWAGA"
    else:
        return "NORMA"
