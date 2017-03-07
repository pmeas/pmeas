import json, os


def read_config_file():
    """
    Reads the configuration file stored in config/
    Returns string being read.
    """
    effects_file = os.path.join( os.path.dirname(os.path.abspath(__file__)), "config/effects.json")

    config_file = open(effects_file)
    config_data = config_file.read()
    config_file.close()
    return config_data


def parse_config_file(config_data):
    """
    Parse the data from the file into respective
    objects.
    Currently prints the objects to the screen for testing.
    """
    config_data = json.loads(config_data)
    return config_data


def get_effects():
    """
    High level function that parses the configuration content
    and returns the result as a dictionary of effects.
    """
    file_contents = read_config_file()
    return parse_config_file(file_contents)
