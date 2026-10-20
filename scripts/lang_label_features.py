"""Old Tamil vs Prakrit label features (F1-F5 of drafts/dravidian_comparison_PLAN.md). Exploration only."""
import json, re, unicodedata
from collections import Counter
S='/tmp/claude-0/-home-claude/5444b495-3534-509a-b0d3-d3a720a00472/scratchpad/'
def norm(s):
    s=unicodedata.normalize('NFKD',s or ''); s=''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]','',s.lower())
def load(fn):
    out=[]
    for l in open(fn):
        d=json.loads(l); w=[x for x in d.get('words',[]) if norm(x.get('form'))]
        if w: out.append(w)
    return out
import pathlib; R=pathlib.Path(__file__).resolve().parents[1]/'data'
tam_cave=load(R/'tamil_brahmi/corpus_roles.jsonl'); tam_obj=load(R/'tamil_brahmi/objects_roles.jsonl'); pra=load(R/'prakrit_eiad/tagged_roles.jsonl')
NAME={'PERSONAL_NAME','PLACE_NAME'}
def feats(T,label):
    T2=[t for t in T if len(t)>=2]
    n=len(T2)
    first=Counter(norm(t[0].get('stem') or t[0]['form']) for t in T2)
    last=Counter(norm(t[-1].get('stem') or t[-1]['form']) for t in T2)
    f_name_first=sum(t[0]['role'] in NAME for t in T2)/n
    f_name_last=sum(t[-1]['role'] in NAME for t in T2)/n
    top_last=sum(c for _,c in last.most_common(5))/n
    top_first=sum(c for _,c in first.most_common(5))/n
    words=[w for t in T for w in t]
    suf=[len(w.get('suffixes') or []) for w in words]
    nb=na=0
    for t in T:
        for i,w in enumerate(t):
            if w['role']=='NUMERAL':
                if i+1<len(t) and t[i+1]['role'] not in ('NUMERAL',): na+=1   # number then noun
                if i>0 and t[i-1]['role'] not in ('NUMERAL',): nb+=1         # noun then number
    lastrole=Counter(t[-1]['role'] for t in T2).most_common(3)
    firstrole=Counter(t[0]['role'] for t in T2).most_common(3)
    print(f"\n== {label}: texts>=2 words {n}, words {len(words)}")
    print(f" F1 name first {f_name_first:.0%} | name last {f_name_last:.0%}")
    print(f" F2 top-5 last words cover {top_last:.0%}: {last.most_common(5)}  roles {lastrole}")
    print(f" F5 top-5 first words cover {top_first:.0%}: {first.most_common(5)}  roles {firstrole}")
    print(f" F3 suffixes/word {sum(suf)/len(suf):.2f}; words with 2+ suffixes {sum(s>=2 for s in suf)/len(suf):.1%}")
    print(f" F4 numeral followed by word {na} | numeral preceded by word {nb}")
for T,l in [(tam_cave,'Old Tamil, cave corpus'),(tam_obj,'Old Tamil, object legends'),(pra,'Prakrit (EIAD)')]: feats(T,l)
