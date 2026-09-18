import pandas as pd
import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "github_analytics_db"
}


QUERY = """
SELECT
    'Total Repositories' AS metric,
    (SELECT COUNT(*) FROM personal_repositories) AS personal_repositories,
    (SELECT COUNT(*) FROM top_repositories) AS top_repositories

UNION ALL

SELECT
    'Total Stars',
    (SELECT SUM(stars_count) FROM personal_repositories),
    (SELECT SUM(stars_count) FROM top_repositories)

UNION ALL

SELECT
    'Total Forks',
    (SELECT SUM(forks_count) FROM personal_repositories),
    (SELECT SUM(forks_count) FROM top_repositories)

UNION ALL

SELECT
    'Unique Known Languages',
    (
        SELECT COUNT(DISTINCT primary_language)
        FROM personal_repositories
        WHERE primary_language <> 'Not Specified'
    ),
    (
        SELECT COUNT(DISTINCT primary_language)
        FROM top_repositories
        WHERE primary_language <> 'Not Specified'
    )

UNION ALL

SELECT
    'Active Repositories',
    (
        SELECT COUNT(*)
        FROM personal_repositories
        WHERE activity_status = 'Active'
    ),
    (
        SELECT COUNT(*)
        FROM top_repositories
        WHERE activity_status = 'Active'
    )

UNION ALL

SELECT
    'Active Repository Rate',
    (
        SELECT ROUND(
            COUNT(CASE WHEN activity_status = 'Active' THEN 1 END)
            * 100.0 / COUNT(*), 2
        )
        FROM personal_repositories
    ),
    (
        SELECT ROUND(
            COUNT(CASE WHEN activity_status = 'Active' THEN 1 END)
            * 100.0 / COUNT(*), 2
        )
        FROM top_repositories
    );
"""


def main():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute(QUERY)

    result = pd.DataFrame(
        cursor.fetchall(),
        columns=cursor.column_names
    )

    print("\n" + "=" * 60)
    print("PERSONAL VS TOP REPOSITORIES COMPARISON")
    print("=" * 60)
    print(result.to_string(index=False))

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()