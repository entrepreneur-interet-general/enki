from datetime import datetime
from dataclasses import dataclass


def remove_extra_last_char_(original_string, char=":", replace_char=""):
    last_char_index = original_string.rfind(char)
    return original_string[:last_char_index] + replace_char + original_string[last_char_index+1:]

@dataclass
class DateType(object):
    """
        L'indicateur de fuseau horaire Z ne doit pas être utilisé. Le fuseau horaire pour UTC doit être représenté par '-00:00'.

        ...

        Attributes
        ----------
        value : str
            a datetime object "\\d\\d\\d\\d-\\d\\d-\\d\\dT\\d\\d:\\d\\d:\\d\\d[\\-+]\\d\\d:\\d\\d"

    """

    value: datetime
    pattern = "\\d\\d\\d\\d-\\d\\d-\\d\\dT\\d\\d:\\d\\d:\\d\\d[\\-+]\\d\\d:\\d\\d"

    def __init__(self, value: str):
        self.value = datetime.strptime(remove_extra_last_char_(value), '%Y-%m-%dT%H:%M:%S%z')

    def validate(self):
        pass
