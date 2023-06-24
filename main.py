import configparser
config = configparser.ConfigParser()
config.read("env.conf")

value_a = config.get("test", "a")