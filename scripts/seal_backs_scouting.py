# Usage: python3 scripts/seal_backs_scouting.py <inscriptions.csv from github.com/yajnadevam/lipi>. Exploration only.
import sys,json; sys.path.insert(0,'/home/claude/indus-research-')
import numpy as np, pandas as pd
from scipy.stats import chi2_contingency, fisher_exact
from indus_workbench import data
raw,_=data.load_raw("indus_website")
c=data.build_corpus(raw,"indus_website",metadata=data.load_metadata("indus_website"),drop_damaged=True,dedupe=False,drop_unidentified=True)
ex=data.explore_only(c).df.copy()   # EXPLORATION ONLY
L=pd.read_csv(sys.argv[1],dtype=str,keep_default_na=False); L['icit']=L.id.str.split('.').str[0]
ex['icit']=ex.text_id.str.lstrip('S')
m=ex.merge(L.drop_duplicates('icit')[['icit','boss','condition','preservation','type','cross-section','thickness(mm)']],on='icit',how='left')
nums=set(json.load(open('/home/claude/indus-research-/hypotheses/H-2026-10-16-51b7445b.json'))['params']['numerals'])
s=m[m.object_type=='seal'].copy(); s['t']=s.signs.map(' '.join)
nsite=s.groupby('t').site.nunique(); cnt=s.t.value_counts()
s['kind']=np.select([s.signs.map(lambda x:len(x)<=3 and x[0] in nums)|(s.t.map(nsite)>=2),
                     (s.t.map(cnt)==1)&(s.signs.map(len)>=4)],['formula','long-unique'],'other')
print(s.kind.value_counts().to_dict())
for col in ['boss','condition','type']:
    t=pd.crosstab(s.kind,s[col]); t=t.loc[:,t.sum()>=10]
    print(f"\n{col}:"); print((t.div(t.sum(1),axis=0)*100).round(0).astype(int).assign(n=t.sum(1)).to_string())
    tt=t.loc[['formula','long-unique']]; print("  chi2 p (formula vs long-unique):", round(chi2_contingency(tt)[1],3))
# within Mohenjo-daro only for boss
md=s[s.site=='Mohenjo-daro']; t=pd.crosstab(md.kind,md.boss); t=t.loc[['formula','long-unique'],t.sum()>=10]
print("\nMD boss:"); print((t.div(t.sum(1),axis=0)*100).round(0).astype(int).assign(n=t.sum(1)).to_string()); print("  p",round(chi2_contingency(t)[1],3))
