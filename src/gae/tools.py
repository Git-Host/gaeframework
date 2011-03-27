import os, re

_applications = None
def applications():
    global _applications
    '''List of all available applications'''
    if _applications is None:
        _applications = dict([(app, os.path.join('apps', app))
                               for app in os.listdir('apps')
                               if os.path.isdir(os.path.join('apps', app))])
    return _applications

def monkey_patch(name, bases, namespace):
    assert len(bases) == 1, 'Exactly one base class is required'
    base = bases[0]
    for name, value in namespace.iteritems():
        if name not in ('__metaclass__', '__module__'):
            setattr(base, name, value)
    return base

def prepare_url_vars(url_address, var_pattern="(?P<\\1>[^/]+)"):
    '''
    Return url address with replaced variables from UPPER_NAME to specified pattern in lower_name style.
    
    Examples:
        blog/BLOG_SLUG/new -> blog/%(blog_slug)s/new
        blog/category:CATEGORY_SLUG -> blog/category:(?P<category_slug>[^/]+)
    '''
    return re.sub("([A-Z][A-Z0-9_]*)", lambda x: re.sub("(.*)", var_pattern, x.group().lower()), url_address).replace(" ", "")