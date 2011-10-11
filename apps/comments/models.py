from gae.db import Model, fields
from apps.user import get_current_user

class Comment(Model):
#    """
#    A user comment about some object.
#    """
    # user info
    author      = fields.User(auto_current_user_add=True)
#    user_name   = fields.String()
#    user_email  = fields.Email()
#    user_site   = fields.Link()
#    user_ip     = fields.String(required=True)
    # comment info
    title       = fields.String(default="Title", required=True)
    text        = fields.Text("message", default="Your message", required=True)
    created     = fields.DateTime(auto_now_add=True)
    active      = fields.Boolean(default=False)
    # references
    obj         = fields.Reference(required=False)
#    comment     = fields.SelfReference("parent comment", collection_name="comments")

    def __unicode__(self):
        return self.title

    def manager(self):
        '''If user allow to manage current comment'''
        current_user = get_current_user()
        return self.author == current_user or current_user.is_admin
