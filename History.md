Useful links:
  * full list of [changes in source code](http://code.google.com/p/gaeframework/source/list)
  * [opened tasks](http://code.google.com/p/gaeframework/issues/list), (bugs and features requests)
  * http://gaeframework.com current release of GAE framework in action

## Project history ##

Since **Jan 2010** we start our work, and continue improve our project for you.

#### GAE framework 1.0 RC8 _(?? March 2011)_ ####

  * **FIXED**
  * **ADDED**
  * **IMPROVED**

#### GAE framework 1.0 RC7 _(10 March 2011)_ ####

  * **FIXED**
    * fixed order of loading templates (firstly from `apps/site/templates` and finally from `apps/app_name/templates`)
    * fixed pagination
    * fixed compatibility with `_ah/admin/` on local dev server to use administrative interface and website in one session
    * fixed bug in `get_object_or_404` if passed incorrect key
    * fixed translate text in `forms.FormModel` (use kind name of model to detect application name)
  * **ADDED**
    * added `db.UniqueModel` and `db.CachedModel` to use with regular `db.Model`
    * added `forms.SelectMultiple`
    * changed apps to work with new `UniqueModel`
    * added `users_list` handler to `apps.user`
    * enabled appstats
    * added standard template loader for compatibility with appengine administrative interface
  * **IMPROVED**
    * improved compatibility with [Django Forms](Forms.md):  `SelectMultiple` and `MultipleHiddenInput`
    * rename `gae.core` to `gae.tools`
    * added native Django i18n support for translate Django Forms messages to site language
    * improved {% url %} template tag to autodetect model instance
    * added some useful translations to russian language
    * improved `get_object_or_404` to work with named keys, ids and real keys in one place

#### GAE framework 1.0 RC3 _(?? January 2011)_ ####

  * **FIXED**
  * **ADDED**
  * **IMPROVED**
    * project moved from SVN to Mercurial repository
    * wiki documentation created from the scratch

#### GAE framework 1.0 RC2 _(07 January 2011)_ ####

  * **FIXED**
  * **ADDED**
  * **IMPROVED**

#### GAE framework 1.0 RC1 _(23 December 2010)_ ####

  * **FIXED**
  * **ADDED**
    * file `appengine_config.py` in root directory _(for session support)_
    * file `apps/cron.py` where described regular tasks _(run every minute)_
  * **IMPROVED**

#### GAE framework 1.0 beta10 _(07 December 2010)_ ####

  * **FIXED**
    * admin app
    * translations mechanism
  * **ADDED**
    * `|translate` template filter
  * **IMPROVED**
    * all applications movet to single directory `apps` _(directory `gae/apps` was removed)_
    * moved request handlers from `__init__.py` to `controllers.py` file for each application
    * blog app: translated to russian; changed date formats
    * welcome page: changed screenshots and textual instruction
    * small changes in design _(light gray colors)_
    * added sidebar banner

#### GAE framework 1.0 beta9 _(26 November 2010)_ ####

  * **FIXED**
    * deleted **article** app _(use **blog** app instead)_
    * repaired `indexes.yaml`
    * serving static files from `gae/apps`
    * blog app: finished improvements and bug fixes
    * shortcuts: added 404 error to response
    * problems with import `instance` from `gae.webapp`
    * **comment** app
    * translate template tag for use variables
  * **ADDED**
    * to `gae.db` added [Model](models.md) class for allow define **KEY\_NAME** property in user models
    * welcome page
    * relocated **blog** app to `gae/apps` directory
    * **adv** app renamed to **banner**
    * added `gae.shortcuts`
    * template tag `debug` for show available properties in passed object
    * `get_var()` method in `BaseNode` template tags
    * `PhoneListProperty` field
    * loading of `settings.yaml` file
  * **IMPROVED**
    * moved `Pages` component to `gae.pages`: allow iterate throught object _(method records() still available)_
    * changed root url definition in `config.yaml`
    * wiki **gae.markup** parser: url detection
    * design in **blog** app
    * **admin** app for support `form` attribute


#### GAE framework 1.0 beta8 (updated) _(14 September 2010)_ ####

  * fixed problem with load static files from `/app_name/static/` directory
  * was delete monkey patching and added `gae.db` and `gae.forms` packages with changed components. Use this components instead of Google App Engine and Django standard components
  * added rule for loading templates in new order _[read more](Templates.md)_

#### GAE framework 1.0 beta8 _(13 September 2010)_ ####

  * upgrade Django to version 1.2.3
  * _changes list not completed yet_

#### GAE framework 1.0 beta7 _(5 July 2010)_ ####

  * implemented application [admin](App#Admin.md)
  * improved application [product](App#Product.md)
  * _changes list not completed yet_

#### GAE framework 1.0 beta6 _(14 Apr 2010)_ ####

  * [r137](https://code.google.com/p/gaeframework/source/detail?r=137) Fixed problem with wiki parser (use `#` in url adress)
  * [r137](https://code.google.com/p/gaeframework/source/detail?r=137) Fixed problem with confirmation window on edit and delete article
  * [r136](https://code.google.com/p/gaeframework/source/detail?r=136) Fixed problem with incorrect show comments count.
  * [r136](https://code.google.com/p/gaeframework/source/detail?r=136) Added **variable app** with instance of current run application
  * [r134](https://code.google.com/p/gaeframework/source/detail?r=134), [r135](https://code.google.com/p/gaeframework/source/detail?r=135) Added **django.zip version 1.1** for use latest features
  * [r132](https://code.google.com/p/gaeframework/source/detail?r=132) Optimized using one instance of environment for many requests _(increased application speed)_
  * [r131](https://code.google.com/p/gaeframework/source/detail?r=131) Changed CSS styles (`.panel` replaced to `.bg`)
  * [r130](https://code.google.com/p/gaeframework/source/detail?r=130) Not handle **favicon.ico** requests by handler and use `/static/img/favicon.ico` file
  * [r129](https://code.google.com/p/gaeframework/source/detail?r=129) Added support of **wiki** markup transformation to html
  * [r126](https://code.google.com/p/gaeframework/source/detail?r=126) Delete comments part from [articles](App#Articles.md) application
  * [r126](https://code.google.com/p/gaeframework/source/detail?r=126) Completed [comments](App#Comments.md) application for work with all types of objects _(now work well with articles application)_

#### GAE framework 1.0 beta5 _(5 Apr 2010)_ ####

> ATTENTION. Add prefix to all models in your applications. For example, in blog application you replace `Post` to `BlogPost`, `Comment` to `BlogComment`, etc

> UPGRADE FROM THE PREVIOUS VERSION. Delete all data in storage before upgrade to current release. You can backup all data before upgrade and restore this data in python script after upgrade to latest version of GAE framework. Old and new models not compatible

  * added prefix (application name) to all models
  * [r119](https://code.google.com/p/gaeframework/source/detail?r=119), [r120](https://code.google.com/p/gaeframework/source/detail?r=120), [r121](https://code.google.com/p/gaeframework/source/detail?r=121) Completed comments part in articles application
  * [r117](https://code.google.com/p/gaeframework/source/detail?r=117) Added new models definition to blogs application _(with comments part)_
  * [r115](https://code.google.com/p/gaeframework/source/detail?r=115) Rewrited comments application from the scratch
  * [r114](https://code.google.com/p/gaeframework/source/detail?r=114) Fixed potential problem with loading not existing application
  * [r113](https://code.google.com/p/gaeframework/source/detail?r=113) Deleted tmp files .pyc and .pyo and ignore this files
  * [r104](https://code.google.com/p/gaeframework/source/detail?r=104) Changed font size of page and fixed mistake in urls.yaml
  * [r103](https://code.google.com/p/gaeframework/source/detail?r=103) `[guestbook]` Fixed redirect to list of all messages after posting message
  * fixed [issue 9](https://code.google.com/p/gaeframework/issues/detail?id=9). Added method "manage" for detect if current user can manage current object
```
  {% if article.manager %}
     | <a href="/{{ app_name }}/edit_{{ article.key.id }}">Edit</a>
     | <a href="/{{ app_name }}/delete_{{ article.key.id }}">Delete</a>
  {% endif %}
```

#### GAE framework 1.0 beta4 _(28 Feb 2010)_ ####

  * ignored `django.zip` package
  * added support of all stable versions of **Django 1.x** framework
  * now need specify application name in call `render()` function
  * fixed bug with set instance to Application class as static attribute
  * added autodetection of `development` or `live` environment
  * added attribute `instance` to `Application` class _(for calls outer of the class)_
  * renamed `NotUserCommentForm` to `GuestCommentForm`
  * improved printing a full information about error in templatetags
  * renamed applications `todo` and `account` to [todos](App#Todos.md) and [accounts](App#Accounts.md). Added main template only for todos
  * changed templates for [articles](App#Articles.md) _(added creation date)_
  * fixed templatetags for work with project and Django libraries in tag `{% load %}`
  * changed option name `params` to `arg` in `urls.yaml`
  * added support of template tags (similar with Django, but with changes)
  * fixed problem with sidebar AdSence block (not closed attribute quote)
  * added [comments](App#Comments.md) application _(alpha)_. Small changes in styles
  * separate css to different files (each file for corresponding application)
  * delete not used import from main.py file
  * fixed width of right sidebar. Added css style `.panel` with gray color text

#### GAE framework 1.0 beta3 _(2 Feb 2010)_ ####

  * added **@login\_required** decorator and apply it in applications
  * fixed [issue 1](https://code.google.com/p/gaeframework/issues/detail?id=1)
  * deleted **.pyc** and **.pyo** files and SVN ignore this files
  * changed **articles** application - show actions panel only for admin user
  * changed redirect to main page after _create, edit or delete_ actions
  * upgrade **jQuery** to 1.4.1
  * created application **todo** _(alpha)_
  * changed application **account** _(alpha)_
  * changed sidebar CSS style. Added AdSense blocks

#### GAE framework 1.0 beta2 _(28 Jan 2010)_ ####

  * project uploaded to GAE server by address http://gae-framework.appspot.com
  * added button 88x31
  * fixed [issue 4](https://code.google.com/p/gaeframework/issues/detail?id=4)
  * added **user** and **user\_auth\_url** variables to all templates
  * added dropdown menu for show all applications
  * changed main page - added description of project
  * added **jQuery** library
  * change footer color to white
  * renamed application **greeting** to **guestook**. Applied **forms** in application guestbook
  * created **account** and **todo** applications
  * added **blog** application _(alpha)_

#### GAE framework 1.0 beta1 _(21 Jan 2010)_ ####

  * implement support of urls map _(**urls.yaml** file)_
  * implement work with GAE **forms**
  * implement work with GAE Django **templates** _(load templates from application directory and project directory)_
  * added base application **app** for implement all useful logic for all applications _(such as **redirect**, **render**, changed GAE template component)_
  * created reusable applications **products** and **greetings** _(all appliccations end to "s" letter)_