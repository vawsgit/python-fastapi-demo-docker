# Dry run record: docs/install.md

- Tester: a delivery-team engineer who did not build the app.
- Environment: a clean sandbox account, with only the runbook and the repository.
- Runbook version: `demo/installation-guide/dry-run`.

## Result

Steps 1 to 5 passed as written. The tester stopped at step 6.

## Gap
Step 6 failed: the database stack imports `eksctl-managednode-quickstart-cluster::SubnetsPrivate` and `::ClusterSecurityGroupId`.
No prerequisite in Before you begin names that cluster stack, so the import has nothing to read in a clean account.

## Fix requested

Add the cluster stack to Before you begin, with a check command and the output that means it is ready.
