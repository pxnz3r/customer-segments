"""
app.py - explore the customer segments. Run it with:

    streamlit run app.py

Tabs:
    Overview          what was done and found,
    Segments          re-run K-Means live with any k and inputs,
    Place a customer  which segment a new customer falls in, and what to do,
    Results           the saved tables and figures from main.py.
"""

import json
import os

import joblib
import pandas as pd
import streamlit as st

from customer_segments.data import ALL_INPUTS, BRIEF_INPUTS, DEALS, DESCRIPTIONS, INCOME, PURCHASES, SPENDING
from customer_segments.data import load_customers as download_customers
from customer_segments.report import FOLDER, results_sections
from customer_segments.segments import action_for, band_names, name_groups
from pxlab.app import setup_page, show_markdown_file, show_results_tabs
from pxlab.cluster.analysis import kmeans_pipeline, plot_groups_2d, profiles, relabel_by
from pxlab.common import MODELS_FOLDER, OUTPUTS_FOLDER


@st.cache_data(show_spinner="Downloading the customer data")
def load_customers():
    """
    The customer table, downloaded once per server.

    Returns:
        The DataFrame from customer_segments.data.
    """
    return download_customers()


@st.cache_resource
def load_model():
    """
    The pipeline saved by main.py and its group names.

    Returns:
        (pipeline, info dictionary).
    """
    pipeline = joblib.load(os.path.join(MODELS_FOLDER, "segments.joblib"))
    with open(os.path.join(MODELS_FOLDER, "segments.json")) as file:
        info = json.load(file)
    return pipeline, info


def show_segments_page():
    """
    The Segments tab: K-Means re-run live.

    Returns:
        Nothing.
    """
    customers = load_customers()
    left, right = st.columns(2)
    choice = left.radio(
        "Inputs",
        ["All four", "Income and spending score only"],
        horizontal=True,
        help="All four adds purchases and the share bought on discount.",
    )
    k = right.slider("Number of segments (k)", 2, 8, 4)
    inputs = ALL_INPUTS if choice == "All four" else BRIEF_INPUTS

    pipeline = kmeans_pipeline(k).fit(customers[inputs])
    labels = relabel_by(pipeline.predict(customers[inputs]), customers[SPENDING])
    names = name_groups(customers, labels) if inputs == ALL_INPUTS else band_names(k)
    st.pyplot(plot_groups_2d(customers, labels, INCOME, SPENDING, names, f"{k} segments"), width="stretch")

    table = profiles(customers, labels, inputs + ["Accepted an offer"], names)
    table = table.rename(columns={"Group": "Segment", "Accepted an offer": "Accepted an offer (share)"})
    st.dataframe(
        table,
        hide_index=True,
        width="stretch",
        column_config={
            INCOME: st.column_config.NumberColumn(format="%.0f"),
            SPENDING: st.column_config.NumberColumn(format="%.0f"),
            "Share": st.column_config.NumberColumn(format="percent"),
            "Accepted an offer (share)": st.column_config.NumberColumn(format="percent"),
        },
    )
    st.caption(
        "Offer acceptance was never shown to K-Means. Segments that differ in it are differences the "
        "grouping found on its own."
    )


def show_place_page():
    """
    The Place a customer tab.

    Returns:
        Nothing.
    """
    pipeline, info = load_model()
    left, right = st.columns(2)
    income = left.number_input(INCOME, 0, 200_000, 45_000, step=1_000, help=DESCRIPTIONS[INCOME])
    spending = right.slider(SPENDING, 1, 100, 40, help=DESCRIPTIONS[SPENDING])
    purchases = left.number_input(PURCHASES, 0, 40, 8, help=DESCRIPTIONS[PURCHASES])
    deals = right.slider(DEALS, 0.0, 1.0, 0.5, step=0.05, help=DESCRIPTIONS[DEALS])

    customer = pd.DataFrame([[income, spending, purchases, deals]], columns=info["inputs"])
    group = int(pipeline.predict(customer)[0])
    name = info["segments"][str(group)]
    st.subheader(name, anchor=False)
    st.markdown(action_for(name))

    path = os.path.join(OUTPUTS_FOLDER, FOLDER, "segments.csv")
    if os.path.isfile(path):
        segment = pd.read_csv(path).set_index("Segment").loc[name]
        st.caption(
            f"{segment['Customers']:,.0f} customers ({segment['Share']:.0%}) are in this segment. On average: "
            f"income {segment[INCOME]:,.0f}, spending score {segment[SPENDING]:.0f}, "
            f"{segment[PURCHASES]:.0f} purchases, {segment[DEALS]:.0%} on discount, and "
            f"{segment['Accepted an offer (share)']:.0%} accepted a marketing offer."
        )


def main():
    """
    Build the page.

    Returns:
        Nothing.
    """
    setup_page("Customer segments")
    overview, segments, place, results = st.tabs(["Overview", "Segments", "Place a customer", "Results"])
    with overview:
        show_markdown_file("app_overview.md")
    with segments:
        show_segments_page()
    with place:
        show_place_page()
    with results:
        show_results_tabs(results_sections())


main()
