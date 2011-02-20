from google.appengine.ext.db import djangoforms
from gae.translation import translate as _
import re
try:
    from django.newforms import *
except ImportError:
    from django.forms import *

'''
TODO: translate "default" value
TODO: translate error messages
'''

class ModelForm(djangoforms.ModelForm):
    '''
    Added: automatically translate fields and choices in model.
    '''
    def __init__(self, *args, **kwargs):
        '''Added i18m support to model fields and choices'''
        # detect current application name by model name
        app_name = re.sub("^([A-Z][^A-Z]+).*", "\\1", self.Meta.model.kind()).lower()
        # translate fields
        for field_name, field in self.base_fields.items():
            # translate label
            if not field.label:
                field.label = field_name.capitalize()
            field.label = _(field.label, app_name)
            # translate choices
            if hasattr(field, "widget") and hasattr(field.widget, "choices"):
                field.widget.choices = [(key, _(name, app_name)) for key, name in field.widget.choices]
        super(ModelForm, self).__init__(*args, **kwargs)

    def _clean_fields(self):
        '''Fix for Django 1.2: use initial data'''
        # set additional properties to model, not editable in form
        if hasattr(self, "initial"):
            self.cleaned_data = {}
            for field_name, value in self.initial.items():
                if field_name not in self.base_fields.keys(): # field not editable in form
                    self.cleaned_data[field_name] = value
        super(ModelForm, self)._clean_fields()