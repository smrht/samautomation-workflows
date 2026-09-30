# Samautomation Workflows

Build or repair importable n8n workflow JSON, check its structure and test valid, duplicate and invalid events in isolation. Includes a read-only checker and a manual fixture tested on n8n 2.23.4. No account connection, network requests or activation by the bundled checker.

Install the plugin archive in a host that supports Agent Plugins, or load `skills/n8n-workflow-check/SKILL.md` in a compatible skill host. It works without a Samautomation account. Python 3 is required for the optional checker. See the skill for commands and interpretation.

Source and examples are MIT licensed. This is an independent plugin; it is not an official n8n or Lovable integration. No production service is activated by installation.

Run the local regression checks:

```sh
python3 -m unittest discover -s tests -v
```

[Privacy](PRIVACY.md) · [Support](https://github.com/smrht/samautomation-workflows/issues) · [Project](https://samautomation.work)
