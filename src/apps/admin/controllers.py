'''
Administration panel.
'''
import os
from gae import forms
from gae.pages import Pages
from apps.user import login_required

"""
TODO: hide in SelfReferenceProperty option reference to current object
"""
def load_config(app_name, model_name):
    """Load model configuration"""
    module = __import__("apps.%s.admin" % app_name, {}, {}, ["admin"])
    # create instance
    return getattr(module, model_name)()

@login_required('admin')
def apps_list(app):
    '''
    Show list of applications with enabled administrative interface and all models in each application.
    '''
    # get list of all applications with admin.py file
    apps = [appname for appname in os.listdir('apps') if os.path.isdir(os.path.join('apps', appname)) and os.path.exists(os.path.join('apps', appname, 'admin.py'))]
    apps_models = []
    # get list of all models in each application
    for app_name in apps:
        obj_models = __import__("apps.%s.admin" % app_name, {}, {}, ["admin"])
        models = [model for model in dir(obj_models) if not model.startswith("_")]
        # set real model name
        for index, model_name in enumerate(models):
            # load model
            config = load_config(app_name, model_name)
            models[index] = (model_name, hasattr(config, "name") and config.name or model_name)
        apps_models.append((app_name, models))
    return app.render("admin/apps_list", {
        'apps': apps_models,
        })

@login_required('admin')
def models_list(app, app_name):
    '''
    Show list of objects in specified application.
    '''
    obj_models = __import__("apps.%s.admin" % app_name, {}, {}, ["admin"])
    models = [path for path in dir(obj_models) if not path.startswith("_")]
    # set real model name
    for index, model_name in enumerate(models):
        # load model
        config = load_config(app_name, model_name)
        models[index] = (model_name, hasattr(config, "name") and config.name or model_name)
    return app.render('admin/models_list', {
        'managed_app': app_name,
        'models': models,
        })

@login_required('admin')
def model_records(app, app_name, model_name):
    '''
    Show list of records in model.

    Args:
      obj - type of objects for list
    Return:
      items_pages - count of all pages
      items - articles list on current page
    '''
#    offset = (page - 1) * on_page
    # load model
    config = load_config(app_name, model_name)
    model = config.model
    # get list of records
    items = model.all()
    # prepare data to show on page
    fields = [{'name': field_name, 'type': getattr(model, field_name).__class__.__name__[0:-8]} for field_name in config.fields if hasattr(model, field_name)]
#    records = [[{'name': field_name, 'type': getattr(model, field_name).__class__.__name__[0:-8]} for field_name in config.fields if hasattr(model, field_name)]]
#    records[0].insert(0, {'name': 'id', 'type': 'Boolean'})
#    for item in items:
#        data = [{'name': field['name'], 'type': getattr(model, field['name']).__class__.__name__[0:-8], 'value': getattr(item, field['name'])} for field in records[0] if field['name'] != 'id']
#        data.insert(0, {'name': 'id', 'type': 'Boolean', 'value': getattr(item, "key")().id()})
#        records.append(data)
    return app.render('admin/model_records', {
        'managed_app': app_name,
        'model': model_name,
        'model_name': hasattr(config, "name") and config.name or model_name,
        'records': Pages(items, 20),
        'fields': fields
        })

@login_required('admin')
def create_record(app, app_name, model_name):
    # load model
    config = load_config(app_name, model_name)
    model = config.model
    # additinal fields from external models
    references = []
    if hasattr(config, "references"):
        for reference in config.references:
            reference = reference.split(".")
            collection = getattr(model, reference[0])
            references.insert(0, (collection, 1 in reference and reference[1] or None))
    # create form for edit model
    Meta = type('Meta', (object,), {'model': model})
    NewForm = type('NewForm', (forms.ModelForm,), {'Meta': Meta}) 
    # handle form
    if app.request.POST:
        # filled form
        form = NewForm(data=app.request.POST)
        if form.is_valid():
            if hasattr(config, "before_save"):
                config.before_save()
            form.save()
            if hasattr(config, "after_save"):
                config.after_save()
            return app.redirect("go back")
    # empty form
    else:
        form = NewForm()
    # render page
    return app.render('admin/create_record', {
        'managed_app': app_name,
        'model': model_name,
        'model_name': hasattr(config, "name") and config.name or model_name,
        'references': references,
        'form': form,
        })

@login_required('admin')
def edit_record(app, app_name, model_name, record_key):
    # load model
    config = load_config(app_name, model_name)
    model = config.model
    # get record object
    record = model.get(record_key)
    # record not found
    if record is None:
        return app.error(404)
    # additinal fields from external models
    references = []
    if hasattr(config, "references"):
        for reference in config.references:
            reference = reference.split(".")
            collection = getattr(record, reference[0])
            references.insert(0, (collection, len(reference)>1 and reference[1] or None))
    # use existing form
    if hasattr(config, "form"):
        form = config.form
#        NewForm.Meta.exclude = []
        Meta = type('Meta', (object, form.Meta,), {'exclude': []})
        NewForm = type('NewForm', (form,), {'Meta': Meta}) 
    # create form for edit model
    else:
        Meta = type('Meta', (object,), {'model': model})
        NewForm = type('NewForm', (forms.ModelForm,), {'Meta': Meta}) 
    # handle form
    if app.request.POST:
        # filled form
        form = NewForm(data=app.request.POST, instance=record)
        if form.is_valid():
            if hasattr(config, "before_change"):
                config.before_change()
            form.save()
            if hasattr(config, "after_change"):
                config.after_change()
            return app.redirect("go back")
    # empty form
    else:
        form = NewForm(instance=record)
    # render page
    return app.render('admin/edit_record', {
        'managed_app': app_name,
        'model': model_name,
        'model_name': hasattr(config, "name") and config.name or model_name,
        'record': record,
        'references': references,
        'form': form,
        })

@login_required('admin')
def delete_record(app, app_name, model_name, record_key=None):
    if record_key is None:
        # get records id from POST request
        record_keys = app.request.get_all("record_key")
    else:
        # use one record key passed to query string
        record_keys = list(record_key)
    try:
        # load model and get record from this model
        config = load_config(app_name, model_name)
        model = config.model
    except (AttributeError):
        record = None
    # delete each specified record
    for record_key in record_keys:
        record = model.get(record_key)
        if record is not None:
            if hasattr(config, "before_delete"):
                config.before_delete()
            record.delete()
            if hasattr(config, "after_delete"):
                config.after_delete()
    return app.redirect("go back")
