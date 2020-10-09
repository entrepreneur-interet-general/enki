def filter_dict_with_keys(d: dict, other: dict):
    print("d")
    print(d)
    print("other")
    print(other)
    result = {k: v for k, v in d.items() if k in other}
    print("result")
    print(result)
    return result

