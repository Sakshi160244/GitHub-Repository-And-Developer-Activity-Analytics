from config import SEARCH_QUERY

from github_data_collection import*


def create_repository_dataframe(repositories):
    df = create_repositories_dataframe(repositories)

    owners = [
        repository.get("owner") or {}
        for repository in repositories
    ]

    licenses = [
        repository.get("license") or {}
        for repository in repositories
    ]

    df["owner_username"] = [
        owner.get("login") for owner in owners
    ]

    df["owner_type"] = [
        owner.get("type") for owner in owners
    ]

    df["license_name"] = [
        license_data.get("name") for license_data in licenses
    ]

    df["topics"] = [
        ", ".join(repository.get("topics") or [])
        for repository in repositories
    ]

    for column in [
        "homepage", "has_issues",
        "has_projects", "has_wiki", "has_pages"
    ]:
        df[column] = [
            repository.get(column)
            for repository in repositories
        ]

    columns = [
        "repository_id", "repository_name", "full_name",
        "owner_username", "owner_type", "repository_url",
        "description", "primary_language", "created_at",
        "updated_at", "pushed_at", "size_kb", "stars_count",
        "watchers_count", "forks_count", "open_issues_count",
        "default_branch", "topics", "license_name", "homepage",
        "has_issues", "has_projects", "has_wiki", "has_pages",
        "is_fork", "is_archived", "is_disabled", "visibility"
    ]

    return df[columns]


def collect_top_data(output_dir):
    params = {
        "q": SEARCH_QUERY,
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
        "page": 1
    }

    result = get_json(
        "https://api.github.com/search/repositories",
        params
    )

    if result.get("incomplete_results"):
        raise ValueError(
            "GitHub returned incomplete search results. Try again later."
        )

    repositories = result.get("items", [])

    if not repositories:
        raise ValueError("GitHub returned no matching repositories.")

    output_dir.mkdir(parents=True, exist_ok=True)

    save_json(
        result,
        output_dir / "top_data_analysis_repositories.json"
    )

    create_repository_dataframe(repositories).to_csv(
        output_dir / "top_data_analysis_repositories.csv",
        index=False
    )

    print(
        f"Collected {len(repositories)} repositories "
        f"from query: {SEARCH_QUERY}"
    )
