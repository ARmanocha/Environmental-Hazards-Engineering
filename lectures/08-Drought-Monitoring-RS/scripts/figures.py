"""Figures for the drought-monitoring lecture. All data are simulated and labelled; spectra are schematic."""
import numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap, BoundaryNorm
from matplotlib.patches import Patch
from scipy.ndimage import gaussian_filter
from scipy import stats as sst

os.makedirs('figs', exist_ok=True)
INK = '#13233A'; SOFT = '#4A5563'; RULE = '#E2DFD7'; ACC = '#C2410C'; BLUE = '#2F6DB5'; GREEN = '#3F7D3A'
plt.rcParams.update({'font.family': ['Helvetica', 'DejaVu Sans'], 'font.size': 18, 'axes.edgecolor': SOFT, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': SOFT, 'ytick.color': SOFT})
DPI = 200
out = {}


def tag(ax, text='Simulated data', x=0.02, y=0.02, ha='left', va='bottom', fs=14):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=fs, color='white', ha=ha, va=va,
            bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))


def clean(ax):
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)


def sn(rng, shape, sigma):
    g = gaussian_filter(rng.normal(0, 1, shape), sigma)
    return g / g.std()


# ---------- 1. reflectance spectra (schematic) ----------
wl = np.linspace(400, 2400, 800)
def bump(c, w): return np.exp(-((wl - c) / w) ** 2)
edge = 1 / (1 + np.exp(-(wl - 715) / 12))
water_abs = 1 - 0.55 * bump(1450, 60) - 0.7 * bump(1940, 80)
healthy = (0.04 + 0.06 * bump(550, 35)) * (1 - edge) + edge * 0.50 * water_abs * (1 - 0.35 * np.clip((wl - 1300) / 1100, 0, 1))
stressed = (0.07 + 0.05 * bump(560, 50) + 0.04 * np.clip((wl - 600) / 120, 0, 1)) * (1 - edge) + edge * (0.32 * (0.6 + 0.4 * water_abs) + 0.06 * np.clip((wl - 1300) / 1100, 0, 1))
soil = 0.12 + 0.18 * np.clip((wl - 400) / 1600, 0, 1) - 0.04 * bump(1940, 80)
water = 0.06 * np.exp(-(wl - 400) / 250) + 0.005
R = lambda s, b: float(np.interp(b, wl, s))
nd = {k: round((R(s, 842) - R(s, 665)) / (R(s, 842) + R(s, 665)), 2) for k, s in (('healthy', healthy), ('stressed', stressed), ('soil', soil), ('water', water))}
out['ndvi'] = nd
fig, ax = plt.subplots(figsize=(11.4, 6.2), dpi=DPI)
for s, c, lab in ((healthy, GREEN, f'Healthy crop (NDVI {nd["healthy"]:.2f})'), (stressed, '#B7892B', f'Stressed crop (NDVI {nd["stressed"]:.2f})'),
                  (soil, '#8C6B4F', f'Dry soil (NDVI {nd["soil"]:.2f})'), (water, BLUE, 'Water')):
    ax.plot(wl, s * 100, color=c, lw=3, label=lab)
for b, lab in ((665, 'Red'), (842, 'NIR'), (1610, 'SWIR')):
    ax.axvspan(b - 20, b + 20, color='#E8E4DA', zorder=0)
    ax.text(b, 60, lab, ha='center', fontsize=15, color=SOFT)
ax.set_xlim(400, 2400); ax.set_ylim(0, 63)
ax.set_xlabel('Wavelength (nm)'); ax.set_ylabel('Reflectance (%)')
ax.legend(loc='upper right', frameon=False, fontsize=15)
clean(ax); tag(ax, 'Schematic: typical shapes', x=0.99, y=0.03, ha='right')
fig.subplots_adjust(left=0.08, right=0.98, top=0.97, bottom=0.13)
fig.savefig('figs/spectra.png', facecolor='white'); plt.close(fig)

# ---------- 2. SPI from simulated monthly rainfall ----------
rng = np.random.default_rng(3)
years = np.arange(1991, 2025)
clim = np.array([10, 8, 10, 15, 35, 160, 300, 270, 180, 70, 20, 10], float)    # monsoon climate, mm/month
yf = np.exp(rng.normal(0, 0.18, years.size))
for y, f in ((2002, 0.62), (2009, 0.6), (2014, 0.7), (2015, 0.58), (2019, 1.35), (2022, 0.75)):
    yf[years == y] = f
rain = np.array([[clim[m] * yf[i] * rng.gamma(4, 0.25) for m in range(12)] for i in range(years.size)]).ravel()
t = np.array([y + (m + 0.5) / 12 for y in years for m in range(12)])
r3 = np.convolve(rain, np.ones(3), 'full')[:rain.size]; r3[:2] = np.nan
spi = np.full(rain.size, np.nan)
for m in range(12):
    idx = np.arange(m, rain.size, 12); v = r3[idx]; ok = np.isfinite(v)
    a, loc, sc = sst.gamma.fit(v[ok], floc=0)
    spi[idx[ok]] = sst.norm.ppf(np.clip(sst.gamma.cdf(v[ok], a, loc=0, scale=sc), 1e-6, 1 - 1e-6))
# show September SPI-3 (Jul-Sep monsoon) per year
sep = spi[8::12]
out['spi_sep'] = {int(y): round(float(s), 2) for y, s in zip(years, sep)}
fig, ax = plt.subplots(figsize=(11.6, 6.0), dpi=DPI)
cols = [ACC if s <= -1 else ('#E7A57A' if s < 0 else '#8FB3DD') for s in sep]
ax.bar(years, sep, color=cols, width=0.75)
for thr, lab in ((-1, 'Moderate drought (−1)'), (-1.5, 'Severe (−1.5)'), (-2, 'Extreme (−2)')):
    ax.axhline(thr, color=SOFT, lw=1.2, ls='--')
    ax.text(1990.6, thr - 0.05, lab, fontsize=14, color=SOFT, va='top')
ax.axhline(0, color=INK, lw=1)
ax.set_ylabel('SPI-3 for July–September'); ax.set_xlim(1990, 2025); ax.set_ylim(-3.0, 2.6)
ax.grid(axis='y', color=RULE); clean(ax)
tag(ax, x=0.99, y=0.97, ha='right', va='top')
fig.subplots_adjust(left=0.1, right=0.98, top=0.97, bottom=0.08)
fig.savefig('figs/spi.png', facecolor='white'); plt.close(fig)

# ---------- 3. NDVI and VCI for a crop pixel ----------
rng = np.random.default_rng(5)
comp = np.arange(23)                        # 16-day composites per year
doy = comp * 16 + 8
yrs = np.arange(2001, 2025)
base = 0.18 + 0.55 * np.exp(-((doy - 255) / 45) ** 2) + 0.15 * np.exp(-((doy - 40) / 35) ** 2)
ndvi = np.array([base * (yf[np.where(years == y)[0][0]] ** 0.55 if y in years else 1) + rng.normal(0, 0.025, comp.size) for y in yrs])
ndvi = np.clip(ndvi, 0.05, 0.92)
nmin, nmax = ndvi.min(0), ndvi.max(0)
vci = (ndvi - nmin) / (nmax - nmin) * 100
iy = list(yrs).index(2015)
out['vci_2015_monsoon_mean'] = round(float(vci[iy, 13:19].mean()), 0)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(11.4, 6.8), dpi=DPI, sharex=True, gridspec_kw={'height_ratios': [1.6, 1], 'hspace': 0.08})
a1.fill_between(doy, nmin, nmax, color='#DCE8D4', label='Range in 2001–2024')
a1.plot(doy, np.median(ndvi, 0), color=SOFT, lw=2, ls='--', label='Typical year')
a1.plot(doy, ndvi[iy], color=ACC, lw=3.5, marker='o', ms=5, label='Drought year')
a1.set_ylabel('NDVI'); a1.legend(loc='upper left', frameon=False, fontsize=15); a1.grid(axis='y', color=RULE); clean(a1)
a2.bar(doy, vci[iy], width=12, color=[ACC if v < 35 else '#8FB3DD' for v in vci[iy]])
a2.axhline(35, color=SOFT, lw=1.3, ls='--'); a2.text(5, 38, 'VCI below 35: drought', fontsize=15, color=SOFT)
a2.set_ylabel('VCI (%)'); a2.set_ylim(0, 100); a2.set_xlabel('Day of year'); a2.grid(axis='y', color=RULE); clean(a2)
tag(a1, x=0.99, y=0.95, ha='right', va='top')
fig.subplots_adjust(left=0.1, right=0.98, top=0.97, bottom=0.1)
fig.savefig('figs/vci.png', facecolor='white'); plt.close(fig)

# ---------- 4. VCI, TCI and VHI maps for one drought month ----------
rng = np.random.default_rng(9)
n = 260
yy, xx = np.mgrid[0:n, 0:n] / n
region = ((xx - 0.5) ** 2 / 0.22 + (yy - 0.5) ** 2 / 0.2 + 0.08 * sn(rng, (n, n), 25)) < 1
dry = 0.95 * np.exp(-((xx - 0.38) ** 2 + (yy - 0.45) ** 2) / 0.06)
VCI = np.clip(62 - 62 * dry + 9 * sn(rng, (n, n), 8), 0, 100)
TCI = np.clip(58 - 55 * dry + 10 * sn(rng, (n, n), 12), 0, 100)
VHI = 0.5 * VCI + 0.5 * TCI
for a in (VCI, TCI, VHI):
    a[~region] = np.nan
bounds = [0, 10, 20, 30, 40, 100]
sev = ListedColormap(['#7A2A08', '#C2410C', '#E7A57A', '#F3D3B5', '#DCE8D4'])
fig, axs = plt.subplots(1, 3, figsize=(15.0, 6.0), dpi=DPI)
seq = LinearSegmentedColormap.from_list('vci', ['#7A2A08', '#E7A57A', '#F1EEE6', '#9CC08F', '#3F7D3A'])
for ax, (tt, f) in zip(axs[:2], (('VCI: vegetation condition', VCI), ('TCI: temperature condition', TCI))):
    im = ax.imshow(f, cmap=seq, vmin=0, vmax=100); ax.set_title(tt, loc='left', fontsize=19, fontweight='bold'); ax.axis('off')
im2 = axs[2].imshow(VHI, cmap=sev, norm=BoundaryNorm(bounds, 5)); axs[2].set_title('VHI = (VCI + TCI) ÷ 2', loc='left', fontsize=19, fontweight='bold'); axs[2].axis('off')
cb = fig.colorbar(im, ax=axs[:2], fraction=0.03, pad=0.02, orientation='horizontal', shrink=0.6); cb.set_label('Index value (0 = worst, 100 = best)', fontsize=18)
axs[2].legend([Patch(fc=c) for c in ['#7A2A08', '#C2410C', '#E7A57A', '#F3D3B5', '#DCE8D4']],
              ['Extreme (< 10)', 'Severe (10–20)', 'Moderate (20–30)', 'Mild (30–40)', 'No drought (≥ 40)'],
              loc='upper left', bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=18)
tag(axs[0], y=0.02)
fig.subplots_adjust(left=0.01, right=0.80, top=0.92, bottom=0.2, wspace=0.05)
fig.savefig('figs/vhi.png', facecolor='white'); plt.close(fig)
reg = VHI[region]
out['vhi_area_pct'] = {k: round(float(np.mean((reg >= lo) & (reg < hi)) * 100), 0) for k, lo, hi in (('extreme', 0, 10), ('severe', 10, 20), ('moderate', 20, 30), ('mild', 30, 40), ('none', 40, 101))}

# ---------- 5. GRACE-style terrestrial water storage anomaly ----------
rng = np.random.default_rng(12)
tm = np.arange(2002.3, 2025.0, 1 / 12)
tws = 6 * np.sin(2 * np.pi * (tm - 0.75)) + rng.normal(0, 1.2, tm.size)
trend = np.where(tm < 2012, 0, np.where(tm < 2016.8, -(tm - 2012) * 4.0, -19.2 + (tm - 2016.8) * 1.2))
trend = np.where(tm > 2019.5, -15.96 + 0 * tm, trend)
tws = tws + trend + 4
gap = (tm > 2017.5) & (tm < 2018.4)
tws[gap] = np.nan
fig, ax = plt.subplots(figsize=(11.6, 6.0), dpi=DPI)
ax.plot(tm, tws, color=INK, lw=2)
ax.axvspan(2012, 2016.8, color='#F3D3B5', alpha=0.7)
ax.text(2014.4, 13.5, 'Multi-year drought', ha='center', fontsize=16, color=ACC)
ax.axvspan(2017.5, 2018.4, color='#E5E2DA')
ax.text(2017.95, 16.2, 'Gap', ha='center', fontsize=15, color=SOFT, va='bottom')
ax.text(2003, 14.0, 'GRACE (2002–2017)', fontsize=15, color=SOFT); ax.text(2019.0, 14.0, 'GRACE-FO (2018– )', fontsize=15, color=SOFT)
ax.axhline(0, color=SOFT, lw=1)
ax.set_ylabel('Water storage anomaly\n(cm of water)'); ax.set_ylim(-28, 18); ax.set_xlim(2002, 2025)
ax.grid(axis='y', color=RULE); clean(ax); tag(ax, x=0.99, y=0.03, ha='right')
fig.subplots_adjust(left=0.12, right=0.98, top=0.97, bottom=0.08)
fig.savefig('figs/grace.png', facecolor='white'); plt.close(fig)

# ---------- banner: NDVI anomaly strip ----------
rng = np.random.default_rng(21)
B = 0.6 * sn(rng, (277, 1920), 40) + 0.4 * sn(rng, (277, 1920), 9)
xx_ = np.linspace(0, 1, 1920)[None, :]
B = B - 1.6 * np.exp(-((xx_ - 0.42) / 0.12) ** 2) + 0.5
div = LinearSegmentedColormap.from_list('ndvi_anom', ['#7A2A08', '#C2410C', '#E7A57A', '#F1EEE6', '#9CC08F', '#3F7D3A'])
fig = plt.figure(figsize=(19.2, 2.77), dpi=150)
ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(B, cmap=div, vmin=-2.6, vmax=2.6, aspect='auto'); ax.axis('off')
ax.text(0.995, 0.04, 'Simulated data', transform=ax.transAxes, fontsize=11, color='white', ha='right', va='bottom', bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))
fig.savefig('figs/banner.png', facecolor='white'); plt.close(fig)

json.dump(out, open('figs/stats.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
