"""
report.py - which saved tables and figures make up the results. The app's
Results tab and docs/results.md both read this list, so they always match.
"""

FOLDER = "segments"


def results_sections():
    """
    The results, grouped into sections.

    Returns:
        A list of (section name, items) for pxlab's show_results_tabs() and
        write_results_doc().
    """
    return [
        (
            "Segments",
            [
                ("figure", f"{FOLDER}/segments_income_spending.png"),
                ("table", "Segments and what to do with each", f"{FOLDER}/segments.csv"),
                ("figure", f"{FOLDER}/segment_profiles.png"),
                ("figure", f"{FOLDER}/segments_pca.png"),
            ],
        ),
        (
            "Choosing k",
            [
                ("figure", f"{FOLDER}/k_sweep_all.png"),
                ("table", "Four inputs: score for each k", f"{FOLDER}/k_sweep_all.csv"),
                ("table", "Income and spending score only: score for each k", f"{FOLDER}/k_sweep_brief.csv"),
            ],
        ),
        (
            "Income and spending only",
            [
                ("figure", f"{FOLDER}/brief_income_spending.png"),
                ("table", "Groups from income and spending score alone", f"{FOLDER}/brief_segments.csv"),
                ("table", "How the two groupings compare", f"{FOLDER}/comparison.csv"),
            ],
        ),
    ]
