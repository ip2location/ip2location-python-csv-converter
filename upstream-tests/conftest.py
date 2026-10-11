"""Shared fixtures for ip2location/ip2location-python-csv-converter tests.

Scope: 纯函数（IP 版本探测、数值/IP 互转、range/cidr/hex 行转换、
schema 组装、CSV 有效性/尾行读取）+ 基于 tmp_path 的小文件端到端
（convert_to_csv）。不碰网络、不读用户真实数据。

csv_to_sqlite 未覆盖：其函数体引用了未定义的 `reader` 变量，
运行时必抛 NameError（上游 bug，已在 PR 描述中如实标注，未改源码）。
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
