from __future__ import annotations
import xml.etree.ElementTree as ET
from .db import connect

NODE_TAG = "{http://graphml.graphdrawing.org/xmlns}node"
EDGE_TAG = "{http://graphml.graphdrawing.org/xmlns}edge"
DATA_TAG = "{http://graphml.graphdrawing.org/xmlns}data"

KEYMAP={
    "d0":"bipartite","d1":"path","d2":"domain","d3":"category","d4":"subcategory",
    "d5":"lang","d6":"url","d7":"network","d8":"node_type","d9":"value"
}

def ingest(path: str, db_path: str | None = None) -> tuple[int,int]:
    con=connect(db_path)
    node_rows=[]; edge_rows=[]; n=e=0
    for _, elem in ET.iterparse(path, events=("end",)):
        if elem.tag == NODE_TAG:
            vals={KEYMAP.get(ch.attrib.get("key"),ch.attrib.get("key")): (ch.text or "") for ch in elem if ch.tag==DATA_TAG}
            node_rows.append((elem.attrib["id"], int(vals.get("bipartite")) if vals.get("bipartite") else None,
                              vals.get("node_type"), vals.get("domain"), vals.get("path"), vals.get("category"),
                              vals.get("subcategory"), vals.get("lang"), vals.get("url"), vals.get("value"), vals.get("network")))
            n += 1
            if len(node_rows)>=2000:
                con.executemany("INSERT OR REPLACE INTO graph_nodes(node_id,bipartite,node_type,domain,path,category,subcategory,lang,url,value,network) VALUES(?,?,?,?,?,?,?,?,?,?,?)", node_rows); node_rows.clear()
            elem.clear()
        elif elem.tag == EDGE_TAG:
            edge_rows.append((elem.attrib["source"], elem.attrib["target"]))
            e += 1
            if len(edge_rows)>=5000:
                con.executemany("INSERT OR IGNORE INTO graph_edges(source,target) VALUES(?,?)", edge_rows); edge_rows.clear()
            elem.clear()
    if node_rows: con.executemany("INSERT OR REPLACE INTO graph_nodes(node_id,bipartite,node_type,domain,path,category,subcategory,lang,url,value,network) VALUES(?,?,?,?,?,?,?,?,?,?,?)", node_rows)
    if edge_rows: con.executemany("INSERT OR IGNORE INTO graph_edges(source,target) VALUES(?,?)", edge_rows)
    con.commit(); con.close(); return n,e
