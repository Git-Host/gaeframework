from gae.tools import applications


def cron(request):
    '''
    Execute cron jobs for each application with file cron.py
    '''
    for app_name in applications():
        print __import__("..%s" % app_name)
    return "Cron jobs completed!"
