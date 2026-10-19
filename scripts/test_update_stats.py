#!/usr/bin/env python3
"""Offline checks for public-only collection and safe dashboard refreshes."""

from datetime import date
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import update_stats as stats


def repository(name, fork=False, stars=0):
    return {
        "name": name, "private": False, "owner": {"login": stats.USER},
        "html_url": f"https://github.com/{stats.USER}/{name}",
        "default_branch": "main", "fork": fork, "stargazers_count": stars,
        "created_at": "2025-01-01T00:00:00Z", "pushed_at": "2026-10-01T00:00:00Z",
    }


class FakeAPI:
    def __init__(self):
        self.repos = [repository(name) for name in stats.FEATURED]
        self.repos += [repository(stats.USER), repository("fork", fork=True, stars=3)]
        self.languages = {"Rust": 8, "Python": 2}
        self.events = []
        self.calls = []

    def get(self, path):
        self.calls.append(path)
        if path == f"/users/{stats.USER}":
            return {"login": stats.USER, "public_repos": len(self.repos)}
        if "/repos?" in path:
            page = int(path.rsplit("=", 1)[1])
            return self.repos[(page - 1) * 100:page * 100]
        if path.endswith("/languages"):
            return self.languages
        if "/events/public?" in path:
            page = int(path.rsplit("=", 1)[1])
            return self.events[(page - 1) * 100:page * 100]
        raise AssertionError(f"Unexpected API request: {path}")


def event(number, repo="easy-invoice", public=True, created="2026-10-19T00:00:00Z"):
    return {"id": str(number), "public": public, "repo": {"name": f"{stats.USER}/{repo}"}, "created_at": created}


class DashboardTests(unittest.TestCase):
    def test_paginated_public_repositories_and_language_totals(self):
        api = FakeAPI()
        api.repos.extend(repository(f"repo-{number}") for number in range(99))
        data = stats.collect(api, date(2026, 10, 19))
        self.assertEqual(data["metrics"], {"public_repos": 105, "original_repos": 104, "total_stars": 3, "featured_projects": 4})
        self.assertEqual(data["languages"], [{"name": "Rust", "bytes": 824}, {"name": "Python", "bytes": 206}])
        self.assertTrue(any("repos?" in path and "page=2" in path for path in api.calls))
        self.assertFalse(any(f"/{stats.USER}/languages" in path or "/fork/languages" in path for path in api.calls))

    def test_events_only_count_returned_public_owned_events_in_window(self):
        api = FakeAPI()
        api.events = [event(1), event(2, public=False), event(3, repo="unknown"), event(4, created="2026-09-19T23:59:59Z")]
        data = stats.collect(api, date(2026, 10, 19))
        self.assertEqual(data["activity"]["window_start"], "2026-09-20")
        self.assertEqual(len(data["activity"]["days"]), 30)
        self.assertEqual(sum(day["count"] for day in data["activity"]["days"]), 1)
        self.assertEqual(data["activity"]["events_returned"], 4)
        self.assertEqual(data["activity"]["events_count"], 1)
        self.assertFalse(data["activity"]["limited"])

    def test_event_ceiling_is_explicit(self):
        api = FakeAPI()
        api.events = [event(number) for number in range(300)]
        data = stats.collect(api, date(2026, 10, 19))
        self.assertTrue(data["activity"]["limited"])
        self.assertEqual(data["activity"]["days"][-1]["count"], 300)
        self.assertEqual(data["activity"]["events_count"], 300)

    def test_private_data_fails_before_assets_change(self):
        api = FakeAPI()
        api.repos[0]["private"] = True
        with tempfile.TemporaryDirectory() as directory:
            existing = Path(directory) / "data.json"
            existing.write_text("keep existing data")
            with patch.object(sys, "argv", ["update_stats.py", "--output-dir", directory, "--data-only"]), patch.object(stats, "GitHub", return_value=api), patch.object(stats, "github_token", return_value=None):
                self.assertEqual(stats.main(), 1)
            self.assertEqual(existing.read_text(), "keep existing data")

    def test_incomplete_or_duplicate_repositories_fail(self):
        for modification in ("count", "duplicate", "owner"):
            with self.subTest(modification=modification):
                api = FakeAPI()
                if modification == "count":
                    original = api.get
                    api.get = lambda path: {"login": stats.USER, "public_repos": 100} if path == f"/users/{stats.USER}" else original(path)
                elif modification == "duplicate":
                    api.repos.append(api.repos[0])
                else:
                    api.repos[0]["owner"]["login"] = "someone-else"
                with self.assertRaises(ValueError):
                    stats.collect(api, date(2026, 10, 19))

    def test_failed_language_fetch_preserves_assets(self):
        api = FakeAPI()
        original = api.get

        def get(path):
            if path.endswith("/languages"):
                raise ValueError("Simulated API failure")
            return original(path)

        api.get = get
        with tempfile.TemporaryDirectory() as directory:
            existing = Path(directory) / "data.json"
            existing.write_text("keep")
            with patch.object(sys, "argv", ["update_stats.py", "--output-dir", directory]), patch.object(stats, "GitHub", return_value=api), patch.object(stats, "github_token", return_value=None):
                self.assertEqual(stats.main(), 1)
            self.assertEqual(existing.read_text(), "keep")

    def test_render_failure_and_unsafe_paths_preserve_assets(self):
        for rendered in ({"chart.svg": "invalid XML"}, {"../chart.svg": '<svg xmlns="http://www.w3.org/2000/svg"/>'}):
            with tempfile.TemporaryDirectory() as directory:
                existing = Path(directory) / "data.json"
                existing.write_text("keep")
                renderer = types.SimpleNamespace(render_dashboard=lambda data: rendered)
                with patch.dict(sys.modules, {"render_assets": renderer}), self.assertRaises((ValueError, stats.ET.ParseError)):
                    stats.write_dashboard({}, directory)
                self.assertEqual(existing.read_text(), "keep")

    def test_valid_render_and_json_are_written_together(self):
        renderer = types.SimpleNamespace(render_dashboard=lambda data: {"chart.svg": '<svg xmlns="http://www.w3.org/2000/svg"/>'})
        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules, {"render_assets": renderer}):
            stats.write_dashboard({"schema_version": 1}, directory)
            self.assertEqual(json.loads((Path(directory) / "data.json").read_text()), {"schema_version": 1})
            self.assertTrue((Path(directory) / "chart.svg").exists())

    def test_failed_file_replacement_rolls_back_prior_files(self):
        renderer = types.SimpleNamespace(render_dashboard=lambda data: {"chart.svg": '<svg xmlns="http://www.w3.org/2000/svg"/>'})
        replace = stats.os.replace
        calls = 0

        def fail_second(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("Simulated filesystem failure")
            return replace(source, destination)

        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules, {"render_assets": renderer}):
            (Path(directory) / "data.json").write_text("old data")
            (Path(directory) / "chart.svg").write_text("old SVG")
            with patch.object(stats.os, "replace", side_effect=fail_second), self.assertRaises(OSError):
                stats.write_dashboard({}, directory)
            self.assertEqual((Path(directory) / "data.json").read_text(), "old data")
            self.assertEqual((Path(directory) / "chart.svg").read_text(), "old SVG")
            self.assertEqual(len(list(Path(directory).iterdir())), 2)


if __name__ == "__main__":
    unittest.main()
