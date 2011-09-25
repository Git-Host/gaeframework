import os

def development_env():
    return os.environ['SERVER_SOFTWARE'].startswith('Development')

_installed_apps = None
def installed_apps():
    '''
    Return list of installed applications.
    '''
    global _installed_apps
    if not _installed_apps:
        _installed_apps = [app for app in os.listdir('apps') if os.path.isdir(os.path.join('apps', app)) and not app.startswith("_")]
    return _installed_apps

def monkey_patch(name, bases, namespace):
    assert len(bases) == 1, 'Exactly one base class is required'
    base = bases[0]
    for name, value in namespace.iteritems():
        if name not in ('__metaclass__', '__module__'):
            setattr(base, name, value)
    return base
