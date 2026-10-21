"""Restoring missing signs in Indus texts.

Models score every candidate sign x for a hidden position i in text s:
- 'unigram': overall frequency.
- 'ngram': P(x | left neighbour) * P(right neighbour | x), add-k smoothed (the sign-pair approach of Yadav et al. 2010).
- 'ngram2': interpolated trigram-style context (two signs on each side when present) plus the bigram terms.
- 'structured': ngram2 combined with a positional prior P(x | slot) where slot = first / last / interior and text length,
  and P(x | object type). Weights are fitted by cross-validation on training data only.
"""
from collections import Counter, defaultdict
import math
import numpy as np

BOS, EOS = "<s>", "</s>"


class Restorer:
    def __init__(self, k=0.1, weights=None):
        self.k = k
        self.w = weights or {"bi": 1.0, "tri": 0.5, "slot": 0.6, "obj": 0.3}

    def fit(self, texts, objects=None):
        self.uni = Counter(); self.bi = defaultdict(Counter); self.rbi = defaultdict(Counter)
        self.tri_l = defaultdict(Counter); self.tri_r = defaultdict(Counter)
        self.slot = defaultdict(Counter); self.obj = defaultdict(Counter)
        objects = objects or [None] * len(texts)
        for s, o in zip(texts, objects):
            t = [BOS] + list(s) + [EOS]
            for j in range(1, len(t) - 1):
                x = t[j]
                self.uni[x] += 1
                self.bi[t[j - 1]][x] += 1; self.rbi[t[j + 1]][x] += 1
                if j >= 2: self.tri_l[(t[j - 2], t[j - 1])][x] += 1
                if j + 2 < len(t): self.tri_r[(t[j + 1], t[j + 2])][x] += 1
                self.slot[self._slot(j - 1, len(s))][x] += 1
                if o is not None: self.obj[o][x] += 1
        self.V = sorted(self.uni); self.idx = {x: n for n, x in enumerate(self.V)}
        self.N = sum(self.uni.values())
        return self

    @staticmethod
    def _slot(i, n):
        lb = "L" + str(min(n, 8))
        return ("first" if i == 0 else "last" if i == n - 1 else "mid") + lb

    def _logp(self, table, key, alpha):
        c = table.get(key)
        V = len(self.V)
        if not c:
            return None
        tot = sum(c.values())
        return np.array([math.log((c.get(x, 0) + alpha) / (tot + alpha * V)) for x in self.V])

    def scores(self, s, i, obj=None, model="structured"):
        V = len(self.V)
        uni = np.array([math.log((self.uni[x] + self.k) / (self.N + self.k * V)) for x in self.V])
        if model == "unigram":
            return uni
        t = [BOS] + list(s) + [EOS]; j = i + 1
        sc = np.zeros(V)
        l = self._logp(self.bi, t[j - 1], self.k); r = self._logp(self.rbi, t[j + 1], self.k)
        # P(x|left) * P(right|x)  ==  P(x|left) * P(x|right) * P(right) / P(x): use reverse-bigram form, divide by unigram once
        sc += self.w["bi"] * ((l if l is not None else uni) + (r if r is not None else uni) - uni)
        if model == "ngram":
            return sc
        if j >= 2:
            tl = self._logp(self.tri_l, (t[j - 2], t[j - 1]), self.k)
            if tl is not None: sc += self.w["tri"] * (tl - uni)
        if j + 2 < len(t):
            tr = self._logp(self.tri_r, (t[j + 1], t[j + 2]), self.k)
            if tr is not None: sc += self.w["tri"] * (tr - uni)
        if model == "ngram2":
            return sc
        sl = self._logp(self.slot, self._slot(i, len(s)), self.k)
        if sl is not None: sc += self.w["slot"] * (sl - uni)
        if obj is not None:
            ob = self._logp(self.obj, obj, self.k)
            if ob is not None: sc += self.w["obj"] * (ob - uni)
        return sc

    def rank_of(self, s, i, obj=None, model="structured"):
        """Rank (1 = best) of the true sign s[i] among all known signs; None if s[i] was never seen in training."""
        if s[i] not in self.idx:
            return None
        sc = self.scores(s, i, obj, model)
        return int((sc > sc[self.idx[s[i]]]).sum()) + 1

    def top(self, s, i, obj=None, model="structured", n=5):
        sc = self.scores(s, i, obj, model)
        o = np.argsort(-sc)[:n]
        z = np.exp(sc - sc.max()); z /= z.sum()
        return [(self.V[k], float(z[k])) for k in o]
