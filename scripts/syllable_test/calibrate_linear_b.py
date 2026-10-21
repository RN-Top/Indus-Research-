import json,sys,re,math,collections
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
D='/tmp/claude-0/-home-claude/5444b495-3534-509a-b0d3-d3a720a00472/scratchpad/ext/paragorth/data/codelib'
lines=[json.loads(l)['seq'] for l in open(D+'/linear_b.jsonl')]
texts=[]; lab={}
for s in lines:
    t=[]
    for tok in s:
        if tok=='NUM': t.append('NUM'); continue
        if re.fullmatch(r'[a-z0-9*\-]+',tok) and any(c.islower() for c in tok):
            for syl in tok.split('-'):
                if syl: t.append('s:'+syl); lab['s:'+syl]='syll'
        elif re.fullmatch(r'[A-Z][A-Z+/]*|\*\d+',tok):
            t.append('L:'+tok); lab['L:'+tok]='logo'
    if len(t)>=2: texts.append(t)
def features(texts, numerals):
    f=collections.Counter(x for t in texts for x in t)
    L=collections.defaultdict(collections.Counter); R=collections.defaultdict(collections.Counter); P=collections.defaultdict(collections.Counter); nn=collections.Counter()
    for t in texts:
        for i,x in enumerate(t):
            L[x][t[i-1] if i else '<s>']+=1; R[x][t[i+1] if i<len(t)-1 else '</s>']+=1
            P[x]['first' if i==0 else 'last' if i==len(t)-1 else 'mid']+=1
            if (i and t[i-1] in numerals) or (i<len(t)-1 and t[i+1] in numerals): nn[x]+=1
    def H(c): n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
    rows=[]
    for x,n in f.items():
        if n<10 or x in numerals: continue
        rows.append(dict(sign=x,logf=math.log(n),Hl=H(L[x]),Hr=H(R[x]),Hpos=H(P[x]),num_adj=nn[x]/n,
                         mid=P[x]['mid']/n,uniqL=len(L[x])/n,uniqR=len(R[x])/n))
    d=pd.DataFrame(rows)
    # remove frequency effect: residual of each feature on log frequency
    for c in ['Hl','Hr','Hpos','num_adj','mid','uniqL','uniqR']:
        b=np.polyfit(d.logf,d[c],1); d[c+'_r']=d[c]-np.polyval(b,d.logf)
    return d
d=features(texts,{'NUM'}); d['y']=d.sign.map(lab)
d=d.dropna(subset=['y']); print(d.y.value_counts().to_dict())
for c in ['logf','Hl_r','Hr_r','Hpos_r','num_adj_r','mid_r','uniqL_r','uniqR_r']:
    print(f"{c:10} AUC syllable-vs-logogram {roc_auc_score(d.y=='syll',d[c]):.2f}")
d.to_csv('/tmp/claude-0/-home-claude/5444b495-3534-509a-b0d3-d3a720a00472/scratchpad/syl/lb_feats.csv',index=False)
