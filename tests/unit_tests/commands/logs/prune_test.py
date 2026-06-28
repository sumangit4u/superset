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

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch


def test_prune_cutoff_is_timezone_aware_utc() -> None:
    """
    The retention cutoff must be a timezone-aware UTC datetime
    (using ``datetime.now(tz=timezone.utc)``), not the deprecated
    ``datetime.utcnow()`` which returns a naive datetime.
    """
    from superset.commands.logs.prune import LogPruneCommand

    captured: dict[str, datetime] = {}

    def fake_execute(stmt):  # noqa: ANN001
        # Capture the bound cutoff value from the WHERE clause.
        for param in stmt.compile().params.values():
            if isinstance(param, datetime):
                captured["cutoff"] = param
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        return result

    session = MagicMock()
    session.execute.side_effect = fake_execute

    with patch("superset.commands.logs.prune.db") as mock_db:
        mock_db.session = session
        LogPruneCommand(retention_period_days=30).run()

    cutoff = captured["cutoff"]
    # The cutoff must be timezone-aware (UTC).
    assert cutoff.tzinfo is not None
    assert cutoff.tzinfo == timezone.utc

    expected = datetime.now(tz=timezone.utc) - timedelta(days=30)
    # Allow a small delta for execution time between computing the two values.
    assert abs((cutoff - expected).total_seconds()) < 60
