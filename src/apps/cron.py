'''
Automatically run cron jobs every minute.

TODO: run all cron.py handlers in the each application.
'''
from datetime import datetime 

NOW = datetime.now()

# clear expired sessions (every hour)
if NOW.minute == 0:
    from gae.sessions import delete_expired_sessions
    delete_expired_sessions()