# Historical scheduling CRM

A historical Django scheduling application with client/staff views, service and appointment models, intake forms, reminders and payment integrations. It is retained as source history; this repository is not identified as the current Renter case or the current BGM application.

## Source map

- `core/`: service, scheduling, intake and payment workflows.
- `accounts/`: account forms, authentication and role handling.
- `templates/`: Django staff and customer interfaces.
- `Procfile` and existing deployment files: historical runtime configuration, requiring a separate environment review.

## Safe review

Use synthetic records in a new local database. Create a fresh local administrator with Django's `createsuperuser`; do not reuse previously documented test credentials. Do not start Celery, reminder delivery or payment/provider integrations against production configuration during source review.

A full current-runtime/test baseline has not been established for this historical repository. Review the dependency files and configuration before local execution. Existing scheduler databases, archives and generated outputs require ownership/reference checks before cleanup; they are not public demonstration datasets.

## Historical credentials

Shared test-account values have been removed from the current README. This does not establish that historical credentials were revoked or that copies disappeared from Git history. The owner should reset any reused credentials and separately review historical copies. No existing deployment or account was changed by this documentation update.

The existing licence and original attribution are preserved. Client-specific assets and source lineage require owner review before promoting this as an independent public case study.
