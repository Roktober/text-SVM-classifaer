import pandas as pd


def get_data_from_csv(filename: str):
    """
    Requared ri and ri_doc in csv headers

    Returns:
        classes: set of unique classes
        classificated_data['ri']: list of util
        classificated_data['ri_doc']: list of util by doc
    """
    df = pd.read_csv(filename, dtype=str)
    df = df.dropna(how='all')
    classificated_data = df[(df['ri'].notnull()) & (df['ri_doc'].notnull())]
    classes = set(classificated_data['ri'])
    return (classes, classificated_data['ri'].values.tolist(
    ), classificated_data['ri_doc'].values.tolist())
