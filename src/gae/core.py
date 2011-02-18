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
