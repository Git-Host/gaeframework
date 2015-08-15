**User** application - allow you register new users in local datastore. After this users can login to your site.

### Detect current logged in user ###

You can get current registered user anywhere in Python code with next code:

```
from apps.user import get_current_user

# get user object
user = get_current_user()
```

In [controllers](Controllers.md) we can do next:

```
from apps.user import get_current_user

def index_page(app):
  # get user object
  user = get_current_user()

  # if user not logged in (user is None)
  if not user:
    # do something with not logged user. For example show error page
    return app.error("not found")
  # do something with logged in user. For example render template for current user
  return app.render("myapp/user", {"user": user})
```

Also you can control if user logged in to site. If user not logged in - than we can show page with error "You are not logged in" and entry form.

```
from apps.user import login_required

@login_required()
def delete_my_account(app):
  # we really can do delete of user account because user is logged in
  return "You really want to delete your account?"
```

### Shortcut for detect current user _(only can be used in controllers)_ ###

We can use this code for detect current user:

```
user = get_current_user()
```

but we have a short form of this call. You can access to current logged in user with this shortcut `app.user` as explained below:

```
from apps.user import get_current_user

def index_page(app):
  # if user not logged in (user is None)
  if not app.user:
    # do something with not logged user. For example show error page
    return app.error("not found")
  # do something with logged in user. For example render template for current user
  return app.render("myapp/user", {"user": app.user})
```

**Really simple?** _Note, that you can do this in [controllers](Controllers.md) only!_

## User roles ##

User role assigned as list of string values for each user to property `roles`. By default this is empty list - user have not additional privilages on site.

You can add roles to user in `roles` property manually.

**Note** that we need use roles as a string values. By convenience we have standard roles: **admin**, **moderator** and **staff**.

You can add additiopnal roles to user and check this roles in your application. For example, you need develop `forum` application and nex next roles: admin, moderator, banned. Than add to user `roles` property next values: forum\_admin, forum\_moderator and forum\_blocked. Separate application name and user role by underscore.

```
# change user roles
user.roles = ["forum_admin", "forum_moderator"]
user.put()
```

### Admin roles defined in configuration file ###

You can specify site administrators simply adding his nick names _(or emails)_ to project [config.yaml](Config.md) file in `apps.user.admins` section like this:

```
# file apps/config.yaml
apps:
  user:
    admins: ["james", "sarra", "bob"]
```

Specified users automatically have administrator privileges on the site.

### Check user role ###

You can check user role with this call:

```
# check user role
if user.has_role("admin") or user.has_role("blog_moderator"):
  # do something
```

Also we have simple shortcuts for check roles:

```
# check user role
if user.is_admin or user.is_blog_moderator:
  # do something
```

If you want to check, if current **user is active** - you need add role **`active`** to this user:

```
# check user role
if user.is_active:
  print "Your account is active!"
```

**Note** that really we not add role to user **roles**. Instead we have detect this action and handle this in different way - we have set user property **`user.active = True`**. This need for select _not active_ users with equal operator.

```
# select not active users with age > 20 years
users = UserLocal.all().filter("active", False).filter("age>", 20)
```

## Work with users in templates ##

In [templates](Templates.md) you can work with users as expected:

```
<p>
  {% if user %}Hello {{ user.name }}!{% endif %}
  {% if user.is_admin or user.is_moderator %}
    You have an additional privilagies on this page.
  {% endif %}
</p>
```

## Actual development tasks ##

You can find all [tasks associated with user application](http://code.google.com/p/appengine-framework/issues/list?q=label:Component-App-User). Please tell us about any problems and propositions in comments below on this page. Or, you can [create new issue](http://code.google.com/p/appengine-framework/issues/entry) if this is critical task.