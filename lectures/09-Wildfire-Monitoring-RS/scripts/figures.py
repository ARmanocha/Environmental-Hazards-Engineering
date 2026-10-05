"""Figures for the wildfire lecture. Planck and sub-pixel figures are computed from physics; maps and series are simulated and labelled."""
import numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap, BoundaryNorm, LightSource
from matplotlib.patches import Patch
from scipy.ndimage import gaussian_filter, distance_transform_edt

os.makedirs('figs', exist_ok=True)
INK = '#13233A'; SOFT = '#4A5563'; RULE = '#E2DFD7'; ACC = '#C2410C'; BLUE = '#2F6DB5'; GREEN = '#3F7D3A'
plt.rcParams.update({'font.family': ['Helvetica', 'DejaVu Sans'], 'font.size': 18, 'axes.edgecolor': SOFT, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': SOFT, 'ytick.color': SOFT})
DPI = 200
out = {}
C1, C2 = 1.191042e8, 1.4387752e4          # W um^4 m-2 sr-1, um K
SIGMA = 5.670374e-8


def planck(lam, T):
    return C1 / (lam ** 5 * (np.exp(C2 / (lam * T)) - 1))


def btemp(lam, L):
    return C2 / (lam * np.log(1 + C1 / (lam ** 5 * L)))


def tag(ax, text='Simulated data', x=0.02, y=0.02, ha='left', va='bottom', fs=14):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=fs, color='white', ha=ha, va=va,
            bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))


def clean(ax):
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)


def sn(rng, shape, sigma):
    g = gaussian_filter(rng.normal(0, 1, shape), sigma)
    return g / g.std()


# ---------- 1. Planck curves (computed) ----------
lam = np.logspace(np.log10(0.5), np.log10(30), 600)
fig, ax = plt.subplots(figsize=(11.4, 6.4), dpi=DPI)
for T, c, lab in ((300, BLUE, 'Land, 300 K (27 °C)'), (600, '#E7A57A', 'Smouldering, 600 K'), (1000, ACC, 'Flaming fire, 1000 K')):
    ax.plot(lam, planck(lam, T), color=c, lw=3, label=lab)
    lp = 2897.77 / T
    ax.plot([lp], [planck(lp, T)], 'o', color=c, ms=9)
for b, lab in ((3.9, '3.9 µm\n(middle infrared)'), (11.0, '11 µm\n(thermal infrared)')):
    ax.axvspan(b * 0.97, b * 1.03, color='#E8E4DA', zorder=0)
    ax.text(b, 1.15e-2, lab, ha='center', va='bottom', fontsize=15, color=SOFT)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlim(0.5, 30); ax.set_ylim(1e-2, 3e4)
ax.set_xticks([0.5, 1, 2, 4, 10, 20]); ax.set_xticklabels(['0.5', '1', '2', '4', '10', '20'])
ax.set_xlabel('Wavelength (µm)'); ax.set_ylabel('Emitted radiance\n(W m⁻² sr⁻¹ µm⁻¹)')
ax.legend(loc='upper right', frameon=False, fontsize=16); clean(ax)
tag(ax, 'Computed: Planck’s law', x=0.02, y=0.97, va='top')
fig.subplots_adjust(left=0.13, right=0.98, top=0.97, bottom=0.13)
fig.savefig('figs/planck.png', facecolor='white'); plt.close(fig)
r39 = planck(3.9, 1000) / planck(3.9, 300); r11 = planck(11, 1000) / planck(11, 300)
out['planck'] = {'wien_300_um': round(2897.77 / 300, 1), 'wien_1000_um': round(2897.77 / 1000, 1), 'ratio_3.9': round(float(r39), 0), 'ratio_11': round(float(r11), 1)}

# ---------- 2. sub-pixel fire: brightness temperatures vs fire fraction (computed) ----------
p = np.logspace(-6, -1, 400)
Tb, Tf = 300.0, 1000.0
bt4 = btemp(3.9, p * planck(3.9, Tf) + (1 - p) * planck(3.9, Tb))
bt11 = btemp(11.0, p * planck(11.0, Tf) + (1 - p) * planck(11.0, Tb))
area = p * 1e6                                      # m2 in a 1 km pixel
fig, ax = plt.subplots(figsize=(11.4, 6.4), dpi=DPI)
ax.plot(area, bt4, color=ACC, lw=3.5, label='3.9 µm (middle infrared)')
ax.plot(area, bt11, color=BLUE, lw=3.5, label='11 µm (thermal infrared)')
ax.axhline(300, color=SOFT, lw=1, ls=':')
for A, lab in ((100, '10 × 10 m'), (1000, '≈ 32 × 32 m')):
    i = np.argmin(np.abs(area - A))
    ax.plot([A, A], [bt11[i], bt4[i]], color=SOFT, lw=1.5, ls='--')
    ax.annotate(f'{lab}: {bt4[i]:.0f} K vs {bt11[i]:.0f} K', xy=(A, bt4[i]), xytext=(A * 0.012, bt4[i] + 22), fontsize=15, color=INK,
                arrowprops=dict(arrowstyle='->', color=INK))
    out.setdefault('subpixel', {})[A] = {'bt4': round(float(bt4[i]), 0), 'bt11': round(float(bt11[i]), 0)}
ax.set_xscale('log'); ax.set_xlim(1, 1e5); ax.set_ylim(290, 520)
ax.set_xlabel('Area of fire inside a 1 km × 1 km pixel (m²)'); ax.set_ylabel('Brightness temperature\nof the whole pixel (K)')
ax.legend(loc='upper left', frameon=False, fontsize=16); ax.grid(axis='y', color=RULE); clean(ax)
tag(ax, 'Computed: 1000 K fire on 300 K ground', x=0.5, y=0.55, ha='center', va='center')
fig.subplots_adjust(left=0.13, right=0.98, top=0.97, bottom=0.13)
fig.savefig('figs/subpixel.png', facecolor='white'); plt.close(fig)

# ---------- 3. simulated fire spread and satellite detections ----------
rng = np.random.default_rng(4)
n = 300; ext = 30.0                                  # 30 km square
yy, xx = np.mgrid[0:n, 0:n] * ext / n
dem = 600 + 500 * sn(rng, (n, n), 30) + 120 * sn(rng, (n, n), 8)
fuel = sn(rng, (n, n), 12) > -1.2                      # about 90% burnable; the rest rock and fields
speed = 1 + 0.25 * sn(rng, (n, n), 6)
ign = (6.0, 6.0)
dx = xx - ign[0]; dy = yy - ign[1]
wind = np.array([0.76, 0.65])                           # towards the south-east (east, south)
along = dx * wind[0] + dy * wind[1]; across = -dx * wind[1] + dy * wind[0]
head, back, flank = 0.42, 0.05, 0.13                    # spread rates, km per hour
arrival = np.sqrt((np.maximum(along, 0) / head) ** 2 + (np.minimum(along, 0) / back) ** 2 + (across / flank) ** 2) / gaussian_filter(speed, 3)
arrival[~fuel] = np.inf
burned = (arrival < 72) & fuel
passes = [(13.5, 'Day 1, 13:30'), (25.5, 'Day 2, 01:30'), (37.5, 'Day 2, 13:30'), (49.5, 'Day 3, 01:30'), (61.5, 'Day 3, 13:30')]
cols = ['#F4D35E', '#F0A04B', '#E36414', '#C2410C', '#7A2A08']
ls = LightSource(azdeg=315, altdeg=45)
shade = ls.hillshade(dem, vert_exag=2, dx=100, dy=100)
fig, ax = plt.subplots(figsize=(9.8, 8.4), dpi=DPI)
ax.imshow(shade, cmap='gray', vmin=-0.5, vmax=1.4, extent=[0, ext, ext, 0])
ax.imshow(np.where(burned, 1.0, np.nan), cmap=ListedColormap(['#5B4636']), alpha=0.35, extent=[0, ext, ext, 0])
step = 375 / (ext * 1000 / n)                       # VIIRS 375 m sampling on the 100 m grid
gi = np.arange(0, n, int(round(3.75)))
GX, GY = np.meshgrid(gi, gi)
for (tp, lab), c in zip(passes, cols):
    front = (arrival[GY, GX] > tp - 5) & (arrival[GY, GX] <= tp) & fuel[GY, GX]
    keep = front & (rng.random(front.shape) < 0.8)
    frp = np.clip(rng.lognormal(2.5, 0.8, keep.sum()), 2, 300)
    jx = rng.uniform(-0.15, 0.15, keep.sum()); jy = rng.uniform(-0.15, 0.15, keep.sum())
    ax.scatter(xx[GY, GX][keep] + jx, yy[GY, GX][keep] + jy, s=8 + frp * 0.9, color=c, edgecolor='#3B2A20', lw=0.4, label=lab, zorder=3)
    out.setdefault('detections', {})[lab] = int(keep.sum())
ax.plot([ign[0]], [ign[1]], marker='*', ms=22, color='white', mec=INK, mew=1.5, zorder=4)
ax.text(ign[0] - 0.6, ign[1] - 1.0, 'Ignition', fontsize=15, color=INK, ha='center', bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85))
ax.annotate('', xy=(27, 4.5), xytext=(22.5, 0.6), arrowprops=dict(arrowstyle='-|>', color=INK, lw=3, mutation_scale=24))
ax.text(23.0, 3.6, 'Wind', fontsize=16, color=INK, rotation=-40)
ax.set_xlim(0, ext); ax.set_ylim(ext, 0); ax.set_xlabel('East (km)'); ax.set_ylabel('South (km)')
leg = ax.legend(loc='lower right', title='Satellite pass (dot size = FRP)', fontsize=14, title_fontsize=15, frameon=True, framealpha=0.9)
tag(ax, x=0.02, y=0.02)
fig.subplots_adjust(left=0.08, right=0.98, top=0.98, bottom=0.08)
fig.savefig('figs/hotspots.png', facecolor='white'); plt.close(fig)
out['burned_km2'] = round(float(burned.sum() * (ext / n) ** 2), 0)

# ---------- 4. spectra for NBR (schematic) ----------
wl = np.linspace(400, 2500, 800)
def bump(c, w): return np.exp(-((wl - c) / w) ** 2)
edge = 1 / (1 + np.exp(-(wl - 715) / 12))
wa = 1 - 0.55 * bump(1450, 60) - 0.7 * bump(1940, 80)
veg = (0.04 + 0.06 * bump(550, 35)) * (1 - edge) + edge * 0.48 * wa * (1 - 0.75 * np.clip((wl - 1300) / 900, 0, 1) ** 0.8)
burnt = 0.05 + 0.10 * np.clip((wl - 400) / 2100, 0, 1) ** 0.8 + 0.02 * np.clip((wl - 1500) / 1000, 0, 1)
R = lambda s, b: float(np.interp(b, wl, s))
nbr_v = (R(veg, 842) - R(veg, 2190)) / (R(veg, 842) + R(veg, 2190)); nbr_b = (R(burnt, 842) - R(burnt, 2190)) / (R(burnt, 842) + R(burnt, 2190))
out['nbr'] = {'veg': round(nbr_v, 2), 'burnt': round(nbr_b, 2), 'dnbr': round(nbr_v - nbr_b, 2)}
fig, ax = plt.subplots(figsize=(11.4, 6.2), dpi=DPI)
ax.plot(wl, veg * 100, color=GREEN, lw=3.5, label=f'Healthy forest (NBR {nbr_v:+.2f})')
ax.plot(wl, burnt * 100, color='#3B2A20', lw=3.5, label=f'Freshly burned (NBR {nbr_b:+.2f})')
for b, lab in ((842, 'NIR'), (2190, 'SWIR')):
    ax.axvspan(b - 25, b + 25, color='#E8E4DA', zorder=0); ax.text(b, 55, lab, ha='center', fontsize=16, color=SOFT)
ax.annotate('', xy=(842, R(burnt, 842) * 100 + 1), xytext=(842, R(veg, 842) * 100 - 1), arrowprops=dict(arrowstyle='->', color=ACC, lw=2.5))
ax.annotate('', xy=(2190, R(burnt, 2190) * 100 + 1), xytext=(2190, R(veg, 2190) * 100 - 1), arrowprops=dict(arrowstyle='->', color=ACC, lw=2.5))
ax.text(880, 30, 'NIR falls', fontsize=16, color=ACC); ax.text(2235, 17, 'SWIR rises', fontsize=16, color=ACC)
ax.set_xlim(400, 2500); ax.set_ylim(0, 58); ax.set_xlabel('Wavelength (nm)'); ax.set_ylabel('Reflectance (%)')
ax.legend(loc='upper right', bbox_to_anchor=(1.0, 0.92), frameon=False, fontsize=16); clean(ax)
tag(ax, 'Schematic: typical shapes', x=0.99, y=0.03, ha='right')
fig.subplots_adjust(left=0.08, right=0.98, top=0.97, bottom=0.13)
fig.savefig('figs/nbr.png', facecolor='white'); plt.close(fig)

# ---------- 5. pre / post false colour and dNBR severity ----------
rng = np.random.default_rng(8)
m = 260
yy2, xx2 = np.mgrid[0:m, 0:m] / m
scar = (((xx2 - 0.5) / 0.32) ** 2 + ((yy2 - 0.52) / 0.26) ** 2 + 0.35 * sn(rng, (m, m), 14)) < 1
inten = np.clip(1 - np.sqrt(((xx2 - 0.47) / 0.32) ** 2 + ((yy2 - 0.5) / 0.26) ** 2) + 0.25 * sn(rng, (m, m), 6), 0, 1) * scar
river = np.abs(yy2 - (0.85 + 0.05 * np.sin(xx2 * 9))) < 0.012
nir_pre = 0.32 + 0.03 * sn(rng, (m, m), 9); sw_pre = 0.09 + 0.012 * sn(rng, (m, m), 9); red_pre = 0.04 + 0.006 * sn(rng, (m, m), 9)
nir_post = nir_pre - 0.22 * inten; sw_post = sw_pre + 0.08 * inten; red_post = red_pre - 0.006 * inten
for a in (nir_pre, sw_pre, red_pre, nir_post, sw_post, red_post):
    a[river] = 0.02
nbr_pre = (nir_pre - sw_pre) / (nir_pre + sw_pre); nbr_post = (nir_post - sw_post) / (nir_post + sw_post)
dnbr = nbr_pre - nbr_post + 0.03 * rng.normal(0, 1, (m, m))
bounds = [-1, 0.1, 0.27, 0.44, 0.66, 2]
sev_cols = ['#DCE8D4', '#F3D3B5', '#E7A57A', '#C2410C', '#7A2A08']
names = ['Unburned (< 0.10)', 'Low (0.10–0.27)', 'Moderate-low (0.27–0.44)', 'Moderate-high (0.44–0.66)', 'High (> 0.66)']
def fc(sw, nir, red):
    return np.clip(np.dstack([sw / 0.35, nir / 0.45, red / 0.14]), 0, 1)
fig, axs = plt.subplots(1, 3, figsize=(15.6, 5.8), dpi=DPI)
axs[0].imshow(fc(sw_pre, nir_pre, red_pre)); axs[0].set_title('Before (SWIR, NIR, red)', loc='left', fontsize=19, fontweight='bold')
axs[1].imshow(fc(sw_post, nir_post, red_post)); axs[1].set_title('After', loc='left', fontsize=19, fontweight='bold')
axs[2].imshow(dnbr, cmap=ListedColormap(sev_cols), norm=BoundaryNorm(bounds, 5)); axs[2].set_title('dNBR = NBR before − after', loc='left', fontsize=19, fontweight='bold')
for a in axs:
    a.set_xticks([]); a.set_yticks([])
fig.legend([Patch(fc=c) for c in sev_cols], names, loc='lower center', ncol=5, frameon=False, fontsize=15)
tag(axs[0])
fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.12, wspace=0.04)
fig.savefig('figs/dnbr.png', facecolor='white'); plt.close(fig)
cls = np.digitize(dnbr[scar], bounds[1:-1])
out['dnbr_class_pct'] = {names[k].split(' (')[0]: round(float(np.mean(cls == k) * 100), 0) for k in range(5)}

# ---------- 6. recovery after fire ----------
rng = np.random.default_rng(11)
t = np.arange(2016, 2026, 16 / 365.25)
season = 0.08 * np.sin(2 * np.pi * (t - 0.6))
ctrl = 0.68 + season + rng.normal(0, 0.02, t.size)
fire_t = 2019.3
rec = np.where(t < fire_t, 0, 0.5 * np.exp(-(t - fire_t) / 2.2))
burn = 0.68 + season - rec + rng.normal(0, 0.02, t.size)
fig, ax = plt.subplots(figsize=(11.4, 6.0), dpi=DPI)
ax.plot(t, ctrl, color='#9CA3AF', lw=2, label='Unburned forest nearby')
ax.plot(t, burn, color=GREEN, lw=2.5, label='Burned forest')
ax.axvline(fire_t, color=ACC, lw=2, ls='--'); ax.text(fire_t + 0.08, 0.2, 'Fire', fontsize=17, color=ACC)
ax.set_ylabel('NDVI'); ax.set_ylim(0.1, 0.9); ax.set_xlim(2016, 2026)
ax.legend(loc='lower right', frameon=False, fontsize=16); ax.grid(axis='y', color=RULE); clean(ax)
tag(ax, x=0.02, y=0.97, va='top')
fig.subplots_adjust(left=0.09, right=0.98, top=0.97, bottom=0.08)
fig.savefig('figs/recovery.png', facecolor='white'); plt.close(fig)
yr = lambda y: float(np.mean((ctrl - burn)[(t > fire_t + y - 0.5) & (t < fire_t + y + 0.5)]))
out['recovery_gap'] = {'after_1yr': round(yr(1), 2), 'after_5yr': round(yr(5), 2)}

# ---------- 7. fire danger: vegetation dryness and fire counts by month ----------
rng = np.random.default_rng(13)
months = np.arange(12)
ndwi = np.array([0.18, 0.12, 0.05, -0.02, -0.06, -0.02, 0.15, 0.24, 0.24, 0.20, 0.17, 0.18]) + rng.normal(0, 0.01, 12)
fires = np.array([40, 120, 520, 1650, 2300, 900, 30, 5, 8, 60, 90, 50]) * rng.uniform(0.9, 1.1, 12)
fig, (a2, a1) = plt.subplots(2, 1, figsize=(11.4, 6.4), dpi=DPI, sharex=True, gridspec_kw={'height_ratios': [1, 1.4], 'hspace': 0.12})
a2.plot(months, ndwi, color=BLUE, lw=3.5, marker='o', ms=7)
a2.axhline(0, color=SOFT, lw=1, ls=':')
a2.set_ylabel('Vegetation\nwater (NDWI)'); a2.grid(axis='y', color=RULE); clean(a2)
a1.bar(months, fires, color=['#C2410C' if f > 500 else '#E7A57A' for f in fires], width=0.65)
a1.set_ylabel('Fire detections\nper month'); a1.grid(axis='y', color=RULE); clean(a1)
a1.set_xticks(months); a1.set_xticklabels(list('JFMAMJJASOND'))
tag(a2, x=0.99, y=0.06, ha='right', va='bottom')
fig.subplots_adjust(left=0.13, right=0.98, top=0.97, bottom=0.07)
fig.savefig('figs/season.png', facecolor='white'); plt.close(fig)

# ---------- banner: false-colour burn scar with fire front ----------
rng = np.random.default_rng(21)
H, W = 277, 1920
by, bx = np.mgrid[0:H, 0:W]
X = bx / W; Y = by / H
fx = 0.62 + 0.03 * np.sin(Y * 7) + 0.015 * np.sin(Y * 19 + 1)
scar_b = (X > 0.28 + 0.05 * np.sin(Y * 6)) & (X < fx)
front = np.abs(X - fx) < 0.0012
base_veg = np.dstack([0.25 + 0.05 * sn(rng, (H, W), 6), 0.55 + 0.08 * sn(rng, (H, W), 10), 0.22 + 0.04 * sn(rng, (H, W), 6)])
base_scar = np.dstack([0.55 + 0.06 * sn(rng, (H, W), 6), 0.22 + 0.04 * sn(rng, (H, W), 8), 0.18 + 0.03 * sn(rng, (H, W), 6)])
img = np.where(scar_b[..., None], base_scar, base_veg)
glow = gaussian_filter(front.astype(float), 2.0) * 3
img = np.clip(img + np.dstack([glow * 1.6, glow * 1.0, glow * 0.2]), 0, 1)
sm = gaussian_filter(rng.normal(0, 1, (H, W)), 14); sm = sm / sm.std()
smoke = np.clip(0.55 + 0.25 * sm - 1.6 * np.abs(Y - 0.35 - (X - fx) * 0.4), 0, 1) * (X > fx) * np.exp(-(X - fx) / 0.25) * 0.8
img = img * (1 - smoke[..., None]) + smoke[..., None] * np.array([0.85, 0.85, 0.88])
fig = plt.figure(figsize=(19.2, 2.77), dpi=150)
ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(np.clip(img, 0, 1), aspect='auto'); ax.axis('off')
ax.text(0.995, 0.04, 'Simulated data', transform=ax.transAxes, fontsize=11, color='white', ha='right', va='bottom', bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))
fig.savefig('figs/banner.png', facecolor='white'); plt.close(fig)

# ---------- worked numbers ----------
A = 1000.0
frp = SIGMA * A * (1000 ** 4 - 300 ** 4) / 1e6
out['frp_example_MW'] = round(frp, 1)
out['frp_biomass_t'] = round(frp * 10 * 3600 * 0.368 / 1000, 0)
json.dump(out, open('figs/stats.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
