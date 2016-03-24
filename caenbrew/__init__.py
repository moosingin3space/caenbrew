import os.path

CONFIG_FILENAME = os.path.expanduser("~/.caenbrewrc")
"""The file in which one's Caenbrew configuration is stored.

Caenbrew configuration is a set of key-value pairs separated by an equals sign.
It looks like this:

    prefix_dir = ~/.my-custom-local
    verbose = 1

"""

_default_config = {
    "prefix_dir": os.path.expanduser("~/.local"),
    "verbose": False,
}
"""The default values for each of the config options."""

_types = {
    "prefix_dir": os.path.expanduser,
    "verbose": lambda x: bool(int(x)),
}
"""The type of each value.

The mapped function is called on the string on the right-hand side of the
equals sign.
"""


def get_config():
    """Read the user's configuration from their config file.

    :returns dict: The configuration dict.
    """
    config = _default_config.copy()
    if not os.path.isfile(CONFIG_FILENAME):
        return config

    with open(CONFIG_FILENAME) as f:
        lines = f.read().splitlines()

    for line in lines:
        try:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
        except ValueError:
            raise ValueError(
                "Expected line in form 'foo = bar', "
                "got: {}".format(line)
            )

        if key not in config:
            raise ValueError("Invalid key: {}".format(key))
        config[key] = _types[key](value)
    return config
