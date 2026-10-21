# Usage: python3 scripts/region_scouting.py <inscriptions.csv from github.com/yajnadevam/lipi>. Exploration split only; the CSV is not copied here.
import sys,json; sys.path.insert(0,'/home/claude/indus-research-')
import numpy as np, pandas as pd
from indus_workbench import data
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import balanced_accuracy_score
raw,_=data.load_raw("indus_website")
c=data.build_corpus(raw,"indus_website",metadata=data.load_metadata("indus_website"),drop_damaged=True,dedupe=True,drop_unidentified=True)
df=data.explore_only(c).df.copy()
L=pd.read_csv(sys.argv[1],dtype=str,keep_default_na=False); L['icit']=L.id.str.split('.').str[0]
df['icit']=df.text_id.str.lstrip('S'); m=df.merge(L.drop_duplicates('icit')[['icit','region','dir.']],on='icit',how='left')
s=m[(m.object_type=='seal')&(m.signs.map(len)>=2)].copy()
print(s.region.value_counts().to_dict())
s=s[s.region.isin(['Lower Indus','Inter-Riverine','Gujarat/Kutch','Eastern Headwaters'])]
P=json.load(open('/home/claude/indus-research-/hypotheses/H-2026-10-16-51b7445b.json'))['params']
ops=set(P['openers']); cl=set(P['closers']); nums=set(P.get('numerals',[]))
pairs=[r.split(',')[:2] for r in open('/home/claude/indus-research-/data/sign_marks/marks_blind_2026-10-20.csv').read().splitlines()[1:] if 'enclosure_strokes' in r]
enc={p[0] for p in pairs}
s['len']=s.signs.map(len); s['opener']=s.signs.map(lambda x:x[0] in ops); s['closer']=s.signs.map(lambda x:x[-1] in cl)
s['G740']=s.signs.map(lambda x:'G740' in x); s['numeral']=s.signs.map(lambda x:any(g in nums for g in x)); s['enclosed']=s.signs.map(lambda x:any(g in enc for g in x))
print(s.groupby('region')[['len','opener','closer','G740','numeral','enclosed']].mean().round(2).assign(n=s.region.value_counts()))
y=s.region.values; X=CountVectorizer(token_pattern=r'\S+',binary=True).fit_transform(s.signs.map(' '.join))
skf=StratifiedKFold(5,shuffle=True,random_state=0); mdl=LogisticRegression(max_iter=3000,class_weight='balanced',C=0.5)
obs=balanced_accuracy_score(y,cross_val_predict(mdl,X,y,cv=skf)); r=np.random.default_rng(0)
null=[balanced_accuracy_score(yp,cross_val_predict(mdl,X,yp,cv=skf)) for yp in (r.permutation(y) for _ in range(200))]
print(f"region from seal text: bal.acc {obs:.3f} null {np.mean(null):.3f} p {(1+sum(v>=obs for v in null))/201:.3f} n={len(y)}")
# which signs are regional? per-sign share by region, chi2
from scipy.stats import chi2_contingency
rows=[]
for g in set(x for t in s.signs for x in t):
    has=s.signs.map(lambda t:g in t)
    if has.sum()<15: continue
    tab=pd.crosstab(s.region,has)
    if tab.shape[1]<2: continue
    p=chi2_contingency(tab)[1]; sh=has.groupby(s.region).mean()
    rows.append((g,int(has.sum()),p,*[round(sh.get(k,0),3) for k in ['Lower Indus','Inter-Riverine','Gujarat/Kutch','Eastern Headwaters']]))
R=pd.DataFrame(rows,columns=['sign','n','p','LowerIndus','InterRiv','Gujarat','EastHead']).sort_values('p')
print(R.head(15).to_string(index=False))
