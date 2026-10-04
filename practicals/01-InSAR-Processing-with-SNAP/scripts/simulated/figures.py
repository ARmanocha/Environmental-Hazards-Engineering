"""Teaching figures for the simulated volcano. Run simulate.py first."""
import numpy as np, matplotlib, os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, hsv_to_rgb
os.makedirs('figs', exist_ok=True)
S = np.load('sim/sim.npz'); X, Y = S['X'], S['Y']; sea = S['sea']
INK = '#13233A'; SOFT = '#4A5563'; NODATA = '#D9D6CE'
plt.rcParams.update({'font.family': ['Helvetica', 'DejaVu Sans'], 'font.size': 17, 'axes.edgecolor': SOFT, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': SOFT, 'ytick.color': SOFT})
hh = np.linspace(0, 1, 256)
PHASE = LinearSegmentedColormap.from_list('phase', hsv_to_rgb(np.stack([hh, 0.72*np.ones(256), 0.95*np.ones(256)], 1)))
radar = np.fliplr          # descending, right-looking: radar geometry is mirrored east-west

def save(name, img, cmap, vmin, vmax, label, ticks=None, ticklabels=None, radar_geom=True, norm=None, mask=None, extra=None):
    fig = plt.figure(figsize=(6.4, 5.6), dpi=200)
    ax = fig.add_axes([0.08, 0.08, 0.70, 0.86] if radar_geom else [0.13, 0.12, 0.64, 0.84]); cax = fig.add_axes([0.81, 0.12, 0.035, 0.78])
    data = np.ma.masked_invalid(img.astype(float))
    if mask is not None: data = np.ma.masked_where(mask, data)
    cm = plt.get_cmap(cmap).copy() if isinstance(cmap, str) else cmap.copy(); cm.set_bad(NODATA)
    im = ax.imshow(data, cmap=cm, vmin=None if norm else vmin, vmax=None if norm else vmax, norm=norm,
                   extent=None if radar_geom else (-20, 20, -20, 20), interpolation='bilinear')
    if radar_geom:
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel('Range  →', fontsize=16, labelpad=6); ax.set_ylabel('←  Azimuth (flight direction)', fontsize=16, labelpad=6)
    else:
        ax.set_xlabel('Easting (km)', fontsize=16); ax.set_ylabel('Northing (km)', fontsize=16)
        ax.yaxis.set_label_position('left'); ax.tick_params(labelsize=14)
    for s in ax.spines.values(): s.set_color('#BBB')
    cb = fig.colorbar(im, cax=cax); cb.set_label(label, fontsize=16); cb.ax.tick_params(labelsize=14)
    if ticks is not None: cb.set_ticks(ticks)
    if ticklabels is not None: cb.set_ticklabels(ticklabels)
    ax.text(0.02, 0.02, 'Simulated data', transform=ax.transAxes, fontsize=13, color='white',
            bbox=dict(boxstyle='round,pad=0.25', fc=(0.07, 0.14, 0.23, 0.75), ec='none'))
    if extra: extra(ax)
    fig.savefig(f'figs/{name}.png', facecolor='white'); plt.close(fig)

pi = np.pi; PT = [-pi, 0, pi]; PL = ['−π', '0', 'π']
amp = S['amp']; lg = np.log10(amp + 1e-4); save('amp', radar(lg), 'gray', np.percentile(lg, 8), np.percentile(lg, 99.5), 'Intensity (log scale)', ticks=[], mask=None)
save('ifg_topo', radar(S['ifg_topo']), PHASE, -pi, pi, 'Phase (radians)', PT, PL, mask=radar(sea))
b = radar(S['ifg_topo']).copy(); b[196:203, :] = np.nan; b[396:403, :] = np.nan
fig_mask = radar(sea)
def bursts(ax):
    for r in (200, 400): ax.axhline(r, color='black', lw=3)
save('ifg_bursts', radar(S['ifg_topo']), PHASE, -pi, pi, 'Phase (radians)', PT, PL, mask=fig_mask, extra=bursts)
save('ifg', radar(S['ifg']), PHASE, -pi, pi, 'Phase (radians)', PT, PL, mask=radar(sea))
save('coh', radar(S['coh']), 'gray', 0, 1, 'Coherence', [0, 0.25, 0.5, 0.75, 1])
save('filt', radar(S['filt']), PHASE, -pi, pi, 'Phase (radians)', PT, PL, mask=radar(sea))
save('unw', radar(S['unw']), 'viridis', np.nanmin(S['unw']), np.nanmax(S['unw']), 'Unwrapped phase (radians)')
norm = TwoSlopeNorm(vmin=-3, vcenter=0, vmax=14)
save('disp_radar', radar(S['disp']), 'RdBu_r', None, None, 'LOS displacement (cm)', norm=norm)
def profile_line(ax):
    ax.plot([-15, 12], [2, 2], color='black', lw=2, ls=(0, (6, 4))); ax.text(-15, 3, 'A', fontsize=18, fontweight='bold'); ax.text(11, 3, 'B', fontsize=18, fontweight='bold')
    ax.plot(0, 2, marker='^', color='black', ms=11)
save('disp_map', S['disp'], 'RdBu_r', None, None, 'LOS displacement (cm)\npositive = toward satellite', norm=norm, radar_geom=False, extra=profile_line)

# multilook comparison (single-look noise vs 4x1 looks + averaging), summit crop
rng = np.random.default_rng(5)
crop = (slice(140, 340), slice(200, 400))
one = radar(np.angle(np.exp(1j*(S['ifg'] + rng.normal(size=S['ifg'].shape)*1.1))))[crop]
def smooth(z, s):
    n = z.shape[0]; k = np.fft.fftfreq(n)[:, None]**2 + np.fft.fftfreq(z.shape[1])[None, :]**2
    return np.fft.ifft2(np.fft.fft2(z)*np.exp(-2*(np.pi**2)*(s**2)*k))
ml = np.angle(smooth(np.exp(1j*one), 1.6))
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.9), dpi=200)
for a, im, t in zip(axs, (one, ml), ('Single look (noisy)', 'After multilooking')):
    a.imshow(im, cmap=PHASE, vmin=-pi, vmax=pi, interpolation='nearest'); a.set_xticks([]); a.set_yticks([]); a.set_title(t, fontsize=19, color=INK, pad=10)
    for s in a.spines.values(): s.set_color('#BBB')
axs[0].text(0.03, 0.03, 'Simulated data', transform=axs[0].transAxes, fontsize=13, color='white', bbox=dict(boxstyle='round,pad=0.25', fc=(0.07, 0.14, 0.23, 0.75), ec='none'))
fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.03, wspace=0.06); fig.savefig('figs/multilook.png', facecolor='white'); plt.close(fig)

# profile A-B through the summit, observed vs model
x = X[0]; r = np.argmin(np.abs(Y[:, 0] - 2.0)); sel = (x >= -15) & (x <= 12)
fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=200)
ax.plot(x[sel], S['disp'][r, sel], color='#4F86C6', lw=2.2, label='Observed (simulated InSAR)')
ax.plot(x[sel], S['los_def'][r, sel], color='#C2410C', lw=2.6, ls=(0, (7, 3)), label='Model: point source 3 km deep')
ax.axhline(0, color='#999', lw=1); ax.set_xlim(-15, 12)
ax.set_xlabel('Distance along profile A–B (km)', fontsize=17); ax.set_ylabel('LOS displacement (cm)', fontsize=17)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#E4E2DC'); ax.legend(frameon=False, fontsize=15, loc='upper left'); ax.tick_params(labelsize=14)
ax.text(-14.7, -2.2, 'A', fontsize=18, fontweight='bold'); ax.text(11.3, -2.2, 'B', fontsize=18, fontweight='bold')
fig.tight_layout(); fig.savefig('figs/profile.png', facecolor='white'); plt.close(fig)
print('figures done')
