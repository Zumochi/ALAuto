from urllib import error, request
import json
from setuptools._vendor.packaging.version import parse
from util.logger import Logger

class UpdateUtil(object):

    def __init__(self, config):
        """Initializes the Enhancement module.

        Args:
            config (Config): ALAuto Config instance
            stats (Stats): ALAuto stats instance
        """
        self.config = config

    def checkUpdate(self):
        version = ''
        latest_version = ''
        _file = open('version.txt', 'r')

        if self.config.updates['channel'] == 'Release':  
            version = _file.readline()
            
            try:
                with request.urlopen("https://api.github.com/repos/egoistically/alauto/releases/latest") as f:
                    _json = json.loads(f.read().decode('utf-8'))
                    latest_version = _json["tag_name"]
            except error.HTTPError as e:
                Logger.log_error("Couldn't check for updates, {}.".format(e))

        else:
            version = _file.readlines()[1]
            
            try:
                with request.urlopen("https://raw.githubusercontent.com/Egoistically/ALAuto/master/version.txt") as f:
                    _f = f.read().decode('utf-8')
                    latest_version = _f.splitlines()[1]
            except error.HTTPError as e:
                Logger.log_error("Couldn't check for updates, {}.".format(e))
            
        _file.close()

        if parse(version) < parse(latest_version):
            Logger.log_debug("Current version: " + version)
            Logger.log_debug("Latest version: " + latest_version)

            return True