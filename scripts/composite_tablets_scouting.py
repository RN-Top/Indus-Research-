# Usage: python3 scripts/composite_tablets_scouting.py <inscriptions.csv from github.com/yajnadevam/lipi>. Exploration only.
import sys,json; sys.path.insert(0,'/home/claude/indus-research-')
import numpy as np, pandas as pd
from collections import Counter
from indus_workbench import data
raw,_=data.load_raw("indus_website")
c=data.build_corpus(raw,"indus_website",metadata=data.load_metadata("indus_website"),drop_damaged=True,dedupe=False,drop_unidentified=True)
ex=data.explore_only(c).df.copy()   # EXPLORATION ONLY
L=pd.read_csv(sys.argv[1],dtype=str,keep_default_na=False); L['icit']=L.id.str.split('.').str[0]
ex['icit']=ex.text_id.str.lstrip('S')
m=ex.merge(L.drop_duplicates('icit')[['icit','area-section','block-house','room-grid','time','sides','type']],on='icit',how='left')
nums=set(json.load(open('/home/claude/indus-research-/hypotheses/H-2026-10-16-51b7445b.json'))['params']['numerals'])
tb=m[(m.object_type=='tablet')&(m.material!='Copper')&m.site.isin(['Harappa','Mohenjo-daro'])].copy()
tb['area']=tb['area-section'].str.strip().replace({'--':'','-':''})
tb['t']=tb.signs.map(' '.join)
RIT={'Scene','Pipal','Anth','T-A-T'}
tb['grp']=np.where(tb.motif.str.startswith('Mult'),'Mult',np.where(tb.motif.isin(RIT),'Ritual',np.where(tb.signs.map(lambda s:any(x in nums for x in s)),'Number','Other')))
# batches: identical text + image + area counted once
b=tb.drop_duplicates(['t','motif','area','site']).copy()
print("tablets",len(tb),"batches",len(b)); print(pd.crosstab(b.site,b.grp))
r=np.random.default_rng(0)
for site in ['Harappa','Mohenjo-daro']:
    x=b[(b.site==site)&(b.area!='')].reset_index(drop=True)
    print(f"\n== {site}: batches with an area {len(x)}")
    print(pd.crosstab(x.area,x.grp).loc[lambda d:d.sum(1)>=3].to_string())
    # concentration of Mult: share in its single most common area vs random sets of same size
    k=(x.grp=='Mult').sum()
    if k>=3:
        top=x[x.grp=='Mult'].area.value_counts().iloc[0]/k
        null=[x.area.iloc[r.choice(len(x),k,replace=False)].value_counts().iloc[0]/k for _ in range(5000)]
        print(f"Mult in its top area: {top:.2f}; random sets {np.mean(null):.2f}; p {(1+sum(v>=top for v in null))/5001:.3f}")
        # co-location with Ritual vs Number: share of Mult batches whose area also has Ritual / Number batches
        for g in ['Ritual','Number']:
            areas=set(x[x.grp==g].area)
            obs=(x[x.grp=='Mult'].area.isin(areas)).mean()
            nl=[x.area.iloc[r.choice(np.where(x.grp!='Mult')[0],k,replace=False)].isin(areas).mean() for _ in range(5000)]
            print(f"  Mult batches in areas that also have {g} tablets: {obs:.2f} vs random non-Mult {np.mean(nl):.2f}")
# text: numerals & sign overlap
print("\nshare of batches with a numeral:", b.groupby('grp').apply(lambda d:d.signs.map(lambda s:any(x in nums for x in s)).mean()).round(2).to_dict())
def vocab(g): return Counter(x for s in b[b.grp==g].signs for x in set(s))
V={g:vocab(g) for g in ['Mult','Ritual','Number','Other']}
def jac(a,b_): A,B=set(a),set(b_); return len(A&B)/len(A|B)
for g in ['Ritual','Number','Other']: print(f"sign-set overlap Mult~{g}: {jac(V['Mult'],V[g]):.2f}  ({len(V[g])} signs)")
print("Mult texts:", b[b.grp=='Mult'][['site','area','t']].to_string(index=False))
print("Ritual texts:", b[b.grp=='Ritual'][['site','area','motif','t']].to_string(index=False))
# period
h=tb[(tb.site=='Harappa')]; h=h.assign(per=h.time.str.extract(r'Period (\S+)')[0])
print(pd.crosstab(h.per,h.grp))
