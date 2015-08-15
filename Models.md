Models in appliations placed in `models.py` file. This models defined as descriibed in oficial [Google App Engine documentation](http://code.google.com/appengine/docs/python/datastore/) with small additions described below.

## Cached properties in models ##

Use `__` two underscores to access to cached properties. On fists  call this value to be stored to memcache and in all next requests this value restored from memcache instead of getting value from datastore.

```
from apps.blog.models import Entity, Blog

blog = Blog.get("my_blog")
author_nick = blog.author__nick # cached property - stored in memcache
blog_posts = blog.entities__count

entity = Entity.get("entity_number_one")
blog_author_nick = entity.blog__author__nick
```

If you need to work without cached properties - use regular syntax:

```
from apps.blog.models import Entity, Blog

blog = Blog.get("my_blog")
author_nick = blog.author.nick # NOT cached property - each time make call to datastore
blog_posts = blog.entities.count()

entity = Entity.get("entity_number_one")
blog_author_nick = entity.blog.author.nick
```

**NOTE #1**. Cached property stored in memcache on the 60 minutes.

## Unique property - `KEY_NAME` ##

You can define named key, based on one or many model properties.

Restrictions:
  * possible define only one named key in model
  * **you can't change _named key_ in future!**

Define unique property in format `%(property_name)s`:
```
class Blog(db.Model):
    KEY_NAME = "%(slug)s"
    slug = db.StringProperty('blog url', required=True)
    name = db.StringProperty('blog name', required=True)

class BlogEntity(db.Model):
    KEY_NAME = "%(blog)s/%(slug)s"
    slug = db.StringProperty('blog post url', required=True)
    title = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    blog = db.ReferenceProperty(reference_class=Blog, required=True)
```

Get object by named key:
```
mike_blog = Blog.get_by_key_name("mike")

entity_in_mike_blog = BlogEntity.get_by_key_name("%s/%s" % ("mike", "my_first_blog_post"))
```