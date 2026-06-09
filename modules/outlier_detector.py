import numpy as np
import pandas as pd


def detect_outliers(df):

    results = []

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        data = df[column].dropna()

        if len(data) == 0:
            continue

        mean = np.mean(data)

        std = np.std(data)

        if std == 0:
            continue

        z_scores = (
            (data - mean) / std
        )

        outlier_mask = (
            np.abs(z_scores) > 3
        )

        outlier_count = int(
            outlier_mask.sum()
        )

        results.append({
            "Column": column,
            "Outlier Count": outlier_count
        })

    return pd.DataFrame(results)


def get_outlier_rows(df):

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    outlier_indices = set()

    for column in numeric_columns:

        data = df[column].dropna()

        if len(data) == 0:
            continue

        mean = np.mean(data)

        std = np.std(data)

        if std == 0:
            continue

        z_scores = (
            (data - mean) / std
        )

        outlier_mask = (
            np.abs(z_scores) > 3
        )

        indices = data[
            outlier_mask
        ].index

        outlier_indices.update(
            indices
        )

    return df.loc[
        list(outlier_indices)
    ]