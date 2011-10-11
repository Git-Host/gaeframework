from gae.config import get_config 
from gae.db import Model, UniqueModel, fields

class User(Model):
    '''User registered by nick name and password in local datastore'''
    KEY_NAME    = "%(nick)s"
    nick        = fields.Slug(required=True, min_length=3, max_length=25)
    password    = fields.String(required=True, min_length=5, max_length=25)
    created     = fields.DateTime(auto_now_add=True)
    last_access = fields.DateTime(auto_now=True)
    active      = fields.Boolean(default=False)
    roles       = fields.StringList()

    def has_role(self, role):
        # predefined user in project config file
        if self.nick in get_config('user.%ss' % role, []):
            return True
        if self.roles and role in self.roles:
            return True
        return False

    def __unicode__(self):
        return self.nick

    def __getattr__(self, name):
        '''
        Return True if user role is found.

        Usage: user_obj.is_admin'''
        # is_admin, is_manager, is_blog_admin, etc
        if name.startswith("is_"):
            role = name[3:]
            return self.has_role(role)
        raise AttributeError
