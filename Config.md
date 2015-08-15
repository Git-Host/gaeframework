We have two types of configurations:
  * **site configuration** - file located in **`apps/site/config.yaml`** where defined project settings. Also we can redefine some settings for each application
  * **application configuration** - file located in **`apps/APP_NAME/config.yaml`** where defined application specific settings

## Work with configurations ##

We have implemented easy for use configuration tools. You can get configuration of project or specified application anywhere in Python code.

```
from gae.config import get_config

config = get_config()
admins = config.get("user.admins")
default_language = config.get("site.language", "en")

# short form - recommender for use
admins = get_config("user.admins", default_value=[])
```

**First argument** - this is path to configuration in dotted style. Initially, we look for an options in **`apps/site/config.yaml`** file. If options not found - we look to **`apps/APP_NAME/config.yaml`** file. If options not found - we return default value specified in  **second argument** _(by default is **None**)_

## Urls mapping ##

To join requests and application handlers we have used **urls mapping**. All rules defined in site config **`apps/site/config.yaml`** file in `urls` section.

```
# global url mapping
urls:
 - url:
   run: page.render
   arg: {template: welcome}

 - url: admin/
   map: admin

 - url: myblog/
   map: blog
```

GAE framework search requested page from the first top rule, and go to the next rule if url not found.

We have explain code, shown above:
| **Requested url** | **Search request handler in ...** |
|:------------------|:----------------------------------|
| **`http://your-site.name`** | apps/page/controllers.py          |
| **`http://your-site.name/admin`** | apps/admin/config.yaml            |
| **`http://your-site.name/myblog`** | apps/blog/config.yaml             |
| other requests    | shown error 404 - page not found  |

We can define url mapping in global configuration and in application configuration files. In any case - we should define urls maping in **urls** section in format, described above. For each url we can define next options:
  1. **`url`** - define url address for compare with requested  page address
  1. **`run`** _(required if not defined **map** option)_ - define request handler in format **`APP_NAME.HANDLER_NAME`**, where HANDLER\_NAME - this is a function name in file [apps/APP\_NAME/controllers.py](Controllers.md)
  1. **`map`** _(required if not defined **url** option)_ - define what application should be attached to this url address for handle request. We have load url mapping from the given application **`apps/APP_NAME/config.yaml`** and search appropriate request handler
  1. **`arg`** _(optional)_ - define default parameters to pass to request handler function. If we have matched parameters in **url** than we have used this values instead of default parameters