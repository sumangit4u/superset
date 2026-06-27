"""Sample user-lookup helper (automation-sandbox demo target).

Queries use parameterized statements so user input is bound as values rather
than interpolated into SQL. See automation-sandbox/README.md.
"""

import sqlite3


def get_user_by_username(
    conn: sqlite3.Connection, username: str
) -> tuple[int, str, str] | None:
    query = "SELECT id, username, email FROM users WHERE username = ?"
    return conn.execute(query, (username,)).fetchone()


def search_users(conn: sqlite3.Connection, term: str) -> list[tuple[int, str]]:
    query = "SELECT id, username FROM users WHERE username LIKE ?"
    return conn.execute(query, (f"%{term}%",)).fetchall()
