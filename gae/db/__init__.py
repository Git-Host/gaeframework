import os, logging
from google.appengine.api import memcache
from google.appengine.ext.db import Model, Property

    
class Model(Model):
    '''
    Base model class with additional features:
     - adds application name to model class name
     - allow compare two model instances by the key
    '''
    @classmethod
    def kind(cls):
        '''Return class name in format <AppnameClassname>'''
        # get application name from path "app_name.models"
        app_name = cls.__module__.split('.')[1].title()
        # application name and model name have the same name like BlogBlog
        if app_name.lower() == cls.__name__.lower():
            return cls.__name__
        # add application name as prefix of model
        return "%s%s" % (app_name, cls.__name__)

    def __eq__(self, other):
        # compare objects keys
        if self.is_saved() and isinstance(other, Model) and other.is_saved():
            return self.key() == other.key()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class UniqueModel:
    '''Model with control unique properties'''
    
    def put(self, **kwargs):
#        if not self.is_saved():
#            self._key_name = self._generate_key()
        self._key_name = self._generate_key()
        super(Model, self).put(**kwargs)

    def _generate_key(self):
        """A Model for entities which automatically generate their own key names
        on creation."""
        key_name = None
        if hasattr(self, 'KEY_NAME'):
            # get value for each property
            properties = dict()
            for prop in self.properties().values():
                value = getattr(self, prop.name)
                if hasattr(value, 'key'):
                    value = value.key().name()
                properties[prop.name] = value 
            # The KEY_NAME must either be a callable or a string.
            # If it's a callable,we call it with the given keyword args.
            if callable(self.KEY_NAME):
                key_name = self.KEY_NAME(properties)
            # If it's a string, we just interpolate the keyword args into the
            # string, ensuring that this results in a different string.
            else:
                # Try to create the key name, catching any key errors arising
                # from the string interpolation
                try:
                    key_name = str(self.KEY_NAME) % properties
                except KeyError:
                    raise RuntimeError, "Missing keys required by %s entity's "\
                                        "KEY_NAME property (got %r)" %\
                                        (self.entity_type(), properties)
                # Make sure the generated key name is actually different from
                # the template
                if key_name == str(self.KEY_NAME):
                    raise RuntimeError, 'Key name generated for %s entity is '\
                                        'same as KEY_NAME template' %\
                                        self.entity_type()
        # return changed arguments
        return key_name


class CachedModel:
    '''Model with cache support for properties'''
    MEMCACHE_LIFETIME = 3600 # in seconds

    def __getattr__(self, name):
        '''
        Return cached property.

        Usage: blog_entry.author__nick'''
        try:
            # check parent class virtual property
            return super(Model, self).__getattr__(name)
        except AttributeError:
            pass
        if name.find("__") <= 0: # not handle "__iter__" and other magic methods
            raise AttributeError
        # try to load cached property
        memcache_key = "Kind: %s. Key: %s. Property: %s" % (self.kind(), self.key(), name)
        # load field from memcache
        field_value = memcache.get(memcache_key)
        if field_value is None:
            try:
                # get field value based on sequence of field names
                field_value = self
                for field in name.split('__'):
                    if field_value is None: break
                    field_value = getattr(field_value, field)
                    # call method
                    if callable(field_value):
                        field_value = field_value()
                # convert value to string
                if isinstance(field_value, (Model, Property)):
                    field_value = unicode(field_value)
            except:
                raise AttributeError
            if field_value is not None: # set field value to memcache
                if not memcache.add(memcache_key, field_value, time=self.MEMCACHE_LIFETIME):
                    logging.error("Memcache set failed. CachedModel field %r" % name)
        return field_value
