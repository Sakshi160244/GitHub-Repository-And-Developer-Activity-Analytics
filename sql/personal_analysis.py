import pandas as pd
import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "github_analytics_db"
}


QUERIES = {
    "1. Personal Repository KPIs": """
        SELECT
            COUNT(*) AS total_repositories,
            SUM(CASE WHEN repository_type = 'Original'
                THEN 1 ELSE 0 END) AS original_repositories,
            SUM(CASE WHEN repository_type = 'Forked'
                THEN 1 ELSE 0 END) AS forked_repositories,
            SUM(stars_count) AS total_stars,
            SUM(forks_count) AS total_forks,
            SUM(CASE WHEN activity_status = 'Active'
                THEN 1 ELSE 0 END) AS active_repositories
        FROM personal_repositories;
    """,

    "2. Personal Activity Status": """
        SELECT
            activity_status,
            COUNT(*) AS repository_count,
            ROUND(
                COUNT(*) * 100.0 /
                (SELECT COUNT(*) FROM personal_repositories), 2
            ) AS percentage
        FROM personal_repositories
        GROUP BY activity_status
        ORDER BY FIELD(
            activity_status,
            'Active',
            'Moderately Active',
            'Inactive',
            'Unknown'
        );
    """,

    "3. Personal Repository Type": """
        SELECT
            repository_type,
            COUNT(*) AS repository_count
        FROM personal_repositories
        GROUP BY repository_type;
    """,

    "4. Personal Languages": """
        SELECT
            primary_language,
            COUNT(*) AS repository_count
        FROM personal_repositories
        GROUP BY primary_language
        ORDER BY repository_count DESC;
    """,

    "5. Personal Repository Sample":"""
        SELECT
            repository_name,
            primary_language,
            stars_count,
            forks_count,
            activity_status
        FROM personal_repositories
       ORDER BY repository_name ASC
        LIMIT 5;
    """,

    "6. GitHub Profile": """
        SELECT
            username,
            name,
            public_repositories,
            followers,
            following,
            account_created_year,
            account_age_days
        FROM github_profile;
    """
}


def main():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        for title, query in QUERIES.items():
            cursor.execute(query)

            result = pd.DataFrame(
                cursor.fetchall(),
                columns=cursor.column_names
            )

            print("\n" + "=" * 60)
            print(title)
            print("=" * 60)
            print(result.to_string(index=False))

    except mysql.connector.Error as error:
        print("MySQL error:", error)

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
            print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()