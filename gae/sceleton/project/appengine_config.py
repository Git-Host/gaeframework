import os
from google.appengine.ext.appstats import recording
from gae.sessions import SessionMiddleware
import gae.webapp

COOKIE_KEY = 'my_private_key_used_for_this_site_%s' % os.environ['APPLICATION_ID']

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key=COOKIE_KEY, cookie_only_threshold=0)
    app = recording.appstats_wsgi_middleware(app)
    return app
