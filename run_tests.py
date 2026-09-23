"""Test runner for quilt-canon-feed (no pytest dep)."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/workspace/repos/quilt-canon-feed")

from quilt_canon_feed.canary import canary
from quilt_canon_feed.generator import canon_to_rss, canon_to_atom, canon_to_jsonfeed, get_recent
from quilt_canon_feed.loader import load_canon

results = []
failures = []


def test(name, func):
    try:
        func()
        results.append((name, "PASS"))
    except AssertionError as e:
        results.append((name, f"FAIL: {e}"))
        failures.append(name)
    except Exception as e:
        results.append((name, f"ERROR: {type(e).__name__}: {e}"))
        failures.append(name)


def t_canary():
    assert canary() == "0x24a555471370b18d"


def t_rss_basic():
    pieces = load_canon()[:3]
    xml = canon_to_rss(pieces)
    assert xml.startswith("<?xml")
    assert "<rss" in xml
    assert "<channel>" in xml
    assert "<title>Quilt Canon</title>" in xml
    assert len(pieces) <= 3


def t_rss_includes_items():
    pieces = load_canon()[:5]
    xml = canon_to_rss(pieces)
    assert xml.count("<item>") == len(pieces)
    # Should have at least one <category>
    assert "<category>" in xml


def t_atom_basic():
    pieces = load_canon()[:3]
    xml = canon_to_atom(pieces)
    assert xml.startswith("<?xml")
    assert "<feed xmlns=" in xml
    assert xml.count("<entry>") == len(pieces)


def t_jsonfeed_basic():
    import json
    pieces = load_canon()[:3]
    jf = canon_to_jsonfeed(pieces)
    data = json.loads(jf)
    assert data["version"] == "https://jsonfeed.org/version/1.1"
    assert data["title"] == "Quilt Canon"
    assert len(data["items"]) == len(pieces)


def t_get_recent():
    pieces = get_recent(10)
    assert len(pieces) <= 10
    if len(pieces) >= 2:
        # Should be sorted by mtime (newest first)
        mtimes = [p.path.stat().st_mtime for p in pieces]
        assert mtimes == sorted(mtimes, reverse=True)


def t_rss_xml_escapes():
    """Special characters should be escaped."""
    from unittest.mock import MagicMock
    p = MagicMock()
    p.title = "A & B <c>"
    p.body = "X & Y"
    p.doctrines_hit = []
    p.name = "test"
    p.path.stat.return_value.st_mtime = 1234567890
    xml = canon_to_rss([p])
    assert "A &amp; B &lt;c&gt;" in xml


def test_rss_output_to_file(tmp):
    pieces = load_canon()[:2]
    out = tmp / "feed.xml"
    xml = canon_to_rss(pieces)
    out.write_text(xml)
    assert out.exists()
    content = out.read_text()
    assert "<rss" in content


with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)
    test("test_canary", t_canary)
    test("test_rss_basic", t_rss_basic)
    test("test_rss_includes_items", t_rss_includes_items)
    test("test_atom_basic", t_atom_basic)
    test("test_jsonfeed_basic", t_jsonfeed_basic)
    test("test_get_recent", t_get_recent)
    test("test_rss_xml_escapes", t_rss_xml_escapes)
    test("test_rss_output_to_file", lambda: test_rss_output_to_file(tmp))

print("\n=== quilt-canon-feed test results ===")
for name, status in results:
    print(f"  {status:60} {name}")

print(f"\n{len(results) - len(failures)}/{len(results)} passed")
if failures:
    sys.exit(1)
