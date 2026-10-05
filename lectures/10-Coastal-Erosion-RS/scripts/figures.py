"""Figures for the coastal-erosion lecture. The breakwater figure is computed from the Pelnard-Considère one-line model;
scenes, shorelines and rates are simulated and labelled; the beach profile is schematic."""
import numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Polygon
from scipy.ndimage import gaussian_filter
from scipy.special import erfc

os.makedirs('figs', exist_ok=True)
INK = '#13233A'; SOFT = '#4A5563'; RULE = '#E2DFD7'; ACC = '#C2410C'; BLUE = '#2F6DB5'; SAND = '#E9D7A7'; SEA = '#8FB3DD'; GREEN = '#6E9A5B'
plt.rcParams.update({'font.family': ['Helvetica', 'DejaVu Sans'], 'font.size': 18, 'axes.edgecolor': SOFT, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': SOFT, 'ytick.color': SOFT})
DPI = 200
DIV = LinearSegmentedColormap.from_list('div', ['#7A2A08', '#C2410C', '#E7A57A', '#ECE9E2', '#8FB3DD', '#2F6DB5', '#123B6D'])
out = {}


def tag(ax, text='Simulated data', x=0.02, y=0.02, ha='left', va='bottom', fs=14):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=fs, color='white', ha=ha, va=va,
            bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))


def clean(ax):
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)


def sn(rng, shape, sigma):
    g = gaussian_filter(rng.normal(0, 1, shape), sigma)
    return g / g.std()


# ---------- one-line model (Pelnard-Considère, 1956): shoreline next to a long breakwater ----------
EPS = 0.30          # shoreline diffusivity, km2 per year
TANA = 0.05         # angle of breaking waves to the shoreline (tan), about 3 degrees


def oneline(x_km, t_yr, eps=EPS, tana=TANA):
    """Shoreline change (km, positive = seaward) at distance x from a structure that blocks all longshore transport.
    Drift runs towards +x: sand piles up on the updrift side (x < 0) and the downdrift side (x > 0) erodes."""
    if t_yr <= 0:
        return np.zeros_like(x_km)
    s = np.sqrt(eps * t_yr)
    u = np.abs(x_km) / (2 * s)
    y = tana * (2 * s / np.sqrt(np.pi) * np.exp(-u ** 2) - np.abs(x_km) * erfc(u))
    return np.where(x_km < 0, y, -y)


x = np.linspace(-8, 8, 801)
fig, ax = plt.subplots(figsize=(11.6, 6.2), dpi=DPI)
for t, c in ((1, '#C9C4BA'), (5, '#8FB3DD'), (15, BLUE), (30, '#123B6D')):
    ax.plot(x, oneline(x, t) * 1000, color=c, lw=3, label=f'After {t} year{"s" if t > 1 else ""}')
ax.axhline(0, color=SOFT, lw=1.2, ls=':')
ax.plot([0, 0], [0, 260], color=INK, lw=6, solid_capstyle='butt')
ax.text(0.15, 245, 'Breakwater', fontsize=16, color=INK)
ax.annotate('', xy=(5.5, 225), xytext=(2.0, 225), arrowprops=dict(arrowstyle='-|>', color=ACC, lw=3, mutation_scale=22))
ax.text(3.75, 235, 'Longshore drift', fontsize=16, color=ACC, ha='center')
ax.text(-4.5, 135, 'Updrift: sand piles up', fontsize=17, color=BLUE, ha='center')
ax.text(4.5, -150, 'Downdrift: beach erodes', fontsize=17, color=ACC, ha='center')
ax.set_xlabel('Distance along the coast from the breakwater (km)'); ax.set_ylabel('Shoreline change (m)\npositive = seaward')
ax.set_xlim(-8, 8); ax.set_ylim(-210, 270); ax.grid(axis='y', color=RULE); clean(ax)
ax.legend(loc='lower left', frameon=False, fontsize=15)
tag(ax, 'Computed: one-line model', x=0.99, y=0.03, ha='right')
fig.subplots_adjust(left=0.12, right=0.98, top=0.97, bottom=0.12)
fig.savefig('figs/breakwater.png', facecolor='white'); plt.close(fig)
out['oneline'] = {'max_change_m_30yr': round(float(oneline(np.array([-1e-6]), 30)[0] * 1000), 0),
                  'affected_km_30yr': round(float(2 * np.sqrt(EPS * 30)), 1)}

# ---------- schematic beach profile with shoreline indicators ----------
xs = np.linspace(0, 205, 820)
z = np.where(xs < 40, 7.5, np.where(xs < 55, 7.5 - (xs - 40) * 0.23, 4.05 - (xs - 55) * 0.04))
fig, ax = plt.subplots(figsize=(13.2, 5.8), dpi=DPI)
ax.fill_between(xs, -3.5, z, color=SAND, zorder=1)
ax.fill_between(xs, -3.5, np.minimum(z, 7.5), where=xs < 42, color='#C9B48A', zorder=1)
for xv in (8, 20, 32):
    ax.plot([xv, xv], [7.5, 9.4], color=GREEN, lw=4); ax.plot([xv], [9.8], 'o', ms=20, color=GREEN)
wl = 0.6
ax.fill_between(xs, z, wl, where=z < wl, color=SEA, alpha=0.75, zorder=2)
for lv, lab in ((1.4, 'High tide (MHW)'), (0.0, 'Mean sea level'), (-1.4, 'Low tide (MLW)')):
    ax.plot([95, 205], [lv, lv], color=BLUE, lw=1.6, ls='--', zorder=3)
    ax.text(207, lv, lab, fontsize=15, color=BLUE, va='center')
def xat(level): return float(np.interp(-level, -z, xs))
marks = [(40.0, 'Vegetation\nline'), (xat(1.4), 'High-water\nline'), (xat(wl), 'Waterline\nin the image'), (xat(0.0), 'Shoreline\nat mean sea level')]
for i, (xm, lab) in enumerate(marks):
    top = 11.0 if i % 2 == 0 else 13.6
    ax.plot([xm, xm], [-3.0, top - 0.2], color=ACC if i == 2 else INK, lw=1.4, ls=':', zorder=4)
    ax.text(xm, top, lab, fontsize=15, color=ACC if i == 2 else INK, ha='center', va='bottom')
ax.text(150, -2.6, 'Beach slope 1:25', fontsize=15, color=SOFT)
ax.set_xlim(0, 245); ax.set_ylim(-3.5, 16.6); ax.axis('off')
ax.text(244, -3.4, 'Schematic', fontsize=13, color='white', ha='right', va='bottom', bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none'))
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig('figs/profile.png', facecolor='white'); plt.close(fig)

# ---------- simulated coastal scene, MNDWI and waterline ----------
rng = np.random.default_rng(3)
n = 300
yy, xx = np.mgrid[0:n, 0:n]
shore = 150 + 25 * np.sin(xx / 60) + 8 * sn(rng, (1, n), 10)[0][None, :]
dist = yy - shore                                   # >0 sea (south), <0 land
sand = (dist < 0) & (dist > -28 - 6 * sn(rng, (n, n), 12))
veg = dist <= -28 - 6 * sn(rng, (n, n), 12)
sea = dist >= 0
green = np.where(sea, 0.06, np.where(sand, 0.24, 0.10)) + 0.006 * sn(rng, (n, n), 4)
swir = np.where(sea, 0.015, np.where(sand, 0.30, 0.16)) + np.where(sea, 0.002, 0.008) * sn(rng, (n, n), 4)
foam = (dist >= 0) & (dist < 4)
green = np.where(foam, 0.20, green); swir = np.where(foam, 0.04, swir)
red = np.where(sea, 0.05, np.where(sand, 0.26, 0.07)) + 0.006 * sn(rng, (n, n), 4)
red = np.where(foam, 0.20, red)
blue = np.where(sea, 0.09, np.where(sand, 0.20, 0.06)) + 0.006 * sn(rng, (n, n), 4)
blue = np.where(foam, 0.22, blue)
swir = np.clip(swir, 0.005, None); green = np.clip(green, 0.005, None)
mndwi = (green - swir) / (green + swir)
v = mndwi.ravel(); h, e = np.histogram(v, 256); c = (e[:-1] + e[1:]) / 2
w0 = np.cumsum(h); w1 = w0[-1] - w0; m0 = np.cumsum(h * c) / np.maximum(w0, 1); m1 = (np.sum(h * c) - np.cumsum(h * c)) / np.maximum(w1, 1)
thr = float(c[np.argmax(w0 * w1 * (m0 - m1) ** 2)]); out['mndwi_otsu'] = round(thr, 2)
fig, axs = plt.subplots(1, 3, figsize=(16.6, 5.8), dpi=DPI, gridspec_kw={'width_ratios': [1, 1, 1.15]})
rgb = np.clip(np.dstack([red, green, blue]) / 0.32, 0, 1)
axs[0].imshow(rgb); axs[0].set_title('True colour', loc='left', fontsize=19, fontweight='bold')
im = axs[1].imshow(mndwi, cmap='RdBu', vmin=-0.8, vmax=0.8); axs[1].contour(mndwi, levels=[thr], colors=[ACC], linewidths=2.5)
axs[1].set_title('MNDWI and the waterline', loc='left', fontsize=19, fontweight='bold')
for a in axs[:2]:
    a.set_xticks([]); a.set_yticks([])
axs[2].hist(v, bins=120, color='#9CA3AF')
axs[2].axvline(thr, color=ACC, lw=3, ls='--'); axs[2].text(thr + 0.03, axs[2].get_ylim()[1] * 0.9, f'Otsu\nthreshold\n{thr:.2f}', color=ACC, fontsize=15, va='top')
axs[2].set_xlim(-0.8, 1.0)
axs[2].text(-0.55, axs[2].get_ylim()[1] * 0.55, 'Land', fontsize=17, color=SOFT, ha='center'); axs[2].text(0.75, axs[2].get_ylim()[1] * 0.55, 'Water', fontsize=17, color=BLUE, ha='center')
axs[2].set_xlabel('MNDWI'); axs[2].set_yticks([]); axs[2].set_title('Histogram', loc='left', fontsize=19, fontweight='bold'); clean(axs[2]); axs[2].spines['left'].set_visible(False)
tag(axs[0])
fig.subplots_adjust(left=0.01, right=0.98, top=0.9, bottom=0.12, wspace=0.08)
fig.savefig('figs/waterline.png', facecolor='white'); plt.close(fig)

# ---------- shorelines through time around a harbour, and rates (simulated from the one-line model) ----------
rng = np.random.default_rng(7)
xk = np.linspace(-6, 6, 241)                         # km along the coast
years = np.arange(1990, 2026)
background = -0.4                                    # m/yr everywhere (sea-level rise, less river sand)
SLOPE = 0.04                                         # beach slope, 1:25
true = {int(yv): oneline(xk, yv - 1990) * 1000 + background * (yv - 1990) for yv in years}
# a waterline per year at a random tide (m), seen through a 10 m pixel with sub-pixel noise
tides = rng.uniform(-0.9, 0.9, years.size)
obs = {int(yv): true[int(yv)] - tides[i] / SLOPE + rng.normal(0, 5, xk.size) for i, yv in enumerate(years)}
corr = {int(yv): obs[int(yv)] + tides[i] / SLOPE for i, yv in enumerate(years)}
A = np.vstack([years - years.mean(), np.ones(years.size)]).T
Y = np.array([corr[int(yv)] for yv in years])
lrr = np.linalg.lstsq(A, Y, rcond=None)[0][0]        # m/yr per transect
out['lrr_range'] = [round(float(lrr.min()), 1), round(float(lrr.max()), 1)]
out['lrr_eroding_pct'] = round(float(np.mean(lrr < -0.5) * 100), 0)
# map view: land at the bottom, sea at the top; positive = seaward (up)
fig, ax = plt.subplots(figsize=(14.6, 6.2), dpi=DPI)
base_y = -350
ax.fill_between(xk, 600, true[2025], color=SEA)
ax.fill_between(xk, true[2025], -500, color=SAND)
cm = plt.get_cmap('viridis')
for yv in (1990, 2000, 2010, 2025):
    ax.plot(xk, corr[yv], color=cm((yv - 1990) / 35), lw=2.2, label=str(yv))
ax.plot([0, 0], [-60, 420], color=INK, lw=6, solid_capstyle='butt'); ax.plot([0.25, 0.25], [-140, 360], color=INK, lw=6, solid_capstyle='butt')
ax.text(-0.2, 400, 'Harbour, built 1990', fontsize=15, color=INK, ha='right')
ax.axhline(base_y, color=INK, lw=2, ls='--'); ax.text(-5.9, base_y - 70, 'Baseline (onshore)', fontsize=15, color=INK)
for xt in np.arange(-5.5, 6, 0.5):
    i = np.argmin(np.abs(xk - xt))
    ax.plot([xt, xt], [base_y, 280], color=DIV(TwoSlopeNorm(vcenter=0, vmin=-6, vmax=6)(lrr[i])), lw=3.2, alpha=0.95)
ax.annotate('', xy=(-2.6, 500), xytext=(-5.0, 500), arrowprops=dict(arrowstyle='-|>', color=ACC, lw=3, mutation_scale=20))
ax.text(-3.8, 530, 'Longshore drift', fontsize=15, color=ACC, ha='center')
ax.text(-5.9, 420, 'Sea', fontsize=17, color=INK); ax.text(-5.9, -470, 'Land', fontsize=17, color=INK)
ax.set_xlim(-6, 6); ax.set_ylim(-500, 600); ax.set_xlabel('Distance along the coast (km)'); ax.set_ylabel('Seaward of the 1990 shoreline (m)')
ax.legend(title='Shoreline', loc='upper right', fontsize=14, title_fontsize=15, ncol=4, frameon=True, framealpha=0.9)
sm = plt.cm.ScalarMappable(cmap=DIV, norm=TwoSlopeNorm(vcenter=0, vmin=-6, vmax=6)); cb = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.01); cb.set_label('Transect rate (m/yr)', fontsize=16)
tag(ax, x=0.99, y=0.02, ha='right')
fig.subplots_adjust(left=0.08, right=0.98, top=0.97, bottom=0.12)
fig.savefig('figs/dsas.png', facecolor='white'); plt.close(fig)

# rates along the coast
fig, ax = plt.subplots(figsize=(11.6, 6.0), dpi=DPI)
cols = [ACC if r < -0.5 else (BLUE if r > 0.5 else '#C9C4BA') for r in lrr]
ax.bar(xk, lrr, width=0.045, color=cols)
ax.axhspan(-0.5, 0.5, color='#E8E4DA', zorder=0); ax.text(-5.8, -7.4, 'Grey band (±0.5 m/yr): call it stable', fontsize=15, color=SOFT)
ax.axvline(0, color=INK, lw=3); ax.text(0.15, ax.get_ylim()[1] * 0.85 if False else 6.2, 'Harbour', fontsize=15, color=INK)
ax.set_xlabel('Distance along the coast (km)'); ax.set_ylabel('Linear regression rate (m/yr)')
ax.set_ylim(-8, 7.5); ax.grid(axis='y', color=RULE); clean(ax)
ax.text(-3.0, 4.2, 'Accreting', fontsize=17, color=BLUE, ha='center'); ax.text(3.0, -6.4, 'Eroding', fontsize=17, color=ACC, ha='center')
tag(ax, x=0.99, y=0.03, ha='right')
fig.subplots_adjust(left=0.1, right=0.98, top=0.97, bottom=0.12)
fig.savefig('figs/rates.png', facecolor='white'); plt.close(fig)

# one transect: raw vs tide-corrected, EPR vs LRR
j = np.argmin(np.abs(xk - 1.5))
raw = np.array([obs[int(yv)][j] for yv in years]); cor = np.array([corr[int(yv)][j] for yv in years])
p = np.polyfit(years, cor, 1); epr = (cor[-1] - cor[0]) / (years[-1] - years[0])
out['transect'] = {'x_km': round(float(xk[j]), 2), 'lrr': round(float(p[0]), 2), 'epr': round(float(epr), 2), 'nsm': round(float(cor[-1] - cor[0]), 0),
                   'raw_std': round(float(np.std(raw - np.polyval(np.polyfit(years, raw, 1), years))), 0), 'cor_std': round(float(np.std(cor - np.polyval(p, years))), 0)}
fig, ax = plt.subplots(figsize=(11.6, 6.0), dpi=DPI)
ax.plot(years, raw, 'o', color='#C9C4BA', ms=7, label='Waterline as seen (any tide)')
ax.plot(years, cor, 'o', color=INK, ms=7, label='Corrected to mean sea level')
ax.plot(years, np.polyval(p, years), color=ACC, lw=3, label=f'Linear regression: {p[0]:.1f} m/yr')
ax.plot([years[0], years[-1]], [cor[0], cor[-1]], color=BLUE, lw=2, ls='--', label=f'End points only: {epr:.1f} m/yr')
ax.set_xlabel('Year'); ax.set_ylabel('Shoreline position on the transect (m)'); ax.grid(axis='y', color=RULE); clean(ax)
ax.legend(loc='lower left', frameon=False, fontsize=15)
tag(ax, x=0.99, y=0.97, ha='right', va='top')
fig.subplots_adjust(left=0.11, right=0.98, top=0.97, bottom=0.12)
fig.savefig('figs/transect.png', facecolor='white'); plt.close(fig)

# ---------- banner: aerial coast with shorelines ----------
rng = np.random.default_rng(21)
H, W = 277, 1920
by, bx = np.mgrid[0:H, 0:W]
xkm = (bx / W) * 24 - 12
sl = 140 + oneline(xkm[0], 30) * 300 + 2 * sn(rng, (1, W), 8)[0]
sea_b = by > sl[None, :]
img = np.where(sea_b[..., None], np.array([0.33, 0.55, 0.70]), np.array([0.90, 0.83, 0.62]))
img = img + 0.015 * sn(rng, (H, W), 6)[..., None]
inland = by < sl[None, :] - 45 - 8 * sn(rng, (H, W), 12)
img = np.where(inland[..., None], np.array([0.40, 0.55, 0.33]) + 0.05 * sn(rng, (H, W), 6)[..., None], img)
img = np.clip(img, 0, 1)
fig = plt.figure(figsize=(19.2, 2.77), dpi=150)
ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(img, aspect='auto', extent=[0, W, H, 0])
for t, c in ((0, '#FFFFFF'), (10, '#F4D35E'), (20, '#E36414'), (30, '#7A2A08')):
    ax.plot(np.arange(W), 140 + oneline(xkm[0], t) * 300, color=c, lw=2.0)
ax.plot([W / 2, W / 2], [140 - 60, 268], color='#3B3B3B', lw=6)
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
ax.text(0.995, 0.04, 'Simulated data', transform=ax.transAxes, fontsize=11, color='white', ha='right', va='bottom', bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))
fig.savefig('figs/banner.png', facecolor='white'); plt.close(fig)

json.dump(out, open('figs/stats.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
