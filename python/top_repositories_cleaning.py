from cleaning_helpers import *


def clean_data(df):
    df = clean_repositories(df)

    text_defaults = {
        "topics": "No Topics",
        "license_name": "No License",
        "homepage": "Not Available"
    }

    for column, default in text_defaults.items():
        df[column] = clean_text(df[column], default)

    for column in [
        "has_issues", "has_projects", "has_wiki", "has_pages"
    ]:
        df[column] = clean_boolean(df[column])

    df["has_license"] = (
        df["license_name"]
        .ne("No License")
        .map({True: "Yes", False: "No"})
    )

    # Zero stars means the ratio is undefined.
    stars = (
        df["stars_count"]
        .astype("Float64")
        .where(df["stars_count"].gt(0))
    )

    df["fork_to_star_ratio"] = (
        df["forks_count"].div(stars).round(4)
    )

    df["issues_per_1000_stars"] = (
        df["open_issues_count"]
        .div(stars)
        .mul(1000)
        .round(2)
    )

    return df
