"""Figures for the land-subsidence lecture. All data are simulated and labelled; geometry uses Sentinel-1 values."""
import numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, hsv_to_rgb
from scipy.ndimage import gaussian_filter
from geo import los

os.makedirs('figs', exist_ok=True)
INK = '#13233A'; SOFT = '#4A5563'; RULE = '#E2DFD7'; ACC = '#C2410C'; BLUE = '#2F6DB5'; NODATA = '#D9D6CE'
plt.rcParams.update({'font.family': ['Helvetica', 'DejaVu Sans'], 'font.size': 18, 'axes.edgecolor': SOFT, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': SOFT, 'ytick.color': SOFT})
DPI = 200
LAM = 5.5466
DIV = LinearSegmentedColormap.from_list('div', ['#123B6D', '#2F6DB5', '#8FB3DD', '#ECE9E2', '#E7A57A', '#C2410C', '#7A2A08'])
hh = np.linspace(0, 1, 256)
PHASE = LinearSegmentedColormap.from_list('phase', hsv_to_rgb(np.stack([hh, 0.72 * np.ones(256), 0.95 * np.ones(256)], 1)))
stats = {}


def tag(ax, text='Simulated data', x=0.02, y=0.02, ha='left', va='bottom', fs=14):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=fs, color='white', ha=ha, va=va,
            bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))


def bowls(X, Y, spec):
    """Vertical velocity (mm/yr, negative = down) and radial horizontal velocity towards bowl centres."""
    vz = np.zeros_like(X); ve = np.zeros_like(X); vn = np.zeros_like(X)
    for cx, cy, s, v0 in spec:
        r2 = (X - cx) ** 2 + (Y - cy) ** 2
        g = np.exp(-r2 / (2 * s ** 2))
        vz += -v0 * g
        # horizontal motion towards the centre, largest on the flanks (about 0.3 of the peak vertical)
        k = 0.5 * v0 * g / s
        ve += -k * (X - cx) * 1.0
        vn += -k * (Y - cy) * 1.0
    return vz, ve, vn


# ---------- city map: vertical velocity points ----------
n = 400; ext = 20.0                                 # 20 km x 20 km
g1 = np.linspace(0, ext, n)
X, Y = np.meshgrid(g1, g1[::-1])
SPEC = [(8.5, 11.0, 2.2, 110.0), (14.0, 6.0, 1.5, 45.0), (4.0, 4.5, 1.2, 25.0)]
vz, ve, vn = bowls(X, Y, SPEC)
rng = np.random.default_rng(4)
uz = gaussian_filter(rng.normal(0, 1, X.shape), 18)
urban = uz / uz.std() > -0.2                     # smooth random field scaled to unit variance: ~60% built-up, the rest fields
city_core = ((X - 9) ** 2 / 36 + (Y - 10) ** 2 / 49) < 1
dens = np.where(city_core, 0.09, np.where(urban, 0.03, 0.006))
keep = rng.random(X.shape) < dens
noise = gaussian_filter(rng.normal(0, 1, X.shape), 10) * 3 + rng.normal(0, 1.5, X.shape)
vz_obs = vz + noise
fig, ax = plt.subplots(figsize=(10.4, 8.6), dpi=DPI)
ax.set_facecolor('#F3F1EC')
ax.add_patch(plt.Polygon([[0, 13.5], [20, 15.5], [20, 16.1], [0, 14.1]], fc='#BFD3E6', ec='none'))   # river
ax.text(1, 14.6, 'River', fontsize=15, color=BLUE)
for yy in (3, 8, 12.5, 17.5):
    ax.plot([0, 20], [yy, yy + 0.4], color='#D9D4C7', lw=2, zorder=1)
for xx in (3, 7, 11, 15, 18.5):
    ax.plot([xx, xx + 0.5], [0, 20], color='#D9D4C7', lw=2, zorder=1)
ax.plot([0, 20], [2.0, 13.0], color=INK, lw=2.5, ls='--', zorder=2)
ax.text(16.6, 12.0, 'Railway', fontsize=15, color=INK, rotation=27)
norm = TwoSlopeNorm(vmin=-100, vcenter=0, vmax=20)
sc = ax.scatter(X[keep], Y[keep], c=vz_obs[keep], cmap=DIV, norm=norm, s=7, lw=0, zorder=3)
ax.plot([6.0], [12.6], marker='s', ms=12, mfc='none', mec=INK, mew=2.5, zorder=4)
ax.text(5.2, 13.15, 'Building\n(next slide)', fontsize=14, color=INK, ha='right', va='bottom')
for cx, cy, s, v0 in SPEC:
    ax.text(cx, cy, f'{-v0:.0f}', fontsize=15, ha='center', va='center', color='white', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', fc=INK, ec='none', alpha=0.8), zorder=5)
ax.set_xlim(0, 20); ax.set_ylim(0, 20); ax.set_xlabel('East (km)'); ax.set_ylabel('North (km)')
cb = fig.colorbar(sc, ax=ax, fraction=0.04, pad=0.02, extend='min'); cb.set_label('Vertical velocity (mm/yr), negative = sinking', fontsize=16)
tag(ax)
fig.subplots_adjust(left=0.1, right=0.9, top=0.98, bottom=0.08)
fig.savefig('figs/city.png', facecolor='white'); plt.close(fig)
stats['bowls_peak_mm_yr'] = [s[3] for s in SPEC]

# ---------- decomposition: ascending, descending -> vertical, east-west ----------
sa, sd = los('asc'), los('desc')
la = ve * sa[0] + vn * sa[1] + vz * sa[2]
ld = ve * sd[0] + vn * sd[1] + vz * sd[2]
# least squares for (E, U) ignoring north
A = np.array([[sa[0], sa[2]], [sd[0], sd[2]]])
Ainv = np.linalg.inv(A)
E_est = Ainv[0, 0] * la + Ainv[0, 1] * ld
U_est = Ainv[1, 0] * la + Ainv[1, 1] * ld
stats['decomp_err_max_mm_yr'] = round(float(np.max(np.abs(U_est - vz))), 1)
stats['cos_theta'] = round(float(sa[2]), 3)
fig, axs = plt.subplots(1, 4, figsize=(17.4, 5.4), dpi=DPI)
norm = TwoSlopeNorm(vmin=-100, vcenter=0, vmax=40)
for ax, (t, f) in zip(axs, (('Ascending LOS', la), ('Descending LOS', ld), ('Vertical (solved)', U_est), ('East–west (solved)', E_est))):
    im = ax.imshow(f, cmap=DIV, norm=norm, extent=[0, ext, 0, ext])
    ax.set_title(t, fontsize=19, loc='left', fontweight='bold', color=INK)
    ax.set_xticks([0, 10, 20]); ax.set_yticks([0, 10, 20]); ax.tick_params(labelsize=14)
tag(axs[0])
cb = fig.colorbar(im, ax=axs, fraction=0.015, pad=0.012); cb.set_label('mm/yr', fontsize=16)
fig.text(0.46, 0.03, 'Two looks, two unknowns. East–west: red = moving east, blue = west (towards the bowl centre).', ha='center', fontsize=16, color=SOFT)
fig.subplots_adjust(left=0.03, right=0.91, top=0.9, bottom=0.14, wspace=0.12)
fig.savefig('figs/decomp.png', facecolor='white'); plt.close(fig)

# ---------- aquifer mechanism: head and compaction, elastic and inelastic ----------
t = np.arange(0, 12, 1 / 30.0)                                     # years, ~12-day samples
head = -5 - 2.2 * t + 3.0 * np.sin(2 * np.pi * (t - 0.3))          # m, seasonal swing plus decline
head = np.where(t > 8, head + 2.2 * (t - 8) * 1.6, head)           # pumping cut after year 8: recovery
Ske, Skv = 0.006, 0.03                                             # m of compaction per m of head change (illustrative)
pre = np.minimum.accumulate(np.r_[-6.0, head])[1:]                 # preconsolidation head = lowest level so far
pre_prev = np.r_[-6.0, pre[:-1]]
comp = np.zeros_like(t)
for i in range(1, t.size):
    dh = head[i] - head[i - 1]
    if head[i] < pre_prev[i]:                                      # new low: inelastic (permanent) compaction
        comp[i] = comp[i - 1] + Skv * (head[i] - pre_prev[i]) + Ske * (pre_prev[i] - head[i - 1])
    else:
        comp[i] = comp[i - 1] + Ske * dh
fig, (a1, a2) = plt.subplots(2, 1, figsize=(11.4, 6.6), dpi=DPI, sharex=True, gridspec_kw={'hspace': 0.1})
a1.plot(t, head, color=BLUE, lw=2.5, label='Groundwater level')
a1.plot(t, pre, color=SOFT, lw=1.6, ls='--', label='Lowest level so far')
a1.set_ylabel('Water level (m)', fontsize=16); a1.legend(loc='lower left', frameon=False, fontsize=15); a1.grid(axis='y', color=RULE)
a2.plot(t, comp * 100, color=INK, lw=2.5)
a2.set_ylabel('Ground level (cm)', fontsize=16); a2.set_xlabel('Years'); a2.grid(axis='y', color=RULE)
a2.annotate('Below the lowest level:\npermanent sinking', xy=(5, comp[150] * 100), xytext=(0.4, comp[240] * 100 + 6), fontsize=15, color=INK,
            arrowprops=dict(arrowstyle='->', color=INK))
a2.annotate('Pumping cut: water recovers,\nground rises only a little', xy=(10.5, comp[315] * 100), xytext=(6.9, -12), fontsize=15, color=ACC,
            arrowprops=dict(arrowstyle='->', color=ACC))
for a in (a1, a2):
    a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)
tag(a1, x=0.99, y=0.95, ha='right', va='top')
fig.subplots_adjust(left=0.12, right=0.98, top=0.97, bottom=0.11)
fig.savefig('figs/mech.png', facecolor='white'); plt.close(fig)
stats['mech'] = {'total_cm': round(float(comp[int(8 * 30)] * 100), 0), 'rebound_cm': round(float((comp[-1] - comp[int(8 * 30)]) * 100), 1)}

# ---------- time series: groundwater and InSAR at two points ----------
days = np.arange(np.datetime64('2016-01-01'), np.datetime64('2025-01-01'), np.timedelta64(12, 'D'))
ty = (days - days[0]).astype(float) / 365.25
gw = -20 - 1.5 * ty + 2.5 * np.sin(2 * np.pi * (ty - 0.6))
gw = np.where(ty > 5, gw + 1.5 * (ty - 5) * 1.3, gw)                # recharge scheme from 2021
rng = np.random.default_rng(8)
inel = np.cumsum(np.r_[0, np.diff(np.minimum.accumulate(gw))]) * 30
lag = np.zeros_like(inel)
for i in range(1, inel.size):
    lag[i] = lag[i - 1] + (inel[i] - lag[i - 1]) * (1 - np.exp(-12 / 365.25 / 0.8))   # 0.8-year drainage delay
clay = lag + (gw - gw.mean()) * 2.0
clay = clay + rng.normal(0, 2.5, ty.size)
rock = rng.normal(0, 2.5, ty.size)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(11.4, 6.6), dpi=DPI, sharex=True, gridspec_kw={'height_ratios': [1, 1.7], 'hspace': 0.1})
a1.plot(days, gw, color=BLUE, lw=2.2)
a1.set_ylabel('Water level\n(m)', fontsize=16); a1.grid(axis='y', color=RULE)
a1.axvline(np.datetime64('2021-01-01'), color=ACC, lw=1.5, ls=':')
a1.text(np.datetime64('2021-02-15'), a1.get_ylim()[0] + 0.5 if False else -21.5, 'Recharge and pumping limits', fontsize=15, color=ACC)
a2.plot(days, clay, 'o-', ms=4, lw=1.2, color=INK, label='House on thick clay')
a2.plot(days, rock, 'o', ms=4, color='#9CA3AF', label='Building on stiff ground')
a2.axvline(np.datetime64('2021-01-01'), color=ACC, lw=1.5, ls=':')
a2.set_ylabel('Vertical displacement\n(mm)', fontsize=16); a2.grid(axis='y', color=RULE)
a2.legend(loc='lower left', frameon=False, fontsize=15)
for a in (a1, a2):
    a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)
tag(a2, x=0.99, y=0.97, ha='right', va='top')
fig.subplots_adjust(left=0.14, right=0.98, top=0.97, bottom=0.08)
fig.savefig('figs/ts.png', facecolor='white'); plt.close(fig)
i21 = np.argmin(np.abs(ty - 5))
stats['ts'] = {'rate_before_mm_yr': round(float(np.polyfit(ty[:i21], clay[:i21], 1)[0]), 0), 'rate_after_mm_yr': round(float(np.polyfit(ty[i21 + 10:], clay[i21 + 10:], 1)[0]), 0),
               'gw_decline_m_yr': -1.5, 'seasonal_gw_amp_m': 2.5}

# ---------- differential settlement and angular distortion ----------
L = 60.0                                                  # building length, m
vA, vB = -40.0, -12.0                                     # mm/yr at the two ends (from InSAR points)
yrs = np.linspace(0, 15, 300)
beta = (abs(vA - vB) / 1000 * yrs) / L
thr = [(1 / 500, 'Safe limit where no cracking is allowed (1/500)'), (1 / 300, 'First cracking in walls (1/300)'), (1 / 150, 'Structural damage likely (1/150)')]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(16.2, 5.8), dpi=DPI, gridspec_kw={'width_ratios': [1, 1.1], 'wspace': 0.26})
xp = np.linspace(-40, 100, 141)
prof = vA + (vB - vA) * (1 / (1 + np.exp(-(xp - 30) / 25)) - 1 / (1 + np.exp(30 / 25))) / (1 / (1 + np.exp(-(L - 30) / 25)) - 1 / (1 + np.exp(30 / 25)))
pts = np.sort(np.random.default_rng(2).uniform(-38, 98, 22))
pv = np.interp(pts, xp, prof) + np.random.default_rng(3).normal(0, 1.5, pts.size)
a1.axvspan(0, L, color='#E8E1D2')
a1.text(L / 2, -2, f'Building, {L:.0f} m', ha='center', va='top', fontsize=15, color=INK)
a1.plot(xp, prof, color=SOFT, lw=1.5, ls='--')
a1.plot(pts, pv, 'o', color=INK, ms=7, label='InSAR points')
a1.plot([0, L], [vA, vB], 's', color=ACC, ms=11)
a1.text(2, vA - 6, f'{vA:.0f} mm/yr', ha='left', va='top', fontsize=15, color=ACC, fontweight='bold')
a1.text(L + 3, vB + 2, f'{vB:.0f} mm/yr', ha='left', va='bottom', fontsize=15, color=ACC, fontweight='bold')
a1.set_xlabel('Distance along the profile (m)'); a1.set_ylabel('Vertical velocity (mm/yr)'); a1.set_ylim(-55, 5); a1.grid(axis='y', color=RULE)
a1.legend(loc='lower right', frameon=False, fontsize=15)
a2.plot(yrs, beta, color=INK, lw=3)
for (b_, lab), c in zip(((1 / 500, '1/500: no cracking\nallowed'), (1 / 300, '1/300: first\ncracks in walls'), (1 / 150, '1/150: structural\ndamage likely')), ('#E7A57A', ACC, '#7A2A08')):
    a2.axhline(b_, color=c, lw=2, ls='--')
    a2.text(15.4, b_, lab, fontsize=14, color=c, va='center', clip_on=False)
t300 = (1 / 300) * L / (abs(vA - vB) / 1000)
a2.plot([t300], [1 / 300], 'o', color=ACC, ms=11)
a2.annotate(f'Reaches 1/300 after\nabout {t300:.0f} years', xy=(t300, 1 / 300), xytext=(8.3, 0.0009), fontsize=15, color=ACC,
            arrowprops=dict(arrowstyle='->', color=ACC))
a2.set_xlabel('Years from today'); a2.set_ylabel('Angular distortion (Δs / L)'); a2.set_ylim(0, 0.0075); a2.set_xlim(0, 15)
a2.grid(axis='y', color=RULE)
for a in (a1, a2):
    a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)
tag(a1, x=0.02, y=0.97, va='top')
fig.subplots_adjust(left=0.07, right=0.86, top=0.95, bottom=0.14)
fig.savefig('figs/diff.png', facecolor='white'); plt.close(fig)
stats['diff'] = {'L': L, 'vA': vA, 'vB': vB, 'beta_per_yr': round(abs(vA - vB) / 1000 / L, 6), 'years_to_1_300': round(float(t300), 1),
                 'years_to_1_500': round(float((1 / 500) * L / (abs(vA - vB) / 1000)), 1), 'years_to_1_150': round(float((1 / 150) * L / (abs(vA - vB) / 1000)), 1)}

# ---------- banner: wrapped one-year interferogram of several bowls ----------
bx = np.linspace(0, 60, 1920); by = np.linspace(8.66, 0, 277)
BX, BY = np.meshgrid(bx, by)
bz, be, bn = bowls(BX, BY, [(9, 4.5, 2.6, 160), (24, 3.5, 1.6, 90), (37, 5.0, 3.0, 200), (51, 4.0, 1.8, 120)])
lb = be * sa[0] + bn * sa[1] + bz * sa[2]                        # mm per year, LOS
ph = -4 * np.pi * lb / (LAM * 10)
ph = ph + gaussian_filter(np.random.default_rng(1).normal(0, 1, ph.shape), 30) * 1.5 + np.random.default_rng(2).normal(0, 0.35, ph.shape)
fig = plt.figure(figsize=(19.2, 2.77), dpi=150)
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(np.angle(np.exp(1j * ph)), cmap=PHASE, vmin=-np.pi, vmax=np.pi, aspect='auto', extent=[0, 60, 0, 8.66], interpolation='nearest')
ax.set_xlim(0, 60); ax.set_ylim(0, 8.66); ax.axis('off')
ax.text(59.6, 0.25, 'Simulated data', fontsize=11, color='white', ha='right', va='bottom', bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))
fig.savefig('figs/banner.png', facecolor='white'); plt.close(fig)

json.dump(stats, open('figs/stats.json', 'w'), indent=1)
print(json.dumps(stats, indent=1))
