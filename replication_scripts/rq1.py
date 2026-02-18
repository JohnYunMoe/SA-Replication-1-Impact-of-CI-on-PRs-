import pandas as pd
from scipy.stats import mannwhitneyu
# from cliffs_delta import cliffs_delta # There seems to be differences between this package and the calculations used by the authors

csv = pd.read_csv("datasets/Provided Data/pull_requests_meta_data.csv", )

project_names = csv["project"].unique()

csv["lifetime"] = csv["merge_time"] + csv["delivery_time"]

mean_times = csv.groupby(["project", "practice"]).agg(
    merge_time=("merge_time", "mean"),
    delivery_time=("delivery_time", "mean"),
	lifetime=("lifetime", "mean"),
).reset_index()


## 1

projects_passed_delivery_p = []
for project in project_names:

	proj_post_ci_dt = csv.loc[(csv["project"] == project) & (csv["practice"] == "CI"), "delivery_time"]
	proj_pre_ci_dt = csv.loc[(csv["project"] == project) & (csv["practice"] == "NO-CI"), "delivery_time"]

	if (mannwhitneyu(proj_post_ci_dt, proj_pre_ci_dt)[1] < 0.05): # and cliffs_delta(proj_post_ci_dt, proj_pre_ci_dt)[1] == "negligible"
		projects_passed_delivery_p.append(project)

n = 0
for project in projects_passed_delivery_p:
	x = mean_times.loc[(mean_times["project"] == project)]
	if (x.loc[x["practice"] == "CI", "delivery_time"].values[0]
		< x.loc[x["practice"] == "NO-CI", "delivery_time"].values[0]):
		n += 1

print(f"1. {n/len(projects_passed_delivery_p):.1%} ({n}/{len(projects_passed_delivery_p)}) of the projects deliver merged PRs more quickly after the adoption of CI.")


## 2

projects_passed_merge_p = []
for project in project_names:
	if (mannwhitneyu(
		csv.loc[(csv["project"] == project) & (csv["practice"] == "CI"), "merge_time"],
		csv.loc[(csv["project"] == project) & (csv["practice"] == "NO-CI"), "merge_time"]
	)[1] < 0.05):
		projects_passed_merge_p.append(project)

n = 0
for project in projects_passed_merge_p:
	x = mean_times.loc[(mean_times["project"] == project)]
	if (x.loc[x["practice"] == "CI", "merge_time"].values[0]
		> x.loc[x["practice"] == "NO-CI", "merge_time"].values[0]):
		n += 1

print(f"2. In {n/len(projects_passed_merge_p):.1%} ({n}/{len(projects_passed_merge_p)}) of the projects, PRs are merged faster before adopting CI.")


## 3

n = 0
for project in project_names:
	x = mean_times.loc[(mean_times["project"] == project)]
	if (x.loc[x["practice"] == "CI", "lifetime"].values[0]
		> x.loc[x["practice"] == "NO-CI", "lifetime"].values[0]):
		n += 1

print(f"3. In {n/len(project_names):.1%} ({n}/{len(project_names)}) of the projects, PRs have a longer lifetime after adopting CI.")


# Yeaa.... not the best code
