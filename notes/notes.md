## Execution Notes

- Running the PR collection script kept failing before it finished retrieving data from the second project, scikit-image.
- The failure looks like a transient network/connection drop from the GitHub API during a PR detail request, which interrupts the run before it finishes scikit-image.
- This looks like connection reset or timeout rather than a data logic error, so the script may need retries/backoff or smaller batches to complete reliably.
