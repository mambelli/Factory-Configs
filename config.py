#!/usr/bin/env python

import yaml

stream = open('configuration.yaml', 'r')
configuration = yaml.safe_load(stream)


class ConfigElement:
    def __init__(self, config):
        self.config = config
        self.key_set = set(config.keys())

    def verify(self):
        raise ConfigError("Something is wrong in the configuration")


class ConfigList(ConfigElement):
    pass


class ConfigDict(ConfigList):
    mandatory_keys = {}
    optional_keys = {}

    def verify(self):
        pass


class ConfigAll(ConfigDict):
    mandatory_keys = {'entries', 'log_retention', 'monitor', 'monitor_footer',
                      'security', 'stage', 'submit', 'glidein', 'condor_tarballs'}
    optional_keys = {'files', 'attributes'}

    def verify(self):
        if self.mandatory_keys | self.optional_keys == self.key_set:
            print('All keys included')
        else:
            raise ConfigError('The configuration is missing a key')
        if not self.mandatory_keys.issubset(self.key_set):
            raise ConfigError('Missing mandatory key(s)')


class Error(Exception):
    pass


class ConfigError(Error):
    pass


myconf = ConfigElement(configuration)
myall = ConfigAll(configuration)

myall.verify()

