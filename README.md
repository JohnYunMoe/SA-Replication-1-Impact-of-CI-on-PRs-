<p style="border:1px; border-style:solid; border-color:black; padding: 1em;">
CS-UH 3260 Software Analytics<br/>
Replication Study<br/>
John Yun Moe & Zavier Shaikh, NYUAD
</p>

# Replication Study: Impact of CI on Pull Request Delivery Time

## 1. Project Title and Overview

- **Paper Title**: Studying the Impact of Adopting Continuous Integration on the Delivery Time of Pull Requests
- **Authors**: João Helis Bernardo, Daniel Alencar da Costa, Uirá Kulesza
- **Conference**: MSR '18: 15th International Conference on Mining Software Repositories (May 2018)
- **Replication Team**: John Yun Moe, Zavier Shaikh
- **Course**: CS-UH 3260 Software Analytics, NYUAD

### Brief Description

**Original Paper**: The paper empirically investigates how adopting Continuous Integration (CI) impacts the delivery time of pull requests in GitHub projects. Through analysis of 162,653 pull requests across 87 projects in 5 programming languages, the authors examine whether CI actually speeds up PR delivery, what factors influence delivery time, and how development activity changes after CI adoption.

**Replication Study**: This replication study aims to reproduce the key findings of the original paper by analyzing the relationship between CI adoption and pull request delivery time in GitHub projects. We examine the merge time, delivery phases, and factors that influence the time-to-delivery of merged PRs before and after CI adoption.

## 2. Repository Structure
```
README.md                 # This documentation file
datasets/                 # [TO BE ADDED] Dataset used for replication
replication_scripts/      # [TO BE ADDED] Scripts for data collection and analysis
outputs/                  # [TO BE ADDED] Generated results (figures, tables, models)
logs/                     # [TO BE ADDED] Console outputs, errors, execution logs
notes/                    # [TO BE ADDED] Notes on discrepancies and observations
```

### Folder Descriptions

- **datasets/**: Will contain the pull request and release data from GitHub projects (to be collected)
- **replication_scripts/**: Will contain scripts for:
  - Data collection from GitHub API
  - PR-to-release linking
  - Statistical analysis (Mann-Whitney-Wilcoxon tests, regression modeling)
  - Visualization generation
- **outputs/**: Will contain replicated results including:
  - Statistical test results
  - Regression model outputs (R² values, variable importance)
  - Figures comparing before/after CI adoption
- **logs/**: Will document script execution, API calls, and any errors encountered
- **notes/**: Will track differences between our results and the original paper

## 3. Setup Instructions

### Prerequisites

**[TO BE ADDED]**

- Operating System: [TBD]
- Programming Language: [TBD - likely Python or R based on paper's statistical analysis]
- Required packages/libraries: [TBD]
- GitHub API access token (for data collection)

### Installation Steps

**[TO BE ADDED]**

Instructions will be provided once the replication environment is established.

## 4. Reproduction Steps

**[TO BE ADDED]**

Detailed steps to reproduce the analysis will be documented here, including:

1. Data collection process
2. PR-to-release linking methodology
3. Statistical analysis steps
4. Figure generation

## 5. Results

**[TO BE ADDED]**

Comparison of our replicated results with the original paper's findings will be documented here.

## 6. GenAI Usage

**Tools Used**: Claude (Anthropic)

**Purpose**: 
- Structuring and fine-editing this README file to ensure clarity and completeness
- Formatting markdown elements for professional documentation

## 7. References

Bernardo, J. H., da Costa, D. A., & Kulesza, U. (2018). Studying the Impact of Adopting Continuous Integration on the Delivery Time of Pull Requests. In *Proceedings of the 15th International Conference on Mining Software Repositories* (MSR '18), 131-141. https://doi.org/10.1145/3196398.3196421

---

*Last Updated*: 