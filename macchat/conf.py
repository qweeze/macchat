import os
from configobj import ConfigObj

CONF_FILE = '.macchatrc'

config = ConfigObj(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), CONF_FILE))
config.update(ConfigObj(os.path.expanduser(CONF_FILE)))
