import pandas as pd
from scipy.stats import mannwhitneyu, pearsonr
from cliffs_delta import cliffs_delta
import matplotlib.pyplot as plt

releases_csv = pd.read_csv("datasets/Provided Data/releases_meta_data.csv", parse_dates=["startedAt", "publishedAt"])

project_names = releases_csv["project"].unique()

mean_data = releases_csv.groupby(["project", "practice"]).agg(
	created_pull_requests=("created_pull_requests", "mean"),
	merged_pull_requests=("merged_pull_requests", "mean"),
	released_pull_requests=("released_pull_requests", "mean"),
)

median_data = releases_csv.groupby(["practice"]).agg(
	created_pull_requests=("created_pull_requests", "median"),
	merged_pull_requests=("merged_pull_requests", "median"),
	released_pull_requests=("released_pull_requests", "median"),
)

# Idk why the authors changed the terminology between the code and paper, but
#   -   created_pull_requests -> Submitted PRs
#   -    merged_pull_requests -> Merged PRs
#   -  released_pull_requests -> Delivered PRs
#   - (sum_submitted_pr_churn -> Amount of code changes in PRs)


## 1 - Increase in PR submissions after CI (by number of projects)

n = 0
for project in project_names:
	if (mean_data.at[(project, 'CI'), "created_pull_requests"] > mean_data.at[(project, 'NO-CI'), "created_pull_requests"]):
		n += 1

print(f"1. {n/len(project_names):.1%} ({n}/{len(project_names)}) of the projects increase PR submissions after adopting CI.")


## 2 - Increase in PRs delivered after CI (overall)

pre_ci_released_prs_list = []
post_ci_released_prs_list = []

n = 0
for project in project_names:
	pre_ci_released_prs_list.append(mean_data.at[(project, 'CI'), "released_pull_requests"])
	post_ci_released_prs_list.append(mean_data.at[(project, 'NO-CI'), "released_pull_requests"])

print(f"2. After adopting CI projects deliver {pd.Series(pre_ci_released_prs_list).agg("median")/pd.Series(post_ci_released_prs_list).agg("median"):.2f} times more PRs per release than before CI.")


# for i in ["created_pull_requests", "merged_pull_requests", "released_pull_requests"]:
#     print(csv[["practice", i]].groupby("practice").describe())

# csv.loc[csv["practice"] == "CI", "merged_pull_requests"].to_csv("oooooo.csv")
# csv.boxplot(column=["merged_pull_requests"], by=["practice"])
# plt.show()





# print(csv.loc[csv["practice"] == "CI", "merged_pull_requests"])

# print(csv.loc[csv["practice"] == "CI", "merged_pull_requests"])
# print(csv.loc[csv["practice"] == "CI", :])
# print(csv.loc[csv["practice"] == "CI", "merged_pull_requests"])
# csv.loc[csv["practice"] == "CI", "merged_pull_requests"]

# boxx = csv.boxplot(by=["merged_pull_requests"])
# print("boxx", boxx)


# plt.boxplot(csv.loc[csv["practice"] == "CI", "merged_pull_requests"].fillna(0))
# plt.show()


## 3 - (No) Difference in release frequency after CI

pre_ci_releases_per_year_list = []
post_ci_releases_per_year_list = []
for project in project_names:
	release_counts = releases_csv.loc[(releases_csv["project"] == project), :].groupby(["practice", releases_csv["publishedAt"].dt.year]).count()["title"]
	# In the form (Series):

	# practice  publishedAt
	# CI        2015           3
	#           2016           4
	#           ...
	# NO-CI     2009           3
	#           2011           5
	#           ...
	# Name: title, dtype: int64

	pre_ci_releases_per_year_list.extend(release_counts["NO-CI"])
	post_ci_releases_per_year_list.extend(release_counts["CI"])

# plt.boxplot(post_ci_releases_per_year_list)
# plt.savefig("releases_per_year_(ci)_boxplot.png", bbox_inches='tight')
# plt.show()

print(f"3. Median releases before and after adopting CI: {pd.Series(pre_ci_releases_per_year_list).agg("median")}, {pd.Series(post_ci_releases_per_year_list).agg("median")}")


## 4

prs_csv = pd.read_csv("datasets/Provided Data/pull_requests_meta_data.csv")

median_prs_csv = prs_csv.groupby(["project", "practice"]).agg(
    contributor_integration_median=("contributor_integration", "median"),
    contributor_experience_median=("contributor_experience", "median"),
)

n = 0
for project in project_names:
	if (median_prs_csv.at[(project, 'CI'), "contributor_integration_median"]
		> median_prs_csv.at[(project, 'NO-CI'), "contributor_integration_median"]):
		n += 1


print(f"4. In {n/len(project_names):.1%} ({n}/{len(project_names)}) of the projects tend to increase the number of PR contributors per release after adopting CI.")
