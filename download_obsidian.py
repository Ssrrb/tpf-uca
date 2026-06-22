#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27",
#   "rich>=13.7",
# ]
# ///

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote, urlparse

import httpx
from rich.console import Console
from rich.table import Table


DEFAULT_URL = (
    "https://www.egrpy.org/050+Base+de+Conocimientos/200++Mi+Zettelkasten/100+Docencia/Ingenier%C3%ADa+del+Software+1/Clase+13+Diagrama+de+Clases+(Fundamentos%2C+Elementos%2C+Relaciones%2C+etc.)/Zk+!MOC+Diagrama+de+Clases+(Fundamentos%2C+Elementos%2C+Relaciones%2C+etc.)"
)

DEFAULT_SCOPE_ROOT = (
    "050 Base de Conocimientos/200  Mi Zettelkasten/100 Docencia/"
    "Ingeniería del Software 1/Trabajos Prácticos/2026 TPF"
)

WIKI_LINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
SITE_INFO_RE = re.compile(r"window\.siteInfo\s*=\s*(\{.*?\});", re.DOTALL)
PRELOAD_PAGE_RE = re.compile(r'window\.preloadPage\s*=\s*f\("([^"]+)"\)')


class DownloadError(RuntimeError):
    pass


@dataclass(frozen=True)
class SiteInfo:
    uid: str
    host: str
    start_path: str


def normalize_page_url(url: str) -> str:
    """Convert copied Obsidian Publish URLs with '+' path spaces into valid URLs."""
    parsed = urlparse(url)
    normalized_path = quote(unquote(parsed.path.replace("+", " ")), safe="/!()–-._~")
    rebuilt = parsed._replace(path=normalized_path)
    return rebuilt.geturl()


def vault_path_from_access_url(url: str, uid: str) -> str:
    marker = f"/access/{uid}/"
    parsed = urlparse(url)
    if marker not in parsed.path:
        raise DownloadError(f"Could not find {marker!r} in preload page URL")
    raw_path = parsed.path.split(marker, 1)[1]
    return unquote(raw_path)


def fetch_site_info(client: httpx.Client, url: str) -> SiteInfo:
    response = client.get(normalize_page_url(url))
    response.raise_for_status()
    html = response.text

    site_match = SITE_INFO_RE.search(html)
    page_match = PRELOAD_PAGE_RE.search(html)
    if not site_match or not page_match:
        raise DownloadError("Could not find Obsidian Publish metadata in the page shell")

    site_data = json.loads(site_match.group(1))
    uid = site_data["uid"]
    host = site_data.get("host") or "publish-01.obsidian.md"
    start_path = vault_path_from_access_url(page_match.group(1), uid)
    return SiteInfo(uid=uid, host=host, start_path=start_path)


def fetch_cache(client: httpx.Client, site: SiteInfo) -> dict[str, Any]:
    response = client.get(f"https://{site.host}/cache/{site.uid}")
    response.raise_for_status()
    return response.json()


def build_note_index(cache: dict[str, Any]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for path in cache:
        if not path.endswith(".md"):
            continue
        names = {
            path,
            path.removesuffix(".md"),
            Path(path).name,
            Path(path).stem,
        }
        for name in names:
            index.setdefault(name, []).append(path)
    return index


def wiki_targets(markdown: str) -> list[str]:
    targets: list[str] = []
    for match in WIKI_LINK_RE.finditer(markdown):
        raw = match.group(1).split("|", 1)[0].strip()
        note = raw.split("#", 1)[0].strip()
        if note:
            targets.append(note)
    return targets


def cache_targets(cache: dict[str, Any], path: str) -> list[str]:
    entry = cache.get(path) or {}
    links = entry.get("links") or []
    embeds = entry.get("embeds") or []
    return [item["link"].split("#", 1)[0] for item in [*links, *embeds] if item.get("link")]


def resolve_note(target: str, current_path: str, index: dict[str, list[str]]) -> str | None:
    candidates: list[str] = []
    clean = target.removesuffix(".md")

    if target.endswith(".md"):
        candidates.append(target)
    candidates.append(f"{clean}.md")
    candidates.append(clean)

    current_dir = str(Path(current_path).parent)
    candidates.append(f"{current_dir}/{clean}.md")

    for candidate in candidates:
        matches = index.get(candidate)
        if matches:
            return prefer_nearby(matches, current_path)
    return None


def prefer_nearby(matches: list[str], current_path: str) -> str:
    if len(matches) == 1:
        return matches[0]
    current_parts = Path(current_path).parts

    def score(path: str) -> tuple[int, int]:
        parts = Path(path).parts
        common = 0
        for left, right in zip(current_parts, parts):
            if left != right:
                break
            common += 1
        return (-common, len(parts))

    return sorted(matches, key=score)[0]


def access_url(site: SiteInfo, path: str) -> str:
    return f"https://{site.host}/access/{site.uid}/{quote(path, safe='/!()–-._~')}"


def fetch_markdown(client: httpx.Client, site: SiteInfo, path: str) -> str:
    response = client.get(access_url(site, path))
    response.raise_for_status()
    return response.text


def output_path(out_dir: Path, scope_root: str, vault_path: str, mirror_full_path: bool) -> Path:
    if mirror_full_path:
        relative = Path(vault_path)
    elif vault_path.startswith(scope_root.rstrip("/") + "/"):
        relative = Path(vault_path).relative_to(scope_root)
    else:
        relative = Path(Path(vault_path).name)
    return out_dir / relative


def crawl(
    client: httpx.Client,
    site: SiteInfo,
    cache: dict[str, Any],
    scope_root: str,
    include_all_wiki_links: bool,
) -> tuple[list[tuple[str, str]], list[str]]:
    index = build_note_index(cache)
    queue: deque[str] = deque([site.start_path])
    visited: set[str] = set()
    downloaded: list[tuple[str, str]] = []
    warnings: list[str] = []

    while queue:
        path = queue.popleft()
        if path in visited:
            continue
        visited.add(path)

        markdown = fetch_markdown(client, site, path)
        downloaded.append((path, markdown))

        targets = set(cache_targets(cache, path))
        targets.update(wiki_targets(markdown))
        for target in sorted(targets):
            resolved = resolve_note(target, path, index)
            if not resolved:
                warnings.append(f"Unresolved link in {path}: {target}")
                continue
            if not include_all_wiki_links and not resolved.startswith(scope_root.rstrip("/") + "/"):
                continue
            if resolved not in visited:
                queue.append(resolved)

    return downloaded, warnings


def write_files(
    pages: list[tuple[str, str]],
    out_dir: Path,
    scope_root: str,
    mirror_full_path: bool,
) -> list[Path]:
    written: list[Path] = []
    for vault_path, markdown in pages:
        destination = output_path(out_dir, scope_root, vault_path, mirror_full_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(markdown, encoding="utf-8")
        written.append(destination)
    return written


def print_pages(console: Console, pages: list[tuple[str, str]], out_dir: Path, scope_root: str, mirror_full_path: bool) -> None:
    table = Table(title="Obsidian pages")
    table.add_column("Vault path")
    table.add_column("Local path")
    for vault_path, _ in pages:
        local = output_path(out_dir, scope_root, vault_path, mirror_full_path)
        table.add_row(vault_path, str(local))
    console.print(table)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download an Obsidian Publish page tree as Markdown.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Obsidian Publish page URL to start from.")
    parser.add_argument("--out", default="obsidian-export", type=Path, help="Output directory.")
    parser.add_argument("--scope-root", default=DEFAULT_SCOPE_ROOT, help="Vault folder root to keep in scoped crawl mode.")
    parser.add_argument(
        "--scope",
        choices=["tpf-tree", "all-wiki-links"],
        default="tpf-tree",
        help="Crawl only the TPF folder tree or every internal wiki link recursively.",
    )
    parser.add_argument("--mirror-full-path", action="store_true", help="Mirror full vault paths under the output directory.")
    parser.add_argument("--dry-run", action="store_true", help="List pages that would be downloaded without writing files.")
    parser.add_argument(
        "--include-assets",
        action="store_true",
        help="Reserved for future use. Current version downloads Markdown pages only.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    console = Console()

    if args.include_assets:
        console.print("[yellow]--include-assets is not implemented yet; downloading Markdown pages only.[/yellow]")

    try:
        with httpx.Client(follow_redirects=True, timeout=30.0) as client:
            site = fetch_site_info(client, args.url)
            cache = fetch_cache(client, site)
            pages, warnings = crawl(
                client=client,
                site=site,
                cache=cache,
                scope_root=args.scope_root,
                include_all_wiki_links=args.scope == "all-wiki-links",
            )
    except (httpx.HTTPError, DownloadError, json.JSONDecodeError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return 1

    print_pages(console, pages, args.out, args.scope_root, args.mirror_full_path)
    for warning in warnings:
        console.print(f"[yellow]Warning:[/yellow] {warning}")

    if args.dry_run:
        console.print(f"[green]Dry run complete.[/green] {len(pages)} Markdown page(s) would be downloaded.")
        return 0

    written = write_files(pages, args.out, args.scope_root, args.mirror_full_path)
    console.print(f"[green]Done.[/green] Wrote {len(written)} Markdown page(s) to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
