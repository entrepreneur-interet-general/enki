from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Union


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
            example 2070-11-02T16:05:29+00:00

    """

    value: datetime
    pattern = "\\d\\d\\d\\d-\\d\\d-\\d\\dT\\d\\d:\\d\\d:\\d\\d[\\-+]\\d\\d:\\d\\d"

    def __init__(self, value: Union[str, datetime]):
        if isinstance(value, str):
            self.value = datetime.strptime(remove_extra_last_char_(value), '%Y-%m-%dT%H:%M:%S%z')
        else:
            self.value = value

    def __repr__(self):
        string_value = self.value.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z')
        return string_value[0:-2] + ":" + string_value[-2:]
