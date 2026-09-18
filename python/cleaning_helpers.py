import pandas as pd
from config import AS_OF_DATE


def clean_text(series, default):
    return (
        series.astype("string")
        .str.strip()
        .replace("", pd.NA)
        .fillna(default)
    )


def clean_boolean(series):
    values = (
        series.astype("string")
        .str.strip()
        .str.lower()
    )

    result = values.map({
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        "1.0": True,
        "0.0": False
    })

    if result.isna().any():
        raise ValueError(
            f"Missing or invalid boolean in {series.name}."
        )

    return result.astype(bool)


def clean_repositories(df):
    if df.empty or df["repository_id"].isna().any():
        raise ValueError(
            "Repository data is empty or contains missing IDs."
        )

    duplicates = df.duplicated("repository_id").sum()
    print(f"Duplicate repository IDs removed: {duplicates}")

    df = df.drop_duplicates("repository_id").copy()

    df["description"] = clean_text(
        df["description"], "No Description"
    )

    df["primary_language"] = clean_text(
        df["primary_language"], "Not Specified"
    )

    # Convert dates.
    for column in ["created_at", "updated_at", "pushed_at"]:
        df[column] = pd.to_datetime(
            df[column], errors="coerce", utc=True
        )

    # Validate numeric columns.
    numeric_columns = [
        "size_kb",
        "stars_count",
        "watchers_count",
        "forks_count",
        "open_issues_count"
    ]

    for column in numeric_columns:
        values = pd.to_numeric(df[column], errors="coerce")

        invalid = (
            values.isna()
            | values.lt(0)
            | values.mod(1).ne(0)
        )

        if invalid.any():
            raise ValueError(
                f"Missing or invalid numbers in {column}."
            )

        df[column] = values.astype("int64")

    for column in ["is_fork", "is_archived", "is_disabled"]:
        df[column] = clean_boolean(df[column])

    # Date-based analysis columns.
    df["repository_age_days"] = (
        AS_OF_DATE - df["created_at"]
    ).dt.days

    df["days_since_update"] = (
        AS_OF_DATE - df["updated_at"]
    ).dt.days

    df["days_since_last_push"] = (
        AS_OF_DATE - df["pushed_at"]
    ).dt.days

    df["created_year"] = df["created_at"].dt.year
    df["created_month"] = df["created_at"].dt.month_name()
    df["updated_year"] = df["updated_at"].dt.year

    df["size_mb"] = (df["size_kb"] / 1024).round(2)

    df["repository_type"] = df["is_fork"].map({
        True: "Forked",
        False: "Original"
    })

    df["has_description"] = (
        df["description"]
        .ne("No Description")
        .map({True: "Yes", False: "No"})
    )

    # Both datasets use the same last-push activity rule.
    activity = pd.cut(
        df["days_since_last_push"],
        bins=[-1, 180, 365, float("inf")],
        labels=["Active", "Moderately Active", "Inactive"]
    )

    df["activity_status"] = (
        activity.astype("string").fillna("Unknown")
    )

    # Custom project score.
    df["popularity_score"] = (
        df["stars_count"] + 2 * df["forks_count"]
    )

    df["analysis_as_of_date"] = AS_OF_DATE.isoformat()

    return df