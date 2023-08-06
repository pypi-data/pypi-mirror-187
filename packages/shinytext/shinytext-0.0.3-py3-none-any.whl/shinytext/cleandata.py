import pandas as pd


def filter_english_records(df: pd.DataFrame, col: str, num: bool=False):
    """
    Returns the records with english text only. Can include numbers
    as well (optional).

    Arguments:
        df -- Dataframe
        col -- Column name

    Keyword Arguments:
        num -- Whether to include numbers (default: {False})

    Returns:
        Dataframe with only english texts and numbers (optional).
    """
    if num:
        df = df[df[col].apply(lambda x: re.search(r'[a-zA-Z0-9\.]', x)).notna()]
    else:
        df = df[df[col].apply(lambda x: re.search(r'[a-zA-Z]', x)).notna()]
    df.reset_index(drop=True, inplace=True)
    return df
