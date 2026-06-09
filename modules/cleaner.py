import pandas as pd
import numpy as np


def get_missing_values(df):

    missing_count = df.isnull().sum()

    missing_percent = (
        df.isnull().sum() / len(df) * 100
    ).round(2)

    missing_df = pd.DataFrame({
        "Column": missing_count.index,
        "Missing Values": missing_count.values,
        "Missing %": missing_percent.values
    })

    missing_df = missing_df[
        missing_df["Missing Values"] > 0
    ]

    return missing_df


def get_duplicate_rows(df):

    duplicate_df = df[df.duplicated()]

    duplicate_count = duplicate_df.shape[0]

    return duplicate_count, duplicate_df


def get_quality_score(df):

    total_cells = df.shape[0] * df.shape[1]

    missing_cells = df.isnull().sum().sum()

    duplicate_rows = df.duplicated().sum()

    penalty = (
        missing_cells +
        duplicate_rows
    )

    score = (
        (total_cells - penalty)
        / total_cells
    ) * 100

    return round(score, 2)


def auto_clean_dataset(df):

    cleaned_df = df.copy()

    rows_before = len(cleaned_df)

    missing_before = (
        cleaned_df.isnull()
        .sum()
        .sum()
    )

    duplicates_before = (
        cleaned_df.duplicated()
        .sum()
    )

    cleaned_df = (
        cleaned_df.drop_duplicates()
    )

    numeric_columns = (
        cleaned_df
        .select_dtypes(
            include=np.number
        )
        .columns
    )

    for column in numeric_columns:

        median_value = (
            cleaned_df[column]
            .median()
        )

        cleaned_df[column] = (
            cleaned_df[column]
            .fillna(median_value)
        )

    categorical_columns = (
        cleaned_df
        .select_dtypes(
            exclude=np.number
        )
        .columns
    )

    for column in categorical_columns:

        mode_value = (
            cleaned_df[column]
            .mode()[0]
        )

        cleaned_df[column] = (
            cleaned_df[column]
            .fillna(mode_value)
        )

    rows_after = len(cleaned_df)

    missing_after = (
        cleaned_df.isnull()
        .sum()
        .sum()
    )

    summary = {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "duplicates_removed":
            duplicates_before,
        "missing_fixed":
            missing_before - missing_after
    }

    return cleaned_df, summary