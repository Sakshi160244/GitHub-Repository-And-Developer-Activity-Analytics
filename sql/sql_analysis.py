import pandas as pd
import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "github_analytics_db"
}


QUERIES = {
    "1. Top Repository KPIs": """
        SELECT
            COUNT(*) AS total_repositories,
            SUM(stars_count) AS total_stars,
            SUM(forks_count) AS total_forks,
            ROUND(AVG(stars_count), 2) AS average_stars
        FROM top_repositories;
    """,

    "2. Activity Status": """
        SELECT
            activity_status,
            COUNT(*) AS repository_count,
            ROUND(
                COUNT(*) * 100.0 /
                (SELECT COUNT(*) FROM top_repositories), 2
            ) AS percentage
        FROM top_repositories
        GROUP BY activity_status
        ORDER BY FIELD(
            activity_status,
            'Active',
            'Moderately Active',
            'Inactive',
            'Unknown'
        );
    """,

    "3. License Availability": """
        SELECT
            has_license,
            COUNT(*) AS repository_count,
            ROUND(
                COUNT(*) * 100.0 /
                (SELECT COUNT(*) FROM top_repositories), 2
            ) AS percentage
        FROM top_repositories
        GROUP BY has_license
        ORDER BY FIELD(has_license, 'Yes', 'No');
    """,

    "4. Top 10 Repositories by Stars": """
        SELECT
            full_name,
            primary_language,
            stars_count,
            forks_count
        FROM top_repositories
        ORDER BY stars_count DESC
        LIMIT 10;
    """,

    "5. Highest Popularity Score": """
        SELECT
            full_name,
            popularity_score
        FROM top_repositories
        ORDER BY popularity_score DESC
        LIMIT 1;
    """,

    "6. Repository Count by Language": """
        SELECT
            primary_language,
            COUNT(*) AS repository_count,
            SUM(stars_count) AS total_stars
        FROM top_repositories
        GROUP BY primary_language
        ORDER BY repository_count DESC;
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

            rows = cursor.fetchall()
            columns = cursor.column_names

            result = pd.DataFrame(rows, columns=columns)

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