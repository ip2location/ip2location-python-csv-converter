"""Shared fixtures for ip2location/ip2location-python-csv-converter tests.

Scope: pure functions (IP version detection, number/IP conversion,
range/cidr/hex row conversion, schema assembly, CSV validity/tail-row
reading) + small-file end-to-end via tmp_path (convert_to_csv).
No network access; no reading of the user's real data.

csv_to_sqlite is intentionally not covered: its body references an
undefined `reader` variable, so any call raises NameError at runtime
(upstream bug, disclosed as-is in the PR description; no source code
changed).
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ip2location_csv_converter import ip2location_csv_converter as conv  # noqa: E402


@pytest.fixture(scope="session")
def c():
    """The converter module under test."""
    return conv


@pytest.fixture()
def sample_csv(tmp_path):
    """A tiny synthetic IP2Location-style CSV (numeric ranges + 2 columns)."""
    p = tmp_path / "sample.csv"
    p.write_text(
        "167772160,167774207,US,United States\n"
        "167774208,167774463,US,United States\n",
        encoding="utf-8",
    )
    return str(p)
