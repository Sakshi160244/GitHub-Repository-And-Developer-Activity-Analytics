import pandas as pd
from config import RAW_DATA_DIR, CLEANED_DATA_DIR, AS_OF_DATE


def load_raw_data():
    profile = pd.read_csv(
        RAW_DATA_DIR / "github_profile.csv"
    )

    personal = pd.read_csv(
        RAW_DATA_DIR / "github_repositories.csv"
    )

    top = pd.read_csv(
        RAW_DATA_DIR / "top_data_analysis_repositories.csv"
    )

    return profile, personal, top


def load_cleaned_data():
    personal = pd.read_csv(
        CLEANED_DATA_DIR / "cleaned_github_repositories.csv"
    )

    top = pd.read_csv(
        CLEANED_DATA_DIR / "cleaned_top_repositories.csv"
    )

    for name, df in [("Personal", personal), ("Top", top)]:
        if df.empty:
            raise ValueError(f"{name} dataset is empty.")

        dates = pd.to_datetime(
            df["analysis_as_of_date"],
            utc=True
        )

        if not dates.eq(AS_OF_DATE).all():
            raise ValueError(
                "Analysis dates differ. Run menu option 1 first."
            )

    return personal, top