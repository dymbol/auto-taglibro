from django.forms import ModelForm
from journal.models import *
from django import forms


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


class ActionForm(ModelForm):
    class Meta:
        model = Action
        fields = ['ActionTemplate',
                  'milage',
                  'date',
                  'comment',
                  'cost',
                  'product',
                  'file'
                  ]
        labels = {
            'ActionTemplate': ('Akcja predefiniowana'),
            'milage': ('Przebieg [km]'),
            'date': ('data'),
            'comment': ('Komentarz'),
            'cost': ('Koszt [zł]'),
            'product': ('Użyty produkt'),
            'file': ('Dokument (fv, paragon)')
        }


class FileForm(forms.Form):
    name = forms.CharField(max_length=100)
    desc = forms.CharField(widget=forms.Textarea)

