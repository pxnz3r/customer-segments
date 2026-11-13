"""
data.py - load the customer data and build the inputs for segmentation.

The data is the "Marketing Campaign" table: 2,240 customers of a food and
drink retailer, with household income, two years of spending per product
type, and how many purchases they made through each channel. main.py
downloads it from OpenML the first time.
"""

import pandas as pd
from sklearn.datasets import fetch_openml

from pxlab.common import DATA_FOLDER

OPENML_ID = 46940

SPENDING_COLUMNS = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
]
CAMPAIGN_COLUMNS = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5", "Response"]

# The inputs. The brief names income and spending score; purchases and the
# share bought on discount describe purchasing behaviour.
INCOME = "Annual income"
SPENDING = "Spending score"
PURCHASES = "Purchases"
DEALS = "Deal share"
BRIEF_INPUTS = [INCOME, SPENDING]
ALL_INPUTS = [INCOME, SPENDING, PURCHASES, DEALS]

DESCRIPTIONS = {
    INCOME: "Yearly household income, in currency units.",
    SPENDING: "Total spent in the last two years, as a rank from 1 (least of all customers) to 100 (most).",
    PURCHASES: "Purchases in the last two years: web, catalogue and store together.",
    DEALS: "Share of purchases made with a discount, from 0 to 1.",
}


def load_customers():
    """
    Download (once) and clean the customer table.

    Customers with no income recorded (24) are dropped, and so is one with
    an income of 666,666, almost certainly a typing placeholder.

    Returns:
        A DataFrame with the four inputs, the raw total spent, and whether
        the customer accepted any of the six marketing offers (used only to
        check the segments afterwards, never to build them).
    """
    raw = fetch_openml(data_id=OPENML_ID, as_frame=True, data_home=DATA_FOLDER, parser="liac-arff").frame
    raw = raw[raw["Income"].notna() & (raw["Income"] < 600_000)].reset_index(drop=True)

    customers = pd.DataFrame()
    customers[INCOME] = raw["Income"].astype(float)
    total_spent = raw[SPENDING_COLUMNS].sum(axis=1)
    # A percentile rank: 1 for the lowest spender, 100 for the highest.
    customers[SPENDING] = (total_spent.rank(pct=True) * 99 + 1).round().astype(int)
    purchases = raw[["NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases"]].sum(axis=1)
    customers[PURCHASES] = purchases
    customers[DEALS] = (raw["NumDealsPurchases"] / purchases.where(purchases > 0)).fillna(0).clip(upper=1).round(3)
    customers["Total spent"] = total_spent
    accepted = (raw[CAMPAIGN_COLUMNS].astype(str) == "Yes").sum(axis=1)  # stored as "Yes" / "No"
    customers["Accepted an offer"] = accepted > 0
    return customers
