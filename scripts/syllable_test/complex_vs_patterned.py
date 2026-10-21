import sys,json; sys.path.insert(0,'/home/claude/indus-research-'); sys.path.insert(0,'/tmp/claude-0/-home-claude/5444b495-3534-509a-b0d3-d3a720a00472/scratchpad/syl')
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
exec(open('/tmp/claude-0/-home-claude/5444b495-3534-509a-b0d3-d3a720a00472/scratchpad/syl/calib.py').read().split("d=features(texts")[0])
from indus_workbench import data
raw,_=data.load_raw("indus_website")
c=data.build_corpus(raw,"indus_website",metadata=data.load_metadata("indus_website"),drop_damaged=True,dedupe=True,drop_unidentified=True)
ex=data.explore_only(c).df.copy()   # EXPLORATION ONLY
L=pd.read_csv('/tmp/claude-0/-home-claude/5444b495-3534-509a-b0d3-d3a720a00472/scratchpad/ext/lipi/src/assets/data/inscriptions.csv',dtype=str,keep_default_na=False); L['icit']=L.id.str.split('.').str[0]
ex['icit']=ex.text_id.str.lstrip('S'); ex=ex.merge(L.drop_duplicates('icit')[['icit','class']],on='icit',how='left')
nums=set(json.load(open('/home/claude/indus-research-/hypotheses/H-2026-10-16-51b7445b.json'))['params']['numerals'])
texts=[list(s) for s in ex.signs if len(s)>=2]
fi=features(texts,nums)
# Linear B model on the three calibrated features
lb=pd.read_csv('/tmp/claude-0/-home-claude/5444b495-3534-509a-b0d3-d3a720a00472/scratchpad/syl/lb_feats.csv')
F=['Hr_r','uniqR_r','num_adj_r']
z=lambda d: (d[F]-d[F].mean())/d[F].std()
m=LogisticRegression().fit(z(lb),lb.y=='syll')
fi['syll_score']=m.predict_proba(z(fi))[:,1]
# enrichment in complex vs patterned texts
cx=ex[ex['class'].isin(['SC','LC'])]; pt=ex[ex['class'].isin(['SP','LP'])]
from collections import Counter
def enr(cxs,pts):
    a=Counter(x for s in cxs for x in s); b=Counter(x for s in pts for x in s); A=sum(a.values()); B=sum(b.values())
    return {g:np.log((a[g]+0.5)/A)-np.log((b[g]+0.5)/B) for g in set(a)|set(b)}
e=enr(cx.signs,pt.signs); fi['enrich']=fi.sign.map(e); f2=fi.dropna(subset=['enrich'])
obs=spearmanr(f2.enrich,f2.syll_score).correlation
r=np.random.default_rng(0); both=list(cx.signs)+list(pt.signs); k=len(cx); null=[]
for _ in range(1000):
    p=r.permutation(len(both)); ee=enr([both[i] for i in p[:k]],[both[i] for i in p[k:]])
    null.append(spearmanr(f2.sign.map(ee),f2.syll_score).correlation)
print(f"signs with 10+ uses: {len(f2)}; complex texts {len(cx)}, patterned {len(pt)}")
print(f"Spearman(enrichment in complex texts, syllable-likeness) = {obs:.3f}; null {np.mean(null):.3f}; p (one-sided) {(1+sum(v>=obs for v in null))/1001:.3f}")
for c_ in F: print(f"  {c_}: rho with enrichment {spearmanr(f2.enrich,f2[c_]).correlation:+.3f}")
print("most complex-leaning signs:", f2.sort_values('enrich').tail(8)[['sign','enrich','syll_score']].round(2).values.tolist())
print("most patterned-leaning:", f2.sort_values('enrich').head(8)[['sign','enrich','syll_score']].round(2).values.tolist())
print("Indus syllable-score distribution:", f2.syll_score.describe().round(2).to_dict())
