from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "cleaned"


def load_data(dataset):
    files = {
        "Top Repositories": "cleaned_top_repositories.csv",
        "My Repositories": "cleaned_github_repositories.csv"
    }
    return pd.read_csv(DATA_DIR / files[dataset])


def filter_data(df, language, activity, license_status):
    result = df.copy()
    for column, selected in [
        ("primary_language", language),
        ("activity_status", activity),
        ("has_license", license_status)
    ]:
        if selected != "All" and column in result.columns:
            result = result[result[column] == selected]
    return result


def show_charts(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    top = df.sort_values(
        ["stars_count", "full_name"], ascending=[False, True]
    ).head(10).iloc[::-1]
    if df["stars_count"].max() > 0:
        axes[0, 0].barh(top["full_name"], top["stars_count"], color="#4E79A7")
    else:
        axes[0, 0].text(0.5, 0.5, "All selected repositories have 0 stars",
                        ha="center", va="center", transform=axes[0, 0].transAxes)
    axes[0, 0].set_title("Top Repositories by Stars")
    axes[0, 0].set_xlabel("Stars")

    languages = df["primary_language"].value_counts().sort_values()
    axes[0, 1].barh(languages.index, languages.values, color="#59A14F")
    axes[0, 1].set_title("Repositories by Programming Language")
    axes[0, 1].set_xlabel("Repository Count")

    order = ["Active", "Moderately Active", "Inactive", "Unknown"]
    activity = df["activity_status"].value_counts().reindex(order, fill_value=0)
    axes[1, 0].bar(activity.index, activity.values,
                   color=["#59A14F", "#F28E2B", "#E15759", "#79706E"])
    axes[1, 0].set_title("Repository Activity Status")
    axes[1, 0].set_ylabel("Repository Count")
    axes[1, 0].tick_params(axis="x", labelrotation=15)

    years = pd.to_numeric(df["created_year"], errors="coerce").dropna().astype(int)
    trend = years.value_counts().sort_index()
    if not trend.empty:
        trend = trend.reindex(range(trend.index.min(), trend.index.max() + 1), fill_value=0)
        axes[1, 1].plot(trend.index, trend.values, marker="o", color="#4E79A7")
        axes[1, 1].set_xticks(trend.index)
        axes[1, 1].tick_params(axis="x", labelrotation=45)
    axes[1, 1].set_title("Selected Repositories by Creation Year")
    axes[1, 1].set_ylabel("Repository Count")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)