"""
segments.py - turn K-Means groups into named segments a marketing team can
act on.

K-Means only returns group numbers. A name comes from reading each group's
averages: how much it spends, and how much of its buying waits for a
discount. The rules below are written once from those averages, so the
same customers always get the same name.
"""

from customer_segments.data import DEALS, SPENDING

BIG_SPENDERS = "Big spenders"
REGULARS = "Regulars"
BARGAIN_HUNTERS = "Bargain hunters"
LIGHT_BUYERS = "Light buyers"

ACTIONS = {
    BIG_SPENDERS: "Loyalty perks, premium ranges and early access at full price. They rarely wait for discounts, so "
    "discounting them gives margin away.",
    REGULARS: "Cross-sell and bundles to grow the basket: they already buy often but in mid-sized amounts.",
    BARGAIN_HUNTERS: "Discount and deal campaigns. Half their purchases use one, and they accept offers far more "
    "often than other low spenders.",
    LIGHT_BUYERS: "Cheap channels only (email, web). They buy little and rarely respond, so costly campaigns "
    "such as printed catalogues don't pay back.",
    "Other": "No action rule for this group.",
}


def segment_name(spending_score, deal_share):
    """
    Name a group from its average spending score and deal share.

    Inputs:
        spending_score: the group's average spending score (1 to 100).
        deal_share: the group's average share of purchases on discount.
    Returns:
        One of the segment names.
    """
    if spending_score >= 70:
        return BIG_SPENDERS
    if spending_score >= 45:
        return REGULARS
    if deal_share >= 0.4:
        return BARGAIN_HUNTERS
    return LIGHT_BUYERS


def name_groups(customers, labels):
    """
    A name for every group number. If two groups would get the same name,
    the later ones are numbered ("Regulars 2") so names stay unique.

    Inputs:
        customers: the customer table.
        labels: the group of each customer.
    Returns:
        Dictionary group number -> name.
    """
    means = customers[[SPENDING, DEALS]].groupby(labels).mean()
    names = {}
    for group, row in means.iterrows():
        name = segment_name(row[SPENDING], row[DEALS])
        count = list(names.values()).count(name) + sum(value.startswith(name + " ") for value in names.values())
        names[int(group)] = name if count == 0 else f"{name} {count + 1}"
    return names


def action_for(name):
    """
    The marketing action for a segment name ("Regulars 2" uses Regulars).

    Input:
        name: a segment name from name_groups().
    Returns:
        The suggested action.
    """
    for base in ACTIONS:
        if name == base or name.startswith(base + " "):
            return ACTIONS[base]
    return ACTIONS["Other"]


def band_names(k):
    """
    Names for groups made from income and spending score alone, where the
    groups sit along one line from low to high (the two inputs rise
    together). Groups must already be numbered from lowest spending up.

    Input:
        k: the number of groups.
    Returns:
        Dictionary group number -> name.
    """
    if k == 4:
        return {0: "Low", 1: "Lower middle", 2: "Upper middle", 3: "High"}
    if k == 3:
        return {0: "Low", 1: "Middle", 2: "High"}
    return {group: f"Band {group + 1} of {k}" for group in range(k)}
