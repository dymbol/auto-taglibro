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


# class ActionForm(ModelForm):
#     class Meta:
#         model = Action
#         fields = ['ActionTemplate',
#                   'milage',
#                   'date',
#                   'comment',
#                   'cost',
#                   'product',
#                   'file'
#                   ]
#         labels = {
#             'ActionTemplate': ('Akcja predefiniowana'),
#             'milage': ('Przebieg [km]'),
#             'date': ('data'),
#             'comment': ('Komentarz'),
#             'cost': ('Koszt [zł]'),
#             'product': ('Użyty produkt'),
#             'file': ('Dokument (fv, paragon)')
#         }


class FileForm(forms.Form):
    file = forms.FileField(label="Plik")
    desc = forms.CharField(widget=forms.Textarea, label="Opis", required=False)
    name = forms.CharField(max_length=100, label="Nazwa pliku")


class ActionForm(forms.Form):
    ActionTemplate = forms.ModelChoiceField(
        queryset=ActionTemplate.objects.all(),
        label="Akcja predefiniowana")
    file = forms.ModelChoiceField(
        queryset=File.objects.all(),
        label="Dokument",
        required=False)
    milage = forms.DecimalField(label="Przebieg")
    comment = forms.CharField(widget=forms.Textarea, label="Opis", required=False)
    date = forms.DateField(label="Data", initial=datetime.now, widget=forms.DateInput(attrs={'type': 'date'}))
    cost = forms.DecimalField(label="Koszt [PLN]")
    product = forms.CharField(label="Użyty produkt", required=False)
