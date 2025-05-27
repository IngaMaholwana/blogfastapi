import configparser

# Load sensitive values from mfihlelo.txt
config = configparser.ConfigParser()
config.read('/home/ingamaholwana/Documents/blogfastapi/mfihlelo.txt')

SECRET_KEY = config.get('DEFAULT', 'SECRET_KEY')
ALGORITHM = config.get('DEFAULT', 'ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get('DEFAULT', 'ACCESS_TOKEN_EXPIRE_MINUTES'))