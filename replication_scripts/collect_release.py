import argparse
import csv
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

from config import PROJECTS, RELEASES_OUTPUT_CSV

UNSTABLE_TAG_TOKENS = ("alpha", "beta", "rc", "pre", "dev")
DEFAULT_PRACTICE = "CI"


def build_headers(token: str | None) -> dict:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def get_with_rate_limit(url: str, headers: dict, params: dict | None = None) -> tuple[list | dict, dict]:
    while True:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
            reset_at = int(response.headers.get("X-RateLimit-Reset", "0"))
            wait_seconds = max(reset_at - int(time.time()), 5)
            print(f"Rate limit reached. Sleeping for {wait_seconds}s...")
            time.sleep(wait_seconds)
            continue
        response.raise_for_status()
        return response.json(), response.headers


def iter_releases(api_base: str, repo: str, headers: dict):
    page = 1
    while True:
        url = f"{api_base}/repos/{repo}/releases"
        params = {"per_page": 100, "page": page}
        data, _ = get_with_rate_limit(url, headers, params)
        if not data:
            break
        for release in data:
            yield release
        page += 1


def is_stable_release(tag_name: str, prerelease: bool, draft: bool) -> bool:
    if prerelease or draft:
        return False
    lowered = (tag_name or "").lower()
    return not any(token in lowered for token in UNSTABLE_TAG_TOKENS)


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def parse_github_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def to_output_datetime(value: datetime | None) -> str:
    if not value:
        return ""
    return value.strftime("%Y-%m-%d %H:%M:%S")


def collect_releases(api_base: str, headers: dict, output_path: Path) -> None:
    fields = [
        "project",
        "title",
        "startedAt",
        "publishedAt",
        "release_duration",
        "created_pull_requests",
        "merged_pull_requests",
        "released_pull_requests",
        "sum_submitted_pr_churn",
        "practice",
    ]

    ensure_parent_dir(output_path)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        total_written = 0
        for repo in PROJECTS:
            print(f"Collecting releases from {repo}...")
            stable_releases: list[dict] = []
            for release in iter_releases(api_base, repo, headers):
                tag_name = (release.get("tag_name") or "").strip()
                published_at = release.get("published_at")
                created_at = release.get("created_at")
                prerelease = bool(release.get("prerelease", False))
                draft = bool(release.get("draft", False))

                if not tag_name or not published_at:
                    continue
                if not is_stable_release(tag_name, prerelease, draft):
                    continue

                stable_releases.append(
                    {
                        "tag_name": tag_name,
                        "published_at": parse_github_datetime(published_at),
                        "created_at": parse_github_datetime(created_at),
                    }
                )

            stable_releases = [r for r in stable_releases if r["published_at"] is not None]
            stable_releases.sort(key=lambda r: r["published_at"], reverse=True)

            for index, release in enumerate(stable_releases):
                published_at_dt = release["published_at"]
                if index + 1 < len(stable_releases):
                    started_at_dt = stable_releases[index + 1]["published_at"] + timedelta(seconds=1)
                else:
                    started_at_dt = release["created_at"] or published_at_dt

                release_duration = int(max((published_at_dt - started_at_dt).total_seconds(), 0) // 86400)

                writer.writerow(
                    {
                        "project": repo,
                        "title": release["tag_name"],
                        "startedAt": to_output_datetime(started_at_dt),
                        "publishedAt": to_output_datetime(published_at_dt),
                        "release_duration": release_duration,
                        "created_pull_requests": 0,
                        "merged_pull_requests": 0,
                        "released_pull_requests": 0,
                        "sum_submitted_pr_churn": "",
                        "practice": DEFAULT_PRACTICE,
                    }
                )
                total_written += 1

        print(f"Collected {total_written} stable releases.")


def parse_args(default_output: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect stable release metadata from GitHub.")
    parser.add_argument(
        "--output",
        default=default_output,
        help="Output CSV path (relative to repo root or absolute).",
    )
    return parser.parse_args()


def resolve_output_path(output: str) -> Path:
    output_path = Path(output)
    if output_path.is_absolute():
        return output_path
    repo_root = Path(__file__).resolve().parents[1]
    return repo_root / output_path


def main() -> None:
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise SystemExit("Missing GITHUB_TOKEN. Set it in replication_scripts/.env")

    api_base = os.getenv("GITHUB_API_BASE", "https://api.github.com").rstrip("/")
    args = parse_args(RELEASES_OUTPUT_CSV)
    output_path = resolve_output_path(args.output)
    headers = build_headers(token)

    collect_releases(api_base, headers, output_path)
    print(f"Done. Wrote {output_path}")


if __name__ == "__main__":
    main()