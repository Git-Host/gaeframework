import os

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