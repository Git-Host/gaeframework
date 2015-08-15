Below we have describe list of standard applications supplied with GAE framework.

Also we tell you more about how to create your own application.

## Standard applications ##

**Now, we have next applications**:
  * [admin](AppsAdmin.md)
  * **[banner](AppsBanner.md)**
  * **[blog](AppsBlog.md)**
  * **[comment](AppsComment.md)**
  * **[guestbook](AppsGuestbook.md)**
  * [location](AppsLocation.md)
  * [message](AppsMessage.md)
  * **[page](AppsPage.md)**
  * [todo](AppsTodo.md)
  * **[user](AppsUser.md)**

Just copy application to your project **`apps`** directory, add this application to [urls mapping](Config#Urls_mapping.md) and restart server. This application is ready to use!

## Create new application ##

Get basic information about project structure in [quick start guide](Start.md).

Now we focused on create new application. We create a simple `myblog` application, where we can create blog entities.

  1. create a directory for your application with empty **`__init__.py`** file
```
apps/myblog/__init__.py
```
  1. create **`apps/myblog/config.yaml`** file and map urls to request handlers [read more](Config.md)
```
urls:
- url:
  run: entities_list

- url: new
  run: entity_create

- url: :entity/edit
  run: entity_edit

- url: :entity/delete
  run: entity_delete

- url: :entity
  run: entity_details
```
  1. describe models used in this application in **`apps/myblog/models.py`** file [read more](Models.md)
```
class Entity(db.Model):
    KEY_NAME = "%(slug)s"
    slug = db.StringProperty('entity url', required=True)
    title = db.StringProperty(required=True)
    description = db.StringProperty('short description')
    text = db.TextProperty('full text', required=True)
    author = db.UserProperty(auto_current_user_add=True, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    changed = db.DateTimeProperty(auto_now=True)
    active = db.BooleanProperty(default=False)

    def __unicode__(self):
        return self.title

    def details_url(self):
        return self.key().name()

    def edit_url(self):
        return "%s/edit" % self.key().name()

    def delete_url(self):
        return "%s/delete" % self.key().name()
```
  1. create a **`apps/myblog/forms.py`** file [read more](Forms.md)
```
from gae import forms
from apps.blog.models import Entity

class EntityCreateForm(forms.ModelForm):
    class Meta:
        model   = Entity
        exclude = ['author']

    def clean_slug(self):
        '''Prevent duplicate entities with equal key names'''
        # entity with given url address already exists
        entity_key = self.cleaned_data['slug']
        if self.Meta.model.get_by_key_name(entity_key):
            raise forms.ValidationError("Blog entity with url '%s' already exists" %
                                         entity_key)
        return entity_key

class EntityEditForm(forms.ModelForm):
    class Meta:
        model   = Entity
        exclude = ['author', 'slug']

    def clean_slug(self):
        '''Prevent change key name for entity'''
        # entity with given url address already exists
        entity_key = self.cleaned_data['slug']
        if self.Meta.model.get_by_key_name(entity_key):
            raise forms.ValidationError("Blog entity with url '%s' already exists" %
                                         entity_key)
        return entity_key
```
  1. create appropriate request handlers in file **`apps/myblog/controllers.py`** [read more](Controllers.md)
```
from apps.user import login_required
from gae.shortcuts import get_object_or_404
from apps.blog.models import Entity
from apps.blog.forms import EntityCreateForm, EntityEditForm
from gae.pages import Pages

def entities_list(app):
    entities = Entity.all().order('-changed')
    # show not published entities
    if app.request.GET.get("show") == "unpublished" and app.user.is_admin:
        entities.filter('active', False)
    # show only active blogs
    else:
        entities.filter('active', True)
    # render page
    return app.render('myblog/entities_list', {
                      'entities': Pages(entities, 20, "entities_page"),
                      })

def entity_details(app, entity):
    entity_obj = get_object_or_404(Entity, entity)
    # render page
    return app.render('myblog/entity_details', {'entity': entity_obj})

@login_required()
def entity_create(app):
    if app.request.POST:
        form = EntityCreateForm(data=app.request.POST)
        if form.is_valid():
            form.save()
            return app.redirect("go back")
    else:
        # empty form
        form = EntityCreateForm()
    # render page
    return app.render('myblog/entity_create', {'form': form})

@login_required()
def entity_edit(app, entity):
    entity_obj = get_object_or_404(Entity, entity)
    if app.request.POST:
        form = EntityEditForm(data=app.request.POST, instance=entity_obj)
        if form.is_valid():
            form.save()
            return app.redirect("go back")
    else:
        # form with initial data
        form = EntityEditForm(instance=entity_obj)
    # render page
    return app.render('myblog/entity_edit', {'form': form})

@login_required()
def entity_delete(app, entity):
    entity_obj = get_object_or_404(Entity, entity)
    # delete blog entity
    entity_obj.delete()
    return app.redirect("go back")
```
  1. create templates to show pages [read more](Templates.md)
    * template file **`apps/myblog/templates/entities_list.html`**
```
  {% for entity in entities %}
    <div class="blog entity">
      <h2><a href="/{{ app }}/{{ entity.details_url }}">{{ entity.title }}</a></h2>
      {{ entity.description|default:""|escape }}
    </div>
  {% empty %}
    {% translate "No blog entities" %}
  {% endfor %}

  {% show_pages entities %}
```
    * template file **`apps/myblog/templates/entity_details.html`**
```
  <h1>{{ entity.title }}</h1>

  <div class="blog entity">
    <blockquote>{{ entity.description|default:"No description"|escape }}</blockquote>
    {{ entity.text }}
  </div>
```
    * template file **`apps/myblog/templates/entity_create.html`**
```
  <h1>{% translate "Create new blog entity" %}</h1>

  <form method="POST" action="" class="blog entity">
    <input type="hidden" name="back_url"  value="{% back_url %}"/>
    <table>
      {{ form }}
    </table>
    <input type="submit" value="{% translate "Create" %}">
    <a href="{% back_url %}">{% translate "Cancel" %}</a>
  </form>
```
    * template file **`apps/myblog/templates/entity_edit.html`**
```
  <h1>{% translate "Edit blog entity" %}</h1>

  <form method="POST" action="" class="blog entity">
    <input type="hidden" name="back_url"  value="{% back_url %}"/>
    <table>
      {{ form }}
    </table>
    <input type="submit" value="{% translate "Save" %}">
    <a href="{% back_url %}">{% translate "Cancel" %}</a>
  </form>
```