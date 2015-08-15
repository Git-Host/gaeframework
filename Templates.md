Templates help you insert prepared data to the web page.

## Templates loading order ##

Templates loaded into next orser:
  1. try to load template from **`/apps/site/templates/app_name/`** directory
  1. try to load template from **`/apps/app_name/templates/`** directory
  1. try to load template from **`/apps/site/templates/`** directory

## Templates overlap ##

If you need change template **`blogs_list.html`** into the **blog** application than copy this template
  * from **`/apps/blog/templates/blogs_list.html`**
  * to **`/apps/site/templates/blog/blogs_list.html`**
and this template to be used.

## Template tags ##

**Default template tags**:
  * **`{% back_url %}`** - return url to previous page
  * **`{% current_url %}`** - return current page address
  * **`{% translate %}`** - return translated text
```
# current used application detected automatically
{% translate "Hello World" %}

# specify application, where we need search translations
{% translate "Hello" "blog" %}

# available template filter
{{ user.name|translate }}
```
  * **`{% show_pages %}`** - show page nuumbers, rendered in template **`/apps/site/template/common/show_pages.html`**
```
  {% show_pages blogs %}
```
  * **`{% debug %}`** - show information about passed variable