from gae.db import Model, fields

class Message(Model):
    created     = fields.DateTime(auto_now_add=True)
    title       = fields.String(max_length=250, required=True)
    text        = fields.Text(required=True)
    email       = fields.Email()

class DirectMessage(Message):
    from_user   = fields.User(auto_current_user_add=True, required=True)
    to_user     = fields.User(required=True)

class Feedback(Message):
    SUBJECTS = ((0, "Other"),
                (1, "I have problems with site"),
                (2, "How it works?"),
                (3, "Advertising"),
                (4, "Investment"))
    subject     = fields.String(choices=SUBJECTS, required=True)