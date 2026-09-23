# Canon — quilt-canon-feed

## What this tool is

A feed generator for canon lore. Emits RSS 2.0, Atom 1.0, and JSON Feed v1 — the three major feed formats. Other agents and humans can subscribe and get canon updates.

## How it proves itself

**It runs.** `pip install -e .` then `quilt-canon-feed rss --output feed.xml`. Tested with 8 tests in `run_tests.py`.

**It polyformalisms.** The canary hash `0x24a555471370b18d` matches across the fleet's 5 ports.

**It measures.** Each entry has pubDate (file mtime), categories (doctrines), and a stable guid. Subscribers can detect new canon vs duplicates.

## Doctrines it instantiates

- **cells_are_scars** — every entry in the feed IS a scar (canon piece with attempted entry)
- **oracle_is_heard** — the feed IS the oracle broadcast; subscribers hear canon
- **substrate_quantum** — adds the streaming substrate

## Commands

1. `rss [--output FILE]` — RSS 2.0 feed
2. `atom [--output FILE]` — Atom 1.0 feed
3. `json [--output FILE]` — JSON Feed v1
4. `serve [--port PORT] [--dir DIR]` — serve all three via HTTP

## Fleet usage

- **`quilt-canon-search`** — sibling
- **`quilt-canon-mcp`** — sibling
- **`quilt-canon-graph`** — sibling
- **`quilt-canon-trace`** — sibling
- **`quilt-canon-witness`** — sibling
- **`quilt-canon-keywords`** — sibling

## Why feeds?

Feeds let any agent or human:
- Subscribe to canon updates automatically
- Track canon evolution over time
- Get notified when new canon is added
- Pull canon into their own systems (WordPress, Hugo, custom readers, etc.)

The substrate gains a heartbeat.
