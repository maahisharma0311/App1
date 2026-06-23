import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Forecasting Data Checker",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Forecasting Data Suitability Checker")

st.write("""
Upload an Excel file. The app will:

✅ Detect numerical columns

✅ Create histograms for each numerical column

✅ Calculate Mean and Median

✅ Check whether Mean and Median are approximately close

✅ Suggest whether the data may be suitable for forecasting
""")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:

    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        numeric_cols = df.select_dtypes(include=np.number).columns

        if len(numeric_cols) == 0:
            st.error("No numerical columns found.")
        else:

            st.subheader("Numerical Column Analysis")

            results = []

            for col in numeric_cols:

                data = df[col].dropna()

                mean_val = data.mean()
                median_val = data.median()

                difference_percent = (
                    abs(mean_val - median_val) /
                    abs(mean_val)
                ) * 100 if mean_val != 0 else 0

                suitable = (
                    "✅ Suitable for Forecasting"
                    if difference_percent <= 10
                    else "⚠️ Data may be skewed"
                )

                results.append([
                    col,
                    round(mean_val, 2),
                    round(median_val, 2),
                    round(difference_percent, 2),
                    suitable
                ])

                st.markdown(f"## {col}")

                col1, col2 = st.columns([2, 1])

                with col1:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.hist(data, bins=15)
                    ax.set_title(f"Histogram - {col}")
                    ax.set_xlabel(col)
                    ax.set_ylabel("Frequency")
                    st.pyplot(fig)

                with col2:
                    st.metric("Mean", round(mean_val, 2))
                    st.metric("Median", round(median_val, 2))
                    st.metric(
                        "% Difference",
                        round(difference_percent, 2)
                    )

                    if difference_percent <= 10:
                        st.success("Suitable for Forecasting")
                    else:
                        st.warning("Potentially Skewed Data")

            st.subheader("Summary Table")

            summary_df = pd.DataFrame(
                results,
                columns=[
                    "Column",
                    "Mean",
                    "Median",
                    "% Difference",
                    "Recommendation"
                ]
            )

            st.dataframe(summary_df)

            csv = summary_df.to_csv(index=False)

            st.download_button(
                "Download Summary Report",
                csv,
                file_name="forecasting_report.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error: {e}")
