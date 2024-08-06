import pandas as pd

def transform_normalize_dict(df: pd.DataFrame, meta: str, record: str) -> pd.DataFrame:
    dfs = []
    df = df[df[record].notna()].copy()
    for i, row in df.iterrows():
        meta_value = row[meta]
        record_value = row[record]

        try:
            df = pd.DataFrame(record_value)

        except:
            df = pd.DataFrame([record_value])

        df.dropna(how="all", inplace=True)
        if df.shape[0] > 0:
            df.insert(0, meta, meta_value)
            dfs.append(df)

    df_conso = pd.concat(dfs, ignore_index=True)
    df_conso = df_conso.drop_duplicates().copy()
    return df_conso