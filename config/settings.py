import tomllib

with open("config/config.toml", "rb") as file:
    config = tomllib.load(file)

EXTRACTORS = config["extractors"]
TRANSFORMERS = config["transformers"]
LOADERS = config["loaders"]