# Methodology

## Question

Can customers be split, without labels, into groups that a marketing team would treat differently? What does each group look like, and do the groups differ in something they weren't built from?

## Data

2,240 customers of a food and drink retailer ("Marketing Campaign", OpenML 46940). 24 customers without a recorded income are dropped, and one with an income of 666,666 (a placeholder, not a real figure), leaving 2,215.

| Input | Built from |
| --- | --- |
| Annual income | household income as recorded |
| Spending score | total spent on wine, fruit, meat, fish, sweets and gold in two years, ranked 1 (lowest) to 100 (highest) |
| Purchases | web + catalogue + store purchases in two years |
| Deal share | purchases made with a discount / purchases (0 for the 6 customers with no purchases) |

The brief names income and spending score; purchases and deal share describe purchasing behaviour. Whether the customer accepted any of six marketing offers is kept aside and used only to check the segments.

## K-Means

Every input is standardised (mean 0, standard deviation 1) so income in thousands doesn't outweigh a 0 to 1 share. K-Means then:

1. places k centres,
2. gives every customer to the nearest centre,
3. moves each centre to the mean of its customers,
4. repeats 2 and 3 until nothing changes.

The result depends on the starting centres, so it runs from 20 random starts (seed 42) and keeps the tightest result. Groups are renumbered from lowest to highest average spending score so the numbering is stable.

## Choosing k

| Measure | What it says |
| --- | --- |
| Inertia | total squared distance from each customer to its centre; always falls as k grows, look for the elbow |
| Silhouette | how much closer each customer is to its own group than to the next (−1 to 1) |
| Stability | agreement (adjusted Rand index) between 10 single-start runs with different seeds; 1 means identical groups |

Silhouette is highest at k = 2 for both input sets, but two groups only separate big from small spenders. k is chosen from 3 to 6 by stability: k = 4 scores 0.97 with four inputs (lowest pair 0.955), well above k = 3 (0.88), 5 (0.71) and 6 (0.76).

## Naming and actions

Each group is named from its averages with fixed rules: spending score of 70 or more is "Big spenders", 45 or more "Regulars", below that "Bargain hunters" if at least 40% of purchases use a discount, otherwise "Light buyers". Each name carries one marketing action (see the README).

## Checks

1. **Offer acceptance per segment**, which K-Means never saw.
2. **Income and spending score alone**: the same procedure on the brief's two inputs, compared with the four-input segments by a cross-table and the adjusted Rand index.

## Limits

- K-Means assumes round groups of similar size; customers don't form clean clusters here (the silhouette at k = 4 is 0.35), so segments are a useful partition of a continuum more than natural types.
- The data is from one retailer and its currency units aren't stated.
- Suggested actions follow from the profiles; they haven't been tested with a campaign.
