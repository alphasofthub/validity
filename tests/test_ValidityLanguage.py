from validity.ValidityLanguage import ValidityLanguage

def test_lang():
    lang = ValidityLanguage("en").load()
    assert lang.get("required") == "The %s is required."
