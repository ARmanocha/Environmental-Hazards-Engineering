"""Kilauea 2018 figures from COMET-LiCSAR products. Run download_data.sh first."""
import numpy as np, rasterio, json, matplotlib, os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, hsv_to_rgb, LightSource
from rasterio.windows import from_bounds
INK='#13233A'; SOFT='#4A5563'
plt.rcParams.update({'font.family':['Helvetica','DejaVu Sans'],'font.size':16,'text.color':INK,'axes.labelcolor':INK,'xtick.color':SOFT,'ytick.color':SOFT})
hh=np.linspace(0,1,256); PHASE=LinearSegmentedColormap.from_list('phase',hsv_to_rgb(np.stack([hh,0.72*np.ones(256),0.95*np.ones(256)],1)))
LAM=5.5465763  # cm
os.makedirs('figs', exist_ok=True)
def read(name, b):
    with rasterio.open('raw/'+name) as r:
        w=from_bounds(*b, r.transform); a=r.read(1, window=w).astype(float)
        nd=r.nodata
    if nd is not None and not np.isnan(nd): a[a==nd]=np.nan
    return a
SITES=[('Summit (Halemaʻumaʻu)',-155.2834,19.4072,'^'),("Puʻu ʻŌʻō",-155.1048,19.3886,'^'),('Leilani Estates fissures',-154.9086,19.4619,'*'),('M6.9 epicentre, 4 May',-155.000,19.318,'o')]
def marks(ax, labels=True, color='black'):
    for n,x,y,m in SITES:
        ax.plot(x,y,marker=m,ms=13 if m!='*' else 18,mfc='white' if m=='o' else color,mec=color,mew=2,ls='none',zorder=5)
        if labels:
            dx,dy,ha={'Summit (Halemaʻumaʻu)':(-0.012,0.022,'center'),"Puʻu ʻŌʻō":(0,0.022,'center'),'Leilani Estates fissures':(-0.01,0.022,'right'),'M6.9 epicentre, 4 May':(-0.015,-0.035,'right')}[n]
            ax.text(x+dx,y+dy,n,fontsize=15,ha=ha,va='bottom',color=INK,fontweight='bold',zorder=6,
                    bbox=dict(boxstyle='round,pad=0.2',fc=(1,1,1,0.78),ec='none'))
def base(b):
    h=read('124A_06996_091406.geo.hgt.tif', b); h[np.isnan(h)]=0
    ls=LightSource(azdeg=315, altdeg=40); return ls.hillshade(h, vert_exag=0.03, dx=100, dy=100), h
def fig_map(name, data, cmap, b, label, vmin=None, vmax=None, norm=None, ticks=None, ticklabels=None, labels=True, extra=None, credit='LiCSAR / COMET; contains modified Copernicus Sentinel data (2018)'):
    hs,h=base(b)
    fig=plt.figure(figsize=(8.2,6.4),dpi=200)
    ax=fig.add_axes([0.10,0.10,0.70,0.85]); cax=fig.add_axes([0.83,0.16,0.03,0.72])
    ext=(b[0],b[2],b[1],b[3])
    sea=np.ma.masked_where(h>0, np.ones_like(h))
    ax.imshow(hs,cmap='gray',extent=ext,vmin=0,vmax=1.4,interpolation='bilinear')
    ax.imshow(sea,cmap=LinearSegmentedColormap.from_list('s',['#D7E3EE','#D7E3EE']),extent=ext,interpolation='nearest')
    im=ax.imshow(np.ma.masked_invalid(data),cmap=cmap,vmin=None if norm else vmin,vmax=None if norm else vmax,norm=norm,extent=ext,alpha=0.92,interpolation='bilinear')
    ax.set_xlabel('Longitude (°)',fontsize=16); ax.set_ylabel('Latitude (°)',fontsize=16); ax.tick_params(labelsize=13)
    ax.set_aspect(1/np.cos(np.radians(19.4)))
    marks(ax, labels)
    if extra: extra(ax)
    cb=fig.colorbar(im,cax=cax); cb.set_label(label,fontsize=16); cb.ax.tick_params(labelsize=13)
    if ticks is not None: cb.set_ticks(ticks)
    if ticklabels is not None: cb.set_ticklabels(ticklabels)
    ax.text(0.01,0.01,credit,transform=ax.transAxes,fontsize=10.5,color=INK,va='bottom',bbox=dict(boxstyle='round,pad=0.25',fc=(1,1,1,0.8),ec='none'))
    fig.savefig('figs/'+name+'.png',facecolor='white'); plt.close(fig)

ZOOM=(-155.42,19.17,-154.80,19.58)   # west, south, east, north
ISL=(-156.10,18.88,-154.78,20.30)
PT=[-np.pi,0,np.pi]; PL=['−π','0','π']
# 1) whole island, 2-8 May wrapped (filtered)
w_isl=read('20180502_20180508.geo.diff_pha.tif',ISL)
def box(ax):
    ax.plot([ZOOM[0],ZOOM[2],ZOOM[2],ZOOM[0],ZOOM[0]],[ZOOM[1],ZOOM[1],ZOOM[3],ZOOM[3],ZOOM[1]],color='black',lw=2.2,ls=(0,(6,4)))
    ax.text(ZOOM[0]+0.01,ZOOM[3]+0.02,'Kīlauea area',fontsize=15,fontweight='bold',color=INK,bbox=dict(boxstyle='round,pad=0.2',fc=(1,1,1,0.8),ec='none'))
fig_map('k_island', w_isl, PHASE, ISL, 'Phase (radians)', -np.pi, np.pi, ticks=PT, ticklabels=PL, labels=False, extra=box)
# 2) zoom wrapped 2-8 May, unfiltered and filtered
for tag,f in (('k_wrap_unf','20180502_20180508.geo.diff_unfiltered_pha.tif'),('k_wrap','20180502_20180508.geo.diff_pha.tif'),('k_wrap_pre','20180420_20180502.geo.diff_pha.tif')):
    fig_map(tag, read(f,ZOOM), PHASE, ZOOM, 'Phase (radians)', -np.pi, np.pi, ticks=PT, ticklabels=PL)
# 3) coherence
cc=read('20180502_20180508.geo.cc.tif',ZOOM)/255.0
fig_map('k_coh', cc, 'gray', ZOOM, 'Coherence', 0, 1, ticks=[0,0.25,0.5,0.75,1])
# 4) LOS displacement (positive = toward satellite), referenced to a stable area north of Kilauea
u=read('20180502_20180508.geo.unw.tif',ZOOM); u[u==0]=np.nan
d=-u*LAM/(4*np.pi)
with rasterio.open('raw/20180502_20180508.geo.unw.tif') as r:
    ref=r.read(1, window=from_bounds(-155.30,19.50,-155.15,19.58,r.transform)).astype(float)
ref[ref==0]=np.nan; dref=np.nanmedian(-ref*LAM/(4*np.pi)); d=d-dref
A=(-155.22,19.52); Bp=(-154.93,19.25)
def prof(ax):
    ax.plot([A[0],Bp[0]],[A[1],Bp[1]],color='black',lw=2.4,ls=(0,(7,4)))
    ax.text(A[0]-0.012,A[1]+0.008,'A',fontsize=19,fontweight='bold'); ax.text(Bp[0]+0.006,Bp[1]-0.025,'B',fontsize=19,fontweight='bold')
lim=np.nanpercentile(np.abs(d),99.5)
norm=TwoSlopeNorm(vmin=-60,vcenter=0,vmax=20)
fig_map('k_disp', d, 'RdBu_r', ZOOM, 'LOS displacement (cm)\npositive = toward satellite', norm=norm, extra=prof)
# 5) pre-eruption LOS displacement 20 Apr-2 May
u2=read('20180420_20180502.geo.unw.tif',ZOOM); u2[u2==0]=np.nan
with rasterio.open('raw/20180420_20180502.geo.unw.tif') as r:
    ref2=r.read(1, window=from_bounds(-155.30,19.50,-155.15,19.58,r.transform)).astype(float)
ref2[ref2==0]=np.nan; d2=-u2*LAM/(4*np.pi) - np.nanmedian(-ref2*LAM/(4*np.pi))
fig_map('k_disp_pre', d2, 'RdBu_r', ZOOM, 'LOS displacement (cm)\npositive = toward satellite', norm=TwoSlopeNorm(vmin=-30,vcenter=0,vmax=15))
# 6) profile A-B
n=500; lons=np.linspace(A[0],Bp[0],n); lats=np.linspace(A[1],Bp[1],n)
H,W=d.shape; cols=((lons-ZOOM[0])/(ZOOM[2]-ZOOM[0])*W).astype(int).clip(0,W-1); rows=((ZOOM[3]-lats)/(ZOOM[3]-ZOOM[1])*H).astype(int).clip(0,H-1)
dist=np.hypot((lons-A[0])*111.32*np.cos(np.radians(19.4)),(lats-A[1])*110.57)
vals=d[rows,cols]
from scipy.ndimage import uniform_filter1d
fig,ax=plt.subplots(figsize=(10,4.4),dpi=200)
ax.plot(dist,vals,color='#4F86C6',lw=1.2,alpha=0.45,label='Every pixel')
v2=np.where(np.isfinite(vals),vals,np.nan)
import warnings; warnings.filterwarnings('ignore')
sm=np.array([np.nanmedian(v2[max(0,i-6):i+7]) for i in range(n)])
ax.plot(dist,sm,color='#C2410C',lw=2.6,label='Smoothed')
ax.axhline(0,color='#999',lw=1); ax.set_xlim(0,dist[np.isfinite(vals)].max()+0.5)
ax.set_xlabel('Distance along profile A–B (km)',fontsize=17); ax.set_ylabel('LOS displacement (cm)',fontsize=17)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',color='#E4E2DC'); ax.legend(frameon=False,fontsize=14,loc='lower left'); ax.tick_params(labelsize=13)
fig.tight_layout(); fig.savefig('figs/k_profile.png',facecolor='white'); plt.close(fig)
st={'d_min':float(np.nanmin(d)),'d_max':float(np.nanmax(d)),'d_p1':float(np.nanpercentile(d,0.5)),'pre_min':float(np.nanmin(d2)),'pre_max':float(np.nanmax(d2)),
    'prof_min':float(np.nanmin(sm)),'prof_max':float(np.nanmax(sm)),'cc_mean_zoom':float(np.nanmean(cc)),'valid_frac':float(np.isfinite(d).mean())}
json.dump(st,open('kstats.json','w'),indent=1); print(json.dumps(st,indent=1))
