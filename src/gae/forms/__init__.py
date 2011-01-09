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
    def __init__(self, **kwargs):
        '''Added i18m support to model fields and choices'''
        # detect current application name by model name
        app_name = re.sub("^([A-Z][^A-Z]+).*", "\\1", self.__class__.__name__).lower()
        # translate fields
        for field_name, field in self.base_fields.items():
            # translate label
            if not field.label:
                field.label = field_name.capitalize()
            field.label = _(field.label, app_name)
            # translate choices
            if hasattr(field, "widget") and hasattr(field.widget, "choices"):
                field.widget.choices = [(key, _(name, app_name)) for key, name in field.widget.choices]
        super(ModelForm, self).__init__(**kwargs)