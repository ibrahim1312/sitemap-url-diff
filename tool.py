"""Compare two local XML sitemaps to find URLs added or removed between site releases."""

import argparse
import json
from decimal import InvalidOperation
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description='Compare two local XML sitemaps to find URLs added or removed between site releases.')
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    args = parser.parse_args()
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

    def load(path):
        root = ET.parse(path).getroot()
        prefix = namespace if root.tag.startswith(namespace) else ""
        if root.tag != f"{prefix}urlset":
            raise ValueError(f"{path}: expected a urlset sitemap")
        urls, duplicate_urls = set(), set()
        for element in root.findall(f"{prefix}url"):
            url = (element.findtext(f"{prefix}loc") or "").strip()
            parsed = urlsplit(url)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname:
                raise ValueError(f"{path}: expected an absolute HTTP(S) URL, found {url!r}")
            if url in urls:
                duplicate_urls.add(url)
            urls.add(url)
        return urls, sorted(duplicate_urls)

    before, before_duplicates = load(args.before)
    after, after_duplicates = load(args.after)
    report = {"added": sorted(after - before), "removed": sorted(before - after),
              "duplicates_before": before_duplicates, "duplicates_after": after_duplicates}
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, OverflowError, InvalidOperation, TypeError, ET.ParseError) as error:
        raise SystemExit(f"Error: {error}") from None
