You can use forms in your application for simplify validation data before save models into datastore.

We have use [Django forms](http://docs.djangoproject.com/en/dev/topics/forms/modelforms/) with some additions, described below.

**Also read**: [Django validation](http://docs.djangoproject.com/en/dev/ref/forms/validation/), [djangororms adoptation to Google App Engine](http://code.google.com/intl/ru/appengine/articles/djangoforms.html).

### Auto-translation ###

GAE framework automatically [translate](Translate.md) some data of your [models](Models.md):
  * field names
  * choices in fields _(html select box with localized options)_

Text translated to language, defined in project [configuration](Config.md) file in **`language`** section.

### Changed behavior: initial values ###

**NOTE** This change is applied only for Django 1.2.

If you have the form where some fields should be not editable by user, than you can push required values to new model instance. Pass required parameters to **`initial`** parameter to form constructor.

For example we have controller in [apps.blog](AppsBlog.md):
```
@login_required()
def entity_create(app, blog):
    blog_obj = get_object_or_404(Blog, blog)
    if app.request.POST:
        form = EntityCreateForm(data=app.request.POST, initial={'blog': blog_obj})
        # filled form
        if form.is_valid():
            form.save()
            return app.redirect("go back")
    else:
        # empty form
        form = EntityCreateForm()
    # render page
    return app.render('blog/entity_create', {'form': form})
```

In this case **`initial={'blog': blog_obj}`** - required value, not editable by user, and should be used to create model instance.