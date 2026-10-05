"""Figures for the landslide-monitoring lecture: geometry (computed) and simulated example data (labelled)."""
import numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, TwoSlopeNorm
from matplotlib.patches import Ellipse, Polygon, FancyArrowPatch
from scipy.ndimage import gaussian_filter
from matplotlib.colors import LinearSegmentedColormap
from geo import sens, los, THETA

os.makedirs('figs', exist_ok=True)
INK = '#13233A'; SOFT = '#4A5563'; RULE = '#E2DFD7'; ACC = '#C2410C'; ASC = '#2F6DB5'; DESC = '#C2410C'
plt.rcParams.update({'font.family': ['Helvetica', 'DejaVu Sans'], 'font.size': 18, 'axes.edgecolor': SOFT, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': SOFT, 'ytick.color': SOFT, 'axes.spines.top': False, 'axes.spines.right': False})
DPI = 200
DIV = LinearSegmentedColormap.from_list('div', ['#123B6D', '#2F6DB5', '#8FB3DD', '#C9C4BA', '#E7A57A', '#C2410C', '#7A2A08'])
stats = {}


def tag(ax, x=0.01, y=0.01, ha='left', va='bottom'):
    ax.text(x, y, 'Simulated data', transform=ax.transAxes, fontsize=15, color='white', ha=ha, va=va,
            bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))


# ---------- 1. velocity scale (Cruden and Varnes 1996) and where each technique works ----------
yr = 1.0                      # mm/yr
UNIT = {'1 mm/yr': 1, '1 cm/yr': 10, '1 m/yr': 1e3, '1 m/month': 1.2e4, '1 m/day': 3.65e5, '1 m/hour': 8.76e6, '1 m/min': 5.26e8, '1 m/s': 3.156e10}
B = [0.3, 16, 1.6e3, 1.56e5, 1.58e7, 1.58e9, 1.58e11, 1.6e13]
NAMES = ['Extremely\nslow', 'Very\nslow', 'Slow', 'Moderate', 'Rapid', 'Very\nrapid', 'Extremely\nrapid']
SEQ = ['#F3E3D3', '#EBC8A6', '#E0A878', '#D3874E', '#C2652A', '#A84A17', '#7F3510']
fig, ax = plt.subplots(figsize=(16.2, 6.2), dpi=DPI)
for i in range(7):
    ax.add_patch(plt.Rectangle((np.log10(B[i]), 4.15), np.log10(B[i + 1]) - np.log10(B[i]), 1.2, fc=SEQ[i], ec='white', lw=3))
    ax.text((np.log10(B[i]) + np.log10(B[i + 1])) / 2, 4.75, NAMES[i],
            ha='center', va='center', fontsize=17, color=INK if i < 4 else 'white', linespacing=1.05)
TECH = [('InSAR time series, C-band (Sentinel-1)', 1, 800, ASC), ('InSAR, L-band (NISAR, ALOS-2)', 3, 1800, ASC),
        ('Offset tracking (SAR or optical images)', 300, 3.65e5, INK), ('Ground-based radar (GB-InSAR)', 10, 3e6, INK)]
for j, (name, lo, hi, c) in enumerate(TECH):
    y = 3.2 - j * 0.85
    ax.add_patch(plt.Rectangle((np.log10(lo), y - 0.27), np.log10(hi) - np.log10(lo), 0.54, fc=c, ec='none', alpha=0.9))
    ax.text(np.log10(hi) + 0.15, y, name, va='center', fontsize=18, color=INK)
ax.set_xlim(np.log10(0.3), np.log10(1.6e13)); ax.set_ylim(-0.2, 5.5)
ax.set_xticks([np.log10(v) for v in UNIT.values()]); ax.set_xticklabels(list(UNIT.keys()), fontsize=17)
ax.set_yticks([]); ax.spines['left'].set_visible(False)
ax.set_xlabel('Landslide velocity (log scale)')
fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.14)
fig.savefig('figs/scale.png', facecolor='white'); plt.close(fig)

# ---------- 2. cross-section: what an ascending pass sees on each side of a ridge ----------
xs = np.array([0, 1.6, 2.8, 3.55, 4.6, 5.6, 6.2, 7.6, 10.0])
zs = np.array([0, 0, 0.56, 1.45, 1.83, 1.25, 0.21, 0.0, 0.0])
t = np.radians(THETA)
def ground(x):
    return np.interp(x, xs, zs)
fig, ax = plt.subplots(figsize=(11.6, 6.6), dpi=DPI)
cls = {'fore': ('#F4C9A0', 'Foreshortened (squeezed)'), 'lay': ('#C2410C', 'Layover (unusable)'),
       'good': ('#8FB3DD', 'Well seen (stretched)'), 'shadow': ('#6B7280', 'Shadow (no signal)'), 'flat': ('#E8E4DA', 'Flat ground')}
for i in range(len(xs) - 1):
    dx, dz = xs[i + 1] - xs[i], zs[i + 1] - zs[i]
    b = np.degrees(np.arctan2(dz, dx))
    k = 'flat' if abs(b) < 1 else (('lay' if b > THETA else 'fore') if b > 0 else ('shadow' if -b > 90 - THETA else 'good'))
    ax.add_patch(Polygon([[xs[i], -0.35], [xs[i], zs[i]], [xs[i + 1], zs[i + 1]], [xs[i + 1], -0.35]], fc=cls[k][0], ec='none'))
    if k != 'flat':
        nx_, nz_ = -dz / np.hypot(dx, dz), dx / np.hypot(dx, dz)
        ax.text((xs[i] + xs[i + 1]) / 2 + 0.32 * nx_, (zs[i] + zs[i + 1]) / 2 + 0.32 * nz_, f'{abs(b):.0f}°', fontsize=18,
                ha='center', va='center', color=INK)
# radar shadow cast by the steep back slope: ground hidden behind the ray grazing point (4.6, 1.83)... use the crest at 5.6
x0, z0 = xs[5], zs[5]
xx = np.linspace(x0, 10, 2000); zr = z0 - (xx - x0) / np.tan(t)
hit = xx[np.argmax(zr <= ground(xx))]
ax.add_patch(Polygon([[x0, z0]] + [[x, ground(x)] for x in np.linspace(x0, hit, 40)], fc='#4B5563', alpha=0.35, ec='none'))
ax.plot(xs, zs, color=INK, lw=2.5)
# radar rays, stopping where they reach the ground
for xs0 in np.arange(-1.9, 6.6, 0.75):
    xx = np.linspace(xs0, xs0 + 6, 3000); zr = 3.0 - (xx - xs0) / np.tan(t)
    j = np.argmax(zr <= ground(xx))
    ax.annotate('', xy=(xx[j], zr[j]), xytext=(xs0, 3.0), arrowprops=dict(arrowstyle='-|>', color=ASC, lw=1.5, alpha=0.7, mutation_scale=15))
ax.text(-0.4, 3.2, 'Ascending pass: the radar looks east, 39° from vertical', color=ASC, fontsize=18, fontweight='bold')
ax.text(0.3, -0.2, 'West', fontsize=18, color=SOFT, va='center'); ax.text(9.0, -0.2, 'East', fontsize=18, color=SOFT, va='center')
order = ('fore', 'lay', 'good', 'shadow')
ax.legend([plt.Rectangle((0, 0), 1, 1, fc=cls[k][0]) for k in order], [cls[k][1] for k in order], loc='upper center',
          bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False, fontsize=17, columnspacing=2.5)
ax.set_xlim(-0.5, 10); ax.set_ylim(-0.35, 3.5); ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.17)
fig.savefig('figs/geom.png', facecolor='white'); plt.close(fig)

# ---------- 3. sensitivity versus slope aspect (computed, 30° slope) ----------
asp = np.linspace(0, 360, 721)
fig = plt.figure(figsize=(8.4, 8.0), dpi=DPI)
ax = fig.add_subplot(111, projection='polar')
ax.set_theta_zero_location('N'); ax.set_theta_direction(-1)
for g, c, lab in (('asc', ASC, 'Ascending (looks east)'), ('desc', DESC, 'Descending (looks west)')):
    ax.plot(np.radians(asp), 100 * np.abs(sens(asp, 30, g)), color=c, lw=3.5, label=lab)
ax.fill_between(np.radians(asp), 0, 30, color='#E8E4DA', alpha=0.8, zorder=0, label='Under 30%: poorly seen')
ax.set_ylim(0, 100); ax.set_yticks([30, 50, 75, 100]); ax.set_yticklabels(['', '50%', '75%', '100%'], fontsize=15, color=SOFT)
ax.set_rlabel_position(202)
ax.set_xticks(np.radians(np.arange(0, 360, 45))); ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], fontsize=19)
ax.grid(color=RULE, lw=1.2)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.04), ncol=2, frameon=False, fontsize=17)
fig.subplots_adjust(left=0.06, right=0.94, top=0.94, bottom=0.17)
fig.savefig('figs/sens.png', facecolor='white'); plt.close(fig)
stats['C30'] = {a: {g: round(float(sens(v, 30, g)), 3) for g in ('asc', 'desc')} for a, v in (('N', 0), ('E', 90), ('S', 180), ('W', 270))}


# ---------- 4. simulated velocity maps, ascending and descending ----------
def terrain(nx, ny, dxkm, seed, valleys):
    rng = np.random.default_rng(seed)
    x = np.arange(nx) * dxkm; y = np.arange(ny) * dxkm
    X, Y = np.meshgrid(x, y[::-1])
    h = np.full_like(X, 2400.0)
    for xv in valleys:
        axis = xv + 0.25 * np.sin(Y / 1.1) + 0.12 * np.sin(Y / 0.37)
        h = np.minimum(h, 700 + 600 * np.abs(X - axis))
    h += 90 * np.sin(2 * np.pi * Y / 1.3) * np.clip(np.abs(X - np.mean(valleys)) / 3, 0, 1)
    h += gaussian_filter(rng.normal(0, 1, X.shape), 6) * 260 + gaussian_filter(rng.normal(0, 1, X.shape), 2.5) * 60
    wob = gaussian_filter(rng.normal(0, 1, X.shape), 18) * 9
    gul = np.sin(2 * np.pi * Y / 0.5 + wob + 1.5 * np.sin(X / 0.7))
    h -= 28 * np.clip(gul, 0, None) ** 4 * np.clip(np.abs(X - np.mean(valleys)) / 1.0, 0, 1) * (1 + gaussian_filter(rng.normal(0, 1, X.shape), 8) * 3).clip(0, 2)
    h = gaussian_filter(h, 1.5)
    return X, Y, h, rng


def slides_field(X, Y, slides):
    v = np.zeros_like(X)
    for cx, cy, ax_, ay, vmax in slides:
        r2 = ((X - cx) / ax_) ** 2 + ((Y - cy) / ay) ** 2
        v += vmax * np.clip(1 - r2, 0, None) ** 0.7
    return v


def los_vel(X, Y, h, vdown, dxkm, geom, rng, noise=1.3):
    gy, gx = np.gradient(h, dxkm * 1000)          # gy along rows (top = north): rows go south
    dhdx, dhdn = gx, -gy
    slope = np.degrees(np.arctan(np.hypot(dhdx, dhdn)))
    aspect = np.degrees(np.arctan2(-dhdx, -dhdn)) % 360
    C = sens(aspect, slope, geom)
    s = los(geom)
    # local geometry: layover if slope towards the satellite steeper than incidence; shadow if away and steeper than 90 - incidence
    gaz = np.radians({'asc': 260, 'desc': 100}[geom])
    rng_slope = np.degrees(np.arctan(-(dhdx * np.sin(gaz) + dhdn * np.cos(gaz))))   # >0: rises away from satellite, faces it
    bad = (rng_slope > THETA) | (-rng_slope > 90 - THETA)
    vl = vdown * C + rng.normal(0, noise, X.shape) + gaussian_filter(rng.normal(0, 1, X.shape), 12) * 4
    return vl, bad, slope, aspect


def points(X, rng, bad, forest, base=0.05):
    p = np.where(forest, 0.008, base)
    keep = (rng.random(X.shape) < p) & ~bad
    return keep


NX, NY, DX = 300, 240, 0.02     # 6 km x 4.8 km
X, Y, h, rng = terrain(NX, NY, DX, 3, [3.0])
SL = [(1.85, 3.1, 0.55, 0.75, 42.0), (4.15, 1.55, 0.5, 0.65, 28.0)]
vd = slides_field(X, Y, SL)
fz = gaussian_filter(rng.normal(0, 1, X.shape), 10)
forest = fz / fz.std() > 0.8                     # smooth random field scaled to unit variance: ~20% forest
ls = LightSource(azdeg=315, altdeg=40)
shade = ls.hillshade(h, vert_exag=1.5, dx=DX * 1000, dy=DX * 1000)
fig, axs = plt.subplots(1, 2, figsize=(16.6, 6.5), dpi=DPI)
norm = TwoSlopeNorm(vmin=-40, vcenter=0, vmax=40)
ext = [0, NX * DX, 0, NY * DX]
for ax, g, title in ((axs[0], 'asc', 'Ascending pass (looks east)'), (axs[1], 'desc', 'Descending pass (looks west)')):
    vl, bad, slope, aspect = los_vel(X, Y, h, vd, DX, g, np.random.default_rng(11 if g == 'asc' else 12))
    keep = points(X, np.random.default_rng(5), bad, forest)
    ax.imshow(shade, cmap='gray', extent=ext, vmin=-0.9, vmax=1.25)
    ax.imshow(np.where(forest, 1.0, np.nan), cmap='Greens', vmin=0, vmax=4, alpha=0.35, extent=ext)
    sc = ax.scatter(X[keep], Y[keep], c=vl[keep], cmap=DIV, norm=norm, s=10, lw=0)
    for k, (cx, cy, a_, b_, _) in enumerate(SL):
        ax.add_patch(Ellipse((cx, cy), 2 * a_, 2 * b_, fill=False, ls='--', lw=2, ec=INK))
        ax.text(cx + a_ * 0.75, cy + b_ * 0.95, 'AB'[k], fontsize=22, fontweight='bold', color=INK,
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85))
        inside = keep & (((X - cx) / (a_ * 0.5)) ** 2 + ((Y - cy) / (b_ * 0.5)) ** 2 < 1)
        stats[f'{g}_{"AB"[k]}_median'] = round(float(np.median(vl[inside])), 1)
    ax.set_title(title, fontsize=20, color=ASC if g == 'asc' else DESC, fontweight='bold', loc='left')
    ax.set_xlabel('East (km)'); ax.set_ylabel('North (km)')
    tag(ax)
cb = fig.colorbar(sc, ax=axs, fraction=0.025, pad=0.02)
cb.set_label('LOS velocity (mm/yr)\npositive = towards satellite', fontsize=17)
fig.subplots_adjust(left=0.05, right=0.86, top=0.92, bottom=0.12, wspace=0.18)
fig.savefig('figs/vel.png', facecolor='white'); plt.close(fig)
gy, gx = np.gradient(h, DX * 1000)
asp_all = np.degrees(np.arctan2(-gx, gy)) % 360
for k, (cx, cy, a_, b_, vmax) in enumerate(SL):
    m = ((X - cx) / a_) ** 2 + ((Y - cy) / b_) ** 2 < 0.25
    stats[f'slide_{"AB"[k]}'] = {'vmax_down': vmax, 'mean_aspect': round(float(np.degrees(np.angle(np.mean(np.exp(1j * np.radians(asp_all[m]))))) % 360), 0),
                                 'mean_slope': round(float(np.mean(np.degrees(np.arctan(np.hypot(gx, gy)))[m])), 1)}

# ---------- banner: three valleys, ascending velocities ----------
X2, Y2, h2, rng2 = terrain(1100, 160, 0.02, 8, [3.0, 9.6, 16.2])
SL2 = [(1.9, 1.7, 0.5, 0.6, 40), (4.1, 1.2, 0.5, 0.6, 30), (8.5, 1.9, 0.45, 0.55, 35), (10.7, 1.4, 0.5, 0.6, 25), (15.1, 1.6, 0.5, 0.6, 38), (17.3, 1.9, 0.45, 0.5, 30)]
vd2 = slides_field(X2, Y2, SL2)
fz2 = gaussian_filter(rng2.normal(0, 1, X2.shape), 10)
fo2 = fz2 / fz2.std() > 0.8
vl2, bad2, _, _ = los_vel(X2, Y2, h2, vd2, 0.02, 'desc', np.random.default_rng(4))
vl2a, bad2a, _, _ = los_vel(X2, Y2, h2, vd2, 0.02, 'asc', np.random.default_rng(6))
vcomb = np.where(np.abs(vl2a) > np.abs(vl2), vl2a, vl2)
keep2 = points(X2, np.random.default_rng(9), bad2 & bad2a, fo2, 0.07)
sh2 = LightSource(azdeg=315, altdeg=40).hillshade(h2, vert_exag=1.5, dx=20, dy=20)
fig = plt.figure(figsize=(19.2, 2.77), dpi=150)
ax = fig.add_axes([0, 0, 1, 1]); ext2 = [0, 22, 0, 3.2]
ax.imshow(sh2, cmap='gray', extent=ext2, vmin=-0.9, vmax=1.25, aspect='auto')
ax.scatter(X2[keep2], Y2[keep2], c=vcomb[keep2], cmap=DIV, norm=norm, s=7, lw=0)
ax.set_xlim(0, 22); ax.set_ylim(0, 3.2); ax.axis('off')
ax.text(21.85, 0.12, 'Simulated data', fontsize=11, color='white', ha='right', va='bottom', bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))
fig.savefig('figs/banner.png', facecolor='white'); plt.close(fig)

# ---------- 5. simulated time series with monsoon rainfall ----------
days = np.arange(np.datetime64('2019-01-01'), np.datetime64('2025-01-01'))
t = (days - days[0]).astype(float)
mon = np.array([d.astype(object).month for d in days]); yrs = np.array([d.astype(object).year for d in days])
MONTHLY = {1: 15, 2: 20, 3: 25, 4: 30, 5: 60, 6: 260, 7: 470, 8: 420, 9: 250, 10: 70, 11: 15, 12: 10}
YF = {2019: 1.0, 2020: 0.9, 2021: 1.05, 2022: 0.85, 2023: 1.55, 2024: 1.0}
rd = np.array([MONTHLY[m] * YF[y] for m, y in zip(mon, yrs)]) / 30 * np.random.default_rng(2).gamma(0.6, 1 / 0.6, len(days))
W = np.zeros_like(rd)
for i in range(1, len(rd)):
    W[i] = W[i - 1] * np.exp(-1 / 45) + rd[i]
v = 0.015 + 0.000022 * np.clip(W - 250, 0, None) ** 1.5      # mm/day downslope
down = np.cumsum(v)
C_A = stats['C30']['E']['asc']
ep = np.arange(0, len(days), 12)
rngt = np.random.default_rng(21)
los_ts = C_A * down[ep] + rngt.normal(0, 2.0, len(ep)); los_ts -= los_ts[0]
ref_ts = rngt.normal(0, 2.0, len(ep)); ref_ts -= ref_ts[0]
ym = [(y, m) for y in range(2019, 2025) for m in range(1, 13)]
rain_m = [rd[(yrs == y) & (mon == m)].sum() for y, m in ym]
mdates = np.array([np.datetime64(f'{y}-{m:02d}-15') for y, m in ym])
fig, (a1, a2) = plt.subplots(2, 1, figsize=(11.4, 6.6), dpi=DPI, sharex=True, gridspec_kw={'height_ratios': [1, 2.3], 'hspace': 0.08})
a1.bar(mdates, rain_m, width=25, color='#8FB3DD')
a1.set_ylabel('Rain\n(mm/month)', fontsize=16); a1.set_yticks([0, 400, 800])
a2.plot(days[ep], ref_ts, 'o', ms=4, color='#9CA3AF', label='Stable ground nearby')
a2.plot(days[ep], los_ts, 'o-', ms=4, lw=1.2, color=INK, label='Point on the landslide')
a2.set_ylabel('LOS displacement (mm)\nascending, negative = away', fontsize=16)
a2.legend(loc='lower left', frameon=False, fontsize=16)
a2.grid(axis='y', color=RULE)
i23 = np.argmin(np.abs(days[ep] - np.datetime64('2023-10-15')))
a2.annotate('Very wet monsoon (2023):\nbiggest jump', xy=(days[ep][i23], los_ts[i23]), xytext=(np.datetime64('2021-07-01'), -72),
            fontsize=16, color=INK, arrowprops=dict(arrowstyle='->', color=INK, lw=1.4))
tag(a2, 0.99, 0.97, 'right', 'top')
fig.subplots_adjust(left=0.13, right=0.98, top=0.97, bottom=0.07)
fig.savefig('figs/ts.png', facecolor='white'); plt.close(fig)
ann = {int(y): round(float(-(los_ts[(days[ep] >= np.datetime64(f'{y}-01-01')) & (days[ep] < np.datetime64(f'{y + 1}-01-01'))][[0, -1]] @ [1, -1])), 0) for y in range(2019, 2024)}
stats['ts_total_los_mm'] = round(float(los_ts[-1]), 0); stats['ts_down_per_year_mm'] = {int(y): round(float(down[yrs == y][-1] - down[yrs == y][0]), 0) for y in range(2019, 2025)}

# ---------- 6. simulated precursory acceleration and inverse-velocity forecast ----------
A = 1 / (0.4 * 150)
te = np.arange(-150, -5, 6.0)                     # Sentinel-1 every 6 days, last image 6 days before failure
x_true = (1 / A) * np.log(150 / -te)
rngi = np.random.default_rng(31)
x_obs = x_true + rngi.normal(0, 1.5, len(te))
win = 3
tv = np.array([te[i:i + win + 1].mean() for i in range(len(te) - win)])
vv = np.array([np.polyfit(te[i:i + win + 1], x_obs[i:i + win + 1], 1)[0] for i in range(len(te) - win)])
iv = 1 / vv
fit_m = tv >= -75
p = np.polyfit(tv[fit_m], iv[fit_m], 1)
tf_pred = -p[1] / p[0]
stats['ivel'] = {'tf_pred_days': round(float(tf_pred), 1), 'last_image_day': -6, 'v_start_mm_day': 0.4, 'v_last_mm_day': round(float(1 / (A * 6)), 1),
                 'x_last_mm': round(float(x_true[-1]), 0)}
fig, (a1, a2) = plt.subplots(2, 1, figsize=(11.4, 6.6), dpi=DPI, sharex=True, gridspec_kw={'hspace': 0.1})
a1.plot(te, x_obs, 'o-', color=INK, ms=5, lw=1.4)
a1.set_ylabel('Downslope\ndisplacement (mm)', fontsize=16); a1.grid(axis='y', color=RULE)
a2.plot(tv, iv, 'o', color=INK, ms=6, label='1 / velocity from the time series')
tt = np.linspace(-80, tf_pred, 50)
a2.plot(tt, np.polyval(p, tt), '--', color=ACC, lw=2.5, label='Straight-line fit, extended to zero')
a2.set_ylim(0, 2.0); a2.set_ylabel('1 / velocity\n(days per mm)', fontsize=16); a2.grid(axis='y', color=RULE)
for a in (a1, a2):
    a.axvline(0, color=SOFT, lw=1.5)
a2.text(-1.5, 1.85, 'Failure\n(day 0)', ha='right', va='top', fontsize=15, color=SOFT)
a2.annotate(f'Forecast failure: day −{abs(tf_pred):.0f}', xy=(tf_pred, 0.0), xytext=(-6, 0.85), ha='right', fontsize=16, color=ACC,
            arrowprops=dict(arrowstyle='->', color=ACC, lw=1.5))
a2.legend(loc='lower left', frameon=False, fontsize=15)
a2.set_xlabel('Days before failure'); a2.set_xlim(-155, 8)
tag(a1, 0.01, 0.95, 'left', 'top')
fig.subplots_adjust(left=0.13, right=0.98, top=0.97, bottom=0.12)
fig.savefig('figs/ivel.png', facecolor='white'); plt.close(fig)

json.dump(stats, open('figs/stats.json', 'w'), indent=1)
print(json.dumps(stats, indent=1))
