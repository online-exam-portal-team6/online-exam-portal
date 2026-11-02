# Release process

This document describes how to prepare and publish a version of the Online
Exam Portal. Releases are made from reviewed code integrated into `main`.

## Before release

1. Confirm the intended changes are merged into `main` and the working tree is
   clean.
2. Review open defects and the release scope with the product owner.
3. Confirm CI passes, including Flake8, Django system checks, migration checks,
   and the Django test suite.
4. Review the dependency inventory at `docs/sbom.json` and regenerate it if
   project dependencies have changed.
5. Check that database migrations are committed and that the deployment
   configuration is ready. Do not include secrets in source control.
6. Prepare release notes in `docs/releases/` describing user-visible changes,
   compatibility notes, and known limitations.

## Tag and publish

For the initial release, create the annotated tag `v1.0` from the approved
`main` commit. For a subsequent patch, use the next patch tag (for example,
`v1.0.1`) after the patch has been reviewed and merged.

```powershell
git switch main
git pull --ff-only origin main
git status --short
git tag -a v1.0 -m "Online Exam Portal v1.0"
git push origin v1.0
```

The CI workflow runs on version tags matching `v*`. Confirm the tag workflow
passes before announcing the release. Create or update the GitHub Release from
the same tag and attach or link the corresponding release notes.

## Post-release and rollback

- Verify the deployed application, authentication, exam creation, MCQ
  management, exam taking, submission, and result pages.
- Record the tag, release notes, deployment date, and any follow-up defects.
- If a release is defective, pause further rollout and prepare a reviewed
  patch release. Restore the last known-good application/database backup when
  required. Do not move or delete a published version tag; publish a new patch
  tag instead.

Production deployment details and environment-specific secrets are maintained
outside this repository and are covered by the deployment task/runbook.
