# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for automation-sandbox/user_lookup.py parameterized queries."""

import importlib.util
import sqlite3
from collections.abc import Iterator
from pathlib import Path

import pytest

# The sandbox directory name contains a hyphen, so it is not importable as a
# package; load the module directly from its file path instead.
_MODULE_PATH = Path(__file__).resolve().parent.parent / "user_lookup.py"
_spec = importlib.util.spec_from_file_location("user_lookup", _MODULE_PATH)
assert _spec is not None
assert _spec.loader is not None
user_lookup = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(user_lookup)

get_user_by_username = user_lookup.get_user_by_username
search_users = user_lookup.search_users


@pytest.fixture
def conn() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)"
    )
    connection.executemany(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        [("alice", "alice@example.com"), ("bob", "bob@example.com")],
    )
    connection.commit()
    yield connection
    connection.close()


def test_get_user_by_username_returns_match(conn: sqlite3.Connection) -> None:
    assert get_user_by_username(conn, "alice") == (1, "alice", "alice@example.com")


def test_get_user_by_username_is_injection_safe(conn: sqlite3.Connection) -> None:
    # A classic injection payload must not bypass the WHERE clause; it should be
    # treated as a literal username and match nothing.
    assert get_user_by_username(conn, "alice' OR '1'='1") is None
    # The table must remain intact after a drop-table payload.
    get_user_by_username(conn, "x'; DROP TABLE users; --")
    assert get_user_by_username(conn, "alice") is not None


def test_search_users_filters_by_term(conn: sqlite3.Connection) -> None:
    assert search_users(conn, "ali") == [(1, "alice")]


def test_search_users_is_injection_safe(conn: sqlite3.Connection) -> None:
    # The payload is treated as a literal LIKE term, matching no users.
    assert search_users(conn, "%' OR '1'='1") == []
