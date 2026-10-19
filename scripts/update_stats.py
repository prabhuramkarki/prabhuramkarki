#!/usr/bin/env python3
"""Refresh the profile dashboard from GitHub's public REST endpoints."""

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


USER = "prabhuramkarki"
FEATURED = (
    "easy-invoice", "code-shell-rs",
    "native-windows-application-runtime-on-linux", "manducart-v2",
)
ROOT = Path(__file__).resolve().parents[1]


def github_token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    try:
        result = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, timeout=10,
            check=False,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


class GitHub:
    def __init__(self, token=None):
        self.token = token

    def get(self, path):
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "prabhuramkarki-profile-dashboard",
        }
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        try:
            with urlopen(Request("https://api.github.com" + path, headers=headers), timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            raise ValueError(f"GitHub returned HTTP {error.code}; existing assets were kept. Retry later or check token permissions.") from None
        except (URLError, TimeoutError, json.JSONDecodeError):
            raise ValueError("GitHub request failed or returned invalid JSON; existing assets were kept.") from None


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("GitHub returned an invalid timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("GitHub returned a timestamp without a timezone")
    return parsed.astimezone(timezone.utc)


def integer(value):
    if type(value) is not int or value < 0:
        raise ValueError("GitHub returned an invalid count")
    return value


def profile_count(api):
    profile = api.get(f"/users/{USER}")
    if not isinstance(profile, dict) or not isinstance(profile.get("login"), str) or profile["login"].lower() != USER:
        raise ValueError("GitHub returned an unexpected user")
    return integer(profile.get("public_repos"))


def collect(api, today=None):
    today = today or datetime.now(timezone.utc).date()
    expected_count = profile_count(api)
    repositories = []
    seen = set()
    page = 1
    while True:
        batch = api.get(f"/users/{USER}/repos?per_page=100&type=owner&sort=full_name&page={page}")
        if not isinstance(batch, list) or len(batch) > 100:
            raise ValueError("GitHub returned an invalid repository page")
        for repo in batch:
            if not isinstance(repo, dict) or repo.get("private") is not False:
                raise ValueError("Repository collection contains unverified or private data")
            owner = repo.get("owner")
            if not isinstance(owner, dict) or not isinstance(owner.get("login"), str) or owner["login"].lower() != USER:
                raise ValueError("Repository collection contains another owner's repository")
            name = repo.get("name")
            if not isinstance(name, str) or not name or "/" in name or name in seen:
                raise ValueError("Repository collection is incomplete or contains duplicates")
            seen.add(name)
            url = f"https://github.com/{USER}/{name}"
            if repo.get("html_url") != url or type(repo.get("fork")) is not bool:
                raise ValueError("GitHub returned invalid repository metadata")
            if not isinstance(repo.get("default_branch"), str) or not repo["default_branch"]:
                raise ValueError("GitHub returned an invalid default branch")
            timestamp(repo.get("created_at"))
            if repo.get("pushed_at") is not None:
                timestamp(repo["pushed_at"])
            repositories.append({
                "name": name, "url": url, "default_branch": repo["default_branch"],
                "created_at": repo["created_at"], "pushed_at": repo.get("pushed_at"),
                "stars": integer(repo.get("stargazers_count")), "fork": repo["fork"],
            })
        if len(batch) < 100:
            break
        page += 1
        if len(repositories) > expected_count:
            raise ValueError("Repository count changed during collection")
    if len(repositories) != expected_count or profile_count(api) != expected_count:
        raise ValueError("Public repository count changed or collection is incomplete")
    if not set(FEATURED).issubset(seen):
        raise ValueError("A featured repository is no longer verified public")

    languages = Counter()
    for repo in repositories:
        if repo["fork"] or repo["name"] == USER:
            continue
        batch = api.get(f"/repos/{USER}/{quote(repo['name'], safe='')}/languages")
        if not isinstance(batch, dict):
            raise ValueError("GitHub returned invalid language data")
        for language, size in batch.items():
            if not isinstance(language, str) or not language:
                raise ValueError("GitHub returned an invalid language name")
            languages[language] += integer(size)

    start = today - timedelta(days=29)
    days = Counter()
    event_ids = set()
    returned = 0
    limited = False
    owned_repos = {f"{USER}/{name}" for name in seen}
    for page in range(1, 4):
        batch = api.get(f"/users/{USER}/events/public?per_page=100&page={page}")
        if not isinstance(batch, list) or len(batch) > 100:
            raise ValueError("GitHub returned an invalid public event page")
        returned += len(batch)
        for event in batch:
            if not isinstance(event, dict) or not isinstance(event.get("id"), str):
                raise ValueError("GitHub returned an invalid public event")
            if event["id"] in event_ids:
                raise ValueError("Public event pages changed during collection; retry later")
            event_ids.add(event["id"])
            if event.get("public") is not True:
                continue
            if not isinstance(event.get("repo"), dict) or not isinstance(event["repo"].get("name"), str):
                raise ValueError("GitHub returned invalid public event repository metadata")
            event_repo = event["repo"]["name"]
            if event_repo not in owned_repos:
                continue
            event_day = timestamp(event.get("created_at")).date()
            if start <= event_day <= today:
                days[event_day] += 1
        if len(batch) < 100:
            break
        limited = page == 3

    return {
        "schema_version": 1, "updated_at": today.isoformat(), "user": USER,
        "metrics": {
            "public_repos": len(repositories),
            "total_stars": sum(repo["stars"] for repo in repositories),
            "original_repos": sum(not repo["fork"] for repo in repositories),
            "featured_projects": len(FEATURED),
        },
        "repositories": sorted(repositories, key=lambda repo: repo["name"].lower()),
        "languages": [{"name": name, "bytes": size} for name, size in sorted(languages.items(), key=lambda item: (-item[1], item[0])) if size],
        "activity": {
            "window_start": start.isoformat(), "window_end": today.isoformat(),
            "events_returned": returned, "events_count": sum(days.values()), "limited": limited,
            "days": [{"date": (start + timedelta(days=offset)).isoformat(), "count": days[start + timedelta(days=offset)]} for offset in range(30)],
        },
        "definitions": {
            "repositories": "Currently public repositories owned by prabhuramkarki; includes forks. Originals excludes forks.",
            "stars": "Sum of current stargazer counts across all currently public owned repositories, including forks.",
            "languages": "GitHub language bytes summed across currently public owned non-fork repositories, excluding the profile repository. Bytes describe repository contents, not skill or effort.",
            "activity": "Returned public GitHub events in currently public owned repositories over 30 inclusive UTC dates. Events are not commits or contributions; one push can contain multiple commits. Zero means no returned events, not proof of no activity.",
            "coverage": "GitHub's public event feed is limited to the latest 300 events and the last 30 days; it can be delayed. limited=true means the 300-event ceiling was reached. Counts may be incomplete even when limited=false.",
            "timeline": "Creation dates of currently public owned non-fork repositories; not a historical account of all repositories ever created.",
            "featured": ", ".join(FEATURED),
        },
    }


def write_dashboard(data, output_dir, data_only=False):
    artifacts = {"data.json": json.dumps(data, indent=2, ensure_ascii=False) + "\n"}
    if not data_only:
        from render_assets import render_dashboard
        rendered = render_dashboard(data)
        if not isinstance(rendered, dict) or not rendered:
            raise ValueError("Renderer did not produce dashboard SVGs")
        for name, content in rendered.items():
            path = Path(name)
            if path.is_absolute() or len(path.parts) != 1 or path.suffix != ".svg":
                raise ValueError("Renderer returned an unsafe artifact path")
            root = ET.fromstring(content)
            if root.tag != "{http://www.w3.org/2000/svg}svg":
                raise ValueError("Renderer returned an invalid SVG")
            artifacts[name] = content
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pending = []
    backups = []
    replaced = []
    try:
        for name, content in artifacts.items():
            destination = output_dir / name
            backup = None
            if destination.exists():
                with tempfile.NamedTemporaryFile(dir=output_dir, delete=False) as handle:
                    backup = Path(handle.name)
                    backups.append(backup)
                    handle.write(destination.read_bytes())
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output_dir, delete=False) as handle:
                pending.append((Path(handle.name), destination, backup))
                handle.write(content)
        for temporary, destination, backup in pending:
            os.replace(temporary, destination)
            replaced.append((destination, backup))
    except OSError:
        for destination, backup in reversed(replaced):
            if backup is None:
                destination.unlink(missing_ok=True)
            else:
                os.replace(backup, destination)
        raise
    finally:
        for temporary, _, _ in pending:
            temporary.unlink(missing_ok=True)
        for backup in backups:
            backup.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets" / "dashboard")
    parser.add_argument("--data-only", action="store_true", help="Refresh JSON without rendering SVGs")
    args = parser.parse_args()
    try:
        data = collect(GitHub(github_token()))
        write_dashboard(data, args.output_dir, args.data_only)
    except (ValueError, OSError, ET.ParseError, ImportError) as error:
        print(f"Dashboard refresh failed: {error}", file=sys.stderr)
        return 1
    print(f"Updated public dashboard for {USER}: {data['metrics']['public_repos']} repositories, {len(data['languages'])} languages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
