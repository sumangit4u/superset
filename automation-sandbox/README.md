# Automation Sandbox

This directory contains **intentionally flawed** sample modules used as bounded,
verifiable targets for the Devin remediation automation
(see the companion repo `devin-superset-automation`).

They are deliberately self-contained and are **not imported** by Superset, so
remediations can be reviewed and merged without touching production code paths
or the main test suite. Each file maps to a GitHub issue labeled `devin-fix`.

| File | Class | Finding |
|------|-------|---------|
| `user_lookup.py` | Security | SQL injection via string-formatted queries |
| `token_utils.py` | Security | Weak MD5 hashing + hardcoded secret |
| `file_processor.py` | Security / Quality | `subprocess` with `shell=True`; bare `except:` |
| `config_loader.py` | Security / Quality | Unsafe `yaml.load`; mutable default argument |
| `http_client.py` | Security | Missing request timeout; TLS verification disabled |

When an issue here is labeled `devin-fix`, the orchestrator opens a Devin session
that fixes the file and raises a pull request.
