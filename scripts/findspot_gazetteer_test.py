"""A fairer null for the water result: sites WITH Indus finds vs contemporary sites WITHOUT. (EXPLORATORY.)

findspots_waterways.md compared find-spots abroad with random land, which is too easy
(people everywhere lived by water). Here the comparison is other places that existed
around 2600-1900 BCE, from the Pleiades gazetteer (CC BY; github.com/isawnyu/pleiades.datasets):
location points in the same region (15-42 N, 42-75 E, South Asia left out) whose dated
range overlaps 2600-1900 BCE. Places within 15 km of an Indus find-spot count as "with".

Tests (median distance to the present sea or a major river):
  1. label permutation: find-spots vs gazetteer sites, 10,000 shuffles of the labels;
  2. distance-matched draws: for each find-spot, a gazetteer site at a similar distance
     from Mohenjo-daro (within 300 km), 10,000 draws.
Same for distance to the sea alone. No holdout is involved; nothing is registered.

    python scripts/findspot_gazetteer_test.py /path/to/pleiades/data/gis /path/to/natural_earth_geojson
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from findspot_routes import ABROAD, MOHENJO, Dist, densify, km, lines  # noqa: E402

RNG = np.random.default_rng(20261015)
N = 10000


def main(pleiades_dir, ne_dir):
    ne = Path(ne_dir)
    coast = Dist(densify(lines(ne / "ne_10m_coastline.geojson")))
    rivers = Dist(densify(lines(ne / "ne_50m_rivers_lake_centerlines.geojson", lambda p: p.get("featurecla") == "River")))

    p = pd.read_csv(Path(pleiades_dir) / "location_points.csv", encoding="utf-8-sig", low_memory=False)
    xy = p["geometry_wkt"].str.extract(r"POINT \(([-\d.]+) ([-\d.]+)\)").astype(float)
    p["lon"], p["lat"] = xy[0], xy[1]
    reg = p[p.lat.between(15, 42) & p.lon.between(42, 75) & ~((p.lon > 66.5) & (p.lat < 34.5))]
    t = reg[(reg.year_after_which <= -1900) & (reg.year_before_which >= -2600)]
    g = t.groupby("place_id").agg(title=("title", "first"), lat=("lat", "mean"), lon=("lon", "mean")).reset_index()

    finds = pd.DataFrame([dict(site=s, lat=v[0], lon=v[1], route=v[3]) for s, v in ABROAD.items() if s != "Luristan"])
    near = [min(km((a, b), (c, d)) for c, d in zip(finds.lat, finds.lon)) for a, b in zip(g.lat, g.lon)]
    g["near_find_km"] = near
    with_finds = g[g.near_find_km <= 15]
    gaz = g[g.near_find_km > 15].reset_index(drop=True)
    for df in (finds, gaz):
        df["water"] = np.minimum(coast(df.lat.values, df.lon.values), rivers(df.lat.values, df.lon.values))
        df["sea"] = coast(df.lat.values, df.lon.values)
        df["from_mohenjo"] = [km(MOHENJO, (a, b)) for a, b in zip(df.lat, df.lon)]
    print(f"Pleiades places in the region dated to overlap 2600-1900 BCE: {len(g)}; within 15 km of an Indus find-spot: "
          f"{len(with_finds)} ({', '.join(with_finds.title.str.slice(0, 40))}); used as 'without': {len(gaz)}")
    print(f"Indus find-spots abroad used: {len(finds)} (Luristan left out: a region, not a site)")
    out = dict(gazetteer_places=len(g), without=len(gaz), with_titles=list(with_finds.title), tests={})

    for col in ["water", "sea"]:
        a, b = finds[col].values, gaz[col].values
        obs = np.median(a) - np.median(b)
        pool = np.r_[a, b]
        null = np.empty(N)
        for i in range(N):
            s = RNG.permutation(pool)
            null[i] = np.median(s[:len(a)]) - np.median(s[len(a):])
        p_perm = float((1 + (null <= obs).sum()) / (N + 1))
        pools = [np.flatnonzero(np.abs(gaz.from_mohenjo.values - d) < 300) for d in finds.from_mohenjo]
        ok = [len(q) > 0 for q in pools]
        draws = np.array([[RNG.choice(q) for q, k in zip(pools, ok) if k] for _ in range(N)])
        nm = np.median(b[draws], axis=1)
        obs_m = float(np.median(a[ok]))
        p_match = float((1 + (nm <= obs_m).sum()) / (N + 1))
        out["tests"][col] = dict(median_finds=float(np.median(a)), median_gazetteer=float(np.median(b)), p_label_permutation=p_perm,
                                 matched_finds=int(sum(ok)), median_matched_draws=float(np.median(nm)), p_distance_matched=p_match)
        print(f"\n== distance to {'sea or major river' if col == 'water' else 'the sea'} ==")
        print(f"   Indus find-spots abroad: median {np.median(a):.0f} km;  contemporary sites without: median {np.median(b):.0f} km"
              f"  (label permutation p = {p_perm:.4f})")
        print(f"   distance-matched draws ({sum(ok)} find-spots matched): {np.median(nm):.0f} km vs {obs_m:.0f} km  (p = {p_match:.4f})")

    reg_counts = gaz.assign(zone=np.select([gaz.lon < 50.5, gaz.lat < 30], ["Mesopotamia and western Iran", "Gulf and Arabia"],
                                          "Iran plateau and Central Asia")).zone.value_counts().to_dict()
    out["gazetteer_by_zone"] = reg_counts
    out["gazetteer_sites"] = gaz[["title", "lat", "lon", "water", "sea"]].round(2).to_dict("records")
    print("\ngazetteer sites by zone:", reg_counts)
    (ROOT / "results" / "findspot_gazetteer_test.json").write_text(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    main(*sys.argv[1:3])
