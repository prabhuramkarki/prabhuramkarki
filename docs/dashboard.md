# Public profile dashboard

The dashboard is a dated snapshot of public GitHub data. Its source is [assets/dashboard/data.json](../assets/dashboard/data.json); the SVGs are rendered locally and committed alongside that snapshot. The README does not depend on a live statistics image service.

## What the numbers mean

| Measure | Definition |
| --- | --- |
| Public repositories | Repositories currently public and owned by `prabhuramkarki`, including forks. Compared against the public user endpoint before and after collection. |
| Original repositories | Those same repositories with `fork=false`. |
| Stars | Current stargazer counts summed across all public owned repositories, including forks. |
| Featured projects | Four verified public repositories: `easy-invoice`, `code-shell-rs`, `native-windows-application-runtime-on-linux`, and `manducart-v2`. Their current URLs and default branches are recorded in the JSON. |
| Languages | GitHub language bytes summed across public owned original repositories. The profile repository is excluded so generated dashboard SVGs do not inflate the result. This measures repository contents, not proficiency, effort, or lines written. |
| Public events | Returned public events in currently public owned repositories during 30 inclusive UTC calendar dates ending on the snapshot date. This is an event count, not commits or GitHub contributions. One push event can contain multiple commits. |
| Creation timeline | Counts of currently public owned original repositories grouped by creation year, including this profile repository. Forks, deleted repositories, and currently private repositories are excluded. This is not a count of shipped products. |

The [GitHub Events API](https://docs.github.com/en/rest/activity/events) retains up to 30 days and returns at most 300 events; events can arrive late. The collector reads up to three pages of 100 events. `activity.events_returned` records the raw feed size; `activity.events_count` counts only qualifying public events in currently public owned repositories within the chart window. `activity.limited=true` means it reached 300 returned events. A false flag does not guarantee a complete historical record. A daily count of zero means **no returned events**, not proof of no activity. The same limitations apply when daily observations are grouped for a chart.

The combined console shows the four KPIs, daily event counts, and the five largest language byte totals plus “Other”. Its event plot uses bars and a straight-segment area line through the returned daily values; no interpolated or synthetic counts are introduced. The detailed desktop activity chart uses daily bars with a numeric scale. The phone variant groups consecutive dates into seven-day intervals, starting on `window_start`; the final interval may contain fewer days. All 30 dates are represented once. Language charts show the five largest byte totals and combine remaining languages as “Other”; exact byte totals remain available in the JSON. Desktop and phone chart variants are generated from the same snapshot in the same refresh.

## Refreshing

The [workflow](../.github/workflows/update-profile.yml) runs Mondays at 06:00 UTC and supports **Actions → Refresh public profile dashboard → Run workflow** on `main`. GitHub may delay scheduled runs. The snapshot date reflects the last successful refresh.

For a local refresh, use Python 3.10 or newer, with no extra packages:

```sh
python3 scripts/test_update_stats.py
python3 scripts/update_stats.py
```

The collector uses `GITHUB_TOKEN` when provided, otherwise it tries the existing `gh auth token` login without printing the token. Anonymous collection is also supported, subject to GitHub rate limits. A token only needs access to public data; never add a personal token to the repository. `--data-only` refreshes only the JSON; `--output-dir PATH` writes to an alternate directory.

All network requests finish and all rendered SVGs pass XML validation before files are staged for replacement. HTTP failures, rate limits, inconsistent repository pages, missing featured repositories, or rendering failures stop the refresh and preserve existing assets. Each destination is replaced atomically; an interrupted replacement rolls prior replacements back when the filesystem remains writable. The workflow commits only `assets/dashboard`, skips unchanged snapshots, and uses an ordinary push. A concurrent change to `main` causes the push to fail safely; rerun the workflow after checking the branch. Branch protection may require publishing the generated changes through a pull request instead.

The workflow uses the repository's built-in token with `contents: write` only in its refresh job; all other default permissions are empty. It does not run on pull requests, request private endpoints, publish event payloads, or store credentials. The snapshot contains only repository metadata, aggregate language bytes, and daily event counts.
