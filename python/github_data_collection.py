import json
import os
import pandas as pd

from config import USERNAME


def get_json(url, params=None):
    import requests

    headers = {
        "Accept": "application/vnd.github+json"
    }

    token = os.getenv("GITHUB_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()
    return response.json()


def save_json(data, path):
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def get_user_repositories(username):
    repositories = []
    page = 1

    while True:
        batch = get_json(
            f"https://api.github.com/users/{username}/repos",
            {
                "per_page": 100,
                "page": page,
                "sort": "updated"
            }
        )

        if not batch:
            return repositories

        repositories.extend(batch)
        page += 1


def create_profile_dataframe(profile):
    # CSV column name: GitHub JSON field name.
    fields = {
        "user_id": "id",
        "username": "login",
        "name": "name",
        "profile_url": "html_url",
        "company": "company",
        "blog": "blog",
        "location": "location",
        "email": "email",
        "bio": "bio",
        "public_repositories": "public_repos",
        "public_gists": "public_gists",
        "followers": "followers",
        "following": "following",
        "account_created_at": "created_at",
        "profile_updated_at": "updated_at"
    }

    row = {
        column: profile.get(key)
        for column, key in fields.items()
    }

    return pd.DataFrame([row])


def create_repositories_dataframe(repositories):
    fields = {
        "repository_id": "id",
        "repository_name": "name",
        "full_name": "full_name",
        "repository_url": "html_url",
        "description": "description",
        "primary_language": "language",
        "created_at": "created_at",
        "updated_at": "updated_at",
        "pushed_at": "pushed_at",
        "size_kb": "size",
        "stars_count": "stargazers_count",
        "watchers_count": "watchers_count",
        "forks_count": "forks_count",
        "open_issues_count": "open_issues_count",
        "default_branch": "default_branch",
        "is_fork": "fork",
        "is_archived": "archived",
        "is_disabled": "disabled",
        "visibility": "visibility"
    }

    rows = []

    for repository in repositories:
        row = {
            column: repository.get(key)
            for column, key in fields.items()
        }

        rows.append(row)

    return pd.DataFrame(rows, columns=list(fields))


def collect_personal_data(output_dir):
    profile = get_json(
        f"https://api.github.com/users/{USERNAME}"
    )

    repositories = get_user_repositories(USERNAME)

    output_dir.mkdir(parents=True, exist_ok=True)

    save_json(
        profile, output_dir / "github_profile_raw.json"
    )

    save_json(
        repositories, output_dir / "github_repositories_raw.json"
    )

    create_profile_dataframe(profile).to_csv(
        output_dir / "github_profile.csv",
        index=False
    )

    create_repositories_dataframe(repositories).to_csv(
        output_dir / "github_repositories.csv",
        index=False
    )

    print(f"Collected {len(repositories)} personal repositories.")
