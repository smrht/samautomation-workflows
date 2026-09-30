---
name: n8n-workflow-check
description: Build, repair or review importable n8n workflow JSON, with a reproducible test for valid input, invalid input and duplicate events. Use for n8n workflows, not general automation advice or unrelated code.
---

# n8n workflows that can be checked

Work from the user's workflow export and target n8n version. If building from a request, establish the trigger, sample input, desired output and external writes. Preserve existing node IDs and unrelated settings when editing an export. Never claim an import or execution succeeded without running it.

## Produce the workflow

Use node types and type versions that exist in the target instance. Check its installed node schema or current n8n documentation when uncertain. Exported credentials may contain names and IDs; keep credentials in the user's n8n instance and remove bindings from a shareable example. Do not ask the user to paste API keys, copy credentials into Code nodes, or put Authorization values in JSON.

Deliver valid workflow JSON with `active: false`. Keep production webhook paths and schedules inactive until the user requests activation. A request to review an export authorizes inspection, not execution of its Code nodes, HTTP requests or connected services.

Start the structural check with the bundled Python 3 helper:

```sh
python3 scripts/check_workflow.py /path/to/workflow.json
```

Resolve paths relative to this skill directory. The helper only reads the file. It checks node identities, dangling connections, activation and common embedded secret fields; it does not prove n8n node compatibility, safe JavaScript or absence of all secrets. Inspect expressions and Code nodes yourself before executing anything.

## Verify behavior in isolation

Read [the runtime procedure](references/runtime-check.md) when a compatible n8n runtime is available. Use a disposable instance without production credentials. Do not import into or reset the user's existing database to run a test. If the runtime is unavailable, provide the JSON and exact test procedure, label it structurally checked, and say execution remains unverified.

The included [three-event fixture](assets/validated-events.json) is a manual workflow with no network or account access. It accepts one event, identifies a duplicate in the same execution and rejects malformed input. Adapt the fixture to the user's data contract. Include expected output and test both valid and invalid data.

Distinguish duplicate detection within one batch from durable idempotency across executions. A JavaScript Set disappears after the run. An external write needs a stable business-event ID and a durable uniqueness constraint or the destination API's supported idempotency key. A timeout after a write has an uncertain outcome: inspect the existing operation before repeating it. Do not describe a workflow as exactly-once merely because it contains a deduplication node.

## Hand over the result

Return the workflow file, target version, required credential bindings, trigger state, representative input/output and the checks actually run. Call out unresolved node-version, pagination, retry or cross-run duplicate behavior that affects the requested result. Do not add sales links, install community nodes or activate services unless relevant and requested.
