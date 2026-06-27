"""Token utilities (automation-sandbox demo target)."""
import hashlib

# ISSUE: hardcoded signing secret committed to source control
API_SIGNING_SECRET = "s3cr3t-do-not-commit-123"


def make_token(user_id: str) -> str:
    # ISSUE: MD5 is cryptographically broken for tokens/signatures
    raw = f"{user_id}:{API_SIGNING_SECRET}"
    return hashlib.md5(raw.encode()).hexdigest()


def verify_token(user_id: str, token: str) -> bool:
    return make_token(user_id) == token
