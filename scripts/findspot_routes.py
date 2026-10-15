"""Where did Indus inscriptions end up, and does that follow the water? (EXPLORATORY; geography only.)

Uses only WHERE inscriptions were found (site metadata for every record, both
splits; never their signs), so it does not touch the locked text holdout.

  1. Find-spot table: coordinates (flagged where approximate), inscriptions per
     find-spot, distance to the present sea coast and to the nearest major river.
  2. Test: are the find-spots outside the Indus region nearer to the sea or a major
     river than random land points at the same straight-line distance from
     Mohenjo-daro (outside South Asia)? 10,000 random sets.
  3. Sea route: the sea finds placed along a coast-following route fixed by
     geography alone (Indus mouth -> Ras al-Hadd -> Strait of Hormuz -> central
     Gulf -> head of the Gulf), with route distance against straight-line distance.

Geography: Natural Earth (public domain) coastline 1:10m, land and rivers 1:50m.
These are MODERN; section 'ancient water' in the write-up lists what differs.
Pass the folder that holds the Natural Earth geojson files.

    python scripts/findspot_routes.py /path/to/natural_earth_geojson
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.path import Path as MPath
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402

RNG = np.random.default_rng(20261015)
N_NULL = 10000
BBOX = (15.0, 45.0, 35.0, 80.0)  # lat min, lat max, lon min, lon max
R = 6371.0
MOHENJO = (27.32917, 68.13889)

# Find-spots outside the Indus region. src: where the coordinates come from.
ABROAD = {
    "Ur": (30.9625, 46.1031, "Mesopotamia", "sea", "approx. (general reference; Ur ruins, Tell al-Muqayyar)"),
    "Kish": (32.54, 44.60, "Mesopotamia", "sea", "approx. (general reference)"),
    "Tell Umma": (31.66722, 45.8875, "Mesopotamia", "sea", "Wikipedia, Umma"),
    "Susa": (32.19, 48.26, "Iran (Elam)", "sea", "approx. (general reference)"),
    "Luristan": (33.5, 48.0, "Iran", "overland", "REGION, not a site: centre of Lorestan, very approximate"),
    "Qala'at al-Bahrain": (26.233, 50.520, "Gulf (Bahrain)", "sea", "approx. (general reference)"),
    "Saar": (26.19, 50.49, "Gulf (Bahrain)", "sea", "approx. (general reference)"),
    "Karzakan": (26.11389, 50.48167, "Gulf (Bahrain)", "sea", "Wikipedia, Karzakan"),
    "Hajar": (26.22, 50.53, "Gulf (Bahrain)", "sea", "approx.: Al Hajar village, Northern Governorate (Wikipedia gives no coordinates); identification of the corpus's 'Hajar' with it is assumed"),
    "Ra's al-Junayz": (22.43, 59.83, "Gulf (Oman)", "sea", "approx. (Ras al-Jinz cape)"),
    "Salut": (22.85, 57.35, "Gulf (Oman)", "sea", "approx.: plain near Bahla, interior Oman (Madain Project gives no coordinates)"),
    "Altyn Depe": (36.8579167, 60.432375, "Central Asia", "overland", "Wikipedia, Altyndepe"),
    "Gonur Depe": (38.21, 62.035, "Central Asia", "overland", "Wikipedia, Gonur Depe"),
    "Shortughai": (37.325, 69.525, "Central Asia", "overland", "Wikipedia, Shortugai"),
}
HOME_EXTRA = {  # home sites missing from data/site_coordinates.csv
    "Chanhujo-daro": (26.16, 68.32, "approx.: about 130 km south of Mohenjo-daro (Wikipedia)"),
    "Nausharo": (29.383, 67.617, "approx.: Mehrgarh's coordinates; Nausharo is about 6 km away (Wikipedia)"),
}
# Coast-following sea route fixed by geography (not by where seals were found).
SEA_ROUTE = [("Indus mouth", 24.0, 67.4), ("Ras al-Hadd (eastern tip of Arabia)", 22.53, 59.80),
             ("Strait of Hormuz", 26.55, 56.45), ("central Gulf", 26.6, 52.0),
             ("head of the Gulf, 3rd-millennium estimate (near Nasiriya)", 31.0, 46.3)]


def xyz(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.c_[np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)]


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def lines(path, keep=lambda p: True):
    g = json.loads(Path(path).read_text())
    for f in g["features"]:
        if not f["geometry"] or not keep(f["properties"]):
            continue
        t, c = f["geometry"]["type"], f["geometry"]["coordinates"]
        for ln in ([c] if t == "LineString" else c):
            yield np.array(ln)[:, :2]


def densify(segs, step_deg=0.02):
    pts = []
    for s in segs:
        for a, b in zip(s[:-1], s[1:]):
            n = max(1, int(np.hypot(*(b - a)) / step_deg))
            pts.append(a + (b - a) * np.linspace(0, 1, n, endpoint=False)[:, None])
        pts.append(s[-1:])
    p = np.vstack(pts)
    la0, la1, lo0, lo1 = BBOX
    m = (p[:, 1] > la0 - 5) & (p[:, 1] < la1 + 5) & (p[:, 0] > lo0 - 5) & (p[:, 0] < lo1 + 5)
    return p[m]


class Dist:
    def __init__(self, pts_lonlat):
        self.tree = cKDTree(xyz(pts_lonlat[:, 1], pts_lonlat[:, 0]))

    def __call__(self, lat, lon):
        d, _ = self.tree.query(xyz(np.atleast_1d(lat), np.atleast_1d(lon)))
        return 2 * R * np.arcsin(np.clip(d / 2, 0, 1))


def land_grid(path, step=0.1):
    la0, la1, lo0, lo1 = BBOX
    lat, lon = np.meshgrid(np.arange(la0, la1, step), np.arange(lo0, lo1, step), indexing="ij")
    P = np.c_[lon.ravel(), lat.ravel()]
    inside = np.zeros(len(P), bool)
    g = json.loads(Path(path).read_text())
    for f in g["features"]:
        geom = f["geometry"]
        polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
        for poly in polys:
            ring = np.array(poly[0])[:, :2]
            if ring[:, 0].max() < lo0 or ring[:, 0].min() > lo1 or ring[:, 1].max() < la0 or ring[:, 1].min() > la1:
                continue
            inside |= MPath(ring).contains_points(P)
    return P[inside][:, 1], P[inside][:, 0]


def along_route(lat, lon):
    """Distance along SEA_ROUTE to the nearest point on it, plus the offset from the route."""
    best, run = None, 0.0
    for (_, a1, o1), (_, a2, o2) in zip(SEA_ROUTE[:-1], SEA_ROUTE[1:]):
        seg = km((a1, o1), (a2, o2))
        for t in np.linspace(0, 1, 400):
            p = (a1 + (a2 - a1) * t, o1 + (o2 - o1) * t)
            off = km(p, (lat, lon))
            if best is None or off < best[1]:
                best = (run + seg * t, off)
        run += seg
    return best


def main(ne_dir):
    ne = Path(ne_dir)
    coast = Dist(densify(lines(ne / "ne_10m_coastline.geojson")))
    rivers = Dist(densify(lines(ne / "ne_50m_rivers_lake_centerlines.geojson",
                                lambda p: p.get("featurecla") == "River")))
    water = lambda la, lo: np.minimum(coast(la, lo), rivers(la, lo))  # noqa: E731

    # inscriptions per find-spot: every record, both splits, metadata only
    raw, _ = data.load_raw("indus_website")
    c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"),
                          drop_damaged=False, dedupe=False, drop_unidentified=False)
    counts = c.df["site"].value_counts()
    coords = pd.read_csv(ROOT / "data" / "site_coordinates.csv")
    home = {r.site: (r.lat, r.lon, "data/site_coordinates.csv (Wikipedia)") for r in coords.itertuples()}
    home.update(HOME_EXTRA)

    rows = []
    for s, n in counts.items():
        if s in ABROAD:
            la, lo, reg, route, src = ABROAD[s]
            group = reg
        elif s in home:
            la, lo, src = home[s]
            route, group = "home", "Indus region"
        else:
            continue
        rows.append(dict(site=s, inscriptions=int(n), group=group, route=route, lat=la, lon=lo, coords_source=src,
                         km_from_mohenjo=round(km(MOHENJO, (la, lo))), km_to_sea=float(coast(la, lo)[0]),
                         km_to_major_river=float(rivers(la, lo)[0])))
    no_coords = {s: int(n) for s, n in counts.items() if s not in ABROAD and s not in home}
    tab = pd.DataFrame(rows).sort_values(["route", "km_from_mohenjo"])
    pd.set_option("display.width", 200)
    print("== 1. Find-spots with coordinates (inscriptions = every record in the corpus, both splits) ==")
    print(tab[["site", "group", "inscriptions", "km_from_mohenjo", "km_to_sea", "km_to_major_river"]]
          .round(0).to_string(index=False))
    print(f"   home find-spots without coordinates (not used): {len(no_coords)} sites, "
          f"{sum(no_coords.values())} inscriptions")
    out = dict(findspots=rows, home_without_coordinates=no_coords, sea_route=SEA_ROUTE)

    # ---- 2. abroad finds vs random land points at the same distance from Mohenjo-daro -----
    glat, glon = land_grid(ne / "ne_50m_land.geojson")
    south_asia = (glon > 66.5) & (glat < 34.5)
    glat, glon = glat[~south_asia], glon[~south_asia]
    gd = np.array([km(MOHENJO, p) for p in zip(glat, glon)])
    gw, gc = water(glat, glon), coast(glat, glon)
    ab = tab[tab.route != "home"]
    tests = {}
    for label, sub in [("all abroad find-spots", ab), ("abroad, Luristan (a region) left out", ab[ab.site != "Luristan"]),
                       ("sea-route group", ab[ab.route == "sea"]), ("overland group", ab[ab.route == "overland"])]:
        pools = [np.flatnonzero(np.abs(gd - d) < 100) for d in sub.km_from_mohenjo]
        obs_w = float(np.median(water(sub.lat.values, sub.lon.values)))
        obs_c = float(np.median(coast(sub.lat.values, sub.lon.values)))
        draws = np.array([[RNG.choice(p) for p in pools] for _ in range(N_NULL)])
        nw, nc = np.median(gw[draws], 1), np.median(gc[draws], 1)
        tests[label] = dict(n=len(sub), median_km_to_water=obs_w, null_median_water=float(np.median(nw)),
                            p_water=float((1 + (nw <= obs_w).sum()) / (N_NULL + 1)),
                            median_km_to_sea=obs_c, null_median_sea=float(np.median(nc)),
                            p_sea=float((1 + (nc <= obs_c).sum()) / (N_NULL + 1)))
    out["tests"] = tests
    print("\n== 2. Nearer to water than random land at the same distance from Mohenjo-daro (outside South Asia)? ==")
    for k, t in tests.items():
        print(f"   {k:40} n={t['n']:2}  to sea or major river: median {t['median_km_to_water']:5.0f} km vs random "
              f"{t['null_median_water']:5.0f} (p={t['p_water']:.4f});  to sea: {t['median_km_to_sea']:5.0f} vs "
              f"{t['null_median_sea']:5.0f} (p={t['p_sea']:.4f})")

    # ---- 3. sea finds along the coast-following route ----------------------------------------
    print("\n== 3. Sea-route finds along a coast-following route (Indus mouth -> Oman -> Hormuz -> Gulf -> head) ==")
    seq = []
    for r in ab[ab.route == "sea"].itertuples():
        d_along, off = along_route(r.lat, r.lon)
        straight = km((SEA_ROUTE[0][1], SEA_ROUTE[0][2]), (r.lat, r.lon))
        seq.append(dict(site=r.site, inscriptions=r.inscriptions, km_along_route=round(d_along), km_off_route=round(off),
                        km_straight_from_indus_mouth=round(straight), detour=round((d_along + off) / straight, 2)))
    seq.sort(key=lambda r: r["km_along_route"])
    for s in seq:
        print(f"   {s['site']:20} {s['inscriptions']} inscr.  {s['km_along_route']:5} km along route (+{s['km_off_route']} km off it);"
              f" straight line {s['km_straight_from_indus_mouth']} km; route/straight {s['detour']}")
    out["sea_sequence"] = seq
    tot = {g: int(ab[ab.route == g].inscriptions.sum()) for g in ["sea", "overland"]}
    out["inscriptions_by_route"] = tot
    print("   inscriptions abroad by route:", tot)

    (ROOT / "results" / "findspots_waterways.json").write_text(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    main(sys.argv[1])
