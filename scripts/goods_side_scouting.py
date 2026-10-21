# Usage: python3 scripts/goods_side_scouting.py <inscriptions.csv from github.com/yajnadevam/lipi>. Exploration only.
import sys,json; sys.path.insert(0,'/home/claude/indus-research-')
import numpy as np, pandas as pd
from indus_workbench import data
raw,_=data.load_raw("indus_website")
c=data.build_corpus(raw,"indus_website",metadata=data.load_metadata("indus_website"),drop_damaged=True,dedupe=False,drop_unidentified=True)
ex=data.explore_only(c).df.copy()   # EXPLORATION ONLY
L=pd.read_csv(sys.argv[1],dtype=str,keep_default_na=False); L['icit']=L.id.str.split('.').str[0]
ex['icit']=ex.text_id.str.lstrip('S'); m=ex.merge(L.drop_duplicates('icit')[['icit','type']],on='icit',how='left')
nums=set(json.load(open('/home/claude/indus-research-/hypotheses/H-2026-10-16-51b7445b.json'))['params']['numerals'])
m['t']=m.signs.map(' '.join); m['len']=m.signs.map(len)
seal=m[m.object_type=='seal']; goods=m[(m.object_type.isin(['tag','impression']))|(m.type=='POT:T:s')]
cnt=seal.t.value_counts(); nsite=seal.groupby('t').site.nunique()
formula=set(t for t in cnt.index if nsite[t]>=2) | set(seal.t[seal.signs.map(lambda x:len(x)<=3 and x[0] in nums)])
unique_long=set(t for t in cnt.index if cnt[t]==1 and len(t.split())>=4)
print(f"seals {len(seal)}, goods-side {len(goods)} ({goods.object_type.value_counts().to_dict()}, stamped pots {(goods.type=='POT:T:s').sum()})")
def prof(d,name):
    print(f"{name:10} n={len(d):4}  len {d.len.mean():.2f}  numeral-first {d.signs.map(lambda x:x[0] in nums).mean():.2f}  "
          f"text is a formula {d.t.isin(formula).mean():.2f}  text is a long unique seal text {d.t.isin(unique_long).mean():.2f}")
prof(seal,'seals'); prof(goods,'goods')
print("goods texts that equal a seal text:", goods.t.isin(set(cnt.index)).sum())
print(goods[['site','object_type','type','t']].assign(formula=goods.t.isin(formula),onseal=goods.t.isin(set(cnt.index))).sort_values('site').to_string(index=False))
P=json.load(open('/home/claude/indus-research-/hypotheses/H-2026-10-16-51b7445b.json'))['params']; ops=set(P['openers'])
mk=lambda x:x[0] in ops or (len(x)>1 and x[1] in ('G2','G60'))   # heading = frozen opener, or any sign followed by a heading marker
for nm,d in [('seals',seal.drop_duplicates(['t','site'])),('goods',goods.drop_duplicates(['t','site']))]:
    print(f"{nm}: distinct texts {len(d)}, heading (frozen opener first) {d.signs.map(lambda x:x[0] in ops).mean():.2f}, heading incl. marker G2/G60 in 2nd place {d.signs.map(mk).mean():.2f}")
from scipy.stats import fisher_exact
a=goods.drop_duplicates(['t','site']).signs.map(mk); b=seal.drop_duplicates(['t','site']).signs.map(mk)
print("Fisher (marker-heading, goods vs seals):", fisher_exact([[a.sum(),(~a).sum()],[b.sum(),(~b).sum()]]))
