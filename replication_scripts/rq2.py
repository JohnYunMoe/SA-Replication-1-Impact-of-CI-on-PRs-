import pandas as pd
from scipy.stats import mannwhitneyu, pearsonr
from cliffs_delta import cliffs_delta
import matplotlib.pyplot as plt

csv = pd.read_csv("datasets/Provided Data/releases_meta_data.csv", parse_dates=["startedAt", "publishedAt"])

project_names = csv["project"].unique()

mean_data = csv.groupby(["project", "practice"]).agg(
	created_pull_requests=("created_pull_requests", "mean"),
	merged_pull_requests=("merged_pull_requests", "mean"),
	released_pull_requests=("released_pull_requests", "mean"),
	# sum_submitted_pr_churn=("sum_submitted_pr_churn", "mean"),
)# .reset_index()

median_data = csv.groupby(["practice"]).agg(
	created_pull_requests=("created_pull_requests", "median"),
	merged_pull_requests=("merged_pull_requests", "median"),
	released_pull_requests=("released_pull_requests", "median"),
	# sum_submitted_pr_churn=("sum_submitted_pr_churn", "median"),
)# .reset_index()

# Idk why the authors changed the terminology between the code and paper, but
#   -   created_pull_requests -> Submitted PRs
#   -    merged_pull_requests -> Merged PRs
#   -  released_pull_requests -> Delivered PRs
#   - (sum_submitted_pr_churn -> Amount of code changes in PRs)

# print(csv, mean_data, median_data, sep="\n\n") # TEMP


## 1 - Increase in PR submissions after CI (by number of projects)

n = 0
for project in project_names:
	if (mean_data.at[(project, 'CI'), "created_pull_requests"] > mean_data.at[(project, 'NO-CI'), "created_pull_requests"]):
		n += 1

print(f"1. {n/len(project_names):.1%} ({n}/{len(project_names)}) of the projects increase PR submissions after adopting CI.")


## 2 - Increase in PRs delivered after CI (overall)

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


# 1. CI & NO-CI
# 2. Find number of releases for each project for each year (Jan-Dec?)
# 3. Box plot of num releases

# publishedAt
pre_ci_releases_per_year_list = []
post_ci_releases_per_year_list = []
for project in project_names:
	release_counts = csv.loc[(csv["project"] == project), :].groupby(["practice", csv["publishedAt"].dt.year]).count()["title"]
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

plt.boxplot(post_ci_releases_per_year_list)
plt.savefig("releases_per_year_(ci)_boxplot.png", bbox_inches='tight')
plt.show()

print(pd.Series(post_ci_releases_per_year_list).describe())

# pre_ci
# count    288.000000
# mean      10.083333
# std       14.438865
# min        1.000000
# 25%        3.000000
# 50%        6.000000
# 75%       11.000000
# max      140.000000
# dtype: float64

# post_ci
# count    287.000000
# mean      15.804878
# std       34.775256
# min        1.000000
# 25%        3.000000
# 50%        7.000000
# 75%       16.000000
# max      434.000000
# dtype: float64

# CI    Name  Year    # Releases
# CI    P1    2026    2
# CI    P1    2025    10
# CI    P2    2026    2
# CI    P2    2025    10

# We do not observe a significant difference of release frequency after adopting CI


## 4

# We find that 75.9% (66/87) of the studied projects tend to increase the number of PR contributors per release after adopting CI.