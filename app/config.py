import configparser

# Load sensitive values from mfihlelo.txt
config = configparser.ConfigParser()
"""
The `configparser.ConfigParser` class is used to read configuration files.
- It provides methods to parse and retrieve values from configuration files.
- In this case, it is used to load sensitive values from the `mfihlelo.txt` file.
"""

config.read('/home/ingamaholwana/Documents/blogfastapi/mfihlelo.txt')
"""
The `config.read()` method reads the specified configuration file.
- `/home/ingamaholwana/Documents/blogfastapi/mfihlelo.txt`: The path to the configuration file containing sensitive values.
- This file is expected to have key-value pairs under a `[DEFAULT]` section.
"""

SECRET_KEY = config.get('DEFAULT', 'SECRET_KEY')
"""
Retrieves the `SECRET_KEY` value from the `[DEFAULT]` section of the configuration file.
- `SECRET_KEY`: A string used for signing and verifying JWT tokens.
"""

ALGORITHM = config.get('DEFAULT', 'ALGORITHM')
"""
Retrieves the `ALGORITHM` value from the `[DEFAULT]` section of the configuration file.
- `ALGORITHM`: The hashing algorithm used for signing JWT tokens .
"""

ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get('DEFAULT', 'ACCESS_TOKEN_EXPIRE_MINUTES'))
"""
Retrieves the `ACCESS_TOKEN_EXPIRE_MINUTES` value from the `[DEFAULT]` section of the configuration file.
- Converts the value to an integer.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: The duration (in minutes) for which a JWT token remains valid.
"""