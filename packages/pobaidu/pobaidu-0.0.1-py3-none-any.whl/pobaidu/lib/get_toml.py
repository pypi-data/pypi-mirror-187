import toml
import logging


def get_toml(toml_path=r'./baidu-config.toml'):
    config_info = toml.load(toml_path)
    logging.info(msg='loading config ok')
    return config_info
