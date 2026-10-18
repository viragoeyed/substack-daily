"""Refreshes data.json from the Substack feeds listed in feeds.json.
Standard library only. Run:  python fetch_feeds.py
"""
import json, re, html, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
NS = {"content": "http://purl.org/rss/1.0/modules/content/"}
PER_FEED = 8
PAID_HINT = re.compile(
    r"this post is for paid subscribers|keep reading with a \d+-day free trial|only visible to paid",
    re.I)


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, */*"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def parse(source, xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for it in list(root.iter("item"))[:PER_FEED]:
        link = (it.findtext("link") or "").strip()
        title = (it.findtext("title") or "").strip()
        if not link or not title:
            continue
        try:
            date = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone.utc).isoformat()
        except Exception:
            date = ""
        desc = strip_html(it.findtext("description"))
        body = it.findtext("content:encoded", namespaces=NS) or ""
        items.append({
            "source": source,
            "title": title,
            "link": link,
            "date": date,
            "snippet": desc[:180],
            "paid": bool(PAID_HINT.search(body + " " + desc)),
        })
    return items


def main():
    feeds = json.load(open("feeds.json", encoding="utf-8"))
    try:
        old = json.load(open("data.json", encoding="utf-8")).get("items", [])
    except Exception:
        old = []
    all_items = []
    for f in feeds:
        try:
            got = parse(f["name"], fetch(f["url"]))
            if not got:
                raise ValueError("no items")
            all_items += got
            print("ok  ", f["name"], len(got))
        except Exception as e:
            # keep yesterday's items for this source so the page never goes empty
            kept = [i for i in old if i["source"] == f["name"]]
            all_items += kept
            print("FAIL", f["name"], "-", e, "- kept", len(kept), "old items", file=sys.stderr)
    all_items.sort(key=lambda i: i["date"], reverse=True)
    json.dump({"updated": datetime.now(timezone.utc).isoformat(), "items": all_items},
              open("data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote data.json with", len(all_items), "items")


if __name__ == "__main__":
    main()
