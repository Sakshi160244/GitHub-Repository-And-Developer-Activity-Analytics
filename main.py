import sys
from pathlib import Path

BASE_FOLDER = Path(__file__).resolve().parent

sys.path.insert(0, str(BASE_FOLDER / "python"))
sys.path.insert(0, str(BASE_FOLDER / "sql"))
from datetime import datetime, timezone
from python.config import*
from python.data_loading import*
from python.data_cleaning import*
from python.top_repositories_cleaning import (clean_data as clean_top_repositories)
from python.eda import run_eda
from python.visualization import run_visualizations
from python.github_data_collection import*
from python.top_repositories_collection import collect_top_data

from sql.sql_analysis import main as run_top_sql
from sql.personal_analysis import main as run_personal_sql
from sql.comparison_analysis import main as run_comparison_sql


# Clean saved raw data
def run_cleaning():
    profile, personal, top = load_raw_data()

    cleaned_profile = clean_profile_data(profile)
    cleaned_personal = clean_repository_data(personal)
    cleaned_top = clean_top_repositories(top)

    save_cleaned_data(
        cleaned_profile,
        cleaned_personal,
        cleaned_top
    )

    print("Cleaning completed.")
    print(f"Analysis date: {AS_OF_DATE.isoformat()}")


# Run EDA
def run_analysis():
    personal, top = load_cleaned_data()
    run_eda(personal, top)


# Generate charts
def run_charts():
    personal, top = load_cleaned_data()
    run_visualizations(top)


# Run cleaning, EDA and charts
def run_all():
    run_cleaning()
    run_analysis()
    run_charts()


# Collect a new GitHub snapshot
def collect_new_snapshot():
    started = datetime.now(timezone.utc)

    folder = (
        BASE_DIR
        / "data"
        / "collected"
        / started.strftime("%Y%m%d_%H%M%S_%f_UTC")
    )

    collect_personal_data(folder)
    collect_top_data(folder)

    finished = datetime.now(timezone.utc).isoformat()

    metadata = {
        "collection_started_at": started.isoformat(),
        "collection_completed_at": finished,
        "username": USERNAME,
        "search_query": SEARCH_QUERY
    }

    save_json(metadata, folder / "collection_metadata.json")

    print(f"New snapshot saved to: {folder}")
    print("To analyze this snapshot, update python/config.py:")
    print("Set RAW_DATA_DIR to the folder shown above.")
    print(f"Set AS_OF_DATE to pd.Timestamp({finished!r}).")
    print("Then run option 4.")


# Main menu
def main():
    while True:
        print("\n========== GITHUB ANALYTICS ==========")
        print("1. Clean saved raw CSV files")
        print("2. Run EDA on cleaned CSV files")
        print("3. Generate charts")
        print("4. Run cleaning + EDA + charts")
        print("5. Collect a new GitHub snapshot")
        print("6. SQL: Top Repositories Analysis")
        print("7. SQL: Personal Repositories Analysis")
        print("8. SQL: Dataset Comparison")
        print("0. Exit")

        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nProgram closed.")
            break

        if choice == "0":
            print("Program closed.")
            break

        try:
            if choice == "1":
                run_cleaning()

            elif choice == "2":
                run_analysis()

            elif choice == "3":
                run_charts()

            elif choice == "4":
                run_all()

            elif choice == "5":
                collect_new_snapshot()

            elif choice == "6":
                run_top_sql()

            elif choice == "7":
                run_personal_sql()

            elif choice == "8":
                run_comparison_sql()

            else:
                print("Enter a number from 0 to 8.")

        except Exception as error:
            print(f"This step could not finish: {error}")


if __name__ == "__main__":
    main()