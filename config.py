import configparser

config = configparser.ConfigParser()
config.read('envfile.ini', 'utf8')

project_dir = config['DEFAULT']['PROJECTDIR']
