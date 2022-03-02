
# Flask Validity
The robust validation library for flask

## Installations
```sh
pip install flask-validity
```

## Usage
```py
from flask import Flask
from validity.Validation import Validation 

app = Flask(__name__)
validation = Validation()

@app.route('/')
@validation .validate(
[
 {
 "field": "title",
 "required": True,
 "type": "str",
 "min": 10,
 "max": 30,
 "regex": None
 }
]
)
def index():
    return 'Web App with Python Flask!'

app.run(host='0.0.0.0', port=81)
```

This class used to validate any incoming json request to your flask route, it validate the request after validation passes then the request enters your route function.

It amins to allow you to write once and used a lot instead of validation request on every route it is better to do it once at top of your function.

It support number of parameter are as follow:

1.  `field`  This is required parameter which indicate the field name you want to accpet.
2.  `required`  This is not required parameter but if this not present any of below validation will not considered, its value either  `True`  or  `False`
3.  `type`  Which type of request value should be it support  `int`,  `float`,  `list`,  `bool`,  `dict`  and  `str`
4.  `min`  and  `max`  These are optional parameter but if one of them present other is required its used to indicate restriction to min and max length or value.
5.  `regex`  It is optional parameter but It is used to validate request base on regex.
6.  `email`  It is optional parameter it validate email.
7.  `phone`  It is optional parameter it validate phone.
8. `file` If validat file set this to true.
	1. `size` File size in bytes.
	2. `ext` File extension it accpet python list.
	3. `mime` File mime types, it accpet python list.


#### Returning Value
Validity support three method for returning the errors
1. As json
	- Return as json array.
2. As String
	- Return as string.
3. As query string
	- Return redirect with query parameters.
4. None
	- None mean it will do nothing but you can get the error with `validator.Errors`

You can pass these flags to `validate` as second argument.

```python

@app.route('/process', methods=['POST', 'GET'])
@validator.validate(
[{
"field": "name",
"required": True,
"type": "str",
}],
None
)
def  process():
	 errors = validator.Errors
	 # rest of code..
```

#### Languages
Currently it support two languages out of the box that includes:
1. English
2. Urdu

You can set the language as below:
```python
# ... 
validator  =  Validator("en")
# ...
```
You can add your langauge by sending `PR` and/or you can pass validator constructor language string as below, assume it will be your own language:
```python
# ...
validator  =  Validator("en", {
"required": "The %s is required.",
"extension": "The %s extension is not allowed.",
"mime": "The %s mimetype is not allowed.",
"size": "The %s size is too large.",
"empty": "The %s must not be empty.",
"type": "The %s must be %s .",
"between": "The %s must be between %s and %s .",
"regx": "The %s must be in correct format.",
"phone": "The phone number should be valid.",
"email": "The email should be valid.",
"error": "Unable to decode the data."
})
# ...
```
## Contributing

Thank you for considering contributing to the validity! Feel free to create a pull request.

### [](https://github.com/alphasofthub/cLISIRT#contrubuting-guide)Contrubuting guide

[https://zestframework.github.io/contribution/](https://zestframework.github.io/contribution/)

## License
- GNU GPL3

## Security Vulnerabilities

If you discover a security vulnerability within Validity, please send an e-mail to our team via  [security@alphasofthub.com](mailto:security@alphasofthub.com). All security vulnerabilities will be promptly addressed.
