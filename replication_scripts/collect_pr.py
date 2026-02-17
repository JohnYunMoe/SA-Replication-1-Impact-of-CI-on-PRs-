import argparse
import csv
import os
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from config import OUTPUT_CSV, PROJECTS

# Language mappings for repositories (can be extended)
LANGUAGE_MAP = {
	"serverless/serverless": "JavaScript",
	"scikit-image/scikit-image": "Python",
	"dropwizard/dropwizard": "Java",
	"bundler/bundler": "Ruby",
	"laravel/laravel": "PHP",
}


def build_headers(token: str | None) -> dict:
	headers = {"Accept": "application/vnd.github.v3+json"}
	if token:
		headers["Authorization"] = f"token {token}"
	return headers


def get_with_rate_limit(url: str, headers: dict, params: dict | None = None) -> tuple[dict, dict]:
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


def iter_pull_requests(api_base: str, repo: str, headers: dict):
	page = 1
	while True:
		url = f"{api_base}/repos/{repo}/pulls"
		payload = {"state": "all", "per_page": 100, "page": page}
		data, _ = get_with_rate_limit(url, headers, payload)
		if not data:
			break
		for pr in data:
			yield pr
		page += 1


def fetch_pr_detail(api_base: str, repo: str, number: int, headers: dict) -> dict:
	url = f"{api_base}/repos/{repo}/pulls/{number}"
	data, _ = get_with_rate_limit(url, headers)
	return data


def parse_timestamp(ts: str | None) -> float:
	"""Convert ISO 8601 timestamp to hours since epoch-like reference."""
	if not ts:
		return 0.0
	try:
		dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
		return dt.timestamp() / 3600.0  # Convert to hours
	except (ValueError, AttributeError):
		return 0.0


def calculate_merge_time(created_at: str, merged_at: str) -> float:
	"""Calculate merge time in hours."""
	if not created_at or not merged_at:
		return 0.0
	try:
		created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
		merged = datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
		delta_hours = (merged - created).total_seconds() / 3600.0
		return max(delta_hours, 0.0)
	except (ValueError, AttributeError):
		return 0.0


def ensure_parent_dir(path: Path) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)


def collect_pull_requests(api_base: str, headers: dict, output_path: Path) -> None:
	fields = [
		"",
		"X.",
		"project",
		"language",
		"pull_id",
		"pull_number",
		"commits_per_pr",
		"changed_files",
		"churn",
		"comments",
		"comments_interval",
		"merge_workload",
		"description_length",
		"contributor_experience",
		"queue_rank",
		"contributor_integration",
		"stacktrace_attached",
		"activities",
		"merge_time",
		"delivery_time",
		"practice",
	]

	ensure_parent_dir(output_path)

	with output_path.open("w", newline="", encoding="utf-8") as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fields)
		writer.writeheader()

		row_index = 0
		for repo in PROJECTS:
			print(f"Collecting PRs from {repo}...")
			language = LANGUAGE_MAP.get(repo, "Unknown")

			for pr in iter_pull_requests(api_base, repo, headers):
				number = pr.get("number")
				if number is None:
					continue

				detail = fetch_pr_detail(api_base, repo, number, headers)
				merged_at = detail.get("merged_at")
				if not merged_at:
					continue

				row_index += 1
				
				# Extract basic info
				created_at = detail.get("created_at")
				pr_id = detail.get("id")
				
				# Calculate derived metrics
				additions = detail.get("additions", 0) or 0
				deletions = detail.get("deletions", 0) or 0
				churn = additions + deletions
				commits_count = detail.get("commits", 0) or 0
				changed_files_count = detail.get("changed_files", 0) or 0
				comments_count = detail.get("comments", 0) or 0
				review_comments_count = detail.get("review_comments", 0) or 0
				
				# Calculate merge time (hours)
				merge_time_hours = calculate_merge_time(created_at, merged_at)
				
				# Use merge_time as delivery_time (can be refined later)
				delivery_time_hours = merge_time_hours
				
				# Body/description length
				body = detail.get("body") or ""
				description_length = len(body)
				
				# Placeholder values (not available from GitHub API directly)
				comments_interval = 0  # Would need to analyze comment timestamps
				merge_workload = 0  # Would need release data
				contributor_experience = 0  # Would need historical contributor data
				queue_rank = 0  # Would need temporal analysis
				contributor_integration = 0  # Would need contribution history
				stacktrace_attached = 1 if "stacktrace" in body.lower() or "traceback" in body.lower() else 0
				activities = comments_count + review_comments_count + commits_count
				
				# Determine practice (placeholder - would need CI detection logic)
				practice = "CI"  # Default to CI; would need release/commit analysis to determine

				writer.writerow(
					{
						"": row_index,
						"X.": row_index,
						"project": repo,
						"language": language,
						"pull_id": pr_id,
						"pull_number": number,
						"commits_per_pr": commits_count,
						"changed_files": changed_files_count,
						"churn": churn,
						"comments": comments_count,
						"comments_interval": comments_interval,
						"merge_workload": merge_workload,
						"description_length": description_length,
						"contributor_experience": contributor_experience,
						"queue_rank": queue_rank,
						"contributor_integration": contributor_integration,
						"stacktrace_attached": stacktrace_attached,
						"activities": activities,
						"merge_time": merge_time_hours,
						"delivery_time": delivery_time_hours,
						"practice": practice,
					}
				)
				
				if row_index % 50 == 0:
					print(f"  Processed {row_index} PRs...")


def parse_args(default_output: str) -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Collect merged PR data from GitHub.")
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
	args = parse_args(OUTPUT_CSV)
	output_path = resolve_output_path(args.output)
	headers = build_headers(token)

	collect_pull_requests(api_base, headers, output_path)
	print(f"Done. Wrote {output_path}")


if __name__ == "__main__":
	main()
