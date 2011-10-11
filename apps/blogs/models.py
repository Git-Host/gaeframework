from gae.db import Model, UniqueModel, fields
from apps.user import get_current_user

class Blog(UniqueModel, Model):
    KEY_NAME = "%(slug)s"
    slug = fields.String('blog url', required=True)
    name = fields.String('blog name', required=True)
    author = fields.User(auto_current_user_add=True, required=True)
    created = fields.DateTime(auto_now_add=True)
    active = fields.Boolean(default=False)

    def __unicode__(self):
        return self.slug

    def manager(self):
        '''If user allow to manage current article'''
        current_user = get_current_user()
        return self.author == current_user or current_user.is_admin
    
    def details_url(self):
        return self.key().name()

    def edit_url(self):
        return "%s/edit" % self.key().name()

    def delete_url(self):
        return "%s/delete" % self.key().name()

class Tag(Model):
    slug = fields.String('tag url', required=True)
    name = fields.String('tag name', required=True)
    used = fields.Integer('tag used times', default=0)

    def __unicode__(self):
        return self.name

class Entity(UniqueModel, Model):
    KEY_NAME = "%(blog)s/%(slug)s"
    slug = fields.String('blog post url', required=True)
    title = fields.String(required=True)
    description = fields.String()
    text = fields.Text(required=True)
    author = fields.User(auto_current_user_add=True, required=True)
    created = fields.DateTime(auto_now_add=True)
    changed = fields.DateTime(auto_now=True)
    active = fields.Boolean(default=False)
    # references
    blog = fields.Reference(reference_class=Blog, required=True)
#    tags = fields.ReferenceList(BlogTag)

    def __unicode__(self):
        return self.title

    def manager(self):
        '''If user allow to manage current article'''
        current_user = get_current_user()
        return self.author == current_user or current_user.is_admin

    def details_url(self):
        return self.key().name()

    def edit_url(self):
        return "%s/edit" % self.key().name()

    def delete_url(self):
        return "%s/delete" % self.key().name()