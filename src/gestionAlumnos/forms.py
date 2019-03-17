from .models import Alumno
from django.forms.models import ModelForm
from ajax_select.fields import AutoCompleteSelectField
from django import forms
from django.utils.translation import ugettext_lazy as _

class AlumnoForm(forms.ModelForm):        
    class Meta:
        form = Alumno
        '''
        help_texts = {
            'nombre': _('Nombre de la persona.'),
        }
        '''             