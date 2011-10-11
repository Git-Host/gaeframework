from gae.db import Model, UniqueModel, fields

class Tag(Model):
    name = fields.String('tag name', required=True)
    used = fields.Integer('tag used times', default=0)

    def __unicode__(self):
        return self.name

class Entity(UniqueModel, Model):
    KEY_NAME = "%(slug)s"
    slug = fields.String('entry url', required=True)
    title = fields.String(required=True)
    description = fields.String()
    text = fields.Text(required=True)
    author = fields.User(auto_current_user_add=True, required=True)
    created = fields.DateTime(auto_now_add=True)
    changed = fields.DateTime(auto_now=True)
    active = fields.Boolean(default=False)
    tags = fields.StringList()

    def __unicode__(self):
        return self.title