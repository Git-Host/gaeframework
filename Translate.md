**Internationalization and localization** - translate text to different languages. Based on YAML files.

### Basic principles ###

With multi lingual support you can create web site translated on on the languages. You simply tell translation and pass English text phrase - and get back translated text to current language specified for user.

To do this, Your need create special translation files for the each application, where saved references between English and translated sentences.

**NOTES:**
  * please restart development server after each change in translation file

### Set available languages and default language ###

You can set available languages for your website and also default language - for show page on this language. Do this in file **`apps/config.yaml`** by adding this lines:

```
language: en
languages: [en, fr, de, ua, ru]
```

### Language codes ###

We have used standard short forms of language names like this: **en, fr, de**.

We have also support language codes in format: **pt-br, es-ar, de-at**.

### About translations ###

If you need translate text - than we search this sentence in the next order:
  1. **`apps/APP_NAME/translate/LANGUAGE.yaml`** - application specific translation
  1. **`translate/LANGUAGE.yaml`** - global translation
  1. return original English sentence if we have not found translation

### Global translation ###

Global translations place is **`translation/`** root directory. You can create new translation by creating or changing existing file. BFor example, we need to add Russian translation of sentence. Than we have create file **`translate/ru.yaml`** with the next contents:

```
Hello: Привет
Hello World: Привет Мир
```

### Application specific translations ###

You can use global translation fr translate sentences. But we recommend You create seperate translation for the each application. You can do this by create translation file in application directory **`apps/APP_NAME/translation/LANGUAGE.yaml`**.

For example, we need translate application [blog](AppsBlog.md) to Russian language. Than create file **`apps/blog/translation/ru.yaml`** with next content:

```
blog: блог
message: сообщение
messages: сообщения
```

**NOTE** that you need quote next values: _yes, no, true, false, 0, 1_. For example:

```
"yes": да
hello: привет
"0": ноль
"True": Истина
```

### Multi language support into Python files ###

You can use translations anywhere in Python files. For get translated string, you need to do next:
  * import translation function: **`from gae.translation import translate as _`**
  * insert translated text into function, like this **`_("Hello")`**

In result your Python script to be next:
```
from gae.translation import translate as _

print _("Hello")
```

Also you can use this principle into your [models.py](odels.md) and [forms.py](Forms.md) files to do translation of messages.

### Multi language support in templates ###

To get translated sentence into templates, you need to use special template tag:

```
<b>{% translate "Hello" %} {% translate user.nick %}</b>
```

In this case we have translate content of variable **`user.nick`**. If we have not found translation of user nick - than we show original user nick.

### More about `gae.translation` ###

Module **`gae.translation`** have next functions:
  * **get\_language()** - return current active language. By default "en"
  * **get\_available\_languages()** - return list of all languages, supported by current site. This is option **`languages`** in project [config.yaml](Config.md)
  * **set\_language_(language)_** - activate current language. All messages to be translated on specified language. This language should be specified in `languages` option in the project [config.yaml](Config.md)
  * **translate_(message, app\_name=None)_** - translate text to current active language. If specified **`app_name`** than used this value instead of current application name used in current request