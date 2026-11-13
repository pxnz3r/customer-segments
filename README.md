<div align="center">

<h1>Customer segments</h1>

<p>Customer segmentation with K-Means clustering on annual income, spending score and purchasing behaviour. 2,215 customers of a food and drink retailer fall into four segments, each with a marketing action, and the segments are checked against offer acceptance, which they never saw. An interactive demo re-runs the clustering live and places new customers.</p>

<p>
<a href="https://github.com/pxnz3r/customer-segments/actions/workflows/ci.yml"><img src="https://github.com/pxnz3r/customer-segments/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<img src="https://img.shields.io/badge/python-3.14-blue" alt="Python 3.14">
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="MIT license"></a>
</p>

<p><a href="docs/results.md">Results</a> · <a href="docs/methodology.md">Methodology</a> · <a href="docs/deploy.md">Deploy the demo</a></p>

<img src="outputs/figures/segments/segments_income_spending.png" width="720" alt="Four segments by income and spending score">

</div>

## How it works

1. **Load and check** 2,215 customers of a food and drink retailer.
2. **Choose k** with the elbow and silhouette scores, then group the customers with K-Means.
3. **Describe each segment** and give it a marketing action.
4. **Validate the groups**: three internal indices, a silhouette diagram, bootstrap stability and a comparison with shuffled data that has no real groups.
5. **Place a new customer** in a segment in the Streamlit demo.

## Results

| Segment | Customers | Income | Spending score | Purchases | Deal share | Accepted an offer | Suggested action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Big spenders | 759 (34%) | 74,700 | 82 | 20 | 8% | 24% | Loyalty perks, premium ranges, full price |
| Regulars | 500 (23%) | 53,100 | 55 | 14 | 22% | 10% | Cross-sell and bundles |
| Bargain hunters | 365 (16%) | 34,500 | 31 | 8 | 53% | 18% | Discount campaigns |
| Light buyers | 591 (27%) | 32,600 | 18 | 5 | 28% | 6% | Cheap channels only |

- **k = 4** is the most stable choice: 10 K-Means runs from different random starts agree at 0.97 (adjusted Rand index), against 0.88 for k = 3 and 0.71 for k = 5. k = 2 has the best silhouette (0.53) but only separates big from small spenders.
- **Offer acceptance**, never an input, ranges from 6% to 24% across segments, so the segments capture real differences in behaviour.
- **Income and spending score alone** (the classic two-input version) give four bands along one diagonal, because the two rise together. Bargain hunters disappear into the two lowest bands; the two groupings agree at only 0.41.

Full tables and figures: [docs/results.md](docs/results.md). How it was done: [docs/methodology.md](docs/methodology.md).

## How sure the results are

**The four segments are real.** Silhouette 0.350 on the real customers against 0.195 on the same data with each column shuffled, which has no true groups.

**They are stable.** Re-running K-Means on 50 bootstrap samples recovers every segment with a mean Jaccard of 0.93 or more (Big spenders 0.97).

**k = 4 is a business choice.** All three internal indices prefer k = 2; four segments are kept because each gets its own marketing action.

Every table and figure behind these is in [docs/results.md](docs/results.md).

## Run it

Needs Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python main.py
uv run streamlit run app.py
```

`main.py` downloads the data from OpenML on its first run, then writes figures and tables to `outputs/`, the fitted pipeline to `models/` and `docs/results.md`.

## The demo

- **Overview**: the method and what was found.
- **Segments**: pick k and the inputs; K-Means re-runs live with a scatter plot and segment profiles.
- **Place a customer**: enter income, spending score, purchases and deal share; see the segment and the action for it.
- **Results**: the saved tables and figures.

## Layout

```
customer_segments/   data.py (download, inputs), segments.py (names and actions), report.py
pxlab/               shared engine (vendored): clustering, plots, app helpers
main.py              the full study
app.py               the Streamlit demo
docs/                methodology, results, deploy
```

## Data

"Marketing Campaign" by Rodolfo Saldanha ([Kaggle](https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign), 2020), downloaded from [OpenML dataset 46940](https://www.openml.org/d/46940), listed there as public. The data isn't stored in this repo.

## License

MIT.
