"""Build the find-spot map: where Indus inscriptions were found, over schematic ancient waterways.

Writes static/findspot_map.html (a standalone page, also shown in the app on the
"Find-spot Map" page). Everything is drawn as inline SVG from Natural Earth
(public domain), so the page needs no map server and works offline.

Inscription counts use every record (both splits, site metadata only). "Has a
closer" is computed for EXPLORATION texts only; holdout texts are counted but
their signs are never read.

    python scripts/findspot_map.py /path/to/natural_earth_geojson [out.html] [body_only.html]
"""

import html
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from findspot_routes import ABROAD, HOME_EXTRA, SEA_ROUTE  # noqa: E402
from functional_skeleton import assign  # noqa: E402
from functional_slots import load  # noqa: E402
from indus_workbench import data  # noqa: E402

LAT0, LAT1, LON0, LON1 = 15.0, 42.0, 42.0, 80.0
K = 30.0
COS = math.cos(math.radians(29))
W, H = (LON1 - LON0) * COS * K, (LAT1 - LAT0) * K


def xy(lat, lon):
    return round((lon - LON0) * COS * K, 1), round((LAT1 - lat) * K, 1)


def path_d(pts, close=False):
    if len(pts) < 2:
        return ""
    s = "M" + " L".join(f"{x},{y}" for x, y in pts)
    return s + (" Z" if close else "")


def thin(coords, step=0.06):
    out, last = [], None
    for lon, lat in coords:
        if last is None or abs(lon - last[0]) + abs(lat - last[1]) >= step:
            out.append((lon, lat))
            last = (lon, lat)
    return out


def in_box(coords, pad=3):
    a = np.array(coords)
    return (a[:, 0].max() > LON0 - pad and a[:, 0].min() < LON1 + pad and
            a[:, 1].max() > LAT0 - pad and a[:, 1].min() < LAT1 + pad)


def land_paths(path):
    g = json.loads(Path(path).read_text())
    ds = []
    for f in g["features"]:
        geom = f["geometry"]
        polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
        for poly in polys:
            ring = [c[:2] for c in poly[0]]
            if len(ring) < 4 or not in_box(ring):
                continue
            ds.append(path_d([xy(la, lo) for lo, la in thin(ring)], close=True))
    return " ".join(d for d in ds if d)


def river_paths(path):
    g = json.loads(Path(path).read_text())
    out = []
    for f in g["features"]:
        if not f["geometry"] or f["properties"].get("featurecla") != "River":
            continue
        t, c = f["geometry"]["type"], f["geometry"]["coordinates"]
        for ln in ([c] if t == "LineString" else c):
            ln = [p[:2] for p in ln]
            if in_box(ln, 0):
                out.append(path_d([xy(la, lo) for lo, la in thin(ln, 0.03)]))
    return " ".join(out)


def site_stats():
    raw, _ = data.load_raw("indus_website")
    every = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"),
                              drop_damaged=False, dedupe=False, drop_unidentified=False).df
    total = every["site"].value_counts()
    hold = every[every["split"] == "holdout"]["site"].value_counts()
    ex = load()  # exploration texts used in the analyses (damaged dropped, duplicates removed)
    roles, _ = assign(list(ex["signs"]))
    ex = ex.assign(has_closer=[any(roles.get(x) == 2 for x in s) for s in ex["signs"]])
    g = ex.groupby("site")["has_closer"].agg(["size", "sum"])
    return total, hold, g


def main(ne_dir, out=None):
    ne = Path(ne_dir)
    total, hold, g = site_stats()
    coords = pd.read_csv(ROOT / "data" / "site_coordinates.csv")
    home = {r.site: (r.lat, r.lon, "Wikipedia (data/site_coordinates.csv)") for r in coords.itertuples()}
    home.update(HOME_EXTRA)
    fw = json.loads((ROOT / "results" / "findspots_waterways.json").read_text())
    dist = {r["site"]: r for r in fw["findspots"]}

    sites = []
    for s, n in total.items():
        if s in ABROAD:
            la, lo, region, route, src = ABROAD[s]
            kind = "abroad"
        elif s in home:
            la, lo, src = home[s]
            region, route, kind = "Indus region", "home", "home"
        else:
            continue
        e = g.loc[s] if s in g.index else None
        sites.append(dict(name=s, kind=kind, region=region, route=route, n=int(n), hold=int(hold.get(s, 0)),
                          ex=int(e["size"]) if e is not None else 0, closer=int(e["sum"]) if e is not None else 0,
                          src=src, approx=src.lower().startswith(("approx", "region")),
                          sea=round(dist.get(s, {}).get("km_to_sea", float("nan"))),
                          river=round(dist.get(s, {}).get("km_to_major_river", float("nan"))),
                          x=xy(la, lo)[0], y=xy(la, lo)[1]))
    no_coords = int(sum(n for s, n in total.items() if s not in ABROAD and s not in home))

    def rate(kind):
        a = [x for x in sites if x["kind"] == kind]
        return sum(x["closer"] for x in a), sum(x["ex"] for x in a)
    hc, hn = rate("home")
    ac, an = rate("abroad")

    # Schematic routes and channels (approximate; see caption)
    anc = json.loads((ROOT / "data" / "ancient_waterways.json").read_text())
    P = lambda pts: path_d([xy(a, b) for a, b in pts])  # noqa: E731
    sea_main = P([(a, b) for _, a, b in SEA_ROUTE])
    spurs = [
        [(26.6, 52.0), (26.2, 50.55)],                       # to Dilmun (Bahrain)
        [(22.53, 59.80), (22.85, 57.35)],                    # inland Magan (Salut)
        [(31.0, 46.3), (30.96, 46.10), (31.67, 45.89), (32.54, 44.60)],  # up the Euphrates: Ur, Umma, Kish
        [(31.0, 46.3), (31.32, 48.67), (32.19, 48.26)],      # to Susa via the Karun plain
    ]
    oxus = P([(30.629, 72.864), (34.01, 71.58), (34.53, 69.17), (36.73, 68.86), (37.325, 69.525)])
    khorasan = [[(27.329, 68.139), (29.6, 67.4), (30.18, 67.0), (31.61, 65.71), (34.35, 62.20), (38.21, 62.035)],
                [(34.35, 62.20), (36.858, 60.432)]]
    short = {"hakra": ("Hakra", 28.35, 72.3), "nara": ("older Nara bed", 26.9, 69.3),
             "euphrates": ("Euphrates then", 32.35, 44.0), "gulfhead": ("Gulf c. 3000 BCE?", 30.75, 48.75),
             "greatrann": ("Rann: shallow sea?", 24.85, 69.6), "murghab": ("old Murghab", 37.75, 62.2),
             "lothal": ("tidal channel", 22.15, 72.5)}

    def anc_feature(i, f):
        pts = [(a, b) for a, b, _ in f["points"]]
        d = path_d([xy(a, b) for a, b in pts], close=f["kind"] == "area")
        cls = "anc-area" if f["kind"] == "area" else ("anc-line old" if f["id"] == "nara" else "anc-line")
        lab = ""
        if f["id"] in short:
            t, a, b = short[f["id"]]
            lab = f'<text class="anclabel" x="{xy(a, b)[0]}" y="{xy(a, b)[1]}">{html.escape(t)}</text>'
        return (f'<g class="anc" tabindex="0" role="button" data-f="{i}" aria-label="{html.escape(f["name"])}">'
                f'<path class="{cls}" d="{d}"></path><path class="hit" d="{d}"></path>{lab}</g>')
    feats = anc["features"]
    anc_svg = "".join(anc_feature(i, f) for i, f in enumerate(feats) if f["kind"] == "area") + \
        "".join(anc_feature(i, f) for i, f in enumerate(feats) if f["kind"] == "line")

    labels = [  # ancient names, placed by hand
        ("Meluhha", "the Indus civilisation", 25.2, 70.6),
        ("Magan", "Oman", 21.0, 57.0),
        ("Dilmun", "Bahrain", 25.0, 49.6),
        ("Sumer & Akkad", "", 34.3, 42.6),
        ("Elam", "", 33.3, 49.3),
        ("Bactria", "", 38.3, 68.0),
        ("Margiana", "", 39.4, 61.2),
        ("Arabian Sea", "", 19.0, 63.5),
        ("Persian Gulf", "", 27.6, 51.4),
    ]

    land = land_paths(ne / "ne_50m_land.geojson")
    rivers = river_paths(ne / "ne_50m_rivers_lake_centerlines.geojson")

    def circ(s):
        r = round(2.2 + 2.2 * math.sqrt(s["n"]), 1) if s["kind"] == "home" else 6.5
        r = min(r, 34)
        lacks = s["ex"] - s["closer"]
        tip = html.escape(s["name"])
        return (f'<g class="site {s["kind"]}" tabindex="0" role="button" data-i="{sites.index(s)}" aria-label="{tip}">'
                f'<circle cx="{s["x"]}" cy="{s["y"]}" r="{r}"></circle>'
                + (f'<circle class="ring" cx="{s["x"]}" cy="{s["y"]}" r="{r + 3.5}"></circle>'
                   if s["kind"] == "abroad" and s["ex"] and lacks == s["ex"] else "")
                + f'<text class="sitelabel" x="{s["x"] + r + 3}" y="{s["y"] + 3}">{tip}</text></g>')

    order = sorted(sites, key=lambda s: -s["n"])
    svg = f"""<svg id="map" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="Map of Indus inscription find-spots">
<defs><clipPath id="frame"><rect width="{W:.0f}" height="{H:.0f}"></rect></clipPath></defs>
<g clip-path="url(#frame)">
<rect class="sea" width="{W:.0f}" height="{H:.0f}"></rect>
<path class="land" d="{land}"></path>
<g data-layer="rivers"><path class="river" d="{rivers}"></path></g>
<g data-layer="ancient">{anc_svg}</g>
<g data-layer="sea"><path class="searoute" d="{sea_main}"></path>{''.join(f'<path class="searoute spur" d="{P(s)}"></path>' for s in spurs)}</g>
<g data-layer="land"><path class="landroute" d="{oxus}"></path>{''.join(f'<path class="landroute" d="{P(s)}"></path>' for s in khorasan)}</g>
<g class="labels">{''.join(f'<text class="region" x="{xy(a, b)[0]}" y="{xy(a, b)[1]}">{html.escape(t)}{f"<tspan class=sub dx=4>{html.escape(u)}</tspan>" if u else ""}</text>' for t, u, a, b in labels)}</g>
<g class="sites">{''.join(circ(s) for s in order)}</g>
</g></svg>"""

    data_js = json.dumps(sites)
    page = TEMPLATE.replace("%%SVG%%", svg).replace("%%DATA%%", data_js).replace("%%ANC%%", json.dumps(feats)) \
        .replace("%%NOTDRAWN%%", " ".join(html.escape(x) for x in anc["not_drawn"])) \
        .replace("%%HC%%", str(hc)).replace("%%HN%%", str(hn)).replace("%%AC%%", str(ac)).replace("%%AN%%", str(an)) \
        .replace("%%HP%%", f"{hc / hn:.0%}").replace("%%AP%%", f"{ac / an:.0%}") \
        .replace("%%NOC%%", str(no_coords)).replace("%%NAB%%", str(sum(s['n'] for s in sites if s['kind'] == 'abroad')))
    out = Path(out) if out else ROOT / "static" / "findspot_map.html"
    head = ('<!doctype html>\n<html lang="en"><meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
    out.write_text(head + page)  # standalone page
    if len(sys.argv) > 3: Path(sys.argv[3]).write_text(page)  # optional body-only copy for hosts that add their own skeleton
    print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB); {len(sites)} find-spots; "
          f"closer: home {hc}/{hn}, abroad {ac}/{an}")


TEMPLATE = r"""<title>Indus Find-spot Map</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Karla:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a field map. Title band, the map as the one big object, a legend strip and a details card below. */
:root {
  --ground: #f3ece0;   /* page: unfired clay */
  --ink: #2e2118;      /* umber */
  --muted: #6d5b4b;
  --sea: #dfe6ea;
  --land: #e8dcc6;
  --coast: #b9a587;
  --river: #4b7fa3;
  --home: #a4442a;     /* carnelian */
  --abroad: #2f4a7a;   /* lapis */
  --route-sea: #2f4a7a;
  --route-land: #a8742a;
  --rule: #d8cab3;
  --card: #fbf7f0;
  --then: #1f7f78;     /* water then: verdigris */
  --then-ink: #145b56;
  --display: "Cormorant Garamond", Georgia, serif;
  --body: "Karla", "Segoe UI", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --ground: #1d1814; --ink: #efe5d6; --muted: #b5a48f; --sea: #17212b; --land: #2c241d; --coast: #5c4c3c;
  --river: #6fa6cc; --home: #e0795c; --abroad: #8fb0e6; --route-sea: #8fb0e6; --route-land: #d9a55a;
  --rule: #3d3229; --card: #261f19; --then: #4fbfb3; --then-ink: #8fe0d6; color-scheme: dark } }
:root[data-theme="dark"] {
  --ground: #1d1814; --ink: #efe5d6; --muted: #b5a48f; --sea: #17212b; --land: #2c241d; --coast: #5c4c3c;
  --river: #6fa6cc; --home: #e0795c; --abroad: #8fb0e6; --route-sea: #8fb0e6; --route-land: #d9a55a;
  --rule: #3d3229; --card: #261f19; --then: #4fbfb3; --then-ink: #8fe0d6; color-scheme: dark }
body { margin: 0; background: var(--ground); color: var(--ink); font-family: var(--body); font-size: 15px; line-height: 1.5;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 20px 40px; }
.wrap { max-width: 1100px; margin: 0 auto; display: grid; gap: 18px; }
h1 { font-family: var(--display); font-weight: 700; font-size: clamp(30px, 5vw, 46px); line-height: 1.05; margin: 0;
  text-wrap: balance; letter-spacing: 0.005em; }
.lede { margin: 6px 0 0; max-width: 64ch; color: var(--muted); }
.stats { display: flex; flex-wrap: wrap; gap: 10px 28px; font-variant-numeric: tabular-nums; }
.stat { display: grid; gap: 2px; min-width: 0; }
.stat b { font-family: var(--mono); font-weight: 500; font-size: 22px; }
.stat span { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); }
.stat.home b { color: var(--home); } .stat.abroad b { color: var(--abroad); }
.mapbox { position: relative; border: 1px solid var(--rule); border-radius: 4px; overflow: hidden; background: var(--sea);
  touch-action: none; }
#map { display: block; width: 100%; height: auto; cursor: grab; user-select: none; }
#map.dragging { cursor: grabbing; }
.sea { fill: var(--sea); }
.land { fill: var(--land); stroke: var(--coast); stroke-width: 0.8; stroke-linejoin: round; }
.river { fill: none; stroke: var(--river); stroke-width: 1.3; stroke-linecap: round; opacity: 0.85; }
.anc-line { fill: none; stroke: var(--then); stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
.anc-line.old { stroke-width: 2; stroke-dasharray: 2 5; opacity: 0.8; }
.anc-area { fill: var(--then); fill-opacity: 0.28; stroke: var(--then); stroke-width: 1.4; stroke-dasharray: 4 3; }
.anc .hit { fill: none; stroke: transparent; stroke-width: 14; }
.anc { cursor: pointer; outline: none; }
.anc:focus-visible .anc-line, .anc.sel .anc-line, .anc:focus-visible .anc-area, .anc.sel .anc-area { stroke: var(--ink); }
.anclabel { font: italic 600 12px var(--body); fill: var(--then-ink); paint-order: stroke; stroke: var(--land); stroke-width: 3px; }
.water { display: inline-flex; border: 1px solid var(--rule); border-radius: 3px; overflow: hidden; }
.water button { font: 600 13px var(--body); color: var(--ink); background: var(--card); border: 0; padding: 6px 12px; cursor: pointer; }
.water button + button { border-left: 1px solid var(--rule); }
.water button[aria-pressed="true"] { background: var(--then); color: var(--ground); }
.water button:focus-visible { outline: 2px solid var(--abroad); outline-offset: -2px; }
.bar { display: flex; flex-wrap: wrap; gap: 10px 18px; align-items: center; }
.bar .lbl { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); }
.searoute { fill: none; stroke: var(--route-sea); stroke-width: 2.4; stroke-dasharray: 9 6; opacity: 0.85; }
.searoute.spur { stroke-width: 1.6; }
.landroute { fill: none; stroke: var(--route-land); stroke-width: 2.2; stroke-dasharray: 3 5; stroke-linecap: round; opacity: 0.9; }
.note { font: italic 11px var(--body); fill: var(--muted); }
.region { font: 600 15px var(--display); fill: var(--muted); letter-spacing: 0.06em; text-transform: uppercase; paint-order: stroke;
  stroke: var(--land); stroke-width: 3px; }
.region .sub { font: italic 11px var(--body); text-transform: none; letter-spacing: 0; }
.site circle { stroke: var(--ground); stroke-width: 1.4; }
.site.home circle { fill: var(--home); fill-opacity: 0.6; }
.site.abroad circle { fill: var(--abroad); }
.site circle.ring { fill: none; stroke: var(--abroad); stroke-width: 1.4; stroke-dasharray: 2 2; }
.site { cursor: pointer; outline: none; }
.site:focus-visible circle:first-child, .site.sel circle:first-child { stroke: var(--ink); stroke-width: 2.5; }
.sitelabel { font: 500 10px var(--mono); fill: var(--ink); paint-order: stroke; stroke: var(--land); stroke-width: 3px; display: none; }
#map.zoomed .sitelabel, .site.sel .sitelabel, .site:hover .sitelabel { display: block; }
#map.zoomed .region { font-size: 10px; }
.tools { position: absolute; top: 10px; right: 10px; display: flex; flex-direction: column; gap: 6px; }
.tools button, .views button { font: 600 13px var(--body); color: var(--ink); background: var(--card); border: 1px solid var(--rule);
  border-radius: 3px; padding: 6px 10px; cursor: pointer; }
.tools button { width: 34px; padding: 4px 0; font-size: 18px; line-height: 1; }
.tools button:focus-visible, .views button:focus-visible, label:focus-within { outline: 2px solid var(--abroad); outline-offset: 2px; }
.views { display: flex; flex-wrap: wrap; gap: 8px; }
.views button[aria-pressed="true"] { background: var(--ink); color: var(--ground); }
.controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 18px; align-items: start; }
fieldset { border: 0; margin: 0; padding: 0; display: grid; gap: 7px; min-width: 0; }
legend { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin-bottom: 4px; }
label { display: flex; align-items: center; gap: 9px; cursor: pointer; }
.key { width: 34px; height: 12px; flex: none; }
.dot { display: flex; align-items: center; gap: 9px; }
.dot i { width: 13px; height: 13px; border-radius: 50%; flex: none; }
.card { background: var(--card); border: 1px solid var(--rule); border-radius: 4px; padding: 14px 16px; min-width: 0; }
.card h2 { font-family: var(--display); font-size: 26px; margin: 0 0 2px; line-height: 1.1; }
.card .where { color: var(--muted); font-size: 13px; margin: 0 0 10px; }
.card dl { display: grid; grid-template-columns: max-content 1fr; gap: 4px 14px; margin: 0; font-variant-numeric: tabular-nums; }
.card dt { color: var(--muted); font-size: 13px; } .card dd { margin: 0; font-family: var(--mono); font-size: 13px; }
.card .hint { color: var(--muted); margin: 0; }
.caveats { font-size: 13px; color: var(--muted); max-width: 80ch; display: grid; gap: 6px; }
.caveats p { margin: 0; }
.caveats strong { color: var(--ink); font-weight: 600; }
@media (max-width: 560px) { .region { font-size: 12px; } .note { display: none; } }
@media (prefers-reduced-motion: no-preference) { #map g.vp { transition: none; } }
</style>

<div class="wrap">
  <header>
    <h1>Where Indus inscriptions were found</h1>
    <p class="lede">Every find-spot with known coordinates, over the water as it was around 2600–1900 BCE (green) and as it is now (blue), with the Bronze Age routes to the Gulf and Central Asia.</p>
  </header>

  <div class="stats" aria-label="Summary">
    <div class="stat"><b>%%NAB%%</b><span>inscriptions found abroad</span></div>
    <div class="stat home"><b>%%HP%%</b><span>home texts with a closer (%%HC%% of %%HN%%)</span></div>
    <div class="stat abroad"><b>%%AP%%</b><span>abroad texts with a closer (%%AC%% of %%AN%%)</span></div>
  </div>

  <div class="bar">
  <span class="lbl" id="water-lbl">Water</span>
  <div class="water" role="group" aria-labelledby="water-lbl">
    <button type="button" data-water="then" aria-pressed="false">Then</button>
    <button type="button" data-water="now" aria-pressed="false">Now</button>
    <button type="button" data-water="both" aria-pressed="true">Both</button>
  </div>
  <div class="views" role="group" aria-label="Map view">
    <button type="button" data-view="all" aria-pressed="true">Whole map</button>
    <button type="button" data-view="gulf" aria-pressed="false">Gulf sea route</button>
    <button type="button" data-view="indus" aria-pressed="false">Indus heartland</button>
    <button type="button" data-view="asia" aria-pressed="false">Central Asia</button>
  </div>
  </div>

  <div class="mapbox">
    %%SVG%%
    <div class="tools"><button type="button" id="zin" aria-label="Zoom in">+</button><button type="button" id="zout" aria-label="Zoom out">−</button></div>
  </div>

  <div class="controls">
    <fieldset>
      <legend>Find-spots</legend>
      <div class="dot"><i style="background:var(--home)"></i>Indus region, sized by inscriptions</div>
      <div class="dot"><i style="background:var(--abroad)"></i>Found abroad (1–2 each)</div>
      <div class="dot"><i style="border:1.5px dashed var(--abroad)"></i>Abroad, no closer on any examined text</div>
    </fieldset>
    <fieldset>
      <legend>Water and routes (schematic)</legend>
      <div class="dot"><svg class="key"><line x1="0" y1="6" x2="34" y2="6" class="anc-line"></line></svg>Water then (c. 2600–1900 BCE), sketched</div>
      <div class="dot"><svg class="key"><rect x="1" y="1" width="32" height="10" class="anc-area"></rect></svg>Sea then, possible extent</div>
      <div class="dot"><svg class="key"><line x1="0" y1="6" x2="34" y2="6" class="anc-line old"></line></svg>Older bed, already dry by then</div>
      <div class="dot"><svg class="key"><line x1="0" y1="6" x2="34" y2="6" class="river"></line></svg>Rivers now</div>
      <label><input type="checkbox" id="l-sea" data-layer="sea" checked><svg class="key"><line x1="0" y1="6" x2="34" y2="6" class="searoute"></line></svg>Sea route: Meluhha – Magan – Dilmun – Sumer</label>
      <label><input type="checkbox" id="l-land" data-layer="land" checked><svg class="key"><line x1="0" y1="6" x2="34" y2="6" class="landroute"></line></svg>Overland routes to Central Asia</label>
    </fieldset>
    <div class="card" id="card" aria-live="polite"><p class="hint">Tap a point to see how many inscriptions were found there. Tap a green line or area to see what the water was like then, and the source.</p></div>
  </div>

  <div class="caveats">
    <p><strong>Water then is a sketch, not a survey.</strong> Each green line joins places that a published source says lay on that channel around 2600–1900 BCE; tap one for the source. The Hakra was monsoon-fed and ended in lakes in Cholistan. The older Sutlej bed through the Nara to the Rann was already dry. The Euphrates ran past Nippur, Uruk and Ur, with an eastern branch past Umma. The Rann of Kutch and the head of the Gulf may have been open water, but both are debated. Not drawn: %%NOTDRAWN%%</p>
    <p><strong>Routes are drawn by hand.</strong> They are not surveyed. The sea route follows the coast past Ras al-Hadd and Hormuz, in the order of Sargon of Akkad's inscription naming the ships of Meluhha, Magan and Dilmun. The overland routes join modern passes and towns (Khyber, Kabul, Kunduz; Bolan, Kandahar, Herat).</p>
    <p><strong>Coastline and rivers are modern</strong> (Natural Earth). The Indus has moved, Lothal's dock is now inland, and the Karun, Murghab, Ravi and Kokcha are missing from this river layer. About half the find-spots abroad have approximate coordinates, and "Luristan" is a region, not a site.</p>
    <p><strong>Find-spots reflect where people dug.</strong> Mesopotamian cities and Bahrain's burial mounds were excavated far more than the Iranian plateau or the Makran coast. %%NOC%% inscriptions from small home sites without coordinates are not shown.</p>
    <p><strong>"Closer" counts use exploration texts only.</strong> Holdout texts are counted but their signs were not read. The abroad figure rests on 14 texts and was noticed after looking, so it is a lead, not a finding. Analysis: results/findspots_waterways.md, results/sign_travel_water.md and results/foreign_seals_scoping.md in the Indus-Research repository.</p>
  </div>
</div>

<script>
(() => {
  const S = %%DATA%%;
  const svg = document.getElementById('map');
  const [W, H] = svg.getAttribute('viewBox').split(' ').slice(2).map(Number);
  let vb = [0, 0, W, H];
  const set = () => { svg.setAttribute('viewBox', vb.map(v => v.toFixed(1)).join(' '));
    svg.classList.toggle('zoomed', vb[2] < W / 1.8); };
  const views = { all: [0, 0, W, H], gulf: [0, H * 0.28, W * 0.62, H * 0.62], indus: [W * 0.6, H * 0.18, W * 0.38, H * 0.42],
                  asia: [W * 0.45, 0, W * 0.5, H * 0.5] };
  document.querySelectorAll('.views button').forEach(b => b.addEventListener('click', () => {
    vb = views[b.dataset.view].slice(); set();
    document.querySelectorAll('.views button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
  }));
  const zoom = (f, cx = vb[0] + vb[2] / 2, cy = vb[1] + vb[3] / 2) => {
    const w = Math.min(W, Math.max(W / 12, vb[2] * f)), h = w * H / W;
    vb = [Math.min(W - w, Math.max(0, cx - (cx - vb[0]) * w / vb[2])), Math.min(H - h, Math.max(0, cy - (cy - vb[1]) * h / vb[3])), w, h];
    set();
  };
  document.getElementById('zin').onclick = () => zoom(0.6);
  document.getElementById('zout').onclick = () => zoom(1 / 0.6);
  const pt = e => { const r = svg.getBoundingClientRect();
    return [vb[0] + (e.clientX - r.left) / r.width * vb[2], vb[1] + (e.clientY - r.top) / r.height * vb[3]]; };
  svg.addEventListener('wheel', e => { e.preventDefault(); const [x, y] = pt(e); zoom(e.deltaY > 0 ? 1.15 : 1 / 1.15, x, y); }, { passive: false });
  let drag = null, moved = false;
  svg.addEventListener('pointerdown', e => { drag = [e.clientX, e.clientY, vb[0], vb[1]]; moved = false; });
  window.addEventListener('pointermove', e => { if (!drag) return; const r = svg.getBoundingClientRect();
    const dx = (e.clientX - drag[0]) / r.width * vb[2], dy = (e.clientY - drag[1]) / r.height * vb[3];
    if (Math.abs(dx) + Math.abs(dy) > 2) { moved = true; svg.classList.add('dragging'); }
    vb[0] = Math.min(W - vb[2], Math.max(0, drag[2] - dx)); vb[1] = Math.min(H - vb[3], Math.max(0, drag[3] - dy)); set(); });
  window.addEventListener('pointerup', () => { drag = null; svg.classList.remove('dragging'); });

  const A = %%ANC%%;
  const gNow = svg.querySelector('g[data-layer="rivers"]'), gThen = svg.querySelector('g[data-layer="ancient"]');
  document.querySelectorAll('.water button').forEach(b => b.addEventListener('click', () => {
    const w = b.dataset.water;
    gNow.style.display = w === 'then' ? 'none' : '';
    gThen.style.display = w === 'now' ? 'none' : '';
    document.querySelectorAll('.water button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
  }));
  document.querySelectorAll('input[data-layer]').forEach(c => {
    const g = svg.querySelector(`g[data-layer="${c.dataset.layer}"]`);
    c.addEventListener('change', () => { g.style.display = c.checked ? '' : 'none'; });
  });

  const card = document.getElementById('card');
  const esc = s => String(s).replace(/[&<>"]/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]));
  const showF = el => {
    document.querySelectorAll('.site.sel, .anc.sel').forEach(x => x.classList.remove('sel'));
    el.classList.add('sel');
    const f = A[+el.dataset.f];
    const along = f.points.map(p => p[2]).filter(Boolean).join(' → ');
    card.innerHTML = `<h2>${esc(f.name)}</h2><p class="where">Water then · ${esc(f.certainty)}</p>
      <p style="margin:0 0 8px">${esc(f.note)}</p>${along ? `<p class="where" style="margin:0 0 8px">Drawn through: ${esc(along)}</p>` : ''}
      <p class="where" style="margin:0">Source: ${esc(f.sources.join('; '))}</p>`;
  };
  svg.querySelectorAll('.anc').forEach(el => {
    el.addEventListener('click', () => { if (!moved) showF(el); });
    el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); showF(el); } });
  });
  const show = el => {
    document.querySelectorAll('.site.sel, .anc.sel').forEach(x => x.classList.remove('sel'));
    el.classList.add('sel');
    const s = S[+el.dataset.i];
    const closer = s.ex ? `${s.closer} of ${s.ex} (${Math.round(100 * s.closer / s.ex)}%)` : 'none examined';
    const km = v => (v === null || Number.isNaN(v)) ? '–' : `${v} km`;
    card.innerHTML = `<h2>${esc(s.name)}</h2><p class="where">${esc(s.region)}${s.kind === 'abroad' ? ' · ' + (s.route === 'sea' ? 'sea and river side' : 'overland') : ''}</p>
      <dl><dt>Inscriptions found</dt><dd>${s.n}</dd>
      <dt>Exploration texts with a closer</dt><dd>${closer}</dd>
      <dt>In the locked holdout</dt><dd>${s.hold} (signs not read)</dd>
      <dt>To the sea today</dt><dd>${km(s.sea)}</dd><dt>To a major river today</dt><dd>${km(s.river)}</dd>
      <dt>Coordinates</dt><dd style="font-family:var(--body)">${esc(s.src)}</dd></dl>`;
  };
  svg.querySelectorAll('.site').forEach(el => {
    el.addEventListener('click', () => { if (!moved) show(el); });
    el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(el); } });
  });
})();
</script>
"""

if __name__ == "__main__":
    main(*sys.argv[1:3])
