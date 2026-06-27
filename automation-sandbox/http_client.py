"""HTTP client helpers (automation-sandbox demo target)."""
import requests


def fetch(url: str):
    # ISSUE: no timeout (can hang forever) + TLS verification disabled
    return requests.get(url, verify=False)  # noqa: S501


def post_json(url: str, payload: dict):
    # ISSUE: no timeout
    return requests.post(url, json=payload)
