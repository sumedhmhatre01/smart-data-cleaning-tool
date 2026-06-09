import streamlit as st

from modules.data_loader import load_csv

from modules.profiler import (
    get_dataset_info,
    get_column_info,
    get_statistics
)

from modules.cleaner import (
    get_missing_values,
    get_duplicate_rows,
    get_quality_score,
    auto_clean_dataset
)

from modules.outlier_detector import (
    detect_outliers,
    get_outlier_rows
)

from modules.suggestions import (
    generate_suggestions
)

st.set_page_config(
    page_title="Smart Data Cleaning Tool",
    page_icon="🧹",
    layout="wide"
)

st.markdown("""
<style>

.main-title{
    font-size:45px;
    font-weight:700;
    color:#2563EB;
}

.sub-title{
    font-size:18px;
    color:#475569;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="main-title">🧹 Smart Data Cleaning Tool</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Clean, Analyze & Improve Your Dataset</p>',
    unsafe_allow_html=True
)

st.divider()

st.subheader("📁 Upload CSV File")

uploaded_file = st.file_uploader(
    "Choose a CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df, error = load_csv(uploaded_file)

    if error:

        st.error(error)

    else:

        st.success("CSV uploaded successfully")

        # ==================================
        # DATASET OVERVIEW
        # ==================================

        st.subheader("📊 Dataset Overview")

        metrics = get_dataset_info(df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Rows",
                metrics["rows"]
            )

        with col2:
            st.metric(
                "Columns",
                metrics["columns"]
            )

        with col3:
            st.metric(
                "Missing Values",
                metrics["missing"]
            )

        with col4:
            st.metric(
                "Memory (KB)",
                metrics["memory"]
            )

        st.divider()

        # ==================================
        # DATASET PREVIEW
        # ==================================

        st.subheader("📋 Dataset Preview")

        st.dataframe(
            df.head(),
            use_container_width=True
        )

        st.divider()

        # ==================================
        # COLUMN INFORMATION
        # ==================================

        st.subheader("🧾 Column Information")

        info_df = get_column_info(df)

        st.dataframe(
            info_df,
            use_container_width=True
        )

        st.divider()

        # ==================================
        # DATASET STATISTICS
        # ==================================

        st.subheader("📈 Dataset Statistics")

        stats_df = get_statistics(df)

        st.dataframe(
            stats_df,
            use_container_width=True
        )

        st.divider()

        # ==================================
        # MISSING VALUES ANALYSIS
        # ==================================

        st.subheader(
            "⚠️ Missing Values Analysis"
        )

        missing_df = get_missing_values(df)

        if missing_df.empty:

            st.success(
                "No missing values found."
            )

        else:

            st.dataframe(
                missing_df,
                use_container_width=True
            )

        st.divider()

        # ==================================
        # DUPLICATE DETECTION
        # ==================================

        st.subheader(
            "🔄 Duplicate Detection"
        )

        duplicate_count, duplicate_df = (
            get_duplicate_rows(df)
        )

        st.metric(
            "Duplicate Rows",
            duplicate_count
        )

        if duplicate_count > 0:

            st.dataframe(
                duplicate_df,
                use_container_width=True
            )

        else:

            st.success(
                "No duplicate rows found."
            )

        st.divider()

        # ==================================
        # DATA QUALITY SUMMARY
        # ==================================

        st.subheader(
            "🏆 Data Quality Summary"
        )

        quality_score = get_quality_score(df)

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Missing Values",
                int(df.isnull().sum().sum())
            )

        with col2:

            st.metric(
                "Duplicate Rows",
                int(df.duplicated().sum())
            )

        with col3:

            st.metric(
                "Quality Score (%)",
                quality_score
            )

        if quality_score >= 90:

            st.success(
                "Excellent Data Quality"
            )

        elif quality_score >= 75:

            st.warning(
                "Good Data Quality - Cleaning Recommended"
            )

        else:

            st.error(
                "Poor Data Quality - Cleaning Required"
            )

        st.divider()

        # ==================================
        # OUTLIER DETECTION
        # ==================================

        st.subheader(
            "🚨 Outlier Detection"
        )

        outlier_df = detect_outliers(df)

        if outlier_df.empty:

            st.success(
                "No numeric columns found."
            )

        else:

            st.dataframe(
                outlier_df,
                use_container_width=True
            )

        st.divider()

        # ==================================
        # OUTLIER RECORDS
        # ==================================

        st.subheader(
            "📌 Outlier Records"
        )

        outlier_rows = get_outlier_rows(df)

        if len(outlier_rows) > 0:

            st.dataframe(
                outlier_rows,
                use_container_width=True
            )

        else:

            st.success(
                "No outlier records found."
            )

        st.divider()

        # ==================================
        # SMART CLEANING SUGGESTIONS
        # ==================================

        st.subheader(
            "💡 Smart Cleaning Suggestions"
        )

        suggestions = generate_suggestions(
            df,
            duplicate_count,
            outlier_df
        )

        for suggestion in suggestions:

            st.info(
                suggestion
            )

        st.divider()

       # ==================================
# AUTO CLEAN DATASET
# ==================================

st.subheader(
    "🧹 Auto Clean Dataset"
)

if st.button(
    "🚀 Auto Clean Data"
):

    cleaned_df, summary = (
        auto_clean_dataset(df)
    )

    st.success(
        "Dataset cleaned successfully."
    )

    st.subheader(
        "📋 Cleaning Summary"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "Rows Before",
            summary["rows_before"]
        )

    with col2:

        st.metric(
            "Rows After",
            summary["rows_after"]
        )

    with col3:

        st.metric(
            "Duplicates Removed",
            summary["duplicates_removed"]
        )

    with col4:

        st.metric(
            "Missing Fixed",
            summary["missing_fixed"]
        )

    st.subheader(
        "📊 Cleaned Dataset Preview"
    )

    st.dataframe(
        cleaned_df,
        use_container_width=True
    )

    st.session_state[
        "cleaned_df"
    ] = cleaned_df

    csv_data = cleaned_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )