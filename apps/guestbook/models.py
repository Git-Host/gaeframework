from gae.db import Model, fields
from apps.user import get_current_user

class Message(Model):
    author  = fields.User(auto_current_user_add=True)
    content = fields.String(multiline=True, required=True)
    date    = fields.DateTime(auto_now_add=True)
    
    def manager(self):
        '''If user allow to manage current message'''
        current_user = get_current_user()
        return self.author == current_user or current_user.is_admin