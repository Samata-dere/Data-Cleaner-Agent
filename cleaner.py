import pandas as pd


def read_data(file):
    if file.name.lower().endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)


def remove_null(df):
    return df.dropna().copy()


def remove_duplicate(df):
    return df.drop_duplicates().copy()


def calculate_quality_score(df):
    if df.empty or len(df.columns) == 0:
        return 0

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0

    missing_cells = df.isnull().sum().sum()
    score = ((total_cells - missing_cells) / total_cells) * 100

    return round(score, 2)
