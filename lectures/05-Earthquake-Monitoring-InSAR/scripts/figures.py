"""Figures for the earthquake-monitoring lecture. Coseismic fields from the Okada (1985) model; all data are simulated and labelled."""
import numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, hsv_to_rgb
from scipy.ndimage import gaussian_filter, binary_fill_holes
from scipy.optimize import least_squares
from okada import fault_enu
from geo import los

os.makedirs('figs', exist_ok=True)
INK = '#13233A'; SOFT = '#4A5563'; RULE = '#E2DFD7'; ACC = '#C2410C'; BLUE = '#2F6DB5'; NODATA = '#D9D6CE'
plt.rcParams.update({'font.family': ['Helvetica', 'DejaVu Sans'], 'font.size': 18, 'axes.edgecolor': SOFT, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': SOFT, 'ytick.color': SOFT})
DPI = 200
LAM = 5.5466                     # Sentinel-1 wavelength, cm
hh = np.linspace(0, 1, 256)
PHASE = LinearSegmentedColormap.from_list('phase', hsv_to_rgb(np.stack([hh, 0.72 * np.ones(256), 0.95 * np.ones(256)], 1)))
DIV = LinearSegmentedColormap.from_list('div', ['#123B6D', '#2F6DB5', '#8FB3DD', '#ECE9E2', '#E7A57A', '#C2410C', '#7A2A08'])
PHASE.set_bad(NODATA); DIV.set_bad(NODATA)
stats = {}


def tag(ax, text='Simulated data', x=0.02, y=0.02, ha='left', va='bottom', fs=14):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=fs, color='white', ha=ha, va=va,
            bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))


def los_field(ue, un, uu, geom='asc'):
    s = los(geom)
    return ue * s[0] + un * s[1] + uu * s[2]          # m, positive towards the satellite


def wrap_cm(d_m, pix_km, noise=0.0, seed=0):
    """Wrapped phase of LOS displacement; masks pixels where fringes are too dense to resolve (decorrelation)."""
    ph = -4 * np.pi * d_m * 100 / LAM
    gy, gx = np.gradient(ph)
    dense = np.hypot(gx, gy) > 1.6
    dense = binary_fill_holes(gaussian_filter(dense.astype(float), 1.5) > 0.2)
    if noise:
        ph = ph + np.random.default_rng(seed).normal(0, noise, ph.shape)
    w = np.angle(np.exp(1j * ph))
    return np.ma.masked_array(w, dense)


def Mw(M0):
    return 2 / 3 * (np.log10(M0) - 9.1)


MU = 3e10
FAULTS = {  # name: (strike, dip, rake, slip m, top km, bottom km, length km)
    'ss': (90, 89.99, 180, 2.0, 0.0, 15.0, 50.0),
    'th': (0, 30, 90, 1.5, 2.0, 15.0, 40.0),
    'no': (0, 50, -90, 2.0, 1.0, 15.0, 40.0)}
for k, (st, dp, rk, sl, tp, bt, ln) in FAULTS.items():
    W = (bt - tp) / np.sin(np.radians(dp))
    stats[f'Mw_{k}'] = round(float(Mw(MU * ln * 1e3 * W * 1e3 * sl)), 2)

# grid, 100 km x 100 km, offset by half a pixel so no point sits on a vertical fault trace
px = 0.25
g = np.arange(-50 + px / 2, 50, px)
E, N = np.meshgrid(g, g[::-1])


def trace(ax, st, dp, tp, bt, ln, xc=0, yc=0):
    s = np.radians(st)
    us, vs = np.sin(s), np.cos(s)
    x1, y1, x2, y2 = xc - us * ln / 2, yc - vs * ln / 2, xc + us * ln / 2, yc + vs * ln / 2
    ax.plot([x1, x2], [y1, y2], color=INK, lw=3)
    if dp < 80:   # surface projection of the dipping plane
        off = (bt - tp) / np.tan(np.radians(dp))
        nx, ny = np.cos(s), -np.sin(s)        # right of strike = dip direction
        ax.plot([x1, x2, x2 + nx * off, x1 + nx * off, x1], [y1, y2, y2 + ny * off, y1 + ny * off, y1], color=INK, lw=1.6, ls='--')


# ---------- 1. three fault types, wrapped ascending interferograms ----------
fig, axs = plt.subplots(1, 3, figsize=(16.6, 6.4), dpi=DPI)
TITLES = {'ss': 'Strike-slip (right-lateral)', 'th': 'Thrust (reverse), dips east', 'no': 'Normal, dips east'}
fields = {}
for ax, k in zip(axs, ('ss', 'th', 'no')):
    st, dp, rk, sl, tp, bt, ln = FAULTS[k]
    ue, un, uu = fault_enu(E, N, 0, 0, st, dp, rk, sl, tp, bt, ln)
    fields[k] = (ue, un, uu)
    d = los_field(ue, un, uu, 'asc')
    stats[f'los_{k}_minmax_cm'] = [round(float(np.nanmin(d)) * 100, 1), round(float(np.nanmax(d)) * 100, 1)]
    stats[f'uplift_{k}_minmax_cm'] = [round(float(np.nanmin(uu)) * 100, 1), round(float(np.nanmax(uu)) * 100, 1)]
    ax.imshow(wrap_cm(d, px, 0.35, 1), cmap=PHASE, vmin=-np.pi, vmax=np.pi, extent=[-50, 50, -50, 50], interpolation='nearest')
    trace(ax, st, dp, tp, bt, ln)
    ax.set_title(TITLES[k], fontsize=20, loc='left', color=INK, fontweight='bold')
    ax.set_xlabel('East (km)'); ax.set_xticks([-40, -20, 0, 20, 40]); ax.set_yticks([-40, -20, 0, 20, 40])
    tag(ax, f'Simulated, Mw {stats["Mw_" + k]:.1f}')
axs[0].set_ylabel('North (km)')
fig.text(0.5, 0.015, 'Sentinel-1 ascending pass. One colour cycle = 2.8 cm of motion along the line of sight. Grey: fringes too dense to resolve.',
         ha='center', fontsize=16, color=SOFT)
fig.subplots_adjust(left=0.05, right=0.99, top=0.92, bottom=0.17, wspace=0.16)
fig.savefig('figs/types.png', facecolor='white'); plt.close(fig)

# ---------- 2. components of the strike-slip field, and why direction matters ----------
ue, un, uu = fields['ss']
st, dp, rk, sl, tp, bt, ln = FAULTS['ss']
ue2, un2, uu2 = fault_enu(E, N, 0, 0, 0, dp, rk, sl, tp, bt, ln)      # same fault striking north-south
panels = [('East', ue), ('North', un), ('Up', uu),
          ('LOS, ascending', los_field(ue, un, uu, 'asc')), ('LOS, descending', los_field(ue, un, uu, 'desc')),
          ('Same fault striking N–S:\nLOS, ascending', los_field(ue2, un2, uu2, 'asc'))]
stats['ns_vs_ew_asc_max_cm'] = [round(float(np.nanmax(np.abs(los_field(ue2, un2, uu2, 'asc')))) * 100, 0), round(float(np.nanmax(np.abs(los_field(ue, un, uu, 'asc')))) * 100, 0)]
fig, axs = plt.subplots(2, 3, figsize=(15.0, 9.4), dpi=DPI)
norm = TwoSlopeNorm(vmin=-100, vcenter=0, vmax=100)
for ax, (t, f) in zip(axs.flat, panels):
    im = ax.imshow(f * 100, cmap=DIV, norm=norm, extent=[-50, 50, -50, 50])
    if t.startswith('Same'):
        trace(ax, 0, dp, tp, bt, ln)
    else:
        trace(ax, st, dp, tp, bt, ln)
    ax.set_title(t, fontsize=19, loc='left', fontweight='bold', color=INK, linespacing=1.1)
    ax.set_xticks([-40, 0, 40]); ax.set_yticks([-40, 0, 40]); ax.tick_params(labelsize=15)
tag(axs[0, 0])
cb = fig.colorbar(im, ax=axs, fraction=0.025, pad=0.02)
cb.set_label('Displacement (cm); LOS: positive = towards satellite', fontsize=17)
fig.subplots_adjust(left=0.04, right=0.86, top=0.93, bottom=0.04, wspace=0.18, hspace=0.32)
fig.savefig('figs/comps.png', facecolor='white'); plt.close(fig)

# ---------- 3. inversion: noisy thrust data, best-fit model, residual ----------
st, dp, rk, sl, tp, bt, ln = FAULTS['th']
ue, un, uu = fields['th']
d_true = los_field(ue, un, uu, 'asc')
rng = np.random.default_rng(7)
atmo = gaussian_filter(rng.normal(0, 1, E.shape), 25)
atmo = atmo / atmo.std() * 0.012                       # 1.2 cm correlated atmosphere
d_obs = d_true + atmo + rng.normal(0, 0.004, E.shape)
ph = -4 * np.pi * d_true * 100 / LAM
gy, gx = np.gradient(ph)
mask = binary_fill_holes(gaussian_filter((np.hypot(gx, gy) > 1.6).astype(float), 1.5) > 0.2)
d_obs = np.ma.masked_array(d_obs, mask)
sub = (slice(None, None, 8), slice(None, None, 8))
Es, Ns, ds, ms = E[sub], N[sub], d_obs.data[sub], mask[sub]
Es, Ns, ds = Es[~ms], Ns[~ms], ds[~ms]


def model(p, Ex, Nx):
    slip, dip, top, bot, xc = p
    a, b, c = fault_enu(Ex, Nx, xc, 0, st, dip, rk, slip, top, bot, ln)
    return los_field(a, b, c, 'asc')


res = least_squares(lambda p: model(p, Es, Ns) - ds, x0=[1.0, 40.0, 5.0, 20.0, 5.0],
                    bounds=([0.1, 10, 0.0, 6.0, -20], [5, 80, 10.0, 30.0, 20]))
pf = res.x
d_mod = model(pf, E, N)
resid = np.ma.masked_array(d_obs.data - d_mod, mask)
W_true = (bt - tp) / np.sin(np.radians(dp)); W_fit = (pf[3] - pf[2]) / np.sin(np.radians(pf[1]))
stats['inv'] = {'true': {'slip': sl, 'dip': dp, 'top': tp, 'bottom': bt, 'x': 0.0, 'Mw': stats['Mw_th']},
                'fit': {'slip': round(float(pf[0]), 2), 'dip': round(float(pf[1]), 1), 'top': round(float(pf[2]), 1), 'bottom': round(float(pf[3]), 1),
                        'x': round(float(pf[4]), 2), 'Mw': round(float(Mw(MU * ln * 1e3 * W_fit * 1e3 * pf[0])), 2)},
                'rms_resid_cm': round(float(resid.std()) * 100, 2)}
fig, axs = plt.subplots(1, 3, figsize=(16.6, 6.2), dpi=DPI)
norm = TwoSlopeNorm(vmin=-30, vcenter=0, vmax=30)
for ax, (t, f) in zip(axs, (('Observed (with noise)', d_obs), ('Best-fit fault model', np.ma.masked_array(d_mod, mask)), ('Residual = observed − model', resid))):
    im = ax.imshow(f * 100, cmap=DIV, norm=norm, extent=[-50, 50, -50, 50])
    trace(ax, st, pf[1] if 'model' in t else dp, pf[2] if 'model' in t else tp, pf[3] if 'model' in t else bt, ln, pf[4] if 'model' in t else 0)
    ax.set_title(t, fontsize=20, loc='left', fontweight='bold', color=INK)
    ax.set_xticks([-40, 0, 40]); ax.set_yticks([-40, 0, 40])
tag(axs[0])
cb = fig.colorbar(im, ax=axs, fraction=0.02, pad=0.015)
cb.set_label('LOS displacement (cm)\npositive = towards satellite', fontsize=16)
fig.subplots_adjust(left=0.04, right=0.88, top=0.9, bottom=0.08, wspace=0.14)
fig.savefig('figs/invert.png', facecolor='white'); plt.close(fig)

# ---------- 4. interseismic: arctan profiles and locking depth ----------
s_rate = 30.0
x = np.linspace(-100, 100, 401)
rng = np.random.default_rng(12)
xo = np.sort(rng.uniform(-95, 95, 160))
D_true = 15.0
vo = s_rate / np.pi * np.arctan(xo / D_true) + gaussian_filter(rng.normal(0, 1, xo.size), 3) * 2.5 + rng.normal(0, 1.2, xo.size)
fit = least_squares(lambda p: p[0] / np.pi * np.arctan(xo / p[1]) - vo, x0=[20, 5], bounds=([1, 0.5], [80, 60]))
stats['inter'] = {'s_true': s_rate, 'D_true': D_true, 's_fit': round(float(fit.x[0]), 1), 'D_fit': round(float(fit.x[1]), 1)}
fig, ax = plt.subplots(figsize=(11.4, 6.4), dpi=DPI)
for D, c in ((5, '#E7A57A'), (25, '#8FB3DD')):
    ax.plot(x, s_rate / np.pi * np.arctan(x / D), color=c, lw=3, label=f'Locked to {D} km')
ax.plot(xo, vo, 'o', ms=5, color=SOFT, alpha=0.75, label='Simulated InSAR velocities')
ax.plot(x, fit.x[0] / np.pi * np.arctan(x / fit.x[1]), color=INK, lw=3.5, label=f'Best fit: {fit.x[0]:.0f} mm/yr, locked to {fit.x[1]:.0f} km')
ax.axvline(0, color=SOFT, lw=1.2, ls=':')
ax.text(1.5, -17.5, 'Fault', fontsize=16, color=SOFT)
ax.set_xlabel('Distance from the fault (km)'); ax.set_ylabel('Fault-parallel velocity (mm/yr)')
ax.set_ylim(-19, 19); ax.grid(axis='y', color=RULE)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.legend(loc='upper left', frameon=False, fontsize=15)
tag(ax, x=0.99, y=0.03, ha='right')
fig.subplots_adjust(left=0.1, right=0.98, top=0.97, bottom=0.13)
fig.savefig('figs/inter.png', facecolor='white'); plt.close(fig)

# ---------- 5. postseismic: step plus afterslip ----------
t = np.arange(-360, 721, 12.0)            # days, Sentinel-1 every 12 days
co, A, tau = -95.0, -15.0, 25.0
u = np.where(t < 0, 0.012 * t, co + A * np.log1p(np.clip(t, 0, None) / tau) + 0.012 * t)
u_obs = u + np.random.default_rng(3).normal(0, 3.0, t.size)
fig, ax = plt.subplots(figsize=(11.4, 6.4), dpi=DPI)
ax.plot(t, u_obs, 'o', ms=5, color=INK)
tt = np.linspace(-360, 720, 1000)
ax.plot(tt, np.where(tt < 0, 0.012 * tt, co + A * np.log1p(np.clip(tt, 0, None) / tau) + 0.012 * tt), color=ACC, lw=2.5)
ax.axvline(0, color=SOFT, lw=1.5, ls=':')
ax.annotate('Earthquake: sudden jump', xy=(0, -50), xytext=(30, -30), fontsize=17, color=INK, arrowprops=dict(arrowstyle='->', color=INK))
ax.text(-340, 12, 'Before: steady', fontsize=17, color=SOFT)
ax.text(230, -88, 'After: afterslip, fast at first,\nthen slowing down', fontsize=17, color=ACC)
ax.set_xlabel('Days from the earthquake'); ax.set_ylabel('LOS displacement (mm)')
ax.grid(axis='y', color=RULE); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
tag(ax, x=0.99, y=0.97, ha='right', va='top')
fig.subplots_adjust(left=0.12, right=0.98, top=0.97, bottom=0.13)
fig.savefig('figs/post.png', facecolor='white'); plt.close(fig)
stats['post'] = {'co_mm': co, 'after_1yr_mm': round(float(A * np.log1p(365 / tau)), 0)}

# ---------- 6. earthquake cycle schematic ----------
fig, ax = plt.subplots(figsize=(11.4, 6.0), dpi=DPI)
T = 100.0
tt = np.linspace(0, 290, 6000)
y = 0.55 * tt / T
for k in (1, 2):
    after = tt >= k * T
    y = y + np.where(after, 0.35 + 0.10 * (1 - np.exp(-(tt - k * T) / 8.0)), 0.0)
ax.plot(tt, tt / T, color=SOFT, lw=1.6, ls='--', label='Long-term plate motion')
ax.plot(tt, y, color=INK, lw=3, label='Ground near the fault')
ax.text(22, 0.03, 'Interseismic: slow build-up', fontsize=17, color=INK)
ax.annotate('Coseismic: sudden slip', xy=(T, 0.72), xytext=(T + 8, 0.42), fontsize=17, color=ACC, arrowprops=dict(arrowstyle='->', color=ACC, lw=1.4))
ax.annotate('Postseismic: afterslip', xy=(T + 14, 0.99), xytext=(T + 30, 0.75), fontsize=17, color=BLUE, arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.4))
ax.set_xlabel('Time (decades to centuries)'); ax.set_ylabel('Displacement near the fault')
ax.set_xticks([]); ax.set_yticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.set_xlim(0, 290); ax.set_ylim(-0.05, 2.95)
ax.legend(loc='upper left', frameon=False, fontsize=16)
tag(ax, 'Schematic', x=0.99, y=0.03, ha='right')
fig.subplots_adjust(left=0.07, right=0.98, top=0.97, bottom=0.1)
fig.savefig('figs/cycle.png', facecolor='white'); plt.close(fig)

# ---------- 7. damage proxy map from coherence (simulated town) ----------
n = 240
rng = np.random.default_rng(5)
yy, xx = np.mgrid[0:n, 0:n]
built = np.zeros((n, n), bool)
for bx in range(20, n - 20, 22):
    for by in range(20, n - 20, 22):
        if rng.random() < 0.82:
            built[by:by + 16, bx:bx + 16] = True
veg = gaussian_filter(rng.normal(0, 1, (n, n)), 8) > 0.4
coh_pre = np.where(built, 0.82, np.where(veg, 0.25, 0.55)) + rng.normal(0, 0.06, (n, n))
damaged = np.zeros((n, n), bool)
cx, cy = 150, 95
for bx in range(20, n - 20, 22):
    for by in range(20, n - 20, 22):
        r = np.hypot(bx + 8 - cx, by + 8 - cy)
        if rng.random() < np.exp(-(r / 55) ** 2) * 0.9:
            damaged[by:by + 16, bx:bx + 16] = True
damaged &= built
coh_co = coh_pre - np.where(damaged, 0.5, 0.0) + rng.normal(0, 0.06, (n, n)) - 0.03
coh_pre = gaussian_filter(np.clip(coh_pre, 0, 1), 1.2); coh_co = gaussian_filter(np.clip(coh_co, 0, 1), 1.2)
dpm = coh_pre - coh_co
fig, axs = plt.subplots(1, 3, figsize=(16.6, 6.2), dpi=DPI)
axs[0].imshow(coh_pre, cmap='gray', vmin=0, vmax=1); axs[0].set_title('Coherence before\n(two images before)', fontsize=19, loc='left', fontweight='bold')
axs[1].imshow(coh_co, cmap='gray', vmin=0, vmax=1); axs[1].set_title('Coherence across the event\n(one before, one after)', fontsize=19, loc='left', fontweight='bold')
axs[2].imshow(coh_co, cmap='gray', vmin=0, vmax=1.6, alpha=0.9)
show = np.ma.masked_less(dpm, 0.25)
im = axs[2].imshow(show, cmap=LinearSegmentedColormap.from_list('dpm', ['#F4D35E', '#E36414', '#9A031E']), vmin=0.25, vmax=0.6)
axs[2].set_title('Damage proxy map\n(coherence drop)', fontsize=19, loc='left', fontweight='bold')
for ax in axs:
    ax.set_xticks([]); ax.set_yticks([])
tag(axs[0])
cb = fig.colorbar(im, ax=axs[2], fraction=0.046, pad=0.03); cb.set_label('Coherence drop', fontsize=16); cb.set_ticks([0.3, 0.45, 0.6])
fig.subplots_adjust(left=0.01, right=0.95, top=0.86, bottom=0.03, wspace=0.08)
fig.savefig('figs/dpm.png', facecolor='white'); plt.close(fig)
stats['dpm'] = {'damaged_blocks_frac': round(float(damaged.sum() / max(built.sum(), 1)), 2)}

# ---------- banner ----------
bx = np.linspace(-150, 150, 1920); by = np.linspace(22, -22, 277)
BE, BN = np.meshgrid(bx, by + 0.0613)
ue, un, uu = fault_enu(BE, BN, 0, 0, 90, 89.99, 180, 1.2, 0.0, 15.0, 120.0)
w = wrap_cm(los_field(ue, un, uu, 'asc'), 300 / 1920, 0.3, 2)
fig = plt.figure(figsize=(19.2, 2.77), dpi=150)
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(w, cmap=PHASE, vmin=-np.pi, vmax=np.pi, aspect='auto', extent=[-150, 150, -22, 22], interpolation='nearest')
ax.plot([-60, 60], [0, 0], color=INK, lw=2.5)
ax.set_xlim(-150, 150); ax.set_ylim(-22, 22); ax.axis('off')
ax.text(148, -20.5, 'Simulated data', fontsize=11, color='white', ha='right', va='bottom', bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))
fig.savefig('figs/banner.png', facecolor='white'); plt.close(fig)

json.dump(stats, open('figs/stats.json', 'w'), indent=1)
print(json.dumps(stats, indent=1))
