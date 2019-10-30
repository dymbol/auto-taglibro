from journal import extras
from django import template
register = template.Library()

@register.filter
def action_extra_days_to_nice_date(days_count):
    """
    format count of days in nice format
    eg: for 60 days it shows 2 months
    :param days_count: integer
    :return: string
    """
    months = round(days_count / 30)

    m_value = ""  # odmiana słowa miesiąc
    if round(months % 12) != 0:
        if round(months % 12) >= 5:
            m_value = "miesięcy"
        elif round(months % 12) == 1:
            m_value = "miesiąc"
        elif round(months % 12) in [2, 3, 4]:
            m_value = "miesięce"


    if months == 0:
        return f'{days_count} dni'
    elif months > 0 and months < 12:
        return f'{months} {m_value}'
    elif months == 12:
        return f'1 rok'
    elif months > 12 and months < 24:
        if round(months%12) != 0:
            return f'{months // 12} rok i {round(months % 12)} {m_value}'
        else:
            return f'{months // 12} rok'
    elif months >= 24:
        if round(months % 12) != 0:
            return f'{round(months/12)} lata i {round(months%12)} {m_value}'
        else:
            if round(months / 12) < 5:
                return f'{months // 12} lata'
            else:
                return f'{months // 12} lat'


@register.filter
def action_extra_data_time_left(act_tmpl_id):
    #shows human readable time left
    if extras.check_when_do_action(act_tmpl_id)["days_left"] is not None:
        return action_extra_days_to_nice_date(extras.check_when_do_action(act_tmpl_id)["days_left"].days)
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
