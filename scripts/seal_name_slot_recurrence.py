"""Name-slot precondition test on seals (controls object type).
Question: do seals open with recurring 2- and 3-sign sequences more than chance?
Null: permute the sign order inside each seal (keeps each seal's sign multiset).
Counts seals per opening prefix; reports prefixes shared by >= 5 seals, within SEAL:S and SEAL:R separately.
"""
import json, random, ast, collections, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
def seqs(fam_prefix):
    out = []
    for r in rows:
        if not r["type"].startswith(fam_prefix): continue
        s = r["seq_strong"]
        if isinstance(s, str): s = ast.literal_eval(s)
        s = [str(x) for x in s]
        if len(s) >= 3: out.append(s)
    return out
def openers(seals, k):
    c = collections.Counter(tuple(s[:k]) for s in seals)
    return c
def observed_and_null(seals, k, reps=200, seed=1):
    # Valid null: each seal is regenerated from the class's unigram sign frequencies
    # (same lengths, same sign frequencies, no order). This keeps common signs but
    # destroys all fixed sequences, so recurrence beyond unigram chance is what is tested.
    obs = openers(seals, k)
    obs_rec = sum(1 for v in obs.values() if v >= 5)
    rng = random.Random(seed)
    pool = [x for s in seals for x in s]
    lengths = [len(s) for s in seals]
    nulls = []
    for _ in range(reps):
        sh = [[rng.choice(pool) for _ in range(L)] for L in lengths]
        nulls.append(sum(1 for v in openers(sh, k).values() if v >= 5))
    return obs, obs_rec, sum(nulls)/len(nulls), sum(n >= obs_rec for n in nulls)/len(nulls)
out = {}
for label, pref in [("SEAL:S", "SEAL:S"), ("SEAL:R", "SEAL:R")]:
    seals = seqs(pref)
    res = {"n": len(seals)}
    for k in (2, 3):
        obs, rec, nmean, p = observed_and_null(seals, k)
        top = obs.most_common(5)
        res[f"k{k}"] = {"recurring_prefixes_>=5": rec, "null_mean": round(nmean, 2),
                        "p": round(p, 4), "top5": [[list(t), n] for t, n in top]}
    out[label] = res
print(json.dumps(out, indent=2))
