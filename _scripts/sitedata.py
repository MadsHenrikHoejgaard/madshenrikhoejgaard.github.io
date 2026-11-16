"""
Reads the lists of writing for the pages that count, group or map it:
the figures on the home page, the Projects page and the map.

You should not need to edit this file. The content comes from
external.yml, the posts folder, _data/series.yml and _data/places.yml.
"""

import datetime
import html
import json
import math
import os
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def to_root():
    """Relative path from the page being built back to the site root."""
    rel = os.path.relpath(ROOT, Path.cwd())
    return "" if rel == "." else rel.replace(os.sep, "/") + "/"


def esc(text):
    return html.escape(str(text), quote=True)


def _date(value):
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    return datetime.date.fromisoformat(str(value).strip()[:10])


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value]
    return [str(value).strip()]


def _front_matter(qmd):
    text = qmd.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def writing():
    """All published pieces, newest first, as dictionaries."""
    base = to_root()
    items = []
    for e in yaml.safe_load((ROOT / "external.yml").read_text(encoding="utf-8")) or []:
        items.append({
            "title": e["title"],
            "href": e["path"],
            "outlet": e.get("outlet", ""),
            "date": _date(e["date"]),
            "description": e.get("description", ""),
            "series": _as_list(e.get("series")),
            "place": _as_list(e.get("place")),
        })
    for qmd in sorted((ROOT / "posts").glob("*/index.qmd")):
        meta = _front_matter(qmd)
        if meta.get("draft") or "date" not in meta:
            continue
        folder = qmd.parent.relative_to(ROOT).as_posix()
        items.append({
            "title": meta.get("title", folder),
            "href": f"{base}{folder}/index.html",
            "outlet": "",
            "date": _date(meta["date"]),
            "description": meta.get("description", ""),
            "series": _as_list(meta.get("series")),
            "place": _as_list(meta.get("place")),
        })
    items.sort(key=lambda i: i["date"], reverse=True)
    return items


def series():
    return yaml.safe_load((ROOT / "_data" / "series.yml").read_text(encoding="utf-8")) or []


def places():
    return yaml.safe_load((ROOT / "_data" / "places.yml").read_text(encoding="utf-8")) or []


def page_href(qmd_path):
    return to_root() + str(qmd_path).replace(".qmd", ".html")


def span(pieces):
    years = sorted({p["date"].year for p in pieces})
    if not years:
        return ""
    return str(years[0]) if years[0] == years[-1] else f"{years[0]}–{years[-1]}"


def count_words(n, one, many):
    return f"{n} {one if n == 1 else many}"


# ------------------------------------------------------------------
# Home page figures
# ------------------------------------------------------------------

def tally_html(figures):
    """figures: list of (number, label, link or None)."""
    cells = []
    for number, label, link in figures:
        num = f'<span class="tally-num">{esc(number)}</span>'
        lab = f'<span class="tally-label">{esc(label)}</span>'
        inner = f'<a href="{esc(link)}">{num}{lab}</a>' if link else num + lab
        cells.append(f'<li class="tally-item">{inner}</li>')
    return '<ul class="tally">' + "".join(cells) + "</ul>"


# ------------------------------------------------------------------
# Projects page
# ------------------------------------------------------------------

def series_overview_html(latest_n=3):
    items = writing()
    blocks = []
    for i, s in enumerate(series()):
        pieces = [p for p in items if s["id"] in p["series"]]
        href = page_href(s["page"])
        meta = f'{count_words(len(pieces), "piece", "pieces")}, {span(pieces)}' if pieces else "No pieces yet"
        latest = "".join(
            f'<li><a href="{esc(p["href"])}">{esc(p["title"])}</a></li>'
            for p in pieces[:latest_n]
        )
        cls = "series-block series-lead" if i == 0 else "series-block"
        blocks.append(
            f'<section class="{cls}" id="series-{esc(s["id"])}">'
            f'<h2 class="series-title"><a href="{esc(href)}">{esc(s["title"])}</a></h2>'
            f'<p class="series-meta">{esc(meta)}</p>'
            f'<p class="series-summary">{esc(s["summary"])}</p>'
            + (f'<p class="series-latest-label">Latest</p><ul class="series-latest">{latest}</ul>' if latest else "")
            + f'<p class="series-more"><a href="{esc(href)}">The whole series</a></p>'
            f'</section>'
        )
    lead, rest = blocks[0], blocks[1:]
    return lead + '<div class="series-grid">' + "".join(rest) + "</div>"


def series_meta(series_id):
    pieces = [p for p in writing() if series_id in p["series"]]
    return f'{count_words(len(pieces), "piece", "pieces")}, {span(pieces)}' if pieces else ""


# ------------------------------------------------------------------
# Map of the writing
# ------------------------------------------------------------------

def _project(lon, lat, m):
    lon0, lon1, lat0, lat1 = m["extent"]
    phi = math.radians(m["standard_parallel"])
    return ((lon - lon0) * math.cos(phi) * m["k"], (lat1 - lat) * m["k"])


def map_html():
    m = json.loads((ROOT / "_data" / "greece-map.json").read_text(encoding="utf-8"))
    items = writing()
    W, H = m["width"], m["height"]
    marks, labels, listing = [], [], []
    for pl in places():
        pieces = [p for p in items if pl["id"] in p["place"]]
        if not pieces:
            continue
        x, y = _project(float(pl["lon"]), float(pl["lat"]), m)
        n = len(pieces)
        r = 7 + 3.2 * math.sqrt(n - 1)
        anchor = f'place-{pl["id"]}'
        name = f'{pl["name"]} ({n})' if n > 1 else pl["name"]
        side = pl.get("label", "right")
        gap = r + 9
        if side == "left":
            tx, ty, ta = x - gap, y + 6, "end"
        elif side == "above":
            tx, ty, ta = x, y - gap - 2, "middle"
        elif side == "below":
            tx, ty, ta = x, y + gap + 16, "middle"
        else:
            tx, ty, ta = x + gap, y + 6, "start"
        what = count_words(n, "piece", "pieces")
        marks.append(
            f'<a href="#{anchor}" class="map-mark" aria-label="{esc(pl["name"])}: {what}">'
            f'<title>{esc(pl["name"])}: {what}</title>'
            f'<circle class="map-glow" cx="{x:.1f}" cy="{y:.1f}" r="{r + 9:.1f}"/>'
            f'<circle class="map-dot" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>'
            f'<text class="map-label" x="{tx:.1f}" y="{ty:.1f}" text-anchor="{ta}">{esc(name)}</text>'
            f'</a>'
        )
        rows = "".join(
            f'<li><a href="{esc(p["href"])}">{esc(p["title"])}</a>'
            f' <span class="map-year">{p["date"].year}</span></li>'
            for p in pieces
        )
        listing.append(
            f'<section class="map-place" id="{anchor}"><h3>{esc(pl["name"])}</h3><ul>{rows}</ul></section>'
        )
    svg = (
        f'<svg class="map-svg" viewBox="0 0 {W:.0f} {H:.1f}" role="img" '
        f'aria-labelledby="map-title map-desc" xmlns="http://www.w3.org/2000/svg">'
        f'<title id="map-title">Map of Greece with the places my writing is set</title>'
        f'<desc id="map-desc">Each dot is a place; the list below the map names the pieces.</desc>'
        f'<path class="map-neighbours" d="{m["neighbours"]}"/>'
        f'<path class="map-land" d="{m["greece"]}"/>'
        + "".join(marks)
        + "</svg>"
    )
    return (
        f'<figure class="map-figure">{svg}'
        f'<figcaption>Coastlines: Natural Earth, public domain. The map is drawn on this site; '
        f'it loads nothing from other websites.</figcaption></figure>'
        f'<div class="map-list">{"".join(listing)}</div>'
    )
