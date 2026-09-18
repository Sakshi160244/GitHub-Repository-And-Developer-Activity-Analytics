import pandas as pd
import mysql.connector
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"

DB = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "github_analytics_db"
}

FILES = {
    "github_profile": "cleaned_github_profile.csv",
    "personal_repositories": "cleaned_github_repositories.csv",
    "top_repositories": "cleaned_top_repositories.csv"
}


def prepare_rows(df):
    for column in df.columns:
        if column.endswith("_at") or column == "analysis_as_of_date":
            dates = pd.to_datetime(df[column], errors="coerce", utc=True)
            df[column] = (
                dates.dt.tz_localize(None)
                .dt.strftime("%Y-%m-%d %H:%M:%S")
            )

    rows = []

    for row in df.itertuples(index=False, name=None):
        values = []
        for value in row:
            if pd.isna(value):
                values.append(None)
            elif hasattr(value, "item"):
                values.append(value.item())
            else:
                values.append(value)
        rows.append(tuple(values))

    return rows


def main():
    connection = mysql.connector.connect(**DB)
    cursor = connection.cursor()

    for table, filename in FILES.items():
        df = pd.read_csv(DATA_DIR / filename)
        rows = prepare_rows(df)

        columns = ", ".join(f"`{column}`" for column in df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))

        query = f"""
            INSERT INTO `{table}` ({columns})
            VALUES ({placeholders})
        """

        cursor.execute(f"TRUNCATE TABLE `{table}`")
        cursor.executemany(query, rows)
        connection.commit()

        print(f"{table}: {len(rows)} rows imported")

    cursor.close()
    connection.close()
    print("All CSV data imported successfully.")


if __name__ == "__main__":
    main()