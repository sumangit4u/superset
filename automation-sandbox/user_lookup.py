# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
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
