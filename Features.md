List of GAE framework features

### Simple project structure ###

Including pluggable [applications](Apps.md), Just copy application folder to your project `apps` directory and start use this application

### Easy [urls](Config#Urls_mapping.md) ###

Urls defined in YAML format.

```
urls:
- url: :blog/new
  run: entity_create

- url: :blog/:entity/edit
  run: entity_edit

- url: :blog/:entity/delete
  run: entity_delete
```

### Local [users](AppsUser.md) registration ###

You can register users in your local datastore. Build on super fast **sessions** stored in memcache + datastore.

### [Administration](AppsAdmin.md) interface ###

Just create description of your models - and this data automatically to be available for administration

### [Internationalization](Translate.md) support ###

Create file `apps/translate/LANG.yaml` and add translations strings _(in this case **LANG** is a short language: `ru, en, de, fr`)_

Sample translation file:
```
Create: Создать
Cancel: Отмена
Save: Сохранить
Edit: Изменить
Delete: Удалить
Show: Показать
```

### Easy work with [configurations](Config.md) ###

```
from gae.config import get_config

language = get_config("site.language", "en")
admins = get_config("user.admins", default_value=[])
```


### Cached properties in [models](Models.md) <sup>(NEW)</sup> ###

```
from apps.blog.models import Entity, Blog

blog = Blog.get("my_blog")
author_nick = blog.author__nick # cached property - stored in memcache
blog_posts = blog.entities__count

entity = Entity.get("entity_number_one")
blog_author_nick = entity.blog__author__nick
```