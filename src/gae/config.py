'''
Work with project and application configuration files.

Usage:
    from gae.config import get_config
    config = get_config()
    admins = config.get("apps.user.admins", default_value=[])
    # short form
    admins = get_config("apps.user.admins", default_value=[])
'''
import os, yaml, sys, copy

__all__ = ["get_config"]

class Config:
    _project_config = None
    _apps_configs = {}

    def __init__(self):
        # load project and all application configurations only once
        if Config._project_config is not None:
            raise Exception, "For access to configuration please use get_config() function"
        # get project information
        App = sys.modules['gae.webapp'].App
        project_dir = os.path.join(App.project_dir, 'apps')
        apps = App.apps_list()
        # get list of configuration files
        apps_configs = [(app_name, os.path.join(app_path, "config.yaml")) for app_name, app_path in apps.items()]
        project_config = os.path.join(project_dir, "config.yaml")
        # load configuration files
        Config._project_config = self._load_config(project_config)
        for app_name, app_config in apps_configs:
            Config._apps_configs[app_name] = self._load_config(app_config)

    def _load_config(self, config_file):
        try:
            fd = open(config_file)
            config = yaml.load(fd)
            fd.close()
            return config
        except:
            raise Exception("Configuration file '%s' not found" % config_file)

    def get(self, path, default_value=None):
        '''Return configuration by given options path.
            1. look in file "apps/config.yaml" and if not found than
            2. look in file "apps/app_name/config.yaml"
            3. return default_value if not found given option

        Usage:
            settings.get("apps.user.admins")
            settings.get("language", "default_value")

        TODO: add support for dictionary lookup: settings["apps.user.admins"]
        '''
        # search in project configuration file
        config = self._project_config
        for piece in path.split('.'):
            config = config.get(piece)
            if config is None: break
        # search in application configuration file
        if config is None and path.startswith("apps."):
            # use path after "apps.app_name"
            app_name, path = path.split('.', 2)[1:]
            config = self._apps_configs.get(app_name, {})
            for piece in path.split('.'):
                config = config.get(piece)
                if config is None: break
        return copy.deepcopy(config) if config is not None else default_value

config = None

def get_config(path=None, default_value=None):
    # create one copy of configuration
    global config
    if config is None:
        config = Config()
    # load given configuration options
    if path is not None:
        return config.get(path, default_value)
    return config