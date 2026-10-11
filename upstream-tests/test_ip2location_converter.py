"""Tests for ip2location/ip2location-python-csv-converter (MIT).

Scope: 纯函数（IP 版本探测、数值/IP 互转、range/cidr/hex 行转换、
schema 组装、CSV 有效性/尾行读取）+ tmp 文件端到端 convert_to_csv。
不碰网络。csv_to_sqlite 故意不覆盖（见 conftest 说明）。
"""
import csv
import os

import pandas as pd
import pytest


# ---------------------------------------------------------------- detect_ip_version
class TestDetectIpVersion:
    def test_small_int_is_v4(self, c):
        assert c.detect_ip_version(123) == 4

    def test_max_v4_is_v4(self, c):
        assert c.detect_ip_version(4294967295) == 4

    def test_above_v4_is_v6(self, c):
        assert c.detect_ip_version(4294967296) == 6
        assert c.detect_ip_version(2**40) == 6

    def test_non_int_raises_type_error(self, c):
        with pytest.raises(TypeError):
            c.detect_ip_version("123")

    def test_negative_raises_value_error(self, c):
        with pytest.raises(ValueError):
            c.detect_ip_version(-1)


# ---------------------------------------------------------------- no2ip
class TestNo2ip:
    def test_known_value(self, c):
        assert c.no2ip(167772161) == "10.0.0.1"

    def test_zero(self, c):
        assert c.no2ip(0) == "0.0.0.0"

    def test_max_v4(self, c):
        assert c.no2ip(4294967295) == "255.255.255.255"

    def test_v6_number(self, c):
        assert c.no2ip(2**32) == "::1:0:0"

    def test_invalid_exits(self, c):
        with pytest.raises(SystemExit):
            c.no2ip("not-a-number")


# ---------------------------------------------------------------- detect_ip_version_from_number
class TestDetectIpVersionFromNumber:
    def test_ipv4_string_number(self, c):
        assert c.detect_ip_version_from_number("5") == "IPv4"

    def test_ipv6_number(self, c):
        assert c.detect_ip_version_from_number(str(2**33)) == "IPv6"

    def test_garbage_is_invalid(self, c):
        assert c.detect_ip_version_from_number("abc") == "Invalid"


# ---------------------------------------------------------------- row converters
class TestRangeNumberToIp:
    def test_replace_mode(self, c):
        out = c.range_number_to_ip(["167772160", "167774207", "x"], "replace")
        assert out == '"10.0.0.0","10.0.7.255","x"\n'

    def test_append_mode(self, c):
        out = c.range_number_to_ip(["167772160", "167774207"], "append")
        assert out == '"167772160","167774207","10.0.0.0","10.0.7.255"\n'

    def test_no_extra_columns(self, c):
        out = c.range_number_to_ip(["167772160", "167774207"], "replace")
        assert out == '"10.0.0.0","10.0.7.255"\n'


class TestNumberToCidr:
    def test_replace_mode(self, c):
        out = c.number_to_cidr(["167772160", "167774207"], "replace")
        assert out == '"10.0.0.0/21"\n'

    def test_append_mode(self, c):
        out = c.number_to_cidr(["167772160", "167774207"], "append")
        assert out == '"167772160","167774207","10.0.0.0/21"\n'

    def test_single_host_is_slash_32(self, c):
        out = c.number_to_cidr(["167772161", "167772161"], "replace")
        assert out == '"10.0.0.1/32"\n'


class TestNumberToHex:
    def test_hex_replace(self, c):
        out = c.number_to_hex(["167772160", "167774207"], "replace", "hex")
        assert out == '"000000000a000000","000000000a0007ff"\n'

    def test_hex4_pads_16(self, c):
        out = c.number_to_hex(["1", "2"], "replace", "hex4")
        assert out.startswith('"0000000000000001"')

    def test_hex6_pads_32(self, c):
        out = c.number_to_hex(["1", "2"], "replace", "hex6")
        assert out.startswith('"00000000000000000000000000000001"')

    def test_hex_append_keeps_originals(self, c):
        out = c.number_to_hex(["167772160", "167774207"], "append", "hex")
        assert out.startswith('"167772160","167774207",')


# ---------------------------------------------------------------- detect_versions_from_chunk
class TestDetectVersionsFromChunk:
    def test_v4_only(self, c):
        df = pd.DataFrame([["167772160", "167774207"], ["1", "2"]])
        assert c.detect_versions_from_chunk(df) == {4}

    def test_mixed_v4_v6(self, c):
        df = pd.DataFrame([["167772160", "167774207"], [str(2**33), str(2**33)]])
        assert c.detect_versions_from_chunk(df) == {4, 6}

    def test_invalid_rows_skipped(self, c):
        df = pd.DataFrame([["abc", "def"], ["167772160", "167774207"]])
        assert c.detect_versions_from_chunk(df) == {4}


# ---------------------------------------------------------------- get_schema
class TestGetSchema:
    def test_db1_has_columns(self, c):
        schema = c.get_schema(1, "DB")
        assert isinstance(schema, dict) and len(schema) > 0

    def test_px1_has_columns(self, c):
        schema = c.get_schema(1, "PX")
        assert isinstance(schema, dict) and len(schema) > 0

    def test_invalid_level_raises(self, c):
        with pytest.raises(ValueError):
            c.get_schema(99, "DB")

    def test_higher_level_superset(self, c):
        low = c.get_schema(1, "DB")
        high = c.get_schema(3, "DB")
        assert set(low) <= set(high)


# ---------------------------------------------------------------- file helpers
class TestCheckDataValidity:
    def test_valid_csv(self, c, sample_csv):
        assert c.check_data_validity(sample_csv) is True

    def test_non_csv(self, c, tmp_path):
        p = tmp_path / "blob.bin"
        p.write_bytes(b"\x00\x01\x02\xff" * 2000)
        assert c.check_data_validity(str(p)) is False


class TestGetLastRow:
    def test_returns_last_line(self, c, sample_csv):
        assert c.get_last_row(sample_csv).strip() == "167774208,167774463,US,United States"


class TestGetLastCsvRowSafe:
    def test_returns_parsed_last_row(self, c, sample_csv):
        row = c.get_last_csv_row_safe(sample_csv)
        assert row[0] == "167774208" and row[2] == "US"


# ---------------------------------------------------------------- end-to-end convert_to_csv
class TestConvertToCsv:
    def test_range_replace(self, c, sample_csv, tmp_path):
        out = str(tmp_path / "out.csv")
        c.convert_to_csv(sample_csv, out, "range", "replace")
        with open(out, encoding="utf-8") as f:
            rows = list(csv.reader(f))
        assert rows[0][:2] == ["10.0.0.0", "10.0.7.255"]
        assert rows[0][2:] == ["US", "United States"]
        assert len(rows) == 2

    def test_cidr_append(self, c, sample_csv, tmp_path):
        out = str(tmp_path / "out.csv")
        c.convert_to_csv(sample_csv, out, "cidr", "append")
        with open(out, encoding="utf-8") as f:
            rows = list(csv.reader(f))
        assert rows[0][2] == "10.0.0.0/21"

    def test_skips_non_numeric_rows(self, c, tmp_path):
        src = tmp_path / "mixed.csv"
        src.write_text("ip_from,ip_to\n167772160,167774207\n", encoding="utf-8")
        out = str(tmp_path / "out.csv")
        c.convert_to_csv(str(src), out, "range", "replace")
        with open(out, encoding="utf-8") as f:
            rows = list(csv.reader(f))
        assert len(rows) == 1
        assert rows[0][0] == "10.0.0.0"

    def test_output_file_created(self, c, sample_csv, tmp_path):
        out = str(tmp_path / "out.csv")
        assert not os.path.exists(out)
        c.convert_to_csv(sample_csv, out, "range", "replace")
        assert os.path.exists(out)
