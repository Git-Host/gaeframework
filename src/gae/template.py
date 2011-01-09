import sys, os
from google.appengine.ext.webapp.template import *
from google.appengine.ext.webapp.template import _swap_settings, _urlnode_render_replacement

def render(template_path, template_dict, debug=False):
    """
    Renders the template at the given path with the given dict of values.
    
    Example usage:
      render("app_name/index.html", {"name": "Bret", "values": [1, 2, 3]})
    
    Args:
      template_path: path to a Django template
      template_dict: dictionary of values to apply to the template
    """
    t = load(template_path, debug)
    return t.render(Context(template_dict))


template_cache = {}
def load(path, debug=False):
    """
    Loads the Django template from the given path.
    
    It is better to use this function than to construct a Template using the
    class below because Django requires you to load the template with a method
    if you want imports and extends to work in the template.
    """
    if not debug:
        template = template_cache.get(path, None)
    else:
        template = None
    
    if not template:
        # get application name and template name
        try:
            app_name, template_path = path.split('/', 1)
        except ValueError:
            app_name = ""
            template_path = path
        project_dir = sys.modules['gae.webapp'].App.project_dir
        directory, file_name = os.path.split(template_path)
        new_settings = {
            'TEMPLATE_DIRS': (os.path.join(project_dir, 'templates', app_name, directory),
                              os.path.join(project_dir, 'apps', app_name, 'templates', directory),
                              os.path.join(project_dir, 'templates', directory)),
            'TEMPLATE_DEBUG': debug,
            'DEBUG': debug,
            }
        old_settings = _swap_settings(new_settings)
        try:
            template = django.template.loader.get_template(file_name)
        finally:
            _swap_settings(old_settings)

        if not debug:
            template_cache[path] = template
    
        def wrap_render(context, orig_render=template.render):
            URLNode = django.template.defaulttags.URLNode
            save_urlnode_render = URLNode.render
            old_settings = _swap_settings(new_settings)
            try:
                URLNode.render = _urlnode_render_replacement
                return orig_render(context)
            finally:
                _swap_settings(old_settings)
                URLNode.render = save_urlnode_render

        template.render = wrap_render
    
    return template