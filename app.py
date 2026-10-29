import streamlit as st
from cleaner import (
    read_data,
    remove_null,
    remove_duplicate,
    calculate_quality_score
)


st.set_page_config(
    page_title="Data Cleaner Agent",
    page_icon="🧹"
)
# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

    /* Main page */
    .main {
        background-color: #f7f9fc;
    }

    /* Main title */
    .main-title {
        text-align: center;
        color: #1f2937;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 18px;
        margin-bottom: 30px;
    }

    /* Upload section */
    .upload-box {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        border: 2px dashed #4f46e5;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Section headings */
    h2, h3 {
        color: #1f2937;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #4f46e5;
        color: white;
        font-weight: 600;
        padding: 10px;
        border: none;
    }

    .stButton > button:hover {
        background-color: #3730a3;
        color: white;
    }

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.title("🧹 Data Cleaner")

st.sidebar.markdown("---")

st.sidebar.subheader("✨ Available Features")

st.sidebar.markdown("""
✅ Upload CSV or Excel File

✅ Remove Missing Values

✅ Remove Duplicate Rows

✅ Preview Cleaned Data

✅ Download Cleaned CSV

✅ Data Quality Score
""")

st.sidebar.markdown("---")

st.sidebar.info("Upload your dataset and clean it easily.")

st.sidebar.markdown("---")

st.sidebar.subheader("🛠️ Cleaning Options")


clean_missing = st.sidebar.checkbox(
    "Remove Missing Values",
    value=True
)

clean_duplicates = st.sidebar.checkbox(
    "Remove Duplicate Rows",
    value=True
)

# ---------------- MAIN APP ----------------

st.markdown(
    '<div class="main-title">🧹 Data Cleaner Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    "### 📂 Upload Your Dataset"
)

uploaded_file = st.file_uploader(
    "📂 Upload CSV or Excel File",
    type=["csv", "xlsx", "xls"]
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

# IMPORTANT:
# Only process the file if the user has uploaded one.
if uploaded_file is not None:

    # Read uploaded file
    df = read_data(uploaded_file)
    # Calculate original quality score
    quality_score_before = calculate_quality_score(df)
    st.subheader("📋 Original Dataset")
    st.dataframe(df)

    # ---------------- DATASET INFORMATION ----------------

    st.subheader("📊 Dataset Information")

    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    st.write("Missing Values:")
    st.write(df.isnull().sum())

    # ---------------- CLEAN DATA ----------------

        # ---------------- CLEAN DATA ----------------

    if st.button("🧹 Clean Data"):

        original_rows = df.shape[0]

        missing_before = df.isnull().sum().sum()
        duplicate_before = df.duplicated().sum()

        # Calculate quality score before cleaning
        quality_score_before = calculate_quality_score(df)

        # Apply selected cleaning operations
        if clean_missing:
            df = remove_null(df)

        if clean_duplicates:
            df = remove_duplicate(df)

        cleaned_rows = df.shape[0]

        # Calculate quality score after cleaning
        quality_score_after = calculate_quality_score(df)

        # ---------------- DASHBOARD ----------------

        st.subheader("📈 Cleaning Dashboard")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.metric(
                "📄 Original Rows",
                original_rows
            )

        with col2:
            st.metric(
                "✨ Cleaned Rows",
                cleaned_rows
            )

        with col3:
            st.metric(
                "🗑️ Rows Removed",
                original_rows - cleaned_rows
            )

        with col4:
            st.metric(
                "⚠️ Missing Values",
                missing_before
            )

        with col5:
            st.metric(
                "🔁 Duplicate Rows",
                duplicate_before
            )

        with col6:
            st.metric(
                "📊 Quality Score",
                f"{quality_score_after}%"
            )

        # ---------------- QUALITY SCORE ----------------

        st.subheader("🎯 Data Quality Score")

        st.progress(quality_score_after / 100)

        st.metric(
            "Overall Data Quality",
            f"{quality_score_after}%"
        )

        # Quality message
        if quality_score_after >= 90:
            st.success("🟢 Excellent Data Quality")

        elif quality_score_after >= 75:
            st.warning("🟡 Good Data Quality")

        elif quality_score_after >= 50:
            st.warning("🟠 Moderate Data Quality")

        else:
            st.error("🔴 Poor Data Quality")

        st.success("✅ Data Cleaned Successfully!")

        # ---------------- CLEANED DATA ----------------

        st.subheader("🗂️ Cleaned Dataset")
        st.dataframe(df)

        # ---------------- DOWNLOAD CSV ----------------

        csv = df.to_csv(index=False)

        st.download_button(
            "⬇️ Download Cleaned CSV",
            csv,
            "cleaned_data.csv",
            "text/csv"
        )

        # ---------------- DOWNLOAD EXCEL ----------------

        if uploaded_file.name.lower().endswith((".xlsx", ".xls")):

            import io
            import pandas as pd

            output = io.BytesIO()

            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Cleaned Data"
                )

            st.download_button(
                "⬇️ Download Cleaned Excel",
                output.getvalue(),
                "cleaned_data.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

else:
    st.info("👆 Please upload a CSV or Excel file to get started.")
