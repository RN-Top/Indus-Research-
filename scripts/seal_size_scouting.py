# Usage: python3 scripts/seal_size_scouting.py <inscriptions.csv from github.com/yajnadevam/lipi>. Exploration only.
import sys,json; sys.path.insert(0,'/home/claude/indus-research-')
import numpy as np, pandas as pd
from indus_workbench import data
raw,_=data.load_raw("indus_website")
c=data.build_corpus(raw,"indus_website",metadata=data.load_metadata("indus_website"),drop_damaged=True,dedupe=False,drop_unidentified=True)
ex=data.explore_only(c).df.copy()   # EXPLORATION ONLY
L=pd.read_csv(sys.argv[1],dtype=str,keep_default_na=False); L['icit']=L.id.str.split('.').str[0]
ex['icit']=ex.text_id.str.lstrip('S')
m=ex.merge(L.drop_duplicates('icit')[['icit','horizontal(mm)','vertical(mm)']],on='icit',how='left')
P=json.load(open('/home/claude/indus-research-/hypotheses/H-2026-10-16-51b7445b.json'))['params']; nums=set(P['numerals']); ops=set(P['openers']); cl=set(P['closers'])
s=m[(m.object_type=='seal')&m.site.isin(['Mohenjo-daro','Harappa'])].copy()
s['size']=np.sqrt(pd.to_numeric(s['horizontal(mm)'],errors='coerce').replace(0,np.nan)*pd.to_numeric(s['vertical(mm)'],errors='coerce').replace(0,np.nan))
s=s.dropna(subset=['size']).copy(); s['L']=s.signs.map(len).clip(upper=8); s['ls']=np.log(s['size'])
s['cell']=s.site+'_'+s.L.astype(str)
feats={'numfirst':lambda x:x[0] in nums,'opener':lambda x:x[0] in ops,'G740':lambda x:'G740' in x,'closer':lambda x:x[-1] in cl}
s['uni']=s.motif.str.startswith('Bull1')
for k,f in feats.items(): s[k]=s.signs.map(f)
r=np.random.default_rng(0)
def stat(g):  # within-cell mean log-size difference, weighted by cell size
    num=den=0
    for _,d in s.assign(g=g).groupby('cell'):
        if d.g.all() or not d.g.any(): continue
        w=len(d); num+=w*(d.ls[d.g].mean()-d.ls[~d.g].mean()); den+=w
    return num/den
for k in list(feats)+['uni']:
    g=s[k].values; obs=stat(g)
    null=[stat(s.groupby('cell')[k].transform(lambda v:r.permutation(v.values)).values) for _ in range(1000)]
    print(f"{k:9} size effect at fixed length+site: {100*(np.exp(obs)-1):+.1f}%  p {(1+np.sum(np.abs(null)>=abs(obs)))/1001:.3f}  (share {s[k].mean():.2f})")
print("n",len(s))
s['animal']=s.motif.str.split(':').str[0]
x=s[s.animal.map(s.animal.value_counts())>=8]
# residual size after length+site cell means
x=x.assign(res=x.ls-x.groupby('cell').ls.transform('mean'))
t=x.groupby('animal').agg(n=('res','size'),rel_size=('res','mean'),median_mm=('size','median')).sort_values('rel_size')
t['rel_size']=(100*(np.exp(t.rel_size)-1)).round(1); print(t)
print("unicorn sub-style:", x[x.animal=='Bull1'].assign(st=x.motif.str.split(':').str[1].fillna('none')).groupby('st').agg(n=('res','size'),rel=('res','mean')).assign(rel=lambda d:(100*(np.exp(d.rel)-1)).round(1)).query('n>=8').to_dict('index'))
