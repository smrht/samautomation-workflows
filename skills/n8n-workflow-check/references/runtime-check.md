# Import and execute without production access

The included fixture was tested on n8n 2.23.4. It uses Manual Trigger v1 and Code v2. JavaScript task runners must be available for Code execution. Version and runtime configuration matter; inspect `n8n --version` and `n8n execute --help` in the test environment.

Use an isolated disposable n8n user folder and database. Import the fixture with `n8n import:workflow --input=/path/to/validated-events.json`, then execute its imported ID with `n8n execute --id=samautomationFixture01 --rawOutput`. The CLI file-execution option is deprecated in that tested version. These commands are for the disposable environment, not the user's production container.

Expected `Validate events` output, in order:

1. `event-001`: accepted, amount 12.
2. `event-001`: duplicate, no second acceptance in this batch.
3. Missing event ID and a nonnumeric amount: rejected.

The workflow has no HTTP requests, credentials or destinations. Each execution starts a fresh Set and therefore accepts the first event again. Add a separate cross-execution test before claiming durable deduplication. For the user's workflow, substitute synthetic destinations or a destination's documented dry-run mode before executing side effects.

After execution inspect each relevant node's actual output and the overall result; an exit code alone is not enough. Remove only the disposable test environment created for this test.

Primary documentation: [n8n CLI source documentation](https://github.com/n8n-io/n8n-docs/blob/main/docs/deploy/host-n8n/configure-n8n/use-the-command-line.md), [workflow export/import](https://github.com/n8n-io/n8n-docs/blob/main/docs/build/manage-workflows/export-and-import.md).
