"""
main.py - run the whole customer segmentation with one command:

    python main.py

It:
    1. loads 2,215 customers and builds the inputs: annual income, spending
       score, purchases and the share bought on discount,
    2. tries k = 2 to 8 groups with K-Means and picks k,
    3. names each segment, describes it and suggests a marketing action,
    4. checks the segments against something they never saw: how often
       each one accepted a marketing offer,
    5. repeats the grouping on income and spending score alone (the two
       inputs the brief names) and compares,
    6. saves the fitted pipeline for the app and writes docs/results.md.
Figures and tables go to outputs/segments/.
"""

import json
import os

import joblib
import pandas as pd

from customer_segments.data import ALL_INPUTS, BRIEF_INPUTS, INCOME, SPENDING, load_customers
from customer_segments.report import FOLDER, results_sections
from customer_segments.segments import action_for, band_names, name_groups
from pxlab.cluster.analysis import (
    agreement,
    choose_k_by_stability,
    k_sweep,
    kmeans_pipeline,
    plot_groups_2d,
    plot_groups_pca,
    plot_k_sweep,
    plot_profile_heatmap,
    profiles,
    relabel_by,
    scale,
)
from pxlab.cluster.validate import run_validation
from pxlab.common import MODELS_FOLDER, save_figure, save_table, set_plot_style, write_results_doc

K_VALUES = range(2, 9)
# k = 2 always scores best on silhouette here, but it only splits customers
# into "spends more" and "spends less", which gives marketing nothing new.
# So k is picked from 3 to 6 by stability: the k whose groups come out the
# same whatever the random starting centres.
K_CHOICES = range(3, 7)


def renumbering(pipeline, customers, inputs):
    """
    How K-Means' own group numbers map to the renumbered ones (ordered by
    spending score), so a new customer's group can be named.

    Inputs:
        pipeline: the fitted pipeline.
        customers: the customer table.
        inputs: the input columns.
    Returns:
        Dictionary K-Means number -> renumbered group.
    """
    raw = pipeline.predict(customers[inputs])
    new = relabel_by(raw, customers[SPENDING])
    return {int(r): int(n) for r, n in set(zip(raw, new))}


def segment(customers, inputs, label):
    """
    Sweep k, choose it, fit K-Means and name the groups.

    Inputs:
        customers: the customer table.
        inputs: the input columns.
        label: "all" or "brief", used in file names.
    Returns:
        (fitted pipeline, labels, names, k).
    """
    features = scale(customers, inputs)
    sweep = k_sweep(features, K_VALUES)
    k, stable = choose_k_by_stability(features, K_CHOICES)
    sweep = sweep.merge(stable, on="k", how="left").round(3)
    save_table(sweep, f"{FOLDER}/k_sweep_{label}.csv")
    if label == "all":
        save_figure(
            plot_k_sweep(sweep, k, f"Choosing k with four inputs (k = {k} chosen)"), f"{FOLDER}/k_sweep_all.png"
        )

    pipeline = kmeans_pipeline(k).fit(customers[inputs])
    labels = relabel_by(pipeline.predict(customers[inputs]), customers[SPENDING])
    names = name_groups(customers, labels) if label == "all" else band_names(k)
    print(f"  {label}: k = {k}, " + ", ".join(names.values()))
    return pipeline, labels, names, k


def segment_table(customers, labels, names, inputs):
    """
    One row per segment: size, averages, offer acceptance and an action.

    Inputs:
        customers: the customer table.
        labels: the segment of each customer.
        names: dictionary segment number -> name.
        inputs: the input columns.
    Returns:
        The table.
    """
    table = profiles(customers, labels, inputs + ["Total spent", "Accepted an offer"], names)
    table = table.rename(columns={"Accepted an offer": "Accepted an offer (share)"})
    table[INCOME] = table[INCOME].round(-2)
    table = table.round(2)
    table["Suggested action"] = [action_for(name) for name in table["Group"]]
    return table.rename(columns={"Group": "Segment"})


def main():
    """
    The full study.

    Returns:
        Nothing.
    """
    set_plot_style()
    customers = load_customers()
    print(f"Customers: {len(customers)}")

    pipeline, labels, names, k = segment(customers, ALL_INPUTS, "all")
    table = segment_table(customers, labels, names, ALL_INPUTS)
    save_table(table, f"{FOLDER}/segments.csv")
    save_figure(
        plot_groups_2d(customers, labels, INCOME, SPENDING, names, f"{k} segments from four inputs"),
        f"{FOLDER}/segments_income_spending.png",
    )
    save_figure(
        plot_profile_heatmap(
            customers, labels, ALL_INPUTS, names, "How each segment differs from the average customer"
        ),
        f"{FOLDER}/segment_profiles.png",
    )
    save_figure(
        plot_groups_pca(scale(customers, ALL_INPUTS), labels, names, "Segments on the two main directions of spread"),
        f"{FOLDER}/segments_pca.png",
    )

    print("Validation:")
    run_validation(scale(customers, ALL_INPUTS), labels, names, k, K_VALUES, FOLDER)

    brief_pipeline, brief_labels, brief_names, brief_k = segment(customers, BRIEF_INPUTS, "brief")
    brief_table = segment_table(customers, brief_labels, brief_names, BRIEF_INPUTS).drop(columns="Suggested action")
    save_table(brief_table, f"{FOLDER}/brief_segments.csv")
    # K-Means centres are in scaled units and in K-Means' own numbering:
    # turn them back into income and score, in the renumbered order.
    raw_to_new = renumbering(brief_pipeline, customers, BRIEF_INPUTS)
    centres = brief_pipeline[0].inverse_transform(brief_pipeline[-1].cluster_centers_)
    centres = centres[[raw for new in range(brief_k) for raw, n in raw_to_new.items() if n == new]]
    figure = plot_groups_2d(
        customers,
        brief_labels,
        INCOME,
        SPENDING,
        brief_names,
        f"{brief_k} groups from income and spending score",
        centres,
    )
    save_figure(figure, f"{FOLDER}/brief_income_spending.png")
    comparison = pd.crosstab(
        pd.Series([names[g] for g in labels], name="Four inputs"),
        pd.Series([brief_names[g] for g in brief_labels], name="Income and spending only"),
    ).loc[list(names.values()), list(brief_names.values())]
    print(f"  agreement between the two groupings (adjusted Rand): {agreement(labels, brief_labels):.3f}")
    save_table(comparison.reset_index(), f"{FOLDER}/comparison.csv")

    os.makedirs(MODELS_FOLDER, exist_ok=True)
    joblib.dump(pipeline, os.path.join(MODELS_FOLDER, "segments.joblib"))
    raw_to_named = {raw: names[new] for raw, new in renumbering(pipeline, customers, ALL_INPUTS).items()}
    info = {"inputs": ALL_INPUTS, "k": k, "segments": raw_to_named, "customers": len(customers)}
    with open(os.path.join(MODELS_FOLDER, "segments.json"), "w") as file:
        json.dump(info, file, indent=2)

    write_results_doc(
        "Results",
        f"Produced by `python main.py` on {len(customers):,} customers. K-Means with 20 random starts, seed 42.",
        results_sections(),
    )
    print("  Done. Run: streamlit run app.py")


if __name__ == "__main__":
    main()
