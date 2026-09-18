USE github_analytics_db;

-- Top repositories KPIs
SELECT
    COUNT(*) AS total_repositories,
    SUM(stars_count) AS total_stars,
    SUM(forks_count) AS total_forks,
    ROUND(AVG(stars_count), 2) AS average_stars
FROM top_repositories;


-- Activity status
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


-- License availability
SELECT
    has_license,
    COUNT(*) AS repository_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM top_repositories), 2
    ) AS percentage
FROM top_repositories
GROUP BY has_license;


-- Top 10 repositories by stars
SELECT
    full_name,
    primary_language,
    stars_count,
    forks_count
FROM top_repositories
ORDER BY stars_count DESC
LIMIT 10;


-- Most popular repository by custom score
SELECT
    full_name,
    popularity_score
FROM top_repositories
ORDER BY popularity_score DESC
LIMIT 1;


-- Repository count by programming language
SELECT
    primary_language,
    COUNT(*) AS repository_count,
    SUM(stars_count) AS total_stars
FROM top_repositories
GROUP BY primary_language
ORDER BY repository_count DESC;