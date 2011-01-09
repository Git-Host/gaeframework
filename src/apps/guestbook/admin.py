'''
Administration interface.
'''
from models import Message

class Message():
    name = "Guestbook messages list"
    model = Message
    fields = ['author', 'date']
