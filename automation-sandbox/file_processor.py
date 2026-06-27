"""File processing helpers (automation-sandbox demo target)."""
import subprocess


def count_lines(path: str) -> str:
    # ISSUE: shell=True with unsanitized input -> command injection
    cmd = "wc -l " + path
    return subprocess.check_output(cmd, shell=True).decode()


def safe_read(path: str):
    try:
        with open(path) as f:
            return f.read()
    except:  # noqa: E722  ISSUE: bare except swallows everything incl. KeyboardInterrupt
        return None
