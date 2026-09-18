import base64

import pandas as pd
import streamlit as st

from python.dashboard import load_data, filter_data, show_charts


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="GitHub Analytics",
    page_icon="🐙",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# GITHUB DARK THEME CSS
# =========================================================

st.markdown(
    """
<style>

/* ---------------- MAIN APP ---------------- */

.stApp {
    background-color: #0d1117;
    color: #f0f6fc;
}

.block-container {
    padding-top: 5.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1500px;
}


/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {
    background-color: #010409;
    border-right: 1px solid #30363d;
}

section[data-testid="stSidebar"] > div {
    background-color: #010409;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f0f6fc !important;
}


/* ---------------- GENERAL TEXT ---------------- */

h1,
h2,
h3 {
    color: #f0f6fc !important;
}

p {
    color: #c9d1d9;
}

[data-testid="stCaptionContainer"] {
    color: #8b949e !important;
}


/* ---------------- DATASET BUTTONS ---------------- */

section[data-testid="stSidebar"] .stButton {
    width: 100%;
}

section[data-testid="stSidebar"] .stButton button {
    width: 100%;
    min-height: 46px;

    border-radius: 7px;

    font-size: 13px;
    font-weight: 600;

    border: 1px solid #30363d;

    transition:
        background-color 0.20s ease,
        border-color 0.20s ease,
        transform 0.20s ease;
}


/* Normal Dataset Button */

section[data-testid="stSidebar"]
.stButton button[kind="secondary"] {

    background-color: #161b22;
    color: #f0f6fc;
    border-color: #30363d;
}


/* Normal Hover */

section[data-testid="stSidebar"]
.stButton button[kind="secondary"]:hover {

    background-color: #21262d;
    color: #f0f6fc;
    border-color: #8b949e;

    transform: translateY(-1px);
}


/* Selected Dataset Button */

section[data-testid="stSidebar"]
.stButton button[kind="primary"] {

    background-color: #238636;
    color: #ffffff;
    border-color: #2ea043;
}


/* Selected Hover */

section[data-testid="stSidebar"]
.stButton button[kind="primary"]:hover {

    background-color: #2ea043;
    color: #ffffff;
    border-color: #3fb950;
}


/* ---------------- KPI CARDS ---------------- */

div[data-testid="stMetric"] {

    background-color: #161b22;

    border: 1px solid #30363d;

    border-radius: 10px;

    padding: 20px 18px;

    min-height: 115px;

    transition:
        transform 0.20s ease,
        border-color 0.20s ease,
        box-shadow 0.20s ease;
}


div[data-testid="stMetric"]:hover {

    transform: translateY(-3px);

    border-color: #58a6ff;

    box-shadow:
        0 5px 18px rgba(0, 0, 0, 0.25);
}


div[data-testid="stMetricLabel"] {
    color: #8b949e !important;
    font-weight: 600;
}


div[data-testid="stMetricValue"] {
    color: #f0f6fc !important;
}


/* ---------------- SELECT BOX ---------------- */

div[data-baseweb="select"] > div {

    background-color: #0d1117 !important;

    border-color: #30363d !important;

    color: #f0f6fc !important;

    border-radius: 7px;
}


/* ---------------- DATAFRAME ---------------- */

[data-testid="stDataFrame"] {

    border: 1px solid #30363d;

    border-radius: 8px;

    overflow: hidden;
}


/* ---------------- DOWNLOAD BUTTON ---------------- */

.stDownloadButton > button {

    background-color: #238636;

    color: #ffffff;

    border: 1px solid #2ea043;

    border-radius: 7px;

    font-weight: 600;

    padding: 8px 18px;

    transition:
        background-color 0.20s ease,
        transform 0.20s ease;
}


.stDownloadButton > button:hover {

    background-color: #2ea043;

    color: #ffffff;

    border-color: #3fb950;

    transform: translateY(-1px);
}


/* ---------------- DIVIDER ---------------- */

hr {
    border-color: #30363d !important;
}


/* ---------------- SPINNER ---------------- */

[data-testid="stSpinner"] {
    color: #58a6ff !important;
}


/* ---------------- ALERTS ---------------- */

[data-testid="stAlert"] {
    border-radius: 8px;
}


/* ---------------- HEADER ---------------- */

.github-title {

    font-size: 30px;

    font-weight: 700;

    color: #f0f6fc;

    line-height: 1.3;

    margin: 0;

    padding: 0;
}


.github-subtitle {

    color: #8b949e;

    font-size: 14px;

    margin-top: 6px;
}


/* ---------------- SECTION TITLE ---------------- */

.section-title {

    font-size: 21px;

    font-weight: 650;

    color: #f0f6fc;

    margin-top: 22px;

    margin-bottom: 14px;
}


/* ---------------- FOOTER ---------------- */

.github-footer {

    color: #8b949e;

    font-size: 13px;

    text-align: center;

    padding-top: 8px;

    padding-bottom: 10px;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## GitHub Analytics")


# =========================================================
# DATASET SESSION STATE
# =========================================================

if "dataset" not in st.session_state:
    st.session_state.dataset = "Top Repositories"


# =========================================================
# DATASET BUTTONS
# TOP-DOWN / VERTICAL
# =========================================================

st.sidebar.markdown("### Dataset")


top_selected = (
    st.session_state.dataset == "Top Repositories"
)


if st.sidebar.button(
    "Top Repositories",
    width="stretch",
    type="primary" if top_selected else "secondary",
    key="top_repositories_button"
):

    st.session_state.dataset = "Top Repositories"

    st.rerun()


my_selected = (
    st.session_state.dataset == "My Repositories"
)


if st.sidebar.button(
    "My Repositories",
    width="stretch",
    type="primary" if my_selected else "secondary",
    key="my_repositories_button"
):

    st.session_state.dataset = "My Repositories"

    st.rerun()


dataset = st.session_state.dataset


# =========================================================
# SIDEBAR DIVIDER
# =========================================================

st.sidebar.divider()


# =========================================================
# LOAD DATA
# =========================================================

try:

    with st.spinner("Loading repository data..."):

        df = load_data(dataset)


except FileNotFoundError:

    st.error(
        "Cleaned CSV file not found. "
        "Run cleaning from main.py first."
    )

    st.stop()


# =========================================================
# EMPTY DATA CHECK
# =========================================================

if df.empty:

    st.warning(
        "The selected dataset is empty."
    )

    st.stop()


# =========================================================
# HEADER - GITHUB LOGO + TITLE
# =========================================================

logo_col, title_col = st.columns(
    [1, 14],
    vertical_alignment="center"
)

with logo_col:
    st.image(
        "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        width=55
    )

with title_col:
    st.markdown(
        "<div class='github-title'>"
        "GitHub Repository & Developer Activity Analytics"
        "</div>",
        unsafe_allow_html=True
    )

    st.caption(
        "Repository Performance • Activity • Languages • Stars • Forks"
    )

st.divider()



# =========================================================
# ANALYSIS DATE
# =========================================================

analysis_date = pd.to_datetime(
    df["analysis_as_of_date"],
    utc=True
).max()


st.caption(
    f"{dataset} • Analysis reference date: "
    f"{analysis_date:%d %B %Y}"
)


if dataset == "Top Repositories":

    st.caption(
        "Selected top 100 repositories "
        "from the data-analysis topic search."
    )


# =========================================================
# FILTERS
# =========================================================

st.sidebar.header("Filters")


# =========================================================
# LANGUAGE FILTER
# =========================================================

languages = sorted(
    df["primary_language"]
    .dropna()
    .astype(str)
    .unique()
)


language = st.sidebar.selectbox(
    "Programming Language",
    ["All"] + languages,
    key=f"{dataset}_language"
)


# =========================================================
# ACTIVITY FILTER
# =========================================================

activity = st.sidebar.selectbox(
    "Activity Status",
    [
        "All",
        "Active",
        "Moderately Active",
        "Inactive",
        "Unknown"
    ],
    key=f"{dataset}_activity"
)


# =========================================================
# LICENSE FILTER
# =========================================================

license_status = "All"


if "has_license" in df.columns:

    license_status = st.sidebar.selectbox(
        "License Availability",
        [
            "All",
            "Yes",
            "No"
        ],
        key=f"{dataset}_license"
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered = filter_data(
    df,
    language,
    activity,
    license_status
)


# =========================================================
# EMPTY FILTER RESULT
# =========================================================

if filtered.empty:

    st.warning(
        "No repositories match these filters. "
        "Change a filter to continue."
    )

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

count = len(filtered)


active = int(
    filtered["activity_status"]
    .eq("Active")
    .sum()
)


known_languages = (
    filtered.loc[
        filtered["primary_language"] != "Not Specified",
        "primary_language"
    ]
    .nunique()
)


total_stars = int(
    filtered["stars_count"].sum()
)


total_forks = int(
    filtered["forks_count"].sum()
)


average_stars = filtered["stars_count"].mean()


# =========================================================
# REPOSITORY OVERVIEW
# =========================================================

st.markdown(
    "<div class='section-title'>"
    "Repository Overview"
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# KPI ROW 1
# =========================================================

cards = st.columns(4)


cards[0].metric(
    "Total Repositories",
    f"{count:,}"
)


cards[1].metric(
    "Total Stars",
    f"{total_stars:,}"
)


cards[2].metric(
    "Total Forks",
    f"{total_forks:,}"
)


cards[3].metric(
    "Average Stars",
    f"{average_stars:,.2f}"
)


st.write("")


# =========================================================
# KPI ROW 2
# =========================================================

cards = st.columns(4)


cards[0].metric(
    "Active Repositories",
    f"{active:,}"
)


cards[1].metric(
    "Active Repository Rate",
    f"{active / count:.2%}"
)


cards[2].metric(
    "Known Languages",
    f"{known_languages:,}"
)


# =========================================================
# KPI 8
# =========================================================

if "has_license" in filtered.columns:

    licensed_rate = (
        filtered["has_license"]
        .eq("Yes")
        .mean()
    )

    cards[3].metric(
        "Licensed Repository Rate",
        f"{licensed_rate:.2%}"
    )


elif "repository_type" in filtered.columns:

    original_repositories = int(
        filtered["repository_type"]
        .eq("Original")
        .sum()
    )

    cards[3].metric(
        "Original Repositories",
        f"{original_repositories:,}"
    )


else:

    cards[3].metric(
        "Dataset",
        dataset
    )


# =========================================================
# REPOSITORY CHARTS
# =========================================================

st.markdown(
    "<div class='section-title'>"
    "Repository Charts"
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# CHART LOADING SPINNER
# =========================================================

with st.spinner(
    "Loading repository charts..."
):

    show_charts(filtered)


# =========================================================
# CHART NOTE
# =========================================================

st.caption(
    f"Creation years describe this selected sample. "
    f"{analysis_date.year} is a partial year. "
    "Activity uses days since last push at the "
    "analysis reference date."
)


# =========================================================
# REPOSITORY DETAILS
# =========================================================

st.markdown(
    "<div class='section-title'>"
    "Repository Details"
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# TABLE COLUMNS
# =========================================================

columns = [
    "full_name",
    "primary_language",
    "stars_count",
    "forks_count",
    "activity_status"
]


# =========================================================
# SORT DATA
# =========================================================

details = filtered.sort_values(
    [
        "stars_count",
        "full_name"
    ],
    ascending=[
        False,
        True
    ]
)


# =========================================================
# REPOSITORY TABLE
# =========================================================

with st.spinner(
    "Loading repository details..."
):

    st.dataframe(
        details[columns],
        hide_index=True,
        width="stretch"
    )


# =========================================================
# DOWNLOAD CSV
# =========================================================

st.write("")


csv_data = (
    filtered
    .to_csv(index=False)
    .encode("utf-8-sig")
)


st.download_button(
    label="Download Filtered CSV",
    data=csv_data,
    file_name="filtered_repositories.csv",
    mime="text/csv"
)


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.markdown(
    "<div class='github-footer'>"
    "GitHub Developer Activity Analytics "
    "• Python • Pandas • Streamlit"
    "</div>",
    unsafe_allow_html=True
)