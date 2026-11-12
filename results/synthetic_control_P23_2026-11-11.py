import random, json, sys

# Forms are lists of morphemes. Roots are plain names; a system's roots are random.
# Each generator builds 1..10, 20, 100 for one base. Labels are NOT passed to the coder.

def make_system(base, rng):
    r = lambda: "r%08x" % rng.getrandbits(32)
    one = {n: r() for n in range(1, 11)}      # roots 1..10 for most bases
    if base == "decimal":
        f = {n: [one[n]] for n in range(1, 11)}
        f[20] = [one[2], one[10]]              # two + ten
        f[100] = [r()]                         # own root
        for n in range(11, 20): f[n] = [one[10], one[n-10]]
    elif base == "vigesimal":
        f = {n: [one[n]] for n in range(1, 11)}
        f[10] = [r()]                          # ten is its own root
        f[20] = [r()]                          # single "score" root, not 2x10
        f[100] = [r()]
    elif base == "quinary":
        five = r()
        f = {1: [r()], 2: [r()], 3: [r()], 4: [r()], 5: [five]}
        for n in range(6, 10): f[n] = [five, f[n-5][0]]   # 5 + n
        f[10] = [f[2][0], five]                          # two x five
        f[20] = [f[4][0], five]
        f[100] = [r()]
    elif base == "duodecimal":
        f = {n: [r()] for n in range(1, 13)}              # 10, 11, 12 all roots
        f[20] = [f[2][0], f[12][0]]
        f[100] = [r()]
    elif base == "other":                                  # no structure
        f = {n: [r()] for n in range(1, 11)}
        f[10] = [r()]
        f[20] = [r(), r()]
        f[100] = [r()]
    return f

def code(f):
    g = lambda k: f.get(k, [])
    # Step 1: vigesimal: 20 is one morpheme and is not a 2 x 10 product
    if len(g(20)) == 1 and g(20)[0] not in (g(2)[:1] + g(10)[:1]) :
        return "vigesimal"
    # Step 2: decimal: 10 single root, 20 = two + ten, 100 own root
    if len(g(10)) == 1 and g(20) == [g(2)[0], g(10)[0]] and len(g(100)) == 1:
        return "decimal"
    # Step 3: quinary: 5 root, 6-9 = 5 + n, 10 = two x five
    if (len(g(5)) == 1 and all(len(g(n)) == 2 and g(n)[0] == g(5)[0] for n in range(6, 10))
            and g(10) == [g(2)[0], g(5)[0]]):
        return "quinary"
    # Step 4: duodecimal: 12 is a single root, 10 and 11 distinct single roots
    if len(g(12)) == 1 and len(g(10)) == 1 and len(g(11)) == 1 and g(10)[0] != g(11)[0]:
        return "duodecimal"
    return "other"

def noisy(f, rng, rate=0.10):
    g = {}
    for k, v in f.items():
        if rng.random() < rate:
            g[k] = [ "v%08x" % rng.getrandbits(32) for _ in v]  # random variant root
        else:
            g[k] = list(v)
    return g

def run(n=300, seed=20261111):
    rng = random.Random(seed)
    bases = ["decimal", "vigesimal", "quinary", "duodecimal"]
    out = {}
    for mode in ["clean", "noisy"]:
        conf = {}
        for b in bases + ["other"]:
            hits = 0
            for _ in range(n):
                f = make_system(b, rng)
                if mode == "noisy": f = noisy(f, rng)
                pred = code(f)
                conf.setdefault(b, {}).setdefault(pred, 0)
                conf[b][pred] += 1
                hits += pred == b
            out.setdefault(mode, {})[b] = hits / n
        out[mode + "_confusion"] = conf
    return out

if __name__ == "__main__":
    res = run()
    print(json.dumps(res, indent=1))
