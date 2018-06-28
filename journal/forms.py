from django.forms import ModelForm
from journal.models import *


class ActionTemplateForm(ModelForm):
    class Meta:
        model = ActionTemplate
        fields = ['periodic',
                  'action_popular',
                  'title',
                  'desc',
                  'action_milage_period',
                  'action_days_period',
                  'action_end_date',
                  'product',
                  'product_quantity'
                  ]
        labels = {
            'periodic': ('Akcja okresowa'),
            'action_popular': ('Popularne akcje'),
            'title': ('Tytuł'),
            'desc': ('Opis'),
            'action_milage_period': ('Okres w km'),
            'action_days_period': ('Okres w dniach'),
            'action_end_date': ('Data końcowa'),
            'product': ('Użyty produkt'),
            'product_quantity': ('Ilośc produktu')
        }