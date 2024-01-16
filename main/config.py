import os.path
from importlib import import_module

env = os.getenv("ENVIRONMENT", "local")
config_file = f"config/{env}.py"
if not os.path.isfile(config_file):
    env = "local"

config_name = f"config.{env}"

module = import_module(config_name)

config = module.Config
config.ENV = env
