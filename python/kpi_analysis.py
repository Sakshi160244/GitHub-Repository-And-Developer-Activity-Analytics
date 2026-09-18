def known_languages(df):
    return df.loc[
        df["primary_language"].notna()
        & df["primary_language"].ne("Not Specified")
    ]


def get_kpis(df):
    total = len(df)
    active = int(df["activity_status"].eq("Active").sum())

    return {
        "Total repositories": total,
        "Total stars": int(df["stars_count"].sum()),
        "Total forks": int(df["forks_count"].sum()),
        "Known languages": (
            known_languages(df)["primary_language"].nunique()
        ),
        "Unspecified languages": total - len(known_languages(df)),
        "Active repositories": active,
        "Active rate": active / total if total else 0
    }