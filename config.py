#!/usr/bin/env python
import yaml


# Error classes
class Error(Exception):
    pass


class ConfigError(Error):
    def __init__(self, message):
        super(ConfigError, self).__init__("Configutation error: %s" % message)


# Config elements
class ConfigElement:
    def __init__(self, config):
        self.config = config

    def verify(self):
        raise ConfigError("Undefined verify method")


class ConfigList(ConfigElement):
    """List of ConfigElements
    """
    def verify(self):
        for i in self.config:
            i.verify()


class ConfigDict(ConfigList):
    """Dictionary of ConfigElements
    """
    mandatory_keys = frozenset()
    optional_keys = frozenset()

    def __init__(self, config):
        super(ConfigDict, self).__init__(config)
        self.key_set = frozenset(config)

    def verify(self):
        # verify that all mandatory keys are there
        if self.mandatory_keys <= self.key_set:
            raise ConfigError("mandatory key/s %s not in dictionary %s" %
                              (self.mandatory_keys-self.key_set, self.config))
        # verify that there is no unknown key (unless fre-form is OK)
        # TODO:  add verify that there is no unknown key
        # verify all items
        for i in self.config:
            self.config[i].verify()


class ConfigAll(ConfigDict):
    mandatory_keys = frozenset(('entries', 'log_retention', 'monitor', 'monitor_footer',
                                'security', 'stage', 'submit', 'glidein', 'condor_tarballs'))
    optional_keys = frozenset(('files', 'attributes'))

    def verify(self):
        if self.mandatory_keys | self.optional_keys == self.key_set:
            print('All keys included')
        else:
            raise ConfigError('The configuration is missing a key')
        if not self.mandatory_keys.issubset(self.key_set):
            raise ConfigError('Missing mandatory key(s)')


# Execute only if not imported
if __name__ == "__main__":
    stream = open('configuration.yaml', 'r')
    configuration = yaml.safe_load(stream)

    myconf = ConfigElement(configuration)
    myall = ConfigAll(configuration)

    myall.verify()

