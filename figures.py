import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
D='data/'; F='figures/'
ws=pd.read_csv(D+'mlw_world_series.csv'); pg=pd.read_csv(D+'mlw_perfect_games.csv',parse_dates=['date'])
b17=pd.read_csv(D+'mlw_stats_2017_batting.csv'); b26=pd.read_csv(D+'mlw_stats_2026_batting.csv'); cov=pd.read_csv(D+'mlw_coverage_matrix.csv')
C={'Western Wildcats':'#d9a400','Eastern Eagles':'#2f6fdb','Central Cardinals':'#c0392b','Northern Nighthawks':'#6c7a89','Midwest Mallards':'#2e9e5b','Coastal Cobras':'#e67e22','Pacific Predators':'#8e44ad','Great Lakes Gators':'#16a3a3','Downtown Diamondbacks':'#d6336c','Metro Magic':'#17a2d8','Seahawks':'#888','Southern Seahawks':'#888'}
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'figure.dpi':140,'axes.titleweight':'bold','axes.titlesize':13})
def save(n): plt.tight_layout(); plt.savefig(F+n,bbox_inches='tight',facecolor='white'); plt.close()

# 1 timeline
fig,ax=plt.subplots(figsize=(11,4.2))
for a,b,l,c in [(2009.5,2017.5,'Cultz Field era','#f3efe4'),(2017.5,2021.5,'The Meadows era','#e8f0f7'),(2021.5,2025.5,'Stadium Series','#f1e8f5')]:
    ax.axvspan(a,b,color=c,zorder=0); ax.text((a+b)/2,3.55,l,ha='center',fontsize=9,color='#444')
teams=list(C)[:10]; ypos={t:i for i,t in enumerate(['Western Wildcats','Eastern Eagles','Central Cardinals','Midwest Mallards','Pacific Predators','Great Lakes Gators','Downtown Diamondbacks','Metro Magic'])}
for _,r in ws.iterrows():
    ax.scatter(r.year,ypos[r.champion]*0.4,s=170,color=C[r.champion],zorder=3,edgecolor='k',lw=.6)
    ax.text(r.year,ypos[r.champion]*0.4+.2,r.series_result,ha='center',fontsize=7)
ax.set_yticks([v*0.4 for v in ypos.values()]); ax.set_yticklabels(ypos.keys()); ax.set_xticks(range(2010,2026)); ax.set_ylim(-.3,3.8)
ax.set_title('Who won the MLW World Series, 2010–2025 (label = series score)'); save('01_champions_timeline.png')

# 2 cumulative titles
fig,ax=plt.subplots(figsize=(9,4.5)); yrs=range(2010,2026)
for t in ypos:
    cum=[(ws[(ws.year<=y)].champion==t).sum() for y in yrs]; ax.step(yrs,cum,where='post',color=C[t],lw=2.5,label=t)
ax.set_title('Cumulative World Series titles: dynasty to parity'); ax.legend(fontsize=8,frameon=False,ncol=2); ax.set_ylabel('titles'); save('02_cumulative_titles.png')

# 3 titles vs runner-up
fr=pd.DataFrame({'t':ws.champion.value_counts(),'r':ws.runner_up.value_counts()}).fillna(0).assign(tot=lambda d:d.t+d.r).sort_values('tot')
fig,ax=plt.subplots(figsize=(8,5)); ax.barh(fr.index,fr.t,color=[C[i] for i in fr.index],label='Titles'); ax.barh(fr.index,fr.r,left=fr.t,color=[C[i] for i in fr.index],alpha=.35,label='Runner-up')
ax.set_title('World Series appearances (solid = won, faded = lost)'); save('03_finals_appearances.png')

# 4 series shape
fig,ax=plt.subplots(figsize=(9,4)); cols=ws.series_result.map({'3-0':'#2e9e5b','3-1':'#2f6fdb','3-2':'#e67e22'})
ax.bar(ws.year,ws.series_wins+ws.series_losses,color=cols); ax.set_ylim(0,5.8)
for _,r in ws.iterrows(): ax.text(r.year,r.series_wins+r.series_losses+.1,r.series_result,ha='center',fontsize=7)
ax.set_title('Series length by year (green sweep · blue 3-1 · orange decided in Game 5)'); ax.set_ylabel('games'); save('04_series_length.png')

# 5 perfect games
fig,ax=plt.subplots(figsize=(10,4)); order=pg.pitcher.value_counts().index.tolist()[::-1]
for _,r in pg.iterrows(): ax.scatter(r.date,order.index(r.pitcher),s=120,color='#d9a400',edgecolor='k',zorder=3)
ax.set_yticks(range(len(order))); ax.set_yticklabels(order); ax.grid(axis='y',alpha=.25); ax.set_title('15 official perfect games, 2010–2026'); save('05_perfect_games.png')

# 6 finals network
import math
ts=['Western Wildcats','Eastern Eagles','Central Cardinals','Northern Nighthawks','Midwest Mallards','Coastal Cobras','Pacific Predators','Great Lakes Gators','Downtown Diamondbacks','Metro Magic']
pos={t:(math.cos(2*math.pi*i/len(ts)),math.sin(2*math.pi*i/len(ts))) for i,t in enumerate(ts)}
fig,ax=plt.subplots(figsize=(7.5,7.5)); ax.axis('off')
for (a,b),n in ws.groupby(['champion','runner_up']).size().items():
    ax.annotate('',xy=pos[b],xytext=pos[a],arrowprops=dict(arrowstyle='-|>',color=C[a],lw=1.5+1.5*n,alpha=.7,shrinkA=22,shrinkB=22,connectionstyle='arc3,rad=.12'))
for t,(x,y) in pos.items(): ax.scatter(x,y,s=1500,color=C[t],zorder=3,edgecolor='k'); ax.text(x*1.25,y*1.25,t.replace(' ','\n',1),ha='center',va='center',fontsize=8)
ax.set_xlim(-1.7,1.7); ax.set_ylim(-1.6,1.6); ax.set_title('Finals network: arrow = champion → runner-up (thicker = repeat matchup)'); save('06_finals_network.png')

# 7 batting environment
fig,axs=plt.subplots(1,3,figsize=(11,3.8)); 
for ax,(k,l) in zip(axs,[('BB','BB% of PA'),('K','K% of PA'),('HR','HR per 100 PA')]):
    v=[b[k].sum()/b.PA.sum()*100 for b in (b17,b26)]; ax.bar(['2017','2026'],v,color=['#6c7a89','#d9a400']); ax.set_title(l)
    for i,x in enumerate(v): ax.text(i,x,f'{x:.1f}',ha='center',va='bottom')
plt.suptitle('Retrieved batting tables: more walks, fewer strikeouts and homers in 2026',fontweight='bold'); save('07_batting_environment.png')

# 8 scatter 2026
fig,ax=plt.subplots(figsize=(8,5.5))
for b,m,l in ((b17,'o','2017'),(b26,'s','2026')):
    ax.scatter(b.OBP,b.SLG,c=[C.get(t,'#888') for t in b.team],marker=m,s=70,edgecolor='k',alpha=.85,label=l)
ax.set_xlabel('OBP'); ax.set_ylabel('SLG'); ax.legend(title='season (circle/square)'); ax.set_title('OBP vs SLG, retrieved leaders (color = team)'); save('08_obp_slg.png')

# 9 coverage
m={'High':3,'Medium/High':2.5,'Medium':2,'Low/Medium':1.5,'Low':1}; fig,ax=plt.subplots(figsize=(8,6))
v=cov.confidence.map(m); ax.barh(cov.category[::-1],v[::-1],color=['#2e9e5b' if x>=3 else '#e6b800' if x>=2 else '#c0392b' for x in v[::-1]])
ax.set_xticks([1,2,3]); ax.set_xticklabels(['Low','Medium','High']); ax.set_title('Dataset coverage confidence by category'); save('09_coverage.png')

# 10 data model diagram
fig,ax=plt.subplots(figsize=(12,6.5)); ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,6.5)
def box(x,y,t,c='#e8f0f7',w=2.3,h=.9):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.04',fc=c,ec='#333',zorder=3)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=8.5,zorder=4)
    return (x+w/2,y+h/2)
N={'ws':box(4.8,3,'world_series\nyear · champion · runner_up\nvenue · series_result','#fff3cc'),
'mvp':box(8.6,4.6,'world_series_mvp\nyear · player · team'),'div':box(8.6,3,'division_champions\nyear · division · champion'),
'teams':box(1,3,'teams_history\nteam · tenure · manager','#dff3e6'),'pg':box(4.8,5.2,'perfect_games\ndate · pitcher · opponent'),
'ven':box(4.8,1.4,'venues\nvenue · location · years'),'play':box(8.6,1.4,'player_index / career_profiles\nplayer · verified · stats'),
'b':box(8.6,.1,'stats_2017 / 2026 batting\nplayer · team · PA…OPS'),'ev':box(1,1.2,'major_events · media\ntournaments · records'),'mh':box(1,5,'master_history\n(denormalized timeline)','#eee'),
'src':box(4.8,.1,'sources · coverage_matrix','#f5e1e1')}
for a,b in [('ws','teams'),('ws','ven'),('ws','mvp'),('ws','div'),('pg','teams'),('mvp','play'),('b','play'),('b','teams'),('div','teams'),('mh','ws'),('ev','ws')]:
    ax.annotate('',xy=N[b],xytext=N[a],arrowprops=dict(arrowstyle='-',color='#777',lw=1.2),zorder=1)
ax.set_title('Data model: how the 17 tables connect (keys: team name, year, player name)'); save('10_data_model.png')

# 11 pipeline
fig,ax=plt.subplots(figsize=(12,2.6)); ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,2.6)
st=['Official MLW\npages (retrieved)','17 CSV tables\n+ XLSX','analyze.py\n(pandas)','figures.py\n(matplotlib)','build_site.py\n(HTML + Chart.js)','README · paper\n· slides']
for i,s in enumerate(st):
    box(.1+i*2,.9,s,'#e8f0f7' if i%2==0 else '#fff3cc',w=1.7,h=1)
    if i<5: ax.annotate('',xy=(.1+(i+1)*2,1.4),xytext=(1.8+i*2,1.4),arrowprops=dict(arrowstyle='-|>',lw=1.5))
ax.set_title('Reproducible build pipeline'); save('11_pipeline.png')
