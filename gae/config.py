'''
Work with project and application configuration files.

Usage:
    from gae.config import get_config
    config = get_config()
    admins = config.get("user.admins", default_value=[])
    # short form
    admins = get_config("user.admins", default_value=[])
    language = get_config("site.language", "en")
'''
import os, yaml, copy
from gae.tools import installed_apps, development_env
__all__ = ["get_config"]


class Config:
    _apps_configs = {}

    def __init__(self):
        # get list of configuration files
        apps_configs = [(app_name, os.path.abspath(os.path.join('apps', app_name, "config.yaml"))) for app_name in installed_apps()]
        # load configuration files
        for app_name, app_config in apps_configs:
            self._apps_configs[app_name] = self._load_config(app_config)

    def _load_config(self, config_file):
        fd = open(config_file)
        config = yaml.load(fd)
        fd.close()
        return config

    def get(self, path, default_value=None):
        '''Return configuration by given options path.
            1. look in file "apps/site/config.yaml" in section "apps"
            2. else, look in file "apps/[app_name]/config.yaml"
            3. else, return default_value 

        Usage:
            settings.get("user.admins")
            settings.get("site.language", "en")
        '''
        try:
            app_name, app_path = path.split('.', 1)
        except:
            raise Exception("To get config you need call get_config('%s.option_name') "
                            "instead of get_config('%s')" % (path, path))
        # search in site application
        config = self._apps_configs.get("site", {}).get("apps", {})
        for piece in path.split('.'):
            config = config.get(piece)
            if config is None: break
        # search in specified application
        if config is None:
            config = self._apps_configs.get(app_name, {})
            for piece in app_path.split('.'):
                config = config.get(piece)
                if config is None: break
        return copy.deepcopy(config) if config is not None else default_value


_config = None
def get_config(path=None, default_value=None):
    # create one copy of configuration
    global _config
    # doesn't cache config in development environment
    if _config is None or development_env():
        _config = Config()
    # load given configuration options
    if path is not None:
        return _config.get(path, default_value)
    return _config
