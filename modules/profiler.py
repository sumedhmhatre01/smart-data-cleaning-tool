import pandas as pd


def get_dataset_info(df):

    total_rows = df.shape[0]
    total_columns = df.shape[1]

    missing_values = df.isnull().sum().sum()

    memory_usage = round(
        df.memory_usage(deep=True).sum() / 1024,
        2
    )

    return {
        "rows": total_rows,
        "columns": total_columns,
        "missing": missing_values,
        "memory": memory_usage
    }


def get_column_info(df):

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Non-Null Count": df.notnull().sum().values
    })

    return info_df


def get_statistics(df):

    return df.describe(include="all")