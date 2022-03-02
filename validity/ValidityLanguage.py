#  Copyright (c) AlphaSoftHub Pvt Ltd.
"ValidityLanguage.py: wrapper class for languages."
__author__ = "Muhammad Umer Farooq"
__license__ = "GNU GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "umer@alphasofthub.com"
__status__ = "Production"

class ValidityLanguage:

    def __init__(self, file, data = {}):
        """
            Init
            :param file: str
            :since 1.0.0
        """
        self.items = {}
        if data != {}:
            self.items = data
        else:
            from pathlib import Path
            self.file = str(Path(__file__).parent.absolute()) + "/locale/" + file + ".json"

    def load(self):
        """
            Load config from language file and save it to py dict.
            :since 1.0.0
            :return: pbkect
            :raises: None
            :example: c.load
        """
        import json, os
        if os.path.isfile(self.file):
            data = open(self.file, 'r', encoding="utf8")
            self.items = json.load(data)
            data.close()
        else:
            raise FileNotFoundError("Unable to load language file")
        return self

    def get(self, key, default=None) -> str:
        """
            Get string from language
            :param key: str
            :param default: str|None
            :since 1.0.0
            :return: str
            :raises: None
            :example: c.get("key")
        """
        if key in self.items:
            return self.items[key]
        else:
            return default
