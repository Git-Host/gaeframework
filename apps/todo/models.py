from gae.db import Model, fields
from apps.user import get_current_user

class Todo(Model):
    author           = fields.User(auto_current_user_add=True, required=True)
    title            = fields.String(required=True)
    description      = fields.String(multiline=True)
    url              = fields.String()
    created          = fields.DateTime(auto_now_add=True)
    updated          = fields.DateTime(auto_now=True)
    due_date         = fields.String(required=True)
    finished         = fields.Boolean(default=False)

    def manager(self):
        '''If user allow to manage current todo'''
        current_user = get_current_user()
        return self.author == current_user or current_user.is_admin