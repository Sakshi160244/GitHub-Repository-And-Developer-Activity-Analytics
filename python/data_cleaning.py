import pandas as pd
from config import *
from cleaning_helpers import *


def clean_profile_data(df):
    df = df.copy()

    text_columns = [
        "name", "company", "blog",
        "location", "email", "bio"
    ]

    for column in text_columns:
        default = (
            "Not Public" if column == "email"
            else "Not Available"
        )

        df[column] = clean_text(df[column], default)

    for column in ["account_created_at", "profile_updated_at"]:
        df[column] = pd.to_datetime(
            df[column], errors="coerce", utc=True
        )

    df["account_age_days"] = (
        AS_OF_DATE - df["account_created_at"]
    ).dt.days

    df["account_created_year"] = (
        df["account_created_at"].dt.year
    )

    df["analysis_as_of_date"] = AS_OF_DATE.isoformat()

    return df


def clean_repository_data(df):
    return clean_repositories(df)


def save_cleaned_data(profile, personal, top):
    CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    datasets = {
        "cleaned_github_profile.csv": profile,
        "cleaned_github_repositories.csv": personal,
        "cleaned_top_repositories.csv": top
    }

    for filename, df in datasets.items():
        df.to_csv(CLEANED_DATA_DIR / filename, index=False)

        print(
            f"Saved {filename}: "
            f"{len(df)} rows, {len(df.columns)} columns"
        )
