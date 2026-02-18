import pandas as pd
from scipy.stats import mannwhitneyu
from cliffs_delta import cliffs_delta

csv = pd.read_csv("datasets/Provided Data/pull_requests_meta_data.csv", )

project_names = csv["project"].unique()

csv["lifetime"] = csv["merge_time"] + csv["delivery_time"]

mean_times = csv.groupby(["project", "practice"]).agg(
    merge_time=("merge_time", "mean"),
    delivery_time=("delivery_time", "mean"),
	lifetime=("lifetime", "mean"),
).reset_index()

# print(mean_times.at[('AnalyticalGraphicsInc/cesium', 'CI'), "merge_time"])
# print(csv.head(), mean_times.head())
# print(mean_times.loc[mean_times["practice"] == "CI", :])
# print(mean_times.loc[mean_times["project"] == "AnalyticalGraphicsInc/cesium", :])
# mean_times.reset_index()
# print(mean_times.head())
# quit()

# In the form:
#                         project practice  merge_time  delivery_time
# 0  AnalyticalGraphicsInc/cesium       CI    3.305398     4311.889077
# 1  AnalyticalGraphicsInc/cesium    NO-CI   38.554683    13613.837985
# 2          BabylonJS/Babylon.js       CI    1.471293     1160.691696
# 3          BabylonJS/Babylon.js    NO-CI    2.553459      130.642543
# ...

# print(mean_times.head())# [mean_times["project"] == "Yelp/mrjob"])

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

# mean_times["merge_time_pre_ci"] = mean_times[mean_times["practice"] == "NO-CI"]["merge_time"]
# mean_times["merge_time_post_ci"] = mean_times[mean_times["practice"] == "CI"]["merge_time"]
# mean_times["delivery_time_pre_ci"] = mean_times[mean_times["practice"] == "NO-CI"]["delivery_time"]
# mean_times["delivery_time_post_ci"] = mean_times[mean_times["practice"] == "CI"]["delivery_time"]
# del mean_times["practice"]

# pre_ci_merge_times = mean_times[mean_times["practice"] == "NO-CI"]["merge_time"]
# post_ci_merge_times = mean_times[mean_times["practice"] == "CI"]["merge_time"] #[["merge_time", "project"]]

# print(csv["project"].unique())


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


# Yeaa.... that was probably some horribly inefficient code
