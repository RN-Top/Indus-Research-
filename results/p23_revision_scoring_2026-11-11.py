import random, json, sys
sys.path.insert(0, '.')
from synth import make_system, noisy

def score_all(f):
    g = lambda k: f.get(k, [])
    def eq(a, b): return a == b and len(a) > 0
    teens = all(eq(g(n), [g(10)[0], g(n-10)[0]]) for n in range(11, 20) if n in f and g(10))
    teen_present = any(n in f for n in range(11, 20))
    rel = {
      "vigesimal": [len(g(20)) == 1, len(g(10)) == 1, len(g(20)) == 1 and g(20) != [g(2)[0], g(10)[0]] if g(2) and g(10) else False],
      "decimal":   [len(g(10)) == 1, eq(g(20), [g(2)[0], g(10)[0]]) if g(2) and g(10) else False,
                    len(g(100)) == 1, teens if teen_present else False],
      "quinary":   [len(g(5)) == 1] + [eq(g(n), [g(5)[0], g(n-5)[0]]) if g(5) and (n-5) in f else False for n in range(6, 10)]
                   + [eq(g(10), [g(2)[0], g(5)[0]]) if g(2) and g(5) else False,
                      eq(g(20), [g(4)[0], g(5)[0]]) if g(4) and g(5) else False],
      "duodecimal":[len(g(12)) == 1, len(g(10)) == 1, len(g(11)) == 1,
                    bool(g(10)) and bool(g(11)) and g(10)[:1] != g(11)[:1]],
    }
    return {b: sum(v)/len(v) for b, v in rel.items()}

def code(f):
    s = score_all(f)
    best = max(s, key=s.get)
    top = s[best]
    second = max(v for b, v in s.items() if b != best)
    if top >= 0.75 and top > second:
        return best
    return "other"

def run(seed, n=300):
    rng = random.Random(seed)
    bases = ["decimal", "vigesimal", "quinary", "duodecimal", "other"]
    out = {}
    for mode in ["clean", "noisy"]:
        per = {}
        for b in bases:
            hits = 0
            for _ in range(n):
                f = make_system(b, rng)
                if mode == "noisy": f = noisy(f, rng)
                hits += code(f) == b
            per[b] = round(hits / n, 3)
        out[mode] = per
        out[mode + "_mean"] = round(sum(per.values()) / len(per), 3)
    return out

if __name__ == "__main__":
    print("TUNING seed 20261111 (not valid as validation):")
    print(json.dumps(run(20261111), indent=1))
    print("VALIDATION seed 20261112:")
    print(json.dumps(run(20261112), indent=1))
