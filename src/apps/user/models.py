from gae import db

class User(db.Model):
    created     = db.DateTimeProperty(auto_now_add=True)
    last_access = db.DateTimeProperty(auto_now=True)
    active      = db.BooleanProperty(default=False)
    roles       = db.StringListProperty()

    @property
    def nick(self):
        raise NotImplemented

    def has_role(self, role):
        if self.roles and role in self.roles:
            return True
        return False

    def __getattr__(self, name):
        '''
        Return True if user role is found.

        Usage: user_obj.is_admin'''
        # is_admin, is_manager, is_blog_admin, etc
        if name.startswith("is_"):
            role = name[3:]
            return self.has_role(role)
        raise AttributeError

    def __eq__(self, other):
        # compare only two User objects
        if not isinstance(other, User):
            return False
        # compare only User Key
        try:
            if self.key() == other.key():
                return True
        except Exception:
            pass
        return False

class OpenIdUser(User):
    '''User registered by OpenId'''
    pass

class OauthUser(User):
    '''User registered by OAuth'''
    auth_domain = db.URLProperty(required=True)
    auth_token  = db.StringProperty(required=True)

class EmailUser(User):
    '''User registered by email and password in local datastore'''
    KEY_NAME    = "%(email)s"
    email       = db.EmailProperty(required=True)
    password    = db.StringProperty(required=True, min_length=5, max_length=25)
    confirmed   = db.BooleanProperty("Email address is confirmed", default=False)

    @property
    def nick(self):
        raise self.email

    def __unicode__(self):
        return str(self.email).split("@")[0]

class LocalUser(User):
    '''User registered by nick name and password in local datastore'''
    KEY_NAME    = "%(nick)s"
    nick        = db.SlugProperty(required=True, min_length=3, max_length=25)
    password    = db.StringProperty(required=True, min_length=5, max_length=25)

    def __unicode__(self):
        return self.nick