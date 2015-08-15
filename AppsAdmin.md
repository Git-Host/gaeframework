Administration interface for all applications in project.

For use administration interface, to do next things for each application:
  1. register managed models _(see below)_
  1. reload development server
  1. open http://localhost:8080/admin admin section for show changed admin section

### Register managed models ###

You need to create file `admin.py` in your application where your need to register all required models.

```
# import required models
from models import BlogPost, Blog
from forms import BlogPostForm

# create new class with name equal to model name
# in this model you can configure administration behavior
class BlogPost:
    name   = "Blog posts"
    model  = BlogPost
    form   = BlogPostForm
    fields = ['title', 'author', 'added']
    order  = ['active', '-added']

    def before_create(self, data):
        if not "title" in data:
            raise Exception("Title is required")
        data.title += " | My blog"

class Blog:
    model  = Blog
```

Available properties _(only `model` property is required, all other - optional)_:
  * `name` - used as name of model. By default used model name like BlogPost
  * `model` - managed model
  * `form` - if given, replace basic form based on specified model class. Use it only if your form have changed model fields
  * `fields` - show only this fields on page with all records list
  * `order` - default sort order

You can add methods _(all optional)_:
  * `before_create` and `after_create` - was called on record create
  * `before_change` and `after_change` - was called on record change (edit)
  * `before_delete` and `after_delete` - was called on record delete