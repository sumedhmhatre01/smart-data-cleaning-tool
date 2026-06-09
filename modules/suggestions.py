import numpy as np
from pandas.api.types import is_numeric_dtype


def generate_suggestions(
    df,
    duplicate_count,
    outlier_df
):

    suggestions = []

    for column in df.columns:

        missing_count = (
            df[column]
            .isnull()
            .sum()
        )

        if missing_count > 0:

            if is_numeric_dtype(df[column]):

                suggestions.append(
                    f"Column '{column}' contains {missing_count} missing values. Fill using median."
                )

            else:

                suggestions.append(
                    f"Column '{column}' contains {missing_count} missing values. Fill using mode."
                )

    if duplicate_count > 0:

        suggestions.append(
            f"{duplicate_count} duplicate rows detected. Remove duplicate rows."
        )

    if not outlier_df.empty:

        for _, row in outlier_df.iterrows():

            if row["Outlier Count"] > 0:

                suggestions.append(
                    f"Column '{row['Column']}' contains {row['Outlier Count']} outliers. Review extreme values."
                )

    if len(suggestions) == 0:

        suggestions.append(
            "Dataset looks clean. No major issues detected."
        )

    return suggestions