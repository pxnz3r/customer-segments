# customer-segments

AI Lab coursework: customer segmentation with K-Means on income, spending score and purchasing behaviour, with a marketing reading of each segment.

## Layout

- `customer_segments/` this project's code: `data.py` (download and inputs), `segments.py` (segment names and actions), `report.py` (which outputs make up the results)
- `pxlab/` vendored copy of the shared engine (see `pxlab/VERSION`). Don't edit it here; it is replaced on the next sync.
- `main.py` runs the full study and rewrites `docs/results.md`; `app.py` is the Streamlit demo; `app_overview.md` the demo's Overview text
- `outputs/` figures and CSV tables, `models/` the fitted pipeline and segment names (both committed for the hosted app), `data/` the download (ignored)
- `docs/` methodology, results, deploy

## Commands

- Full study: `uv run python main.py`
- Demo: `uv run streamlit run app.py`
- Lint: `uv run ruff check . && uv run ruff format --check .`

## Conventions

- Beginner-student style on purpose: plain functions, docstrings on every function, comments explaining the AI concepts.
- Seed 42 everywhere.
- After changing the study, re-run `main.py` and refresh the README results and `app_overview.md`.
