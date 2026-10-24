"""Is the human figure G90 a name marker at home? (scouting, EXPLORATION split only)
Laursen (2010: 116-118) proposes a 'man' sign marks personal names on Gulf seals. If G90 does that at home too,
the sign right after (or before) it should be rare (a name) more often than for other signs of similar frequency.
Rare = 5 or fewer uses in exploration. Null: 200 sets of frequency-matched signs (within +-30% of G90's uses)."""
import sys
from collections import Counter
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
from functional_slots import load  # noqa: E402
df = load(); seqs = [list(s) for s in df.signs]
use = Counter(x for s in seqs for x in s); rare = {g for g, n in use.items() if n <= 5}
def nb_rare(g):
    a = b = na = nb = 0; first = last = tot = 0
    for s in seqs:
        for k, x in enumerate(s):
            if x != g: continue
            tot += 1; first += k == 0; last += k == len(s) - 1
            if k + 1 < len(s): na += 1; a += s[k + 1] in rare
            if k > 0: nb += 1; b += s[k - 1] in rare
    return dict(after=a / max(na, 1), before=b / max(nb, 1), first=first / tot, last=last / tot, n=tot)
g = nb_rare("G90"); print("G90:", {k: round(v, 3) for k, v in g.items()})
pool = [x for x, n in use.items() if x != "G90" and 0.7 * use["G90"] <= n <= 1.3 * use["G90"]]
ctl = [nb_rare(x) for x in pool]
for key in ("after", "before", "first", "last"):
    vals = np.array([c[key] for c in ctl])
    print(f"  {key:6} G90 {g[key]:.2f} vs {len(pool)} frequency-matched signs mean {vals.mean():.2f}; "
          f"share of them at or above G90: {(vals >= g[key]).mean():.2f}")
print("G90 commonest right neighbours:", Counter(s[k+1] for s in seqs for k, x in enumerate(s) if x == "G90" and k+1 < len(s)).most_common(8))
print("G90 commonest left neighbours:", Counter(s[k-1] for s in seqs for k, x in enumerate(s) if x == "G90" and k > 0).most_common(8))
