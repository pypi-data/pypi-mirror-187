from collections.abc import MutableMapping
import logging
import ruamel.yaml as yaml
from pathlib import Path

logger = logging.getLogger(__name__)
path = f"{Path.home()}/.gisterconfig"


def get_parsed_context():
    logger.debug("start reading file")

    # TODO: validate posible args
    # if not args:
    #     raise AssertionError(
    #         "Function must be invoked with context args set."
    #     )
    logger.debug("%d", )
    logger.debug("attempting to open file: %s", path)
    with open(path) as yaml_file:
        yaml_loader = yaml.YAML(typ='safe', pure=True)
        payload = yaml_loader.load(yaml_file)

        if not isinstance(payload, MutableMapping):
            raise TypeError("yaml file must be a dictionary at the top. Like key: value")

        logger.info("parsed. D: %d Done.", len(payload))
        return payload


def write_parsed_context(env):
    logger.debug("%d", )
    logger.debug("attempting to open file: %s", path)
    with open(path) as yaml_file:
        yaml_loader = yaml.YAML()
        payload = yaml_loader.load(yaml_file)

        payload["gitenv"]["active"] = env
        with open(path, "w") as fw:
            yaml_loader.dump(payload, fw)


class ConfigReader:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__configpath = f"{Path.home()}/.gisterconfig"

    def read_yml_configs(self):
        path = self.__configpath
        logger.debug("%d", )
        logger.debug("attempting to open file: %s", path)
        with open(path) as yaml_file:
            yaml_loader = yaml.YAML()
            payload = yaml_loader.load(yaml_file)
            yaml_file.close()
        return payload

    def __writenewymlproperties__(self, payload):
        logger.debug("%d", )
        logger.debug("attempting to open file: %s", self.__configpath)
        with open(self.__configpath, "w") as fw:
            yaml_loader = yaml.YAML()
            yaml_loader.dump(payload, fw)
            fw.close()

    def read_json_configs(self):
        logger.debug("start reading file")

        # TODO: validate posible args
        # if not args:
        #     raise AssertionError(
        #         "Function must be invoked with context args set."
        #     )
        path_file = self.__configpath
        logger.debug("%d", )
        logger.debug("attempting to open file: %s", path_file)
        with open(path_file) as yaml_file:
            yaml_loader = yaml.YAML(typ='safe', pure=True)
            payload = yaml_loader.load(yaml_file)

            if not isinstance(payload, MutableMapping):
                raise TypeError("yaml file must be a dictionary at the top. Like key: value")

            logger.info("parsed. D: %d Done.", len(payload))
            return payload

    def write_new_yml_properties(self, payload):
        self.__writenewymlproperties__(payload)
