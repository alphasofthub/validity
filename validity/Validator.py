#  Copyright (c) AlphaSoftHub Pvt Ltd.
"self.py: self wrapper class for flask."
__author__ = "Muhammad Umer Farooq"
__license__ = "GNU GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "umer@alphasofthub.com"
__status__ = "Production"

from functools import wraps

import sys, os

# Check if flask is not installed.
if "flask" not in sys.modules:
    raise ImportError("Flask is not installed.")

from flask import request, jsonify, redirect
from .ValidityLanguage import ValidityLanguage

class Validator:

    def __init__(self, lang: str = "en", langs = {}) -> None:
        """
            Constructor
            :param lang: The shortcode of language i.e en, ur, br
            :param langs: The raw language string in python dictionary.
            :since 1.0.0
            return object
            :raise None
        """
        
        self.Errors = {}
        if langs != {}:
            self.L = ValidityLanguage(lang, langs)
        else:
            self.L = ValidityLanguage(lang).load()
        
    def validate(self, arg, returns="json"):
        """
            validate the flask request.
            :param arg: list of dictionaries
            :param returns: str|None
            :since 1.0.0
            :return: object
            :raises: None
            :example: validator.validate([
                {
                    "field": "name",
                    "required": True,
                    "type": "str",
                },
            )
        """
        def validate_internal(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                import json

                try:
                    data = request.data
                    files = request.files
                    # Check if request.data is empty or none.
                    if request.data is None or request.data == b'':
                        if request.form is None or request.form == b'' or request.form == {}:
                            # get, GET params.
                            data = request.args
                        else:
                            # get the data from forms.
                            data = request.form

                    # determine if data is not json.
                    try:
                        json.loads(data)
                    except:
                        data = json.dumps(data)

                    data = json.loads(data)

                except:
                    return jsonify({"error": self.L.get("error")}), 400
                errors = {}

                # get the params
                params = arg

                for items in params:
                    _ty = items.get("type")  # type of the param
                    # python type for checking.
                    _t = int if _ty == "int" else float if _ty == "float" else bool if _ty == "bool" else list if _ty == "list" else dict if _ty == "dict" else str

                    item = items['field']
                    errors[item] = []

                    if "file" in items and items['file'] == True:
                        # check file size
                        file = files.get(item, None)
                        if "required" in items and items['required'] == True:
                            if file is None:
                                errors[item].append(self.L.get('required') % (item,))
                            else:
                                # validate file extension.
                                ext = file.filename.split(".")[-1]
                                if "ext" in items and ext not in items['ext']:
                                    errors[item].append(self.L.get('extension') % (item,))

                                # validate file mimetype.
                                mime = file.mimetype
                                if "mime" in items and mime not in items['mime']:
                                    errors[item].append(self.L.get('mime') % (item,))

                                # validate file size
                                file.seek(0, os.SEEK_END)
                                size = file.tell()
                                file.seek(0, 0)  # reset the file pointer.
                                if "size" in items and size > items['size']:
                                    errors[item].append(self.L.get('size') % (item,))

                    else:
                        # If input is requierd.
                        if "required" in items and items['required'] == True:
                            # Input is missing.
                            if item not in data:
                                errors[item].append(self.L.get('required') % (item,))
                            else:
                                # It should not be empty.
                                if data[item] is None or data[item] == "":
                                    errors[item].append(self.L.get('empty') % (item,))

                                # If input is not of the type.
                                elif _t is not type(data[item]):
                                    errors[item].append(self.L.get('empty') % (item, str(items['type']),))
                                else:
                                    # Validate the min and max base on type.
                                    if "min" in items and "max" in items:
                                        if type(data[item]) is list:
                                            if len(data[item]) < items['min'] or len(data[item]) > items['max']:
                                                errors[item].append(self.L.get('between') % (item, str(items['min']), str(items['max'])))
                                        elif type(data[item]) is dict:
                                            if len(data[item]) < items['min'] or len(data[item]) > items['max']:
                                                errors[item].append(self.L.get('between') % (item, str(items['min']), str(items['max'])))
                                        elif type(data[item]) is str:
                                            if len(data[item]) < items['min'] or len(data[item]) > items['max']:
                                                errors[item].append(self.L.get('between') % (item, str(items['min']), str(items['max'])))
                                        elif type(data[item]) is int or type(data[item]) is float:
                                            if data[item] < items['min'] or data[item] > items['max']:
                                                errors[item].append(self.L.get('between') % (item, str(items['min']), str(items['max'])))

                                    # Validate the regex.
                                    if "regex" in items and items['regex'] is not None:
                                        import re
                                        if not re.match(items['regex'], data[item]):
                                            errors[item].append(self.L.get("regx") % (item, ))

                                    # Validate the email.
                                    if "email" in items and items['email'] is True:
                                        import re
                                        if not re.match(r"[^@]+@[^@]+\.[^@]+", data[item]):
                                            errors[item].append(self.L.get("email"))

                                    # Validate the phone number.
                                    if "phone" in items and items['phone'] is True:
                                        import re
                                        if not re.match(r"^[0-9]{10}$", data[item]):
                                            errors[item].append(self.L.get("phone"))

                # get errors dict keys.
                keys = errors.keys()
                error = False
                for key in keys:
                    if errors[key] != []:
                        error = True
                        break

                if error == True:
                    self.Errors = errors

                    if returns == "json":
                        return jsonify({"errors": errors}), 400
                    elif returns == "str":
                        return str(errors)
                    elif returns == "redirect":
                        # build the error message.
                        url = str(request.referrer) + "?" + "&".join(
                            ["{}={}".format(key, value) for key, value in errors.items()])
                        # redirect
                        return redirect(url)

                return f(*args, **kwargs)
            return decorated_function
        return validate_internal
