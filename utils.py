
import pandas as pd

def superitems(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            for i in superitems(v):
                yield (k,) + i
    else:
        yield (obj,)


def nested_dict_to_md(data,columns):
    '''
    Converts Nested dict to markdown table
    Data: nested dict
    columns: column name that you want (Order should be the same as nested dict parent keys to child keys)
    '''
    df = pd.DataFrame([*superitems(data)],columns=columns)
    return df.to_markdown()