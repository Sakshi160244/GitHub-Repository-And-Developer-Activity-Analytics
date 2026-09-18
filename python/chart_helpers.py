import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.ticker import FuncFormatter
from config import *


def setup_charts():
    sns.set_theme(style="whitegrid")

    plt.rcParams.update({
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "font.family": "DejaVu Sans"
    })


def add_labels(ax, horizontal=False):
    for container in ax.containers:
        values = []

        for bar in container:
            value = (
                bar.get_width() if horizontal
                else bar.get_height()
            )
            values.append(value)

        ax.bar_label(
            container,
            labels=[f"{value:,.0f}" for value in values],
            padding=4
        )

    if horizontal:
        ax.margins(x=0.18)
        ax.xaxis.set_major_formatter(
            FuncFormatter(lambda x, pos: f"{x:,.0f}")
        )
        ax.grid(axis="y", visible=False)

    else:
        ax.margins(y=0.2)
        ax.grid(axis="x", visible=False)


def save_chart(fig, filename, total, note=""):
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    footer = (
        f"Saved GitHub API sample: {total} repositories; "
        "topic: data-analysis.\n"
        f"Analysis: {AS_OF_DATE.isoformat()} "
        "(not a fresh collection timestamp)."
    )

    if note:
        footer += "\n" + note

    fig.text(
        0.02, 0.015, footer,
        fontsize=8, color="#555555", va="bottom"
    )

    fig.tight_layout(rect=(0, 0.14, 1, 1))

    fig.savefig(
        CHART_DIR / filename,
        dpi=200,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close(fig)
    print(f"Chart saved: {filename}")
