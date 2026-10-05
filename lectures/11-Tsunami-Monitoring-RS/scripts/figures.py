"""Figures for the tsunami lecture. The wave-speed curves and the seafloor uplift (Okada, 1985) are computed; the ocean basin is
simulated, and the tsunami crossing it is computed with the linear long-wave equations; records, scenes and DEMs are simulated
and labelled; two diagrams are schematic."""
import numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Rectangle, FancyArrowPatch
from scipy.ndimage import gaussian_filter, distance_transform_edt
from matplotlib.ticker import FuncFormatter
import okada

os.makedirs('figs', exist_ok=True)
INK = '#13233A'; SOFT = '#4A5563'; RULE = '#E2DFD7'; ACC = '#C2410C'; BLUE = '#2F6DB5'; SAND = '#E9D7A7'; SEA = '#8FB3DD'
LAND = '#D8D2C2'; GREEN = '#6E9A5B'
plt.rcParams.update({'font.family': ['Helvetica', 'DejaVu Sans'], 'font.size': 18, 'axes.edgecolor': SOFT, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': SOFT, 'ytick.color': SOFT})
DPI = 200
plt.rcParams['savefig.dpi'] = DPI
G = 9.81
DIV = LinearSegmentedColormap.from_list('div', ['#123B6D', '#2F6DB5', '#8FB3DD', '#ECE9E2', '#E7A57A', '#C2410C', '#7A2A08'])
SEQ = LinearSegmentedColormap.from_list('seq', ['#FBEBDD', '#F4C9A0', '#E7A57A', '#C2410C', '#7A2A08'])
DMG = LinearSegmentedColormap.from_list('dmg', ['#F4C9A0', '#C2410C', '#7A2A08'])
rng = np.random.default_rng(2004)
out = {}


def tag(ax, text='Simulated data', x=0.02, y=0.02, ha='left', va='bottom', fs=14):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=fs, color='white', ha=ha, va=va,
            bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))


def clean(ax):
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)


def sn(shape, sigma):
    g = gaussian_filter(rng.normal(0, 1, shape), sigma)
    return g / g.std()


def speed(h):
    """Long-wave (shallow-water) speed in m/s for depth h in m."""
    return np.sqrt(G * h)


# ---------- 1. speed and height against depth (computed) ----------
d = np.logspace(0.7, np.log10(6000), 300)
fig, ax = plt.subplots(1, 2, figsize=(14, 5.8), constrained_layout=True)
ax[0].semilogx(d, speed(d) * 3.6, color=INK, lw=3)
for dd, lab, txy, ha in ((4000, 'Deep ocean, 4000 m', (1500, 720), 'right'), (200, 'Shelf edge, 200 m', (330, 90), 'left'), (10, 'Near shore, 10 m', (6, 250), 'left')):
    c = speed(dd) * 3.6
    ax[0].plot(dd, c, 'o', color=ACC, ms=11, zorder=3)
    ax[0].annotate(f'{lab}\n{c:.0f} km/h', (dd, c), txy, fontsize=16, color=INK, ha=ha, va='center',
                   arrowprops=dict(arrowstyle='-', color=SOFT, lw=1.2, shrinkB=8))
ax[0].set_xlabel('Water depth (m)'); ax[0].set_ylabel('Wave speed (km/h)'); ax[0].set_title('Speed = √(g × depth)', loc='left', fontsize=19, color=INK)
ax[0].set_ylim(0, 850); clean(ax[0])
A0 = 0.5
ax[1].semilogx(d, A0 * (4000 / d) ** 0.25, color=ACC, lw=3)
for dd in (4000, 200, 10):
    a = A0 * (4000 / dd) ** 0.25
    ax[1].plot(dd, a, 'o', color=ACC, ms=11, zorder=3)
    ax[1].annotate(f'{a:.1f} m', (dd, a), (dd * 0.75, a - 0.32), fontsize=16, color=INK)
ax[1].invert_xaxis(); ax[1].set_xlabel('Water depth (m), towards the coast →'); ax[1].set_ylabel('Wave height (m)')
ax[1].set_title("Height grows as depth falls (Green's law)", loc='left', fontsize=19, color=INK); ax[1].set_ylim(0, 3.2); clean(ax[1])
for a_ in ax:
    a_.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f'{v:,.0f}'))
fig.savefig('figs/speed.png', facecolor='white'); plt.close(fig)
out['speed'] = {'deep_kmh': round(float(speed(4000) * 3.6)), 'shelf_kmh': round(float(speed(200) * 3.6)), 'shore_kmh': round(float(speed(10) * 3.6)),
                'green_10m': round(float(A0 * 400 ** 0.25), 2)}

# ---------- 2. the simulated ocean basin and the earthquake source ----------
DX = 4.0; NX, NY = 400, 250                       # 4 km cells: 1600 km east-west, 1000 km north-south
x = (np.arange(NX) + 0.5) * DX; y = (np.arange(NY) + 0.5) * DX
X, Y = np.meshgrid(x, y)
coast = 150 + 40 * np.sin(Y / 180) + 12 * sn((NY, NX), 12)[:, :1]
dist = X - coast                                  # km from the mainland coast
h = np.where(dist < 60, 10 + 140 * dist / 60, np.where(dist < 180, 150 + 3850 * (dist - 60) / 120, 4000.0))
h = h - 1800 * np.exp(-((X - 780) / 45) ** 2) * (0.7 + 0.3 * np.sin(Y / 140))       # a submarine ridge
arc = 1400 + 50 * np.cos(Y / 300)                                                  # island arc
tr = arc - 60                                                                      # trench
h = np.where(X > tr - 80, np.maximum(h, 0) + 1000 * np.exp(-((X - tr) / 25) ** 2), h)
h = np.where(X > tr, 5000 - 4980 * np.clip((X - tr) / 60, 0, 1), h)
h = gaussian_filter(h, 1.5)
isl = (np.abs(X - arc) < 14) & (np.sin(Y / 55) > -0.35)
h = np.where(isl, -50.0, h)
h = np.where(X > arc + 14, 1500.0, h)
h = np.where(dist < 0, -50.0, h)
wet = h > 5

FAULT = dict(xc=float(tr[NY // 2, 0]), yc=500.0, strike=0.0, dip=12.0, rake=90.0, slip=8.0, top=5.0, bottom=40.0, length=320.0)
ue, un, uz = okada.fault_enu(X, Y, FAULT['xc'], FAULT['yc'], FAULT['strike'], FAULT['dip'], FAULT['rake'], FAULT['slip'],
                             FAULT['top'], FAULT['bottom'], FAULT['length'])
r = np.hypot(X - FAULT['xc'] - 60, (Y - 500) / 1.4)
eta0 = np.where(wet, gaussian_filter(uz, 1.5) * np.exp(-np.clip(r - 150, 0, None) ** 2 / (2 * 60 ** 2)), 0.0)

# ---------- 3. linear long-wave equations on a staggered grid ----------
DXM = DX * 1000
hw = np.where(wet, h, 0.0)
hx = np.zeros((NY, NX + 1)); hx[:, 1:-1] = np.where(wet[:, 1:] & wet[:, :-1], 0.5 * (hw[:, 1:] + hw[:, :-1]), 0)
hy = np.zeros((NY + 1, NX)); hy[1:-1, :] = np.where(wet[1:, :] & wet[:-1, :], 0.5 * (hw[1:, :] + hw[:-1, :]), 0)
u = np.zeros((NY, NX + 1)); v = np.zeros((NY + 1, NX)); eta = eta0.copy()
dt = 0.45 * DXM / speed(hw.max()) / np.sqrt(2)
ns = 25
ramp = lambda k: np.clip((ns - np.arange(k)) / ns, 0, 1) ** 2                       # absorbing sponge at the open edges
damp = 1 - 0.03 * np.maximum.outer(np.maximum(ramp(NY), ramp(NY)[::-1]), ramp(NX)[::-1])
cell = lambda xk, yk: (int(yk / DX), int(xk / DX))
ST = {'Island harbour': cell(float(arc[125, 0]) - 18, 500), 'DART buoy': cell(900, 850), 'Mainland port': cell(float(coast[125, 0]) + 6, 500)}
arr = np.full(h.shape, np.nan); mx = np.zeros(h.shape); snaps = {}; ts = {k: [] for k in ST}; tt = []
T_END = 4.5 * 3600; t = 0.0
while t < T_END:
    u[:, 1:-1] -= G * dt * (eta[:, 1:] - eta[:, :-1]) / DXM * (hx[:, 1:-1] > 0)
    v[1:-1, :] -= G * dt * (eta[1:, :] - eta[:-1, :]) / DXM * (hy[1:-1, :] > 0)
    fx = hx * u; fy = hy * v
    eta -= dt * ((fx[:, 1:] - fx[:, :-1]) + (fy[1:, :] - fy[:-1, :])) / DXM
    eta *= damp; u[:, :-1] *= damp; v[:-1, :] *= damp
    t += dt
    arr[np.isnan(arr) & (np.abs(eta - eta0) > 0.02) & wet] = t
    mx = np.maximum(mx, eta)
    tt.append(t)
    for k, (j, i) in ST.items():
        ts[k].append(eta[j, i])
    for m in (75, 90):
        if m not in snaps and t >= m * 60:
            snaps[m] = eta.copy()
tt = np.array(tt); ts = {k: np.array(vv) for k, vv in ts.items()}
arr_min = {k: float(arr[j, i] / 60) for k, (j, i) in ST.items()}
MW = 2 / 3 * (np.log10(3e10 * FAULT['length'] * 1e3 * (FAULT['bottom'] - FAULT['top']) / np.sin(np.radians(FAULT['dip'])) * 1e3 * FAULT['slip']) - 9.1)
out['sim'] = {'mw': round(float(MW), 1), 'arrival_min': {k: round(vv) for k, vv in arr_min.items()},
              'max_m': {k: round(float(ts[k].max()), 2) for k in ST}, 'uplift_max_m': round(float(uz.max()), 1),
              'subsidence_max_m': round(float(uz.min()), 1), 'dt_s': round(float(dt), 1)}


def hm(m):
    return f'{int(m // 60)} h {int(round(m % 60)):02d} min' if m >= 60 else f'{m:.0f} min'


def land_layer(ax):
    ax.contourf(x, y, h, levels=[h.min() - 1, 5], colors=[LAND], zorder=2)


def fill(a):
    """Fill land (and unreached) cells with the nearest sea value, so a smooth coastline can be drawn on top."""
    idx = distance_transform_edt(~wet | np.isnan(a), return_distances=False, return_indices=True)
    return a[tuple(idx)]


# ---------- 4. travel-time map (computed on simulated bathymetry) ----------
fig, ax = plt.subplots(figsize=(11.5, 7.6), constrained_layout=True)
im = ax.imshow(fill(arr) / 3600, origin='lower', extent=[0, NX * DX, 0, NY * DX], cmap=SEQ, vmin=0, vmax=3)
land_layer(ax)
cs = ax.contour(x, y, np.where(wet, arr / 3600, np.nan), levels=[0.5, 1, 1.5, 2, 2.5], colors=INK, linewidths=1.4, zorder=3)
ax.clabel(cs, fmt=lambda v: f'{v:g} h', fontsize=14, inline_spacing=6)
ax.add_patch(Rectangle((FAULT['xc'], 500 - FAULT['length'] / 2), 165, FAULT['length'], fill=False, ec=INK, lw=2, ls='--', zorder=4))
ax.text(FAULT['xc'] - 12, 500 + FAULT['length'] / 2 + 20, 'Earthquake\nrupture', fontsize=15, color=INK, ha='right')
for k, (j, i) in ST.items():
    ax.plot(x[i], y[j], marker='^' if k == 'DART buoy' else 'o', color='white', mec=INK, mew=2, ms=15, zorder=5)
lab = {'Island harbour': (1320, 330, 'right'), 'DART buoy': (900, 790, 'center'), 'Mainland port': (240, 420, 'left')}
for k, (tx, ty, ha) in lab.items():
    ax.text(tx, ty, f'{k}\n{hm(arr_min[k])}', fontsize=16, color=INK, ha=ha, va='top', fontweight='bold', zorder=6,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=0.85))
ax.text(40, 960, 'Mainland', fontsize=17, color=INK, zorder=6); ax.text(1465, 700, 'Islands', fontsize=17, color=INK, zorder=6, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85))
cb = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02); cb.set_label('Arrival time (hours)'); cb.outline.set_visible(False)
ax.set_xlabel('Distance east (km)'); ax.set_ylabel('Distance north (km)')
tag(ax, 'Simulated basin; travel times computed', x=0.98, y=0.02, ha='right')
fig.savefig('figs/travel.png', facecolor='white'); plt.close(fig)

# ---------- 5. the cover strip: the wave field 75 minutes after the earthquake ----------
j0, j1 = 75, 133
fig = plt.figure(figsize=(19.2, 19.2 * (j1 - j0) / NX)); ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(fill(snaps[75]), origin='lower', cmap=DIV, norm=TwoSlopeNorm(vcenter=0, vmin=-0.5, vmax=0.5),
          extent=[0, NX * DX, 0, NY * DX], aspect='auto', interpolation='bilinear')
land_layer(ax); ax.set_xlim(0, NX * DX); ax.set_ylim(y[j0], y[j1 - 1])
ax.axis('off'); tag(ax, x=0.995, y=0.06, ha='right', fs=13)
fig.savefig('figs/banner.png', dpi=DPI, facecolor='white'); plt.close(fig)

# ---------- 6. satellite altimetry across the wave (simulated) ----------
snap = snaps[90]
p0, p1 = np.array([250.0, 0.0]), np.array([610.0, 1000.0])
L = np.hypot(*(p1 - p0)); s_km = np.arange(0, L, 6.2)                     # one sample every 6.2 km, as a 1 Hz altimeter
px_, py_ = p0[0] + (p1 - p0)[0] * s_km / L, p0[1] + (p1 - p0)[1] * s_km / L
ii, jj = np.clip((px_ / DX).astype(int), 0, NX - 1), np.clip((py_ / DX).astype(int), 0, NY - 1)
model = snap[jj, ii]; meas = model + rng.normal(0, 0.04, model.size)
fig, ax = plt.subplots(1, 2, figsize=(15.5, 6.2), gridspec_kw={'width_ratios': [1.05, 1.3]}, constrained_layout=True)
ax[0].imshow(fill(snap), origin='lower', extent=[0, NX * DX, 0, NY * DX], cmap=DIV, norm=TwoSlopeNorm(vcenter=0, vmin=-0.5, vmax=0.5))
land_layer(ax[0])
ax[0].plot([p0[0], p1[0]], [p0[1], p1[1]], color=INK, lw=3, ls='--', zorder=4)
ax[0].text(1000, 120, 'Dashed: satellite\nground track', fontsize=15, color=INK, ha='center', zorder=5,
           bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=0.85))
ax[0].set_xlabel('Distance east (km)'); ax[0].set_ylabel('Distance north (km)')
ax[0].set_title('Sea surface 90 minutes after the earthquake', loc='left', fontsize=18, color=INK)
k = int(np.argmax(model))
ax[1].axhline(0, color=RULE, lw=2)
ax[1].plot(s_km, meas * 100, 'o', color=BLUE, ms=5, alpha=0.75, label='Altimeter measurements')
ax[1].plot(s_km, model * 100, color=ACC, lw=3, label='Tsunami (model)')
ax[1].annotate(f'Crest: about {model[k] * 100:.0f} cm', (s_km[k], model[k] * 100), (s_km[k] + 120, model[k] * 100 + 6), fontsize=16, color=INK,
               arrowprops=dict(arrowstyle='-', color=SOFT))
ax[1].set_xlabel('Distance along the track (km)'); ax[1].set_ylabel('Sea-surface height (cm)')
ax[1].set_title('One pass: the wave in a single profile', loc='left', fontsize=18, color=INK)
ax[1].legend(frameon=False, fontsize=15, loc='lower left'); clean(ax[1]); ax[1].set_ylim(-45, 85)
tag(ax[0]); tag(ax[1], x=0.02, y=0.96, va='top')
fig.savefig('figs/altimetry.png', facecolor='white'); plt.close(fig)
out['altimetry'] = {'crest_cm': round(float(model[k] * 100))}

# ---------- 7. a DART bottom-pressure record (simulated) ----------
th = np.arange(-6, 6, 15 / 3600)                                           # hours from the earthquake, 15 s samples
tide = 0.55 * np.cos(2 * np.pi * (th + 2.1) / 12.42) + 0.18 * np.cos(2 * np.pi * (th + 0.7) / 12.0)
tsu = np.interp(th * 3600, tt, ts['DART buoy'], left=0.0, right=0.0) * np.clip((4.5 - th) / 0.5, 0, 1)
seis = np.where((th > 0) & (th < 0.25), rng.normal(0, 1, th.size) * 0.06 * np.exp(-np.clip(th, 0, None) / 0.06), 0)
raw = tide + tsu + seis + rng.normal(0, 0.003, th.size)
pre = th < 0
Amat = lambda tv: np.column_stack([np.ones_like(tv)] + [f(2 * np.pi * tv / p) for p in (12.42, 12.0, 25.82, 23.93) for f in (np.cos, np.sin)])
coef = np.linalg.lstsq(Amat(th[pre]), raw[pre], rcond=None)[0]
resid = raw - Amat(th) @ coef
fig, ax = plt.subplots(2, 1, figsize=(11.5, 7.6), constrained_layout=True, gridspec_kw={'height_ratios': [1, 1.25]})
ax[0].plot(th, raw, color=INK, lw=1.6); ax[0].axvline(0, color=ACC, lw=2, ls='--')
ax[0].text(0.15, 0.75, 'Earthquake', color=ACC, fontsize=15)
ax[0].set_ylabel('Sea level (m)'); ax[0].set_title('1. What the sensor records: mostly the tide', loc='left', fontsize=18, color=INK)
ax[0].set_xlim(-6, 6); ax[0].set_ylim(-1.0, 1.0); clean(ax[0])
w = (th > -0.5) & (th < 3)
ax[1].plot(th[w] * 60, resid[w] * 100, color=INK, lw=1.6); ax[1].axhline(0, color=RULE, lw=2, zorder=0); ax[1].axvline(0, color=ACC, lw=2, ls='--')
kk = np.argmax(np.where(w, resid, -9))
ax[1].annotate('Seismic waves shake the sensor', (3, 4), (-25, 24), fontsize=15, color=SOFT,
               arrowprops=dict(arrowstyle='-', color=SOFT))
ax[1].annotate(f'Tsunami: +{resid[kk] * 100:.0f} cm,\n{th[kk] * 60:.0f} min after the earthquake', (th[kk] * 60, resid[kk] * 100), (th[kk] * 60 + 22, resid[kk] * 100 - 6),
               fontsize=15, color=INK, arrowprops=dict(arrowstyle='-', color=SOFT))
ax[1].set_xlabel('Minutes after the earthquake'); ax[1].set_ylabel('Tide removed (cm)')
ax[1].set_title('2. After removing the predicted tide', loc='left', fontsize=18, color=INK); clean(ax[1])
ax[1].set_xlim(-30, 180); ax[1].set_ylim(-35, 35)
tag(ax[0], x=0.98, y=0.04, ha='right'); tag(ax[1], x=0.98, y=0.04, ha='right')
fig.savefig('figs/dart.png', facecolor='white'); plt.close(fig)
out['dart'] = {'peak_cm': round(float(resid[kk] * 100)), 'peak_min': round(float(th[kk] * 60)), 'tide_range_m': round(float(raw[pre].max() - raw[pre].min()), 1)}

# ---------- 8. the seafloor moves: Okada profile across the fault (computed) ----------
xp = np.linspace(FAULT['xc'] - 150, FAULT['xc'] + 300, 900)
_, _, uzp = okada.fault_enu(xp, np.full_like(xp, 500.0), FAULT['xc'], FAULT['yc'], FAULT['strike'], FAULT['dip'], FAULT['rake'],
                            FAULT['slip'], FAULT['top'], FAULT['bottom'], FAULT['length'])
xr = xp - FAULT['xc']
fig, ax = plt.subplots(2, 1, figsize=(11.5, 7.6), sharex=True, constrained_layout=True, gridspec_kw={'height_ratios': [1.1, 1]})
ax[0].axhline(0, color=RULE, lw=2)
ax[0].fill_between(xr, 0, uzp, where=uzp > 0, color=ACC, alpha=0.85, lw=0)
ax[0].fill_between(xr, 0, uzp, where=uzp < 0, color=BLUE, alpha=0.85, lw=0)
iu, idn = np.argmax(uzp), np.argmin(uzp)
ax[0].annotate(f'Seafloor uplift: +{uzp[iu]:.1f} m\nthe sea surface rises with it', (xr[iu], uzp[iu]), (xr[iu] - 140, uzp[iu] - 1.0), fontsize=15, color=INK,
               arrowprops=dict(arrowstyle='-', color=SOFT))
ax[0].annotate(f'Subsidence: {uzp[idn]:.1f} m'.replace('-', '−') + '\nland further back sinks', (xr[idn], uzp[idn]), (xr[idn] + 30, uzp[idn] + 2.2), fontsize=15, color=INK,
               arrowprops=dict(arrowstyle='-', color=SOFT))
ax[0].set_ylabel('Vertical movement (m)'); ax[0].set_ylim(-3.5, 6); clean(ax[0])
ax[0].yaxis.set_major_formatter(FuncFormatter(lambda v, p: f'{v:g}'.replace('-', '−')))
ax[0].set_title(f"Computed (Okada, 1985): thrust fault {FAULT['length']:.0f} km long, {FAULT['slip']:.0f} m of slip, about Mw {MW:.1f}", loc='left', fontsize=17, color=INK)
sea = np.interp(xr, [-150, 0, 60, 70, 300], [-4.5, -5.0, -0.2, 0.5, 0.6])
ax[1].fill_between(xr, sea, 0, where=sea < 0, color=SEA, lw=0)
ax[1].fill_between(xr, -45, sea, color=LAND, lw=0)
ax[1].plot(xr, sea, color=SOFT, lw=1.5)
xf = np.array([0, (FAULT['bottom'] - FAULT['top']) / np.tan(np.radians(FAULT['dip']))])
ax[1].plot(xf, [-FAULT['top'], -FAULT['bottom']], color=ACC, lw=5, solid_capstyle='round')
ax[1].text(xf[1] * 0.55, -FAULT['bottom'] * 0.62 - 6, 'Fault: the plates slip here', color=ACC, fontsize=15, rotation=-9)
ax[1].text(-140, -2.4, 'Ocean', fontsize=16, color=INK); ax[1].text(-6, -9.5, 'Trench', fontsize=15, color=INK, ha='right')
ax[1].text(78, 2.2, 'Islands', fontsize=15, color=INK)
ax[1].set_ylim(-45, 6); ax[1].set_ylabel('Depth (km)'); ax[1].set_xlabel('Distance from the trench (km)'); clean(ax[1])
ax[1].text(0.99, 0.05, 'Vertical scale exaggerated', transform=ax[1].transAxes, ha='right', fontsize=14, color=SOFT)
fig.savefig('figs/source.png', facecolor='white'); plt.close(fig)

# ---------- 9. tsunami in the ionosphere (schematic and simulated) ----------
fig, ax = plt.subplots(1, 2, figsize=(15.5, 6.2), gridspec_kw={'width_ratios': [1, 1.25]}, constrained_layout=True)
a = ax[0]; a.set_xlim(0, 10); a.set_ylim(0, 10); a.axis('off')
a.add_patch(Rectangle((0, 6.0), 10, 1.6, color='#E5E8F0', lw=0)); a.text(5.2, 7.0, 'Ionosphere, about 300 km up', fontsize=15, color=INK)
xs = np.linspace(0, 10, 300)
a.fill_between(xs, 0, 1.0 + 0.35 * np.exp(-((xs - 3) / 0.5) ** 2), color=SEA, lw=0)
a.add_patch(Rectangle((8.6, 0), 1.4, 1.35, color=LAND, lw=0)); a.text(9.3, 0.5, 'Coast', fontsize=14, color=INK, ha='center')
a.text(3, 0.45, 'Tsunami', fontsize=14, color=INK, ha='center')
for k in range(4):
    yy = np.linspace(1.5, 6.0, 50); xx = 3 + 0.12 * k + (yy - 1.5) * (0.25 + 0.08 * k)
    a.plot(xx, yy, color=ACC, lw=2, alpha=0.9 - 0.15 * k)
a.text(0.2, 3.9, 'Air pushed up by the\nwave grows as it rises', fontsize=14, color=ACC)
a.plot(9.3, 1.35, marker='^', ms=16, color=INK); a.plot(1.2, 9.4, marker='s', ms=14, color=INK)
a.text(1.6, 9.3, 'GNSS satellite', fontsize=14, color=INK, va='center')
a.plot([9.3, 1.2], [1.35, 9.4], color=INK, lw=1.5, ls='--')
pp = 9.3 + (6.8 - 1.35) / (9.4 - 1.35) * (1.2 - 9.3)
a.plot(pp, 6.8, 'o', ms=14, mfc='white', mec=INK, mew=2, zorder=5); a.text(pp - 0.35, 6.25, 'Pierce point', fontsize=14, color=INK, ha='right')
a.set_title('Schematic, not to scale', loc='left', fontsize=17, color=SOFT)
tmin = np.arange(0, 150, 0.5)
LAG = 20.0; V = speed(4000) * 3.6 / 60                                     # km per minute
for dkm, col, off in ((250, '#8FB3DD', 0.0), (500, BLUE, -1.2), (750, INK, -2.4)):
    ta = dkm / V + LAG
    sig = 0.35 * np.exp(-((tmin - ta - 6) / 7) ** 2) * np.sin(2 * np.pi * (tmin - ta) / 12) * (tmin > ta - 6)
    ax[1].plot(tmin, off + sig + 0.03 * sn(tmin.shape, 2), color=col, lw=2.2)
    ax[1].text(147, off + 0.12, f'{dkm} km from source', fontsize=14, color=INK, ha='right')
land_t = 1200 / V
ax[1].axvline(land_t, color=ACC, lw=2.5, ls='--'); ax[1].text(land_t - 2, 0.55, f'Wave reaches a coast\n1200 km away: {land_t:.0f} min', fontsize=14, color=ACC, ha='right')
ax[1].set_yticks([]); ax[1].set_xlabel('Minutes after the earthquake'); ax[1].set_ylabel('Change in electron content (offset)')
ax[1].set_title('Disturbances move out with the tsunami', loc='left', fontsize=17, color=INK); ax[1].set_ylim(-3, 1.1); ax[1].set_xlim(0, 150)
for sp in ('top', 'right', 'left'):
    ax[1].spines[sp].set_visible(False)
tag(ax[1], x=0.02, y=0.02)
fig.savefig('figs/tec.png', facecolor='white'); plt.close(fig)

# ---------- 10. run-up, flow depth and inundation (schematic) ----------
xs = np.linspace(-1.2, 3.2, 500)
ground = np.where(xs < 0, 4.0 * xs, 1.8 * xs)
surf = 6.0 - 1.2 * xs
xl = 6.0 / 3.0; zl = 1.8 * xl
fig, ax = plt.subplots(figsize=(15, 5.8), constrained_layout=True)
ax.fill_between(xs, -5, ground, color=LAND, lw=0)
ax.fill_between(xs, ground, np.where(xs < 0, 0, np.nan), color=SEA, lw=0, alpha=0.6)
m = (xs >= -1.2) & (xs <= xl)
ax.fill_between(xs[m], np.maximum(ground[m], np.where(xs[m] < 0, 0, ground[m])), surf[m], color=BLUE, alpha=0.55, lw=0)
ax.plot(xs[m], surf[m], color=BLUE, lw=3)
ax.axhline(0, color=SOFT, lw=1.5, ls=':'); ax.text(-1.15, 0.25, 'Mean sea level', fontsize=15, color=SOFT)
ax.plot(xs, ground, color=INK, lw=2)


def arrow(p, q, text, tx, ty, col=INK, ha='left'):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='<->', mutation_scale=22, color=col, lw=2.2))
    ax.text(tx, ty, text, fontsize=16, color=col, ha=ha, fontweight='bold')


arrow((0.02, 0), (0.02, 6.0), 'Tsunami height\nat the shore', 0.1, 4.4)
arrow((0.9, 1.8 * 0.9), (0.9, 6.0 - 1.2 * 0.9), 'Flow depth', 0.98, 3.0)
arrow((0, -0.9), (xl, -0.9), 'Inundation distance', xl / 2, -1.9, ha='center')
arrow((xl + 0.25, 0), (xl + 0.25, zl), 'Run-up height', xl + 0.33, 1.6, ACC)
ax.plot([xl, xl + 0.32], [zl, zl], color=ACC, lw=1.5, ls=':'); ax.plot(xl, zl, 'o', color=ACC, ms=10)
ax.text(xl + 0.05, zl + 0.5, 'Inundation limit', fontsize=15, color=ACC)
ax.text(-1.0, 4.7, 'Tsunami', fontsize=17, color=BLUE, fontweight='bold')
ax.set_xlim(-1.2, 3.2); ax.set_ylim(-3, 7.6); ax.axis('off')
tag(ax, 'Schematic: vertical scale greatly exaggerated', x=0.99, y=0.02, ha='right')
fig.savefig('figs/runup.png', facecolor='white'); plt.close(fig)

# ---------- 11. damage from radar coherence (simulated) ----------
N = 360
yy_, xx_ = np.mgrid[0:N, 0:N]
shore = 40 + 10 * np.sin(yy_ / 45) + 4 * sn((N, N), 20)
sea_m = xx_ < shore
lim = shore + 150 + 35 * np.sin(yy_ / 60 + 1) + 12 * sn((N, N), 25)       # true inundation limit, about 1.5 km at 10 m pixels
inund = (~sea_m) & (xx_ < lim)
blk = ((xx_ % 22) < 16) & ((yy_ % 22) < 16) & (xx_ > shore + 25) & (xx_ < 300) & (yy_ > 30) & (yy_ < 330)
blk &= gaussian_filter(rng.random((N, N)), 2) > 0.38
veg = (~sea_m) & (~blk) & (sn((N, N), 10) > 0.2)
base = np.where(sea_m, 0.05, np.where(blk, 0.85, np.where(veg, 0.25, 0.45)))
noise = lambda: 0.07 * sn((N, N), 1.2)
destroyed = blk & inund & (gaussian_filter(rng.random((N, N)), 3) > 0.4)
c_pre = np.clip(base + noise(), 0, 1)
c_co = np.clip(np.where(destroyed, 0.2, np.where(inund & ~blk & ~sea_m, base * 0.7, base)) + noise(), 0, 1)
dpm = np.where(c_pre > 0.6, np.clip(c_pre - c_co, 0, None), 0)
dpm = gaussian_filter(dpm, 1.0)
fig, ax = plt.subplots(1, 3, figsize=(16.5, 6.1), constrained_layout=True)
for a_, img, ttl in ((ax[0], c_pre, '1. Coherence before the event'), (ax[1], c_co, '2. Coherence across the event')):
    a_.imshow(img, cmap='gray', vmin=0, vmax=1, origin='upper'); a_.set_title(ttl, loc='left', fontsize=17, color=INK)
ax[2].imshow(c_pre, cmap='gray', vmin=0, vmax=1, alpha=0.45, origin='upper')
dm = np.ma.masked_less(dpm, 0.2)
ax[2].imshow(dm, cmap=DMG, vmin=0.2, vmax=0.7, origin='upper')
ax[2].contour(inund.astype(float), levels=[0.5], colors=BLUE, linewidths=2.2, linestyles='--')
ax[2].set_title('3. Damage proxy: coherence lost', loc='left', fontsize=17, color=INK)
ax[2].text(0.98, 0.93, 'Dashed: true\ninundation limit', transform=ax[2].transAxes, ha='right', va='top', fontsize=14, color=BLUE,
           bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.85))
for a_ in ax:
    a_.set_xticks([]); a_.set_yticks([])
    a_.text(0.04, 0.5, 'Sea', transform=a_.transAxes, color='white', fontsize=15, rotation=90, va='center')
    tag(a_, x=0.98, y=0.02, ha='right')
fig.savefig('figs/damage.png', facecolor='white'); plt.close(fig)
hit = (dpm > 0.2)
out['damage'] = {'detected_pct_of_destroyed': round(float((hit & destroyed).sum() / destroyed.sum() * 100)),
                 'false_pct_outside': round(float((hit & ~inund).sum() / max(hit.sum(), 1) * 100))}

# ---------- 12. why the elevation model matters (computed on a simulated plain) ----------
xk = np.linspace(0, 4, 800)
truth = 1.0 + 1.6 * xk + 0.25 * np.sin(xk * 5)
dem = truth + 2.5 + 0.25 * gaussian_filter(rng.normal(0, 1, xk.size), 12) / gaussian_filter(rng.normal(0, 1, xk.size), 12).std()
RUN = 5.0


def limit(z):
    beyond = np.where(z >= RUN)[0]
    return float(xk[beyond[0]]) if beyond.size else float(xk[-1])


L_true, L_dem = limit(truth), limit(dem)
fig, ax = plt.subplots(figsize=(12.5, 6.2), constrained_layout=True)
ax.fill_between(xk, 0, truth, color=LAND, lw=0)
ax.plot(xk, truth, color=INK, lw=2.5, label='Ground (lidar)')
ax.plot(xk, dem, color=ACC, lw=2.5, label='Global DEM: tree and roof tops, +2.5 m bias')
ax.axhline(RUN, color=BLUE, lw=2.5, ls='--'); ax.text(3.97, RUN + 0.25, f'Water level {RUN:.0f} m', color=BLUE, fontsize=16, ha='right')
for Lx, col, txt_, yo in ((L_true, INK, 'Lidar', 0.55), (L_dem, ACC, 'Global DEM', 1.45)):
    ax.plot([Lx, Lx], [0, RUN], color=col, lw=1.5, ls=':')
    ax.annotate('', (0, yo), (Lx, yo), arrowprops=dict(arrowstyle='<->', color=col, lw=2))
    ax.text(Lx + 0.04, yo - 0.1, f'{txt_}: floods to {Lx:.1f} km', color=col, fontsize=16, fontweight='bold', va='center')
ax.set_xlabel('Distance inland (km)'); ax.set_ylabel('Elevation (m)'); ax.set_xlim(0, 4); ax.set_ylim(0, 10)
ax.legend(frameon=False, fontsize=15, loc='upper left'); clean(ax)
tag(ax, 'Simulated coastal plain; flooding by a simple level test', x=0.99, y=0.97, ha='right', va='top')
fig.savefig('figs/dem.png', facecolor='white'); plt.close(fig)
out['dem'] = {'lidar_km': round(L_true, 1), 'dem_km': round(L_dem, 1)}

json.dump(out, open('figs/stats.json', 'w'), indent=1)
print(json.dumps(out))
