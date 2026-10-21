# Usage: python3 scripts/context_scouting.py <path to inscriptions.csv from github.com/yajnadevam/lipi (src/assets/data)>
# The CSV has no licence file, so it is not copied into this repository. Exploration split only.
# Ignore that file's 'sanskrit' and 'translation' columns (one author's readings, unused here).
import sys,json; sys.path.insert(0,'/home/claude/indus-research-')
import numpy as np, pandas as pd
from indus_workbench import data
raw,_=data.load_raw("indus_website")
c=data.build_corpus(raw,"indus_website",metadata=data.load_metadata("indus_website"),drop_damaged=True,dedupe=False,drop_unidentified=True)
df=data.explore_only(c).df.copy()   # EXPLORATION ONLY
L=pd.read_csv(sys.argv[1],dtype=str,keep_default_na=False); L['icit']=L.id.str.split('.').str[0]
df['icit']=df.text_id.str.lstrip('S')
m=df.merge(L.drop_duplicates('icit'),on='icit',how='left',suffixes=('','_L'))
P=json.load(open('/home/claude/indus-research-/hypotheses/H-2026-10-16-51b7445b.json'))['params']
ops=set(P['openers']); cl=set(P['closers'])
r=np.random.default_rng(0)
# A. neighbourhood similarity
m['area']=m['area-section'].str.strip()
for site in ['Mohenjo-daro','Harappa']:
    x=m[(m.site==site)&(~m.area.isin(['--','-','']))&(m.signs.map(len)>=2)].reset_index(drop=True)
    x=x[x.area.map(x.area.value_counts())>=5].reset_index(drop=True)
    S=[set(s) for s in x.signs]; n=len(S)
    J=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            J[i,j]=len(S[i]&S[j])/len(S[i]|S[j])
    iu=np.triu_indices(n,1); a=np.asarray(x.area.to_numpy(dtype=object))
    def stat(a):
        same=(a[:,None]==a[None,:])[iu]; v=J[iu]; return v[same].mean()-v[~same].mean()
    obs=stat(a); null=[stat(r.permutation(a)) for _ in range(500)]
    print(f"A {site}: {n} texts, {x.area.nunique()} areas; same-area minus diff-area sign overlap {obs:+.4f}, null {np.mean(null):+.4f}, p {(1+sum(v>=obs for v in null))/501:.3f}")
    print("  top areas:",x.area.value_counts().head(6).to_dict())
# B. time at Harappa
h=m[(m.site=='Harappa')].copy()
h['per']=h.time.str.extract(r'Period (\d[A-C]?)')[0]
h['per']=h.per.replace({'3':None})
print("B periods:",h.per.value_counts().to_dict())
h=h[h.per.isin(['3A','3B','3C','4','5'])]
h['opener']=h.signs.map(lambda s:s[0] in ops); h['closer']=h.signs.map(lambda s:s[-1] in cl)
h['len']=h.signs.map(len); h['G740']=h.signs.map(lambda s:'G740' in s)
print(h.groupby('per').agg(n=('len','size'),len=('len','mean'),opener=('opener','mean'),closer=('closer','mean'),G740=('G740','mean')).round(2))
print(pd.crosstab(h.per,h.object_type))
print("--- controlled for object type ---")
for site in ['Harappa','Mohenjo-daro']:
  for ot in ['seal','tablet']:
    x=m[(m.site==site)&(m.object_type==ot)&(~m.area.isin(['--','-','']))&(m.signs.map(len)>=2)].reset_index(drop=True)
    x=x[x.area.map(x.area.value_counts())>=5].reset_index(drop=True)
    if len(x)<40: continue
    S=[set(s) for s in x.signs]; n=len(S); J=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n): J[i,j]=len(S[i]&S[j])/len(S[i]|S[j])
    iu=np.triu_indices(n,1); a=np.asarray(x.area.to_numpy(dtype=object))
    def stat(a):
        same=(a[:,None]==a[None,:])[iu]; v=J[iu]; return v[same].mean()-v[~same].mean()
    obs=stat(a); null=[stat(r.permutation(a)) for _ in range(500)]
    print(f"A {site} {ot}: {n} texts, {x.area.nunique()} areas; diff {obs:+.4f} null {np.mean(null):+.4f} p {(1+sum(v>=obs for v in null))/501:.3f}")
for ot in ['seal','tablet']:
    print(ot); print(h[h.object_type==ot].groupby('per').agg(n=('len','size'),len=('len','mean'),opener=('opener','mean'),closer=('closer','mean'),G740=('G740','mean')).round(2))
print("--- tablets, duplicates within an area collapsed ---")
for site in ['Harappa','Mohenjo-daro']:
    x=m[(m.site==site)&(m.object_type=='tablet')&(~m.area.isin(['--','-','']))&(m.signs.map(len)>=2)].copy()
    x['t']=x.signs.map(' '.join); x=x.drop_duplicates(['area','t']).reset_index(drop=True)
    x=x[x.area.map(x.area.value_counts())>=5].reset_index(drop=True)
    S=[set(s) for s in x.signs]; n=len(S); J=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n): J[i,j]=len(S[i]&S[j])/len(S[i]|S[j])
    iu=np.triu_indices(n,1); a=np.asarray(x.area.to_numpy(dtype=object))
    def stat(a):
        same=(a[:,None]==a[None,:])[iu]; v=J[iu]; return v[same].mean()-v[~same].mean()
    obs=stat(a); null=[stat(r.permutation(a)) for _ in range(500)]
    print(f"{site} tablet unique-per-area: {n}; diff {obs:+.4f} p {(1+sum(v>=obs for v in null))/501:.3f}")
print("--- Harappa 3B vs 3C, permutation within object type ---")
hh=h[h.per.isin(['3B','3C'])&h.object_type.isin(['seal','tablet'])].reset_index(drop=True)
for f in ['len','opener']:
    y=hh[f].astype(float).values; late=(hh.per=='3C').values
    obs=y[late].mean()-y[~late].mean(); null=[]
    for _ in range(2000):
        p=hh.groupby('object_type').per.transform(lambda v:r.permutation(v.values)).values=='3C'
        null.append(y[p].mean()-y[~p].mean())
    print(f"{f}: 3C-3B {obs:+.3f}  p {(1+sum(abs(v)>=abs(obs) for v in null))/2001:.4f}")
