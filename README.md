# Sitemap URL Diff

Compare two local XML sitemaps to find URLs added or removed between site releases.

## Quick start

Requires Python 3.11 or later. Uses the standard library and runs locally.

```bash
python3 tool.py before.xml after.xml
```

Output is formatted JSON on standard output. Invalid inputs report an error on standard error and exit with status 1. Run the tool with --help for all arguments.

Accepts individual urlset documents. URLs are compared as written after trimming whitespace. Sitemap indexes and remote downloads are outside its scope.

## Example input

**before.xml**

```
<urlset><url><loc>https://example.com/a</loc></url></urlset>
```

**after.xml**

```
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.com/b</loc></url><url><loc>https://example.com/b</loc></url></urlset>
```

## Example output

```json
{
  "added": [
    "https://example.com/b"
  ],
  "removed": [
    "https://example.com/a"
  ],
  "duplicates_before": [],
  "duplicates_after": [
    "https://example.com/b"
  ]
}
```

## License

[MIT](LICENSE).
