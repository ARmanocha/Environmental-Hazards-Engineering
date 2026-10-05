"""Figures for the volcano lecture. The Mogi (1958) and Okada (1985) deformation fields and the Planck curves are computed;
volcano scenes, time series, plumes and DEMs are simulated and labelled."""
import numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, LightSource, hsv_to_rgb
from scipy.ndimage import gaussian_filter
import okada

os.makedirs('figs', exist_ok=True)
INK = '#13233A'; SOFT = '#4A5563'; RULE = '#E2DFD7'; ACC = '#C2410C'; BLUE = '#2F6DB5'; LAND = '#D8D2C2'
plt.rcParams.update({'font.family': ['Helvetica', 'DejaVu Sans'], 'font.size': 18, 'axes.edgecolor': SOFT, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': SOFT, 'ytick.color': SOFT})
DPI = 200
plt.rcParams['savefig.dpi'] = DPI
LAM = 5.5466                       # Sentinel-1 wavelength, cm: one fringe = LAM / 2 = 2.8 cm of line-of-sight motion
NU = 0.25                          # Poisson's ratio
THETA, G2S = 39.0, 260.0           # incidence angle and ground-to-satellite azimuth for an ascending Sentinel-1 pass
hh = np.linspace(0, 1, 256)
PHASE = LinearSegmentedColormap.from_list('phase', hsv_to_rgb(np.stack([hh, 0.72 * np.ones(256), 0.95 * np.ones(256)], 1)))
PHASE.set_bad('#D9D6CE')
DIV = LinearSegmentedColormap.from_list('div', ['#123B6D', '#2F6DB5', '#8FB3DD', '#ECE9E2', '#E7A57A', '#C2410C', '#7A2A08'])
SEQ = LinearSegmentedColormap.from_list('seq', ['#FBEBDD', '#F4C9A0', '#E7A57A', '#C2410C', '#7A2A08'])
rng = np.random.default_rng(1991)
out = {}


def tag(ax, text='Simulated data', x=0.02, y=0.02, ha='left', va='bottom', fs=14):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=fs, color='white', ha=ha, va=va,
            bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))


def clean(ax):
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)


def sn(shape, sigma):
    g = gaussian_filter(rng.normal(0, 1, shape), sigma)
    return g / g.std()


def mogi(x, y, depth, dV, nu=NU):
    """Surface displacement (m) of a point pressure source (Mogi, 1958): depth in m, volume change dV in m3."""
    r2 = x ** 2 + y ** 2
    c = (1 - nu) * dV / np.pi / (r2 + depth ** 2) ** 1.5
    return c * x, c * y, c * depth                  # east, north, up


def los(ue, un, uu):
    """Line-of-sight displacement, positive towards the satellite."""
    t, a = np.radians(THETA), np.radians(G2S)
    return ue * np.sin(t) * np.sin(a) + un * np.sin(t) * np.cos(a) + uu * np.cos(t)


def wrap(d_m):
    return np.angle(np.exp(-1j * 4 * np.pi * d_m * 100 / LAM))


def wrap_masked(d_m, limit=0.6):
    """Wrapped phase, with pixels masked where fringes are too dense to resolve (the radar loses coherence there)."""
    ph = -4 * np.pi * d_m * 100 / LAM
    gy, gx = np.gradient(ph)
    dense = gaussian_filter((np.hypot(gx, gy) > limit).astype(float), 1.5) > 0.2
    return np.ma.masked_where(dense, wrap(d_m))


# ---------- 1. Mogi: depth and fringes (computed) ----------
r = np.linspace(-15e3, 15e3, 601)
fig, ax = plt.subplots(1, 2, figsize=(15, 6.2), gridspec_kw={'width_ratios': [1.25, 1]}, constrained_layout=True)
DV = 10e6
for dpt, col in ((2e3, ACC), (4e3, BLUE), (8e3, INK)):
    ue, _, uu = mogi(r, 0 * r, dpt, DV)
    ax[0].plot(r / 1e3, uu * 100, color=col, lw=3, label=f'Up, source {dpt / 1e3:.0f} km deep')
    ax[0].plot(r / 1e3, ue * 100, color=col, lw=2, ls='--')
ax[0].axhline(0, color=RULE, lw=2, zorder=0)
ax[0].text(7.5, 21, 'Solid: up\nDashed: outwards (east)', fontsize=15, color=SOFT)
ax[0].set_xlabel('Distance from the centre (km)'); ax[0].set_ylabel('Ground movement (cm)')
ax[0].set_title(f'Same volume, {DV / 1e6:.0f} million m³, at three depths', loc='left', fontsize=18, color=INK)
ax[0].legend(frameon=False, fontsize=15, loc='upper left'); clean(ax[0]); ax[0].set_ylim(-25, 64)
g = np.linspace(-12e3, 12e3, 481); X, Y = np.meshgrid(g, g)
ue, un, uu = mogi(X, Y, 4e3, DV)
ax[1].imshow(wrap(los(ue, un, uu)), cmap=PHASE, vmin=-np.pi, vmax=np.pi, extent=[-12, 12, -12, 12], origin='lower')
ax[1].plot(0, 0, '^', color='white', mec=INK, ms=14)
ax[1].set_xlabel('East (km)'); ax[1].set_ylabel('North (km)')
ax[1].set_title('Ascending interferogram, source 4 km deep', loc='left', fontsize=18, color=INK)
ax[1].text(0.98, 0.03, 'One colour cycle = 2.8 cm', transform=ax[1].transAxes, ha='right', fontsize=14, color=INK,
           bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.85))
fig.savefig('figs/mogi.png', facecolor='white'); plt.close(fig)
u0 = {f'{d // 1000}km': round(float(mogi(0.0, 0.0, d, DV)[2] * 100), 1) for d in (2000, 4000, 8000)}
out['mogi'] = {'dV_Mm3': DV / 1e6, 'uplift_cm': u0, 'fringes_4km': round(float((los(ue, un, uu).max() - los(ue, un, uu).min()) * 100 / (LAM / 2)), 1)}

# ---------- 2. a dyke under a town (computed, Okada 1985 tensile dislocation) ----------


def dyke_enu(E, N, xc, yc, strike, top, bottom, length, opening, nu=NU):
    """A vertical dyke centred at (xc, yc) km, opening in metres; returns (ue, un, uu) in m."""
    st = np.radians(strike)
    us, vs = np.sin(st), np.cos(st)                 # along strike (east, north)
    un_, vn_ = -np.cos(st), np.sin(st)              # 90 degrees to the left of strike
    x0, y0 = xc - us * length / 2, yc - vs * length / 2
    dx, dy = E - x0, N - y0
    xo = dx * us + dy * vs
    yo = dx * un_ + dy * vn_
    ux, uy, uz = okada.okada85(xo, yo, bottom, 90.0, length, bottom - top, 0.0, 0.0, opening, nu)
    return ux * us + uy * un_, ux * vs + uy * vn_, uz


g = np.linspace(-14, 14, 561); X, Y = np.meshgrid(g, g)
DK = dict(xc=0.0, yc=0.0, strike=40.0, top=0.8, bottom=5.0, length=15.0, opening=2.0)
ue, un, uu = dyke_enu(X, Y, **DK)
fig, ax = plt.subplots(1, 3, figsize=(17, 6.0), gridspec_kw={'width_ratios': [1, 1, 1.15]}, constrained_layout=True)
lim = np.abs(uu).max()
im = ax[0].imshow(uu * 100, cmap=DIV, norm=TwoSlopeNorm(vcenter=0, vmin=-lim * 100, vmax=lim * 100), extent=[-14, 14, -14, 14], origin='lower')
cb = fig.colorbar(im, ax=ax[0], shrink=0.75, pad=0.02); cb.set_label('Up (cm)'); cb.outline.set_visible(False)
ax[0].set_title('1. Vertical movement', loc='left', fontsize=18, color=INK)
ax[1].imshow(wrap_masked(los(ue, un, uu)), cmap=PHASE, vmin=-np.pi, vmax=np.pi, extent=[-14, 14, -14, 14], origin='lower')
ax[1].set_title('2. Ascending interferogram', loc='left', fontsize=18, color=INK)
ax[1].text(0.02, 0.03, 'Grey: too many fringes to count', transform=ax[1].transAxes, fontsize=13, color=INK, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85))
s = np.radians(DK['strike'])
for a_ in ax[:2]:
    a_.plot([-7.5 * np.sin(s), 7.5 * np.sin(s)], [-7.5 * np.cos(s), 7.5 * np.cos(s)], color=INK, lw=2, ls='--')
    a_.set_xlabel('East (km)')
ax[0].set_ylabel('North (km)')
pr = np.linspace(-12, 12, 481)
pe, pn = pr * np.cos(s), -pr * np.sin(s)                          # a profile at right angles to the dyke
ue_p, un_p, uu_p = dyke_enu(pe, pn, **DK)
across = ue_p * np.cos(s) - un_p * np.sin(s)
ax[2].axhline(0, color=RULE, lw=2)
ax[2].plot(pr, uu_p * 100, color=ACC, lw=3, label='Up')
ax[2].plot(pr, across * 100, color=BLUE, lw=3, ls='--', label='Across the dyke')
ax[2].annotate('Graben: the ground\nabove the dyke drops', (0, uu_p[240] * 100), (2.0, -32), fontsize=15, color=INK,
               arrowprops=dict(arrowstyle='-', color=SOFT))
ax[2].set_xlabel('Distance across the dyke (km)'); ax[2].set_ylabel('Movement (cm)')
ax[2].set_title('3. Profile across the dyke', loc='left', fontsize=18, color=INK); ax[2].legend(frameon=False, fontsize=15, loc='upper right'); clean(ax[2])
ax[2].set_ylim(-np.abs(across).max() * 100 - 8, np.abs(across).max() * 100 + 25)
fig.savefig('figs/dyke.png', facecolor='white'); plt.close(fig)
out['dyke'] = {'graben_cm': round(float(uu_p.min() * 100)), 'flank_up_cm': round(float(uu_p.max() * 100)), 'widening_cm': round(float((across.max() - across.min()) * 100))}

# ---------- 3. multi-sensor time series around an eruption (simulated) ----------
t = np.arange(0, 730)                                   # days
T_ER, T_END = 600, 640
rate = np.where(t < 300, 0.02, 0.02 + 0.08 * ((t - 300) / 300) ** 2)   # cm/day, accelerating inflation
up = np.cumsum(np.where(t < T_ER, rate, 0))
up = np.where(t < T_ER, up, up[T_ER - 1] - (up[T_ER - 1] * 0.75) * (1 - np.exp(-(t - T_ER) / 6)))
up_obs = up + rng.normal(0, 0.6, t.size)
ins = t[::12]
vrp = np.where((t >= T_ER) & (t < T_END), 2000 * np.exp(-(t - T_ER) / 15) + 150, np.where(t > T_ER - 25, 3 + (t - (T_ER - 25)) * 0.3, 2.0))
vrp = np.where(t >= T_END, 2 + 40 * np.exp(-(t - T_END) / 20), vrp) * np.exp(rng.normal(0, 0.35, t.size))
so2 = np.where((t >= T_ER) & (t < T_END), 60 * np.exp(-(t - T_ER) / 10) + 4, np.where(t > T_ER - 60, 0.4 + (t - (T_ER - 60)) * 0.03, 0.3))
so2 = np.where(t >= T_END, 0.3 + 3 * np.exp(-(t - T_END) / 15), so2) * np.exp(rng.normal(0, 0.3, t.size))
day = rng.random(t.size) > 0.35                         # TROPOMI misses cloudy days
fig, ax = plt.subplots(3, 1, figsize=(12.5, 8.2), sharex=True, constrained_layout=True)
for a_ in ax:
    a_.axvspan(T_ER, T_END, color='#F4C9A0', alpha=0.6, lw=0); clean(a_)
ax[0].plot(ins, up_obs[::12], 'o', color=BLUE, ms=6); ax[0].plot(t, up, color=INK, lw=1.5, alpha=0.6)
ax[0].set_ylabel('Uplift (cm)'); ax[0].set_title('1. Ground uplift from InSAR, every 12 days', loc='left', fontsize=17, color=INK)
ax[0].text(T_ER + 4, up.max() * 0.92, 'Eruption', fontsize=15, color=ACC, fontweight='bold')
ax[1].semilogy(t, vrp, color=ACC, lw=1.4); ax[1].set_ylabel('Heat (MW)')
ax[1].set_title('2. Volcanic radiative power from thermal infrared, daily', loc='left', fontsize=17, color=INK)
ax[2].semilogy(t[day], so2[day], '.', color=INK, ms=6); ax[2].set_ylabel('SO₂ (kt/day)')
ax[2].set_title('3. Sulfur dioxide from TROPOMI, on clear days', loc='left', fontsize=17, color=INK)
ax[2].set_xlabel('Days since monitoring began'); ax[2].set_xlim(0, 730)
for a_ in ax:
    tag(a_, x=0.01, y=0.9, va='top')
fig.savefig('figs/series.png', facecolor='white'); plt.close(fig)
out['series'] = {'uplift_before_cm': round(float(up[T_ER - 1])), 'eruption_day': T_ER}

# ---------- 4. heat: Planck curves (computed) and a SWIR scene (simulated) ----------
C1, C2 = 1.191042e8, 1.4387752e4                       # W um4 m-2 sr-1, um K


def planck(lam_um, T):
    return C1 / (lam_um ** 5 * (np.exp(C2 / (lam_um * T)) - 1))


lam = np.linspace(0.8, 14, 800)
fig, ax = plt.subplots(1, 2, figsize=(15.5, 6.2), gridspec_kw={'width_ratios': [1.15, 1]}, constrained_layout=True)
for T, lab, col in ((1373, 'Fresh lava, 1100 °C', ACC), (873, 'Cooling crust, 600 °C', BLUE), (300, 'Ground, 27 °C', INK)):
    ax[0].semilogy(lam, planck(lam, T), color=col, lw=3, label=lab)
    pk = 2898 / T
    ax[0].plot(pk, planck(pk, T), 'o', color=col, ms=9)
for lo, hi, nm in ((1.55, 1.75, 'SWIR'), (2.1, 2.3, ''), (3.6, 4.0, 'MIR'), (10.5, 12.5, 'TIR')):
    ax[0].axvspan(lo, hi, color='#E5E8F0', zorder=0)
    if nm:
        ax[0].text((lo + hi) / 2 + (0.35 if nm == 'SWIR' else 0), 2e5, nm, ha='center', fontsize=15, color=SOFT)
ax[0].set_xlabel('Wavelength (µm)'); ax[0].set_ylabel('Emitted radiance (W m⁻² sr⁻¹ µm⁻¹)')
ax[0].set_title('Hotter surfaces peak at shorter wavelengths', loc='left', fontsize=18, color=INK)
ax[0].set_ylim(1e-3, 1e6); ax[0].legend(frameon=False, fontsize=15, loc='lower right'); clean(ax[0])
N = 300
yy, xx = np.mgrid[0:N, 0:N]
path = 150 + 40 * np.sin(yy / 55) + 10 * sn((N, N), 18)[:, :1]
width = 10 + 0.09 * yy
dist = np.abs(xx - path) / width
flow = (dist < 1) & (yy > 20)
core = (dist < 0.28) & (yy > 20) & (yy < 230)
veg = sn((N, N), 6)
bg = np.stack([0.28 + 0.04 * veg, 0.42 + 0.06 * veg, 0.30 + 0.05 * veg], -1)
img = bg.copy()
img[flow] = [0.12, 0.12, 0.13]
hot = np.clip(1 - dist / 0.28, 0, 1) * core * np.clip((240 - yy) / 120, 0.3, 1)
img = img * (1 - hot[..., None]) + hot[..., None] * np.array([1.0, 0.82, 0.25])
glow = gaussian_filter(hot, 3) * 0.8
img = np.clip(img + glow[..., None] * np.array([0.9, 0.45, 0.05]), 0, 1)
img[(yy < 26) & (np.abs(xx - path) < 22)] = [0.35, 0.33, 0.32]
ax[1].imshow(img, origin='upper', extent=[0, 6, 6, 0])
ax[1].text(path[10, 0] / 50 + 0.6, 0.35, 'Vent', fontsize=15, color='white', fontweight='bold')
ax[1].text(4.0, 5.6, 'Hot core of the flow', fontsize=15, color='white', ha='center', fontweight='bold')
ax[1].set_xlabel('km'); ax[1].set_ylabel('km')
ax[1].set_title('Sentinel-2 false colour (SWIR 2, SWIR 1, NIR)', loc='left', fontsize=18, color=INK)
tag(ax[1], x=0.98, y=0.02, ha='right')
fig.savefig('figs/thermal.png', facecolor='white'); plt.close(fig)
out['wien_um'] = {'lava': round(2898 / 1373, 1), 'crust': round(2898 / 873, 1), 'ground': round(2898 / 300, 1)}

# ---------- 5. lava volume from DEM differencing (simulated) ----------
N = 260; PIX = 10.0                                       # 10 m pixels
yy, xx = np.mgrid[0:N, 0:N]
pre = 600 - 0.9 * yy * PIX / 10 + 2.5 * sn((N, N), 25)  # a slope falling towards the bottom of the map
path = 120 + 35 * np.sin(yy / 50) + 8 * sn((N, N), 15)[:, :1]
wd = 12 + 0.12 * yy
d = np.abs(xx - path) / wd
thick = np.where((d < 1) & (yy > 15), 14 * np.sqrt(np.clip(1 - d ** 2, 0, 1)) * np.clip(1 - yy / 330, 0.25, 1), 0)
thick = gaussian_filter(thick, 1.2)
post = pre + thick
err_pre, err_post = 0.6 * sn((N, N), 3), 0.6 * sn((N, N), 3)
dz = (post + err_post) - (pre + err_pre)
mask = dz > 2.5
vol = float(dz[mask].sum() * PIX ** 2)
true_vol = float(thick.sum() * PIX ** 2)
fig, ax = plt.subplots(1, 2, figsize=(15, 6.2), gridspec_kw={'width_ratios': [1, 1.25]}, constrained_layout=True)
ls_ = LightSource(azdeg=315, altdeg=40)
ax[0].imshow(ls_.hillshade(post, vert_exag=4), cmap='gray', vmin=0, vmax=1, extent=[0, N * PIX / 1000, N * PIX / 1000, 0])
im = ax[0].imshow(np.ma.masked_where(~mask, dz), cmap=SEQ, vmin=0, vmax=14, alpha=0.9, extent=[0, N * PIX / 1000, N * PIX / 1000, 0])
cb = fig.colorbar(im, ax=ax[0], shrink=0.8, pad=0.02); cb.set_label('New lava thickness (m)'); cb.outline.set_visible(False)
ax[0].set_xlabel('km'); ax[0].set_ylabel('km'); ax[0].set_title('After minus before', loc='left', fontsize=18, color=INK)
row = 120
xr = np.arange(N) * PIX
ax[1].fill_between(xr, pre[row].min() - 6, pre[row], color=LAND, lw=0)
ax[1].fill_between(xr, pre[row], post[row], color=ACC, lw=0, alpha=0.85)
ax[1].plot(xr, pre[row], color=INK, lw=2, label='Before (DEM 1)'); ax[1].plot(xr, post[row], color=ACC, lw=2.5, label='After (DEM 2)')
ax[1].set_xlim(0, N * PIX); ax[1].set_ylim(pre[row].min() - 6, post[row].max() + 10)
ax[1].set_xlabel('Distance across the flow (m)'); ax[1].set_ylabel('Elevation (m)')
ax[1].set_title(f'Volume = sum of thickness × pixel area ≈ {vol / 1e6:.1f} million m³', loc='left', fontsize=17, color=INK)
ax[1].legend(frameon=False, fontsize=15, loc='upper right'); clean(ax[1])
ax[0].axhline(row * PIX / 1000, color='white', lw=1.5, ls='--')
tag(ax[0]); tag(ax[1], x=0.02, y=0.04)
fig.savefig('figs/lava.png', facecolor='white'); plt.close(fig)
out['lava'] = {'volume_Mm3': round(vol / 1e6, 1), 'true_Mm3': round(true_vol / 1e6, 1), 'area_km2': round(float(mask.sum() * PIX ** 2 / 1e6), 2)}

# ---------- 6. SO2 plume from TROPOMI-like pixels (simulated) ----------
DU_KG = 2.6867e20 * 0.064066 / 6.02214e23                 # kg of SO2 per m2 for one Dobson unit
PX, PY = 3.5, 5.5                                          # km, TROPOMI pixel since August 2019
nx, ny = 120, 50
xc_ = (np.arange(nx) + 0.5) * PX - 60; yc_ = (np.arange(ny) + 0.5) * PY - 80
Xs, Ys = np.meshgrid(xc_, yc_)
ang = np.radians(20)                                       # plume blows towards east-north-east
along = Xs * np.cos(ang) + Ys * np.sin(ang); acr = -Xs * np.sin(ang) + Ys * np.cos(ang)
spread = 6 + 0.12 * np.clip(along, 0, None)
col = np.where(along > 0, 150 * np.exp(-along / 160) * np.exp(-(acr - 0.0003 * along ** 2) ** 2 / (2 * spread ** 2)) * 6 / spread, 0)
col = col + 0.4 * rng.normal(0, 1, col.shape)
cloud = gaussian_filter(rng.random(col.shape), 2) > 0.62
show = np.ma.masked_where(cloud, col)
mass_t = float(np.clip(col, 0, None)[col > 1.0].sum() * PX * PY * 1e6 * DU_KG / 1e3)
fig, ax = plt.subplots(figsize=(13, 6.0), constrained_layout=True)
cm_ = LinearSegmentedColormap.from_list('so2', ['#F6F5F1', '#F4C9A0', '#E7A57A', '#C2410C', '#7A2A08']); cm_.set_bad('#C9CED8')
im = ax.imshow(show, origin='lower', cmap=cm_, vmin=0, vmax=60, extent=[xc_[0] - PX / 2, xc_[-1] + PX / 2, yc_[0] - PY / 2, yc_[-1] + PY / 2], interpolation='nearest')
ax.plot(0, 0, '^', color=INK, ms=16, mec='white', mew=1.5); ax.text(-5, -24, 'Volcano', fontsize=16, color=INK, ha='center', fontweight='bold')
ax.annotate('', (200, -10), (110, -43), arrowprops=dict(arrowstyle='->', color=INK, lw=2.5)); ax.text(120, -22, 'Wind', fontsize=16, color=INK, rotation=21)
ax.text(0.02, 0.95, 'Grey: cloud, no data', transform=ax.transAxes, fontsize=15, color=INK, va='top',
        bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.85))
cb = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02); cb.set_label('SO₂ column (Dobson units)'); cb.outline.set_visible(False)
ax.set_xlabel('East of the volcano (km)'); ax.set_ylabel('North (km)')
ax.set_title(f'One overpass: about {mass_t / 1e3:.0f} thousand tonnes of SO₂ in view', loc='left', fontsize=18, color=INK)
tag(ax, x=0.98, y=0.02, ha='right')
fig.savefig('figs/so2.png', facecolor='white'); plt.close(fig)
out['so2'] = {'mass_kt': round(mass_t / 1e3), 'du_kg_m2': DU_KG}

# ---------- 7. finding ash: the split-window test (simulated) ----------
N = 260
yy, xx = np.mgrid[0:N, 0:N]
bt11 = 288 + 4 * sn((N, N), 12)
ash_path = (np.abs((yy - 60) - 0.55 * (xx - 40) - 0.0012 * (xx - 40) ** 2) < 14 + 0.12 * (xx - 40)) & (xx > 40)
ash = np.where(ash_path, np.clip(1 - np.abs(xx - 160) / 160, 0.25, 1), 0) * (gaussian_filter(rng.random((N, N)), 3) * 0 + 1)
ash = gaussian_filter(ash, 3)
met = gaussian_filter((sn((N, N), 9) > 1.0).astype(float), 2) * np.clip((yy - 140) / 40, 0, 1)
bt11 = bt11 - 45 * ash - 50 * met
btd = 0.4 * sn((N, N), 2) * 0.5 + 2.2 * met - 3.0 * ash
fig, ax = plt.subplots(1, 2, figsize=(15.5, 6.2), gridspec_kw={'width_ratios': [1, 1.15]}, constrained_layout=True)
sel = rng.random(N * N) < 0.06
A_, M_ = ash.ravel()[sel], met.ravel()[sel]
cls = np.where(A_ > 0.3, 'ash', np.where(M_ > 0.3, 'met', 'clear'))
for c_, colr, lab in (('clear', '#B8C4D6', 'Clear sky'), ('met', BLUE, 'Water and ice cloud'), ('ash', ACC, 'Volcanic ash')):
    k = cls == c_
    ax[0].plot(bt11.ravel()[sel][k], btd.ravel()[sel][k], 'o', ms=4, color=colr, alpha=0.6, label=lab)
ax[0].axhline(0, color=INK, lw=2, ls='--')
ax[0].set_xlabel('Brightness temperature at 11 µm (K)'); ax[0].set_ylabel('BT 11 µm − BT 12 µm (K)')
ax[0].set_title('Ash falls below zero; cloud stays above', loc='left', fontsize=18, color=INK)
ax[0].legend(frameon=False, fontsize=15, loc='lower right', markerscale=2.5); clean(ax[0])
im = ax[1].imshow(btd, cmap=DIV.reversed(), norm=TwoSlopeNorm(vcenter=0, vmin=-3.5, vmax=3.5), origin='upper', extent=[0, 520, 520, 0])
ax[1].plot(40 * 2, 60 * 2, '^', color=INK, ms=15, mec='white')
cb = fig.colorbar(im, ax=ax[1], shrink=0.85, pad=0.02); cb.set_label('BT 11 µm − BT 12 µm (K)'); cb.outline.set_visible(False)
ax[1].set_title('Negative (orange): ash. Positive (blue): cloud', loc='left', fontsize=18, color=INK)
ax[1].set_xlabel('km'); ax[1].set_ylabel('km')
tag(ax[0], x=0.02, y=0.96, va='top'); tag(ax[1], x=0.98, y=0.02, ha='right')
fig.savefig('figs/ash.png', facecolor='white'); plt.close(fig)

# ---------- 8. the cover strip: an interferogram over a simulated volcano ----------
W, H = 1920 * 2, 277 * 2
xk = np.linspace(-34.6, 34.6, W // 2); yk = np.linspace(-5, 5, H // 2)
Xb, Yb = np.meshgrid(xk, yk)
topo = 2400 * np.exp(-(Xb ** 2 + Yb ** 2) / (2 * 6 ** 2)) + 60 * sn(Xb.shape, 8)
ue, un, uu = mogi(Xb * 1e3, Yb * 1e3, 4e3, 18e6)
ph = wrap(los(ue, un, uu))
rgb = PHASE((ph + np.pi) / (2 * np.pi))[..., :3]
shade = LightSource(azdeg=315, altdeg=45).hillshade(topo, vert_exag=0.06)
fade = np.exp(-(np.hypot(Xb, Yb) / 13) ** 4)[..., None]
base = np.array([0.80, 0.78, 0.73]) * np.ones_like(rgb)
rgb = (rgb * fade + base * (1 - fade)) * (0.55 + 0.45 * shade[..., None])
fig = plt.figure(figsize=(19.2, 2.77)); ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(rgb, aspect='auto', interpolation='bilinear'); ax.axis('off')
tag(ax, 'Computed fringes on a simulated volcano', x=0.995, y=0.06, ha='right', fs=13)
fig.savefig('figs/banner.png', dpi=DPI, facecolor='white'); plt.close(fig)

json.dump(out, open('figs/stats.json', 'w'), indent=1)
print(json.dumps(out))
