### What this is

Customer segmentation with **K-Means clustering**: 2,215 customers of a food and drink retailer are split into groups that behave alike, so marketing can treat each group differently. Clustering is unsupervised: nobody labelled the customers, the algorithm finds the groups from the data.

Four inputs, standardised so each counts equally:

- **Annual income** of the household.
- **Spending score**: total spent in two years, as a rank from 1 to 100.
- **Purchases**: web, catalogue and store purchases in two years.
- **Deal share**: the share of purchases made with a discount.

### What to try

- **Segments**: re-run K-Means with any number of groups, with all four inputs or income and spending score alone.
- **Place a customer**: enter a customer and see their segment and the suggested action.
- **Results**: how k was chosen, each segment's profile, and the comparison with two inputs.

### What was found

| Segment | Customers | Income | Spending score | Deal share | Accepted an offer | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Big spenders | 34% | 74,700 | 82 | 8% | 24% | Loyalty perks and premium ranges at full price |
| Regulars | 23% | 53,100 | 55 | 22% | 10% | Cross-sell and bundles |
| Bargain hunters | 16% | 34,500 | 31 | 53% | 18% | Discount campaigns |
| Light buyers | 27% | 32,600 | 18 | 28% | 6% | Cheap channels only |

- **k = 4** was chosen because its groups come out the same whatever K-Means' random start (agreement 0.97 across 10 seeds; 0.71 for k = 5). k = 2 scores best on silhouette but only splits big from small spenders.
- **The segments predict something they never saw.** Offer acceptance wasn't an input, yet it ranges from 6% (light buyers) to 24% (big spenders).
- **Purchasing behaviour finds a segment income and spending can't.** Bargain hunters earn and spend about the same as light buyers, but accept offers three times as often. With income and spending score alone, they are split across the two lowest groups.

Code and every figure: [github.com/pxnz3r/customer-segments](https://github.com/pxnz3r/customer-segments).
