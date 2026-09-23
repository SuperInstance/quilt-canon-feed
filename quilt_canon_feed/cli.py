"""CLI for quilt-canon-feed."""
import argparse
import sys
from pathlib import Path

from .generator import canon_to_rss, canon_to_atom, canon_to_jsonfeed, get_recent


def cmd_rss(args):
    pieces = get_recent(args.limit)
    xml = canon_to_rss(pieces, title=args.title, link=args.link, description=args.description)
    if args.output:
        Path(args.output).write_text(xml)
        print(f"✓ RSS feed → {args.output} ({len(pieces)} items)")
    else:
        sys.stdout.write(xml)


def cmd_atom(args):
    pieces = get_recent(args.limit)
    xml = canon_to_atom(pieces, title=args.title, link=args.link, description=args.description)
    if args.output:
        Path(args.output).write_text(xml)
        print(f"✓ Atom feed → {args.output} ({len(pieces)} items)")
    else:
        sys.stdout.write(xml)


def cmd_jsonfeed(args):
    pieces = get_recent(args.limit)
    json_str = canon_to_jsonfeed(pieces, title=args.title, link=args.link, description=args.description)
    if args.output:
        Path(args.output).write_text(json_str)
        print(f"✓ JSON Feed → {args.output} ({len(pieces)} items)")
    else:
        sys.stdout.write(json_str)


def cmd_serve(args):
    """Serve the feed on a local HTTP server."""
    import http.server
    import socketserver

    pieces = get_recent(args.limit)
    rss = canon_to_rss(pieces, title=args.title, link=args.link, description=args.description)
    atom = canon_to_atom(pieces, title=args.title, link=args.link, description=args.description)
    jf = canon_to_jsonfeed(pieces, title=args.title, link=args.link, description=args.description)

    base_dir = Path(args.dir).resolve()
    base_dir.mkdir(parents=True, exist_ok=True)
    (base_dir / "feed.xml").write_text(rss)
    (base_dir / "feed.atom").write_text(atom)
    (base_dir / "feed.json").write_text(jf)
    print(f"✓ Wrote 3 feeds to {base_dir}")
    print(f"  Serving on http://localhost:{args.port}/")

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(base_dir), **kw)

    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        httpd.serve_forever()


def main():
    p = argparse.ArgumentParser(description="quilt-canon-feed — RSS/Atom/JSON feed for canon")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--title", default="Quilt Canon")
    p.add_argument("--link", default="https://superinstance.dev/canon")
    p.add_argument("--description", default="Substrate walker canon lore")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_r = sub.add_parser("rss", help="Generate RSS 2.0 feed")
    p_r.add_argument("--output", help="Output file (default: stdout)")
    p_r.set_defaults(func=cmd_rss)

    p_a = sub.add_parser("atom", help="Generate Atom 1.0 feed")
    p_a.add_argument("--output", help="Output file (default: stdout)")
    p_a.set_defaults(func=cmd_atom)

    p_j = sub.add_parser("json", help="Generate JSON Feed v1")
    p_j.add_argument("--output", help="Output file (default: stdout)")
    p_j.set_defaults(func=cmd_jsonfeed)

    p_s = sub.add_parser("serve", help="Serve feeds via HTTP")
    p_s.add_argument("--port", type=int, default=8766)
    p_s.add_argument("--dir", default="./canon-feeds")
    p_s.set_defaults(func=cmd_serve)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
