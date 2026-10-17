import pandas as pd, numpy as np, json, collections
D='data/'
ws=pd.read_csv(D+'mlw_world_series.csv'); pg=pd.read_csv(D+'mlw_perfect_games.csv',parse_dates=['date'])
b17=pd.read_csv(D+'mlw_stats_2017_batting.csv'); b26=pd.read_csv(D+'mlw_stats_2026_batting.csv')
S={}
S['titles']=ws.champion.value_counts().to_dict(); S['runner_ups']=ws.runner_up.value_counts().to_dict()
S['finals_apps']=dict(collections.Counter(ws.champion.tolist()+ws.runner_up.tolist()))
S['distinct_champs']=int(ws.champion.nunique()); S['n_seasons']=len(ws)
def hhi(s): p=s.value_counts(normalize=True); return float((p**2).sum())
for name,m in {'2010-2015':ws.year<=2015,'2016-2025':ws.year>=2016}.items():
    sub=ws[m]; S['era_'+name]={'titles':len(sub),'distinct':int(sub.champion.nunique()),'hhi':round(hhi(sub.champion),3),'top':sub.champion.value_counts().head(1).to_dict()}
ws['games']=ws.series_wins+ws.series_losses
S['sweeps']=int((ws.series_losses==0).sum()); S['game5']=int((ws.games==5).sum()); S['avg_games']=round(float(ws.games.mean()),2)
S['wildcat_finals']=int(((ws.champion=='Western Wildcats')|(ws.runner_up=='Western Wildcats')).sum())
S['comebacks']=ws[ws.notes.str.contains('0-2')][['year','champion']].values.tolist()
S['pg_by_pitcher']=pg.pitcher.value_counts().to_dict()
y=pg.date.dt.year
S['pg_by_era']={'2010-2013':int((y<=2013).sum()),'2017-2020':int(y.between(2017,2020).sum()),'2022-2026':int((y>=2022).sum())}
def agg(b):
    pa,ab,h,hr,bb,k=[int(b[c].sum()) for c in ['PA','AB','H','HR','BB','K']]
    return dict(n=len(b),PA=pa,AVG=round(h/ab,3),HR_per_PA=round(hr/pa,3),BBpct=round(bb/pa*100,1),Kpct=round(k/pa*100,1),HRtotal=hr,OPS_mean=round(float(b.OPS.mean()),3))
S['bat2017']=agg(b17); S['bat2026']=agg(b26)
json.dump(S,open('data/analysis.json','w'),indent=1,default=int)
print(json.dumps(S,indent=1,default=int))
