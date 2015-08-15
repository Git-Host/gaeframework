**Controllers** (or **request handlers**) - this is a regular Python functions.

This function apply one required parameter (always first) - **`app`** - to access to useful functions _(like: redirect, show error page, access to POST and GET parameters, etc)_.

Controller should return rendered HTML page (or JSON, or XML - depends of your choice). This text will be send back to user browser.

**NOTE #1**. In this chapter we have create an **`/apps/myapp/`** application. Create this directory with empty file **`__init__.py`**

Basic controller definition:
```
def my_action(app):
  return "<html><body>This is simple page!</body></html>"
```

### How to run controller? ###

To access to this controller, you need define:
  1. to file **`/apps/site/config.yaml`** add next lines (after "**`urls:`** line)
```
urls:
 - url: my_app/
   map: myapp
```
  1. create file **`/apps/myapp/config.yaml`** with contents
```
urls:
- url: simple_page
  run: my_action
```
  1. create file **`/apps/myapp/controllers.py`** with contents
```
def my_action(app):
  return "<html><body>This is simple page!</body></html>"
```
  1. save all files. [Restart development server](Start.md) and open page http://localhost:8080/my_app/simple_page. Appear text "This is simple page!"

### Application main page ###

Maybe, you think about "how to show page by address http://localhost:8080/my_app". Answer s easy - define empty url in **`urls.yaml`** file:
```
urls:
- url:
  run: main_page
```

### Pass parameters to controller ###

You can pass parameters to controller. For example, you need pass user name in url string. Define next rule:
```
urls:
- url: user/:user_name
  run: say_hello
```

where **`:user_name`** is a variable from requested path. For example, you can access to http://localhost:8080/my_app/user/james, where `user_name` contain "james".

Next, define controller with parameters:
```
def say_hello(app, user_name):
  return "<html><body>Hello %s!</body></html>" % user_name
```

Also, you can define not required parameters in controllers.
```
def say_hello(app, user_name=None):
  if not user_name: user_name = "anonymous"
  return "<html><body>Hello %s!</body></html>" % user_name
```

And finally, you can define some default parameters in **`config.yaml`**
```
urls:
- url: user/:user_name
  run: say_hello
  arg: {country: USA}
- url: user/:user_name/:country
  run: say_hello
```

And change controller to work with new parameter:
```
def say_hello(app, user_name, country=None):
  if not country: country = "[not specified]"
  return "<html><body>Hello %s! You are from %s</body></html>" % (user_name, country)
```

Restart server. And access to the next urls:
  * http://localhost:8080/my_app/user/james
  * http://localhost:8080/my_app/user/alex/Russia
  * http://localhost:8080/my_app/user/michael/Ukraine