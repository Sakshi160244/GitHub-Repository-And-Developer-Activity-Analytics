import pandas as pd

from config import AS_OF_DATE, ACTIVITY_ORDER
from kpi_analysis import *


def show_summary(df):
    for name, value in get_kpis(df).items():
        if name == "Active rate":
            display = f"{value:.2%}"
        else:
            display = f"{value:,}"

        print(f"{name}: {display}")


def show_activity(df):
    counts = (
        df["activity_status"]
        .value_counts()
        .reindex(ACTIVITY_ORDER, fill_value=0)
    )

    table = counts.to_frame("Repository Count")
    table["Percentage"] = (counts / len(df) * 100).round(2)

    print("\nActivity status (Percentage is in %):")
    print(table.to_string())


def analyze_personal_repositories(df):
    print("\n========== PERSONAL REPOSITORIES ==========")

    show_summary(df)

    print(
        f"Original: "
        f"{df['repository_type'].eq('Original').sum()}"
    )

    print(
        f"Forked: "
        f"{df['repository_type'].eq('Forked').sum()}"
    )

    show_activity(df)

    print("\nRepository count by language, including unspecified:")
    print(df["primary_language"].value_counts().to_string())

    columns = [
        "repository_name",
        "primary_language",
        "stars_count",
        "forks_count",
        "activity_status"
    ]

    all_tied = (
        df["stars_count"].nunique() == 1
        and df["forks_count"].nunique() == 1
    )

    if all_tied:
        print("\nAll stars/forks are tied. Five examples, alphabetically:")
        selected = df.sort_values("repository_name").head(5)

    else:
        print("\nTop 5 by stars, then forks:")

        selected = df.sort_values(
            ["stars_count", "forks_count", "repository_name"],
            ascending=[False, False, True]
        ).head(5)

    print(selected[columns].to_string(index=False))


def analyze_top_repositories(df):
    print("\n========== SELECTED TOP REPOSITORIES ==========")

    show_summary(df)

    print(f"Average stars: {df['stars_count'].mean():,.2f}")
    print(f"Median stars: {df['stars_count'].median():,.2f}")
    print(f"Average forks: {df['forks_count'].mean():,.2f}")

    print(
        f"Average open_issues_count: "
        f"{df['open_issues_count'].mean():,.2f}"
    )

    ranked = df.sort_values(
        ["stars_count", "full_name"],
        ascending=[False, True]
    )

    print("\nTop 10 by stars:")

    columns = [
        "full_name", "primary_language",
        "stars_count", "forks_count"
    ]

    print(ranked[columns].head(10).to_string(index=False))

    print("\nHighest custom popularity score (stars + 2 * forks):")

    leaders = df.loc[
        df["popularity_score"].eq(df["popularity_score"].max()),
        ["full_name", "popularity_score"]
    ]

    print(leaders.to_string(index=False))

    print("\nRepository count by language, including unspecified:")
    print(df["primary_language"].value_counts().to_string())

    language_table = (
        known_languages(df)
        .groupby("primary_language")
        .agg(
            repository_count=("repository_id", "count"),
            total_stars=("stars_count", "sum"),
            average_stars=("stars_count", "mean"),
            average_forks=("forks_count", "mean")
        )
        .round(2)
        .sort_values("total_stars", ascending=False)
    )

    print("\nKnown-language analysis (Not Specified excluded):")
    print(language_table.to_string())

    print(
        "Read averages with group sizes; "
        "some groups have one repository."
    )

    show_activity(df)

    print("\nLicense availability:")
    print(df["has_license"].value_counts().to_string())

    print(
        f"Licensed rate: "
        f"{df['has_license'].eq('Yes').mean():.2%}"
    )

    print("\nCreation years within this sample:")

    print(
        df["created_year"]
        .value_counts(dropna=False)
        .sort_index()
        .to_string()
    )

    print(
        f"{AS_OF_DATE.year} is partial-year data; "
        "this is not overall GitHub growth."
    )


def compare_datasets(personal, top):
    print("\n========== DATASET COMPARISON ==========")

    table = pd.DataFrame({
        "Personal": get_kpis(personal),
        "Selected Top": get_kpis(top)
    })

    display = table.astype(object)

    for column in display:
        for metric in display.index:
            value = table.loc[metric, column]

            if metric == "Active rate":
                display.loc[metric, column] = f"{value:.2%}"
            else:
                display.loc[metric, column] = f"{value:,.0f}"

    print(display.to_string())

    print(
        "Samples differ in size and selection; "
        "this is not a developer ranking."
    )

    return table


def run_eda(personal, top):
    print(f"Analysis reference time: {AS_OF_DATE.isoformat()}")

    analyze_personal_repositories(personal)
    analyze_top_repositories(top)
    compare_datasets(personal, top)

    print("\nEDA completed successfully.")
