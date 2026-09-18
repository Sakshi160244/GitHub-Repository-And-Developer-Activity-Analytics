import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.ticker import *
from config import *
from kpi_analysis import known_languages
from chart_helpers import *

def plot_top_repositories(df):
    top = df.sort_values(
        ["stars_count", "full_name"],
        ascending=[False, True]
    ).head(10)

    fig, ax = plt.subplots(figsize=(13, 7))
    ax.barh(top["full_name"], top["stars_count"], color="#4C78A8")
    ax.invert_yaxis()

    ax.set(
        title="Top 10 Repositories by Stars",
        xlabel="Stars",
        ylabel="Repository"
    )

    add_labels(ax, horizontal=True)
    save_chart(fig, "top_10_repositories_by_stars.png", len(df))


def plot_language_distribution(df):
    known = known_languages(df)

    counts = (
        known["primary_language"]
        .value_counts()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(11, 8))
    ax.barh(counts.index, counts.values, color="#4C78A8")

    ax.set(
        title="Repository Count by Primary Language",
        xlabel="Repositories"
    )

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    add_labels(ax, horizontal=True)

    note = (
        f"Excludes {len(df) - len(known)} repositories "
        "with unspecified language."
    )

    save_chart(fig, "repositories_by_language.png", len(df), note)


def plot_stars_by_language(df):
    known = known_languages(df)

    stars = (
        known.groupby("primary_language")["stars_count"]
        .sum()
        .nlargest(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(11, 8))
    ax.barh(stars.index, stars.values, color="#59A14F")

    ax.set(
        title="Top 10 Languages by Total Stars",
        xlabel="Total Stars"
    )

    add_labels(ax, horizontal=True)

    note = (
        f"Excludes {len(df) - len(known)} "
        "unspecified-language repositories. "
        "Totals depend on group size."
    )

    save_chart(fig, "total_stars_by_language.png", len(df), note)


def plot_activity_status(df):
    counts = (
        df["activity_status"]
        .value_counts()
        .reindex(ACTIVITY_ORDER, fill_value=0)
    )

    if counts["Unknown"] == 0:
        counts = counts.drop("Unknown")

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.bar(
        counts.index,
        counts.values,
        color=[ACTIVITY_COLORS[status] for status in counts.index]
    )

    ax.set(
        title="Repositories by Activity Status",
        ylabel="Repositories"
    )

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    add_labels(ax)

    note = (
        "Last push: Active 0–180 days; Moderately Active 181–365; "
        "Inactive >365.\nUnknown: missing or future push date."
    )

    save_chart(
        fig, "repositories_by_activity_status.png", len(df), note
    )


def plot_creation_trend(df):
    counts = (
        df["created_year"]
        .dropna()
        .astype(int)
        .value_counts()
        .sort_index()
    )

    if counts.empty:
        raise ValueError("No valid creation years to plot.")

    counts = counts.reindex(
        range(counts.index.min(), counts.index.max() + 1),
        fill_value=0
    )

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(
        counts.index, counts.values,
        marker="o", color="#4C78A8"
    )

    for year, count in counts.items():
        ax.annotate(
            str(count), (year, count),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center", fontsize=9
        )

    ax.set(
        title="Creation Years of Selected Repositories",
        xlabel="Creation Year",
        ylabel="Repositories",
        ylim=(0, max(counts.max(), 1) * 1.2)
    )

    ax.set_xticks(counts.index)
    ax.tick_params(axis="x", rotation=45)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    note = (
        f"{AS_OF_DATE.year} is partial-year data. "
        "This sample is not overall GitHub growth.\n"
        f"Missing creation years excluded: "
        f"{df['created_year'].isna().sum()}."
    )

    save_chart(fig, "repository_creation_trend.png", len(df), note)


def plot_stars_vs_forks(df):
    selected = df.loc[
        df["stars_count"].gt(0)
        & df["forks_count"].gt(0)
    ]

    if selected.empty:
        raise ValueError(
            "No positive stars/forks available for a logarithmic chart."
        )

    fig, ax = plt.subplots(figsize=(11, 7))

    sns.scatterplot(
        data=selected,
        x="stars_count",
        y="forks_count",
        hue="activity_status",
        palette=ACTIVITY_COLORS,
        s=65,
        ax=ax
    )

    ax.set(
        xscale="log",
        yscale="log",
        title="Relationship Between Stars and Forks",
        xlabel="Stars (Log Scale)",
        ylabel="Forks (Log Scale)"
    )

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(LogLocator(base=10, subs=(1, 2, 5)))
        axis.set_major_formatter(
            FuncFormatter(lambda x, pos: f"{x:,.0f}")
        )
        axis.set_minor_formatter(NullFormatter())

    ax.legend(
        title="Activity Status",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

    note = (
        f"Both axes are logarithmic; "
        f"{len(df) - len(selected)} zero-star/fork rows excluded."
    )

    save_chart(fig, "stars_vs_forks.png", len(df), note)


def plot_license_availability(df):
    counts = (
        df["has_license"]
        .value_counts()
        .reindex(["Yes", "No"], fill_value=0)
    )

    counts = counts[counts.gt(0)]

    names = {"Yes": "Licensed", "No": "No License"}
    colors = {"Yes": "#4C78A8", "No": "#F28E2B"}

    labels = [
        f"{names[key]} (n={count})"
        for key, count in counts.items()
    ]

    fig, ax = plt.subplots(figsize=(9, 8))

    ax.pie(
        counts.values,
        labels=labels,
        colors=[colors[key] for key in counts.index],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white"}
    )

    ax.set_title("Repository License Availability")

    save_chart(
        fig, "repository_license_availability.png", len(df)
    )


def run_visualizations(df):
    setup_charts()

    plot_top_repositories(df)
    plot_language_distribution(df)
    plot_stars_by_language(df)
    plot_activity_status(df)
    plot_creation_trend(df)
    plot_stars_vs_forks(df)
    plot_license_availability(df)

    print("\nAll 7 charts saved successfully.")
