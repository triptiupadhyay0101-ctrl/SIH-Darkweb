import argparse, json, os, sys
from .db import init_db, connect
from .probe import probe, probe_batch
from .ingest_tor_metrics import ingest as ingest_metrics
from .ingest_graphml import ingest as ingest_graph
from .ingest_agora import ingest as ingest_agora
from .classify import classify
from .export import export_json, export_csv, export_report
from .temporal import analyze_target_history

def main():
    ap=argparse.ArgumentParser(description="SIH Dark-Web Cybersecurity & Infrastructure Intelligence Module")
    sub=ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init-db")
    p=sub.add_parser("probe"); p.add_argument("target")
    p=sub.add_parser("probe-batch"); p.add_argument("file", help="text file, one .onion address per line")
    p=sub.add_parser("ingest-tor-metrics"); p.add_argument("path")
    p=sub.add_parser("ingest-graphml"); p.add_argument("path")
    p=sub.add_parser("ingest-agora"); p.add_argument("path")
    p=sub.add_parser("classify"); p.add_argument("text")
    p=sub.add_parser("report")
    p=sub.add_parser("export-json"); p.add_argument("out")
    p=sub.add_parser("export-csv"); p.add_argument("out")
    p=sub.add_parser("export-report"); p.add_argument("out")
    p=sub.add_parser("history"); p.add_argument("target")
    args=ap.parse_args()
    if args.cmd=="init-db":
        init_db(); print("Database initialized")
    elif args.cmd=="probe":
        init_db(); print(json.dumps(probe(args.target), indent=2))
    elif args.cmd=="probe-batch":
        init_db()
        with open(args.file) as f:
            targets=[line.strip() for line in f]
        results=probe_batch(targets)
        print(json.dumps(results, indent=2))
        ok=sum(1 for r in results if "error" not in r)
        print(f"\n{ok}/{len(results)} targets probed successfully", file=sys.stderr)
    elif args.cmd=="ingest-tor-metrics":
        init_db(); print(f"Imported {ingest_metrics(args.path)} Tor metric rows")
    elif args.cmd=="ingest-graphml":
        init_db(); n,e=ingest_graph(args.path); print(f"Imported {n} nodes and {e} edges")
    elif args.cmd=="ingest-agora":
        init_db(); print(f"Imported {ingest_agora(args.path)} Agora listings")
    elif args.cmd=="classify":
        print(json.dumps(classify(args.text), indent=2))
    elif args.cmd=="report":
        init_db(); con=connect();
        out={
          "observations": con.execute("SELECT COUNT(*) FROM observations").fetchone()[0],
          "indicators": con.execute("SELECT COUNT(*) FROM indicators").fetchone()[0],
          "tor_metric_days": con.execute("SELECT COUNT(*) FROM tor_metrics").fetchone()[0],
          "graph_nodes": con.execute("SELECT COUNT(*) FROM graph_nodes").fetchone()[0],
          "graph_edges": con.execute("SELECT COUNT(*) FROM graph_edges").fetchone()[0],
        }
        try:
            out["agora_listings"] = con.execute("SELECT COUNT(*) FROM agora_listings").fetchone()[0]
        except Exception:
            out["agora_listings"] = 0
        con.close(); print(json.dumps(out, indent=2))
    elif args.cmd=="export-json":
        init_db(); path=export_json(args.out); print(f"Wrote {path}")
    elif args.cmd=="export-csv":
        init_db(); path=export_csv(args.out); print(f"Wrote {path}")
    elif args.cmd=="export-report":
        init_db(); path=export_report(args.out); print(f"Wrote {path}")
    elif args.cmd=="history":
        init_db(); print(json.dumps(analyze_target_history(args.target), indent=2))

if __name__=="__main__": main()
