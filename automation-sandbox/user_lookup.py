"""Sample user-lookup helper (automation-sandbox demo target).

Intentionally contains SQL injection vulnerabilities for the Devin
remediation demo. See automation-sandbox/README.md.
"""
import sqlite3


def get_user_by_username(conn: sqlite3.Connection, username: str):
    # ISSUE: user input concatenated directly into SQL -> injection
    query = "SELECT id, username, email FROM users WHERE username = '%s'" % username
    return conn.execute(query).fetchone()


def search_users(conn: sqlite3.Connection, term: str):
    # ISSUE: same problem with LIKE
    query = "SELECT id, username FROM users WHERE username LIKE '%" + term + "%'"
    return conn.execute(query).fetchall()
