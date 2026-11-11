import json,sys
def load(path):
    d=json.load(open(path)); d=d.get('content',d); S={}
    for s in d['sheets']:
        rows=[]
        for dat in s.get('data',[]):
            for r in dat.get('rowData',[]):
                rows.append([((list(c['effectiveValue'].values())[0]) if c.get('effectiveValue') else None, c.get('hyperlink')) for c in r.get('values',[])])
        S[s['properties']['title']]=rows
    return S
def g(row,i): return row[i][0] if i<len(row) else None
def rnd(x): return round(x,6) if isinstance(x,float) else x
def sstr(v): return '' if v is None else (str(int(v)) if isinstance(v,float) and v.is_integer() else str(v))
def parse(path, source):
    S=load(path); recipes=[]; cur=None
    for row in S.get('Recipes',[])[1:]:
        a,b,c,dd=[g(row,k) for k in range(4)]; phase=g(row,9)
        if (a in (None,'')) and (b in (None,'')): cur=None; continue
        if a=='Name' and b=='Amount': continue
        if b in (None,'') and c in (None,'') and isinstance(a,str): cur={'name':a.strip(),'ingredients':[]}; recipes.append(cur); continue
        if cur is None or a in (None,''): continue
        ing={'name':str(a).strip(),'amount':rnd(b) if isinstance(b,(int,float)) else 0,'unit':(c or '').strip() if isinstance(c,str) else sstr(c)}
        if isinstance(dd,(int,float)): ing['grams']=rnd(dd)
        if phase and phase not in('Title','Header'): ing['phase']=str(phase)
        cur['ingredients'].append(ing)
    info={}
    for row in S.get('Recipe Info',[])[1:]:
        n=g(row,0)
        if not n: continue
        bt=g(row,6); cpb=g(row,3)
        info[str(n).strip()]={'book':sstr(g(row,1)),'bookUrl':(row[1][1] if len(row)>1 else None) or '','page':sstr(g(row,2)),
          'cookiesPerBatch':cpb if isinstance(cpb,(int,float)) else None,'refrigerate':sstr(g(row,4)),'ovenTemp':sstr(g(row,5)),'bakeMinutes':bt if isinstance(bt,(int,float)) else None}
    for r in recipes:
        r.update(info.pop(r['name'],{})); r['notes']=f'Imported from {source}.'
    for n,v in info.items(): recipes.append({'name':n,'ingredients':[],**v,'notes':f'Imported from {source}.'})
    gram=[{'ingredient':str(g(r,0)),'unit':sstr(g(r,1)),'grams':rnd(g(r,2))} for r in S.get('Gram Conversions',[])[1:] if g(r,0) and isinstance(g(r,2),(int,float))]
    bulk=[{'ingredient':str(g(r,0)),'unit':sstr(g(r,1)),'bulkUnit':sstr(g(r,2)),'perBulk':rnd(g(r,3))} for r in S.get('Bulk Conversions',[])[1:] if g(r,0) and isinstance(g(r,3),(int,float))]
    return {'recipes':recipes,'gramConversions':gram,'bulkConversions':bulk,'extra':{k:[[sstr(g(r,i)) for i in range(len(r))] for r in v] for k,v in S.items() if k not in('Recipes','Recipe Info','Gram Conversions','Bulk Conversions')}}
if __name__=='__main__':
    out=parse(sys.argv[1],sys.argv[2]); json.dump(out,open(sys.argv[3],'w'),indent=1)
    rs=out['recipes']; print(sys.argv[2],len(rs),'recipes;',sum(1 for r in rs if r['ingredients']),'with ingredients;',len(out['gramConversions']),'gram',len(out['bulkConversions']),'bulk')
    print('  ',[r['name'] for r in rs])
