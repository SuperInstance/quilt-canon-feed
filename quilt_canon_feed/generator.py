"""RSS 2.0 + Atom 1.0 feed generator for canon lore.

Emits a feed of canon pieces (newest first). Other agents can subscribe
and get canon updates automatically.
"""
import html
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from .loader import DOCTRINES, load_canon


def _rfc2822(dt: datetime) -> str:
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def _iso8601(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def canon_to_rss(pieces: List, title: str = "Quilt Canon",
                 link: str = "https://superinstance.dev/canon",
                 description: str = "Substrate walker canon lore") -> str:
    """Build an RSS 2.0 feed of canon pieces (newest first)."""
    items_xml = []
    for p in pieces:
        # Use file modification time as pubDate; fallback to NOW
        try:
            mtime = p.path.stat().st_mtime
            pub_dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
        except Exception:
            pub_dt = datetime.now(timezone.utc)

        title_safe = html.escape(p.title)
        link_safe = f"{link}/{html.escape(p.name)}"
        desc_safe = html.escape((p.body[:500] + "...") if len(p.body) > 500 else (p.body or ""))
        categories = "".join(f"<category>{html.escape(d)}</category>" for d in p.doctrines_hit)

        items_xml.append(f"""
    <item>
      <title>{title_safe}</title>
      <link>{link_safe}</link>
      <guid isPermaLink="false">canon-{html.escape(p.name)}</guid>
      <pubDate>{_rfc2822(pub_dt)}</pubDate>
      <description>{desc_safe}</description>
      {categories}
    </item>""")

    last_build = datetime.now(timezone.utc)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{html.escape(title)}</title>
  <link>{html.escape(link)}</link>
  <description>{html.escape(description)}</description>
  <language>en</language>
  <lastBuildDate>{_rfc2822(last_build)}</lastBuildDate>
  <atom:link href="{html.escape(link)}/feed.xml" rel="self" type="application/rss+xml" />
  {"".join(items_xml)}
</channel>
</rss>"""


def canon_to_atom(pieces: List, title: str = "Quilt Canon",
                  link: str = "https://superinstance.dev/canon",
                  description: str = "Substrate walker canon lore") -> str:
    """Build an Atom 1.0 feed."""
    feed_id = f"{link}/feed.atom"
    now = datetime.now(timezone.utc)

    entries = []
    for p in pieces:
        try:
            mtime = p.path.stat().st_mtime
            pub_dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
        except Exception:
            pub_dt = now

        title_safe = html.escape(p.title)
        entry_id = f"{link}/{html.escape(p.name)}"
        summary_safe = html.escape((p.body[:500] + "...") if len(p.body) > 500 else (p.body or ""))
        categories = "".join(f'<category term="{html.escape(d)}" />' for d in p.doctrines_hit)

        entries.append(f"""
  <entry>
    <title>{title_safe}</title>
    <id>{entry_id}</id>
    <link href="{entry_id}" />
    <updated>{_iso8601(pub_dt)}</updated>
    <published>{_iso8601(pub_dt)}</published>
    <summary>{summary_safe}</summary>
    {categories}
  </entry>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{html.escape(title)}</title>
  <id>{feed_id}</id>
  <link href="{html.escape(link)}" />
  <updated>{_iso8601(now)}</updated>
  <subtitle>{html.escape(description)}</subtitle>
  {"".join(entries)}
</feed>"""


def canon_to_jsonfeed(pieces: List, title: str = "Quilt Canon",
                      link: str = "https://superinstance.dev/canon",
                      description: str = "Substrate walker canon lore") -> str:
    """JSON Feed v1 format."""
    import json
    items = []
    for p in pieces:
        try:
            mtime = p.path.stat().st_mtime
            pub_dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
        except Exception:
            pub_dt = datetime.now(timezone.utc)

        items.append({
            "id": f"canon-{p.name}",
            "title": p.title,
            "url": f"{link}/{p.name}",
            "content_text": (p.body[:500] + "...") if len(p.body) > 500 else (p.body or ""),
            "date_published": _iso8601(pub_dt),
            "tags": p.doctrines_hit,
        })

    return json.dumps({
        "version": "https://jsonfeed.org/version/1.1",
        "title": title,
        "home_page_url": link,
        "feed_url": f"{link}/feed.json",
        "description": description,
        "items": items,
    }, indent=2)


def get_recent(n: int = 20, canon_dir=None) -> List:
    """Get the N most recent canon pieces."""
    pieces = load_canon(canon_dir)
    # Sort by file modification time (newest first)
    def mtime_key(p):
        try:
            return p.path.stat().st_mtime
        except Exception:
            return 0
    pieces.sort(key=mtime_key, reverse=True)
    return pieces[:n]
