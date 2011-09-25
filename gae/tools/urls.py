import re
from gae.exceptions import IncorrectUrlDefinition
from gae.config import get_config
from gae.exceptions import UrlNotFound


def prepare_url_vars(url_address, template):
    '''
    Return url address with replaced variables to regex pattern.
    
    Examples:
        blog/(blog_slug)/new -> blog/%(blog_slug)s/new
        blog/category-(category_id:number) -> blog/category:(?P<category_slug>[0-9]+)
    '''
    placeholder_types = {
        'string': '[^/]+',
        'all':    '.+',
        'key':    '\w{32}',
        'number': '[0-9]+',
    }
    
    def prepare_url_variable(var_name, var_type):
        if var_type is None: var_type = 'string'
        if "," in var_type: # list of values
            var_type_regex = "(%s)" % "|".join([re.escape(str.strip()) for str in var_type.split(',')])
        else:
            var_type_regex = placeholder_types.get(var_type)
            if var_type_regex is None:
                raise IncorrectUrlDefinition("Url mapping rule has incorrect placeholder type %r" % var_type)
        try:
            return template % (var_name, var_type_regex)
        except TypeError:
            return template % var_name
    
    result = re.sub("\(([a-z][a-z0-9_]*)(:([a-z, ]+))?\)", lambda x: prepare_url_variable(x.group(1), x.group(3)), url_address).replace(" ", "")
    return result


def reverce_url(path_to_controller, *args, **kwargs):
    '''
    Return absolute url address to specified controller (host not included).
    
    Args:
        path_to_controller: String in format "app_name.short_name"
        agrs, kwargs: Only positional or named arguments passed to build url
    '''
    app_name, short_name = path_to_controller.split('.')
    # search in global urls mapping
    for site_url in get_config("site.urls", []):
        if site_url.get('run', "") != app_name: continue
        url_prefix = site_url.get('url') or ""
        # search in mapped application
        for url in get_config("%s.urls" % app_name, []):
            if url.get('short_name', "") == short_name:
                try:
                    return "/%s%s" % (url_prefix, prepare_url_vars(url.get('url') or "", "%%s")) % args
                except:
                    return "/%s%s" % (url_prefix, prepare_url_vars(url.get('url') or "", "%%(%s)s")) % kwargs
    raise UrlNotFound
