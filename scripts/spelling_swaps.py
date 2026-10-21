import sys,csv; sys.path.insert(0,'/home/claude/indus-research-')
import numpy as np, pandas as pd
from collections import Counter, defaultdict
from indus_workbench import data
raw,_=data.load_raw("indus_website")
c=data.build_corpus(raw,"indus_website",metadata=data.load_metadata("indus_website"),drop_damaged=True,dedupe=False,drop_unidentified=True)
ex=data.explore_only(c).df   # exploration only
base={}
for r in csv.DictReader(open('/home/claude/indus-research-/data/sign_marks/marks_blind_2026-10-20.csv')):
    base[r['sign']]=r['sign'] if r['base'] in ('self','') else r['base']
def fam(g):
    seen=set()
    while g in base and base[g]!=g and g not in seen: seen.add(g); g=base[g]
    return g
texts=sorted(set(tuple(s) for s in ex.signs if len(s)>=3))
# one-position minimal pairs
slots=defaultdict(list)
for t in texts:
    for i in range(len(t)):
        slots[(len(t),i,t[:i],t[i+1:])].append(t[i])
pairs=Counter()
for k,v in slots.items():
    v=sorted(set(v))
    for a in range(len(v)):
        for b in range(a+1,len(v)): pairs[(v[a],v[b])]+=1
print("minimal-pair contexts:",sum(pairs.values()),"distinct swap pairs:",len(pairs))
for p in [('G717','G760'),('G744','G747'),('G421','G422')]:
    print(p, "contexts elsewhere:", pairs.get(p,0))
ann=lambda a,b: (a in base and b in base)
obs=[(a,b,n) for (a,b),n in pairs.items() if ann(a,b)]
same=sum(n for a,b,n in obs if fam(a)==fam(b)); tot=sum(n for a,b,n in obs)
# null: random pairs drawn with token frequencies, among annotated signs
freq=Counter(x for t in texts for x in t if x in base); signs=list(freq); w=np.array([freq[s] for s in signs],float); w/=w.sum()
r=np.random.default_rng(0); null=[]
for _ in range(2000):
    a=r.choice(signs,size=tot,p=w); b=r.choice(signs,size=tot,p=w)
    m=a!=b; null.append(np.mean([fam(x)==fam(y) for x,y in zip(a[m],b[m])]))
print(f"swaps between same-family signs: {same}/{tot} = {same/tot:.3f}; random pairs {np.mean(null):.3f}")
print("top swaps:")
for (a,b),n in pairs.most_common(25):
    if ann(a,b): print(f"  {a}<->{b} x{n}  same family: {fam(a)==fam(b)}")
for p in [('G806','G831'),('G231','G233'),('G220','G233'),('G904','G905')]:
    print(p, "contexts:", pairs.get(p,0), "same family:", fam(p[0])==fam(p[1]))
