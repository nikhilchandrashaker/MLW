import pandas as pd, json
D='data/'; r=lambda n: pd.read_csv(D+n+'.csv').fillna('')
ws=r('mlw_world_series'); mvp=r('mlw_world_series_mvp').set_index('year'); dc=r('mlw_division_champions')
rows=[]
for _,x in ws.iterrows():
    d=dc[dc.year==x.year]
    rows.append(dict(year=int(x.year),champ=x.champion,ru=x.runner_up,res=x.series_result,w=int(x.series_wins),l=int(x.series_losses),venue=x.venue,note=x.notes,
      mvp=(mvp.loc[x.year].player if x.year in mvp.index else ''),div={k:v for k,v in zip(d.division,d.champion)}))
data=dict(ws=rows,pg=r('mlw_perfect_games').to_dict('records'),teams=r('mlw_teams_history').to_dict('records'),b17=r('mlw_stats_2017_batting').to_dict('records'),b26=r('mlw_stats_2026_batting').to_dict('records'),
 venues=r('mlw_venues').to_dict('records'),media=r('mlw_media_history').to_dict('records'),events=r('mlw_major_events').to_dict('records'),cov=r('mlw_coverage_matrix').to_dict('records'),S=json.load(open(D+'analysis.json')))
html=open('scripts/template.html').read().replace('__DATA__',json.dumps(data,ensure_ascii=False))
open('site/index.html','w').write(html); print(len(html)//1024,'KB')
