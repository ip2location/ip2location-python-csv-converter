"""Edge cases for the CSV tail-row readers used by csv_to_parquet.

get_last_row() seeks from the end of the file, so it raises OSError on
files smaller than 2 bytes and misreads single-line files; csv_to_parquet
used to inherit both failures. It now uses get_last_csv_row_safe, whose
single-chunk fallback previously referenced an unimported `io` name.
"""
import pandas as pd
import pytest


class TestTailRowEdgeCases:
    def test_empty_file_returns_no_row(self, c, tmp_path):
        p = tmp_path / "empty.csv"
        p.write_bytes(b"")
        assert c.get_last_csv_row_safe(str(p)) == []

    def test_single_line_file_returns_parsed_row(self, c, tmp_path):
        p = tmp_path / "one.csv"
        p.write_text("167772160,167774207,US,United States\n", encoding="utf-8")
        row = c.get_last_csv_row_safe(str(p))
        assert row[0] == "167772160" and row[2] == "US"

    def test_parquet_from_single_line_csv(self, c, tmp_path):
        src = tmp_path / "one.csv"
        src.write_text("167772160,167774207,US,United States\n", encoding="utf-8")
        out = str(tmp_path / "one.parquet")
        c.csv_to_parquet(str(src), out, "DB1")
        df = pd.read_parquet(out)
        assert len(df) == 1
        assert df.iloc[0]["country_code"] == "US"

    def test_parquet_from_empty_csv_exits_cleanly(self, c, tmp_path):
        src = tmp_path / "empty.csv"
        src.write_bytes(b"")
        with pytest.raises(SystemExit):
            c.csv_to_parquet(str(src), str(tmp_path / "empty.parquet"), "DB1")
