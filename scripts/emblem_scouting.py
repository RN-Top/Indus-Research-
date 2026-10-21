import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np, pandas as pd, json
from collections import Counter
from indus_workbench import data
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import balanced_accuracy_score
DS={"drop_damaged": True, "dedupe": True, "drop_unidentified": True}
raw,_=data.load_raw("indus_website")
c=data.build_corpus(raw,"indus_website",metadata=data.load_metadata("indus_website"),**DS)
ex=data.explore_only(c).df
s=ex[(ex.object_type=='seal')&(ex.motif!='unknown')].copy()
s['animal']=s.motif.str.split(':').str[0]
keep=[a for a,n in s.animal.value_counts().items() if n>=8]
s=s[s.animal.isin(keep)]
print(s.animal.value_counts().to_dict())
docs=s.signs.map(' '.join)
def run(y, X, label, nperm=200):
    skf=StratifiedKFold(5,shuffle=True,random_state=0)
    m=LogisticRegression(max_iter=3000,class_weight='balanced',C=0.5)
    pred=cross_val_predict(m,X,y,cv=skf); obs=balanced_accuracy_score(y,pred)
    r=np.random.default_rng(1); null=[]
    for _ in range(nperm):
        yp=r.permutation(y); null.append(balanced_accuracy_score(yp,cross_val_predict(m,X,yp,cv=skf)))
    print(f"{label}: bal.acc {obs:.3f}  null {np.mean(null):.3f}  p {(1+sum(n>=obs for n in null))/(nperm+1):.3f}  n={len(y)}")
X=CountVectorizer(token_pattern=r'\S+',ngram_range=(1,1),binary=True).fit_transform(docs)
y=np.array(s.animal)
run(y,X,"all animals, sign set")
y2=np.where(s.animal=='Bull1','unicorn','other')
run(y2,X,"unicorn vs other")
# site check
print(pd.crosstab(s.animal,s.site.where(s.site.isin(['Mohenjo-daro','Harappa']),'other')))
# per-sign enrichment non-unicorn
cnt=Counter(); cu=Counter()
for sg,a in zip(s.signs,s.animal):
    for g in set(sg): (cu if a=='Bull1' else cnt)[g]+=1
nu=(s.animal=='Bull1').sum(); no=len(s)-nu
rows=[(g,cnt[g],cu[g],cnt[g]/no,cu[g]/nu) for g in set(cnt)|set(cu) if cnt[g]+cu[g]>=10]
df=pd.DataFrame(rows,columns=['sign','nonuni','uni','share_non','share_uni']); df['ratio']=(df.share_non+1e-3)/(df.share_uni+1e-3)
print(df.sort_values('ratio').head(8).to_string()); print(df.sort_values('ratio').tail(10).to_string())
