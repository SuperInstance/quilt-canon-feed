# quilt-canon-feed

**RSS / Atom / JSON feeds for canon lore — streaming substrate.**

## Quick start

```bash
pip install -e .

# Generate RSS feed
quilt-canon-feed rss --output feed.xml

# Atom feed
quilt-canon-feed atom --output feed.atom

# JSON Feed v1
quilt-canon-feed json --output feed.json

# Serve all three on a local HTTP server
quilt-canon-feed serve --port 8766 --dir ./feeds

# Custom title/link
quilt-canon-feed rss --title "My Canon" --link "https://example.com" --limit 50
```

## What it generates

Three standard feed formats:
- **RSS 2.0** (`feed.xml`) — the classic blog feed format
- **Atom 1.0** (`feed.atom`) — IETF standard, modern replacement
- **JSON Feed v1** (`feed.json`) — modern JSON-based format

All three:
- Include the N most recent canon pieces (default 20)
- Use file modification time as pubDate
- Tag each entry with its doctrine anchors (`<category>` tags)
- Escape XML/HTML special characters
- Have valid feed structure

## Subscribe from anywhere

Any RSS reader (Feedly, NetNewsWire, etc.) can subscribe to the URL. The feed is also consumable by other AI agents via the standard feed protocol — useful for "canon updates" notifications.

## Fleet integration

- **`quilt-canon-search`** — sibling, full-text search
- **`quilt-canon-mcp`** — exposes canon as MCP tools
- **`quilt-canon-graph`** — sibling, knowledge graph
- **`quilt-canon-trace`** — walker trajectories
- **`quilt-canon-witness`** — cryptographic log

## The 5 bedrock doctrines

1. `cells_are_scars` — every cell records an attempted entry
2. `witness_log_is_prediction` — the log IS the prediction
3. `canon_gate_is_chord` — canon passes when multiple agents agree
4. `oracle_is_heard` — JEV probes canon with multi-model consensus
5. `substrate_quantum` — the substrate is the walker; canon is substrate-aware

## Polyformalism canary

```bash
python -m quilt_canon_feed.canary
# → 0x24a555471370b18d
```

## License

MIT
