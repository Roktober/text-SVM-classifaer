import configparser


def get_config_for_section(section=None):
    config = configparser.ConfigParser()
    config.read('config.ini')
    if section and section in config.sections():
        return config[section]
    return config
