def filter_dict_with_keys(d: dict, other: dict):
    result = {k: v for k, v in d.items() if k in other}
    return result

