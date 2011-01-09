'''
Administration interface.
'''
from apps.comment.models import Comment

class Comment():
    name = "Comments list"
    model = Comment
    fields = ('title', 'author', 'created', "active")
