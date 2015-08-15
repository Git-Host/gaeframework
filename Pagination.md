You can create pagination by results set. This is very easy!

## Pagination with `gae.pages` ##

So, we describe how to create pagination by blogs. Open file **`apps/blog/controllers.py`** and study source code:

```
from gae.pages import Pages

def blogs_list(app):
  blogs = Blog.all().order('-created')
  return app.render('blog/blogs_list', {
                     # pass records set, specify records per page
                     # and *optional* variable name used in GET
                    'blogs': Pages(blogs, 20, "blogs_page"),
                    })
```

### How it works ###

See on line `Pages(blogs, 20, "blogs_page")` - this is create a pager, where we pass next parameters:
  * collection of results _(google.appengine.ext.db.Query object)_
  * count of records per page
  * _optional_ variable name used in GET. We see links like this **`/blog/blogs_list?blogs_page=2`** instead on **`/blog/blogs_list?page=2`**

### Use pager in templates ###

Open **`blog/templates/blogs_list.html`** file.

You can show records on curent page from `blogs` collection. This code is show all records from collection:
```
  {% for blog in blogs %}
    <div class="blog">
      <h2><a href="/{{ app }}/{{ blog.details_url }}">{{ blog.name }}</a></h2>
    </div>
  {% empty %}
    {% translate "No blogs" %}
  {% endfor %}
```

This is show pagination links:
```
  {% show_pages blogs %}
```