"""Figures for the SAR flood-mapping lecture. All data are simulated and labelled."""
import numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap, LightSource
from matplotlib.patches import Patch, FancyArrowPatch, Rectangle, Polygon
from scipy.ndimage import gaussian_filter, binary_opening
from scene import make, lee, otsu

os.makedirs('figs', exist_ok=True)
INK = '#13233A'; SOFT = '#4A5563'; RULE = '#E2DFD7'; ACC = '#C2410C'; BLUE = '#2F6DB5'; NAVY = '#123B6D'; LIGHTB = '#8FB3DD'
plt.rcParams.update({'font.family': ['Helvetica', 'DejaVu Sans'], 'font.size': 18, 'axes.edgecolor': SOFT, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': SOFT, 'ytick.color': SOFT})
DPI = 200
stats = {}


def tag(ax, text='Simulated data', x=0.02, y=0.02, ha='left', va='bottom', fs=14):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=fs, color='white', ha=ha, va=va,
            bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))


S = make()
pre_f, post_f = lee(S['pre']), lee(S['post'])
ext = [0, S['X'].max(), S['Y'].max(), 0]

# ---------- methods ----------
thr = otsu(post_f)
m_otsu = post_f < thr
diff = post_f - pre_f
m_change = (diff < -3.0) & (post_f < thr + 2)
m_change_hand = m_change & (S['hand'] < 15)
m_change_hand = binary_opening(m_change_hand, iterations=1)
m_vegflood = (diff > 3.0) & (S['hand'] < 15) & (S['cover'] == 'forest')
truth = S['flooded']
perm = S['channel']


def scores(m, include_veg=False):
    t = truth & ~perm
    m = m & ~perm
    tp = (m & t).sum(); fp = (m & ~t).sum(); fn = (~m & t).sum()
    return dict(hit=round(float(tp / (tp + fn)) * 100, 0), far=round(float(fp / max(tp + fp, 1)) * 100, 0), csi=round(float(tp / (tp + fp + fn)), 2))


stats['otsu_db'] = round(float(thr), 1)
stats['methods'] = {'otsu': scores(m_otsu), 'change': scores(m_change), 'change_hand': scores(m_change_hand),
                    'change_hand_veg': scores(m_change_hand | binary_opening(m_vegflood, iterations=1))}
area_px = (S['px'] / 1000) ** 2
stats['flood_km2_true'] = round(float((truth & ~perm).sum() * area_px), 1)
stats['flood_km2_mapped'] = round(float(((m_change_hand | binary_opening(m_vegflood, iterations=1)) & ~perm).sum() * area_px), 1)
stats['scene_km'] = round(float(S['X'].max()), 1)

# ---------- 1. pre, post, RGB change composite, flood map ----------
def gray(db, lo=-25, hi=0):
    return np.clip((db - lo) / (hi - lo), 0, 1)

rgb = np.dstack([gray(pre_f), gray(post_f), gray(post_f)])
cls = np.zeros(truth.shape, int)
cls[perm] = 1
cls[m_change_hand & ~perm] = 2
cls[binary_opening(m_vegflood, iterations=1)] = 3
ls = LightSource(azdeg=315, altdeg=45)
shade = ls.hillshade(S['dem'], vert_exag=3, dx=S['px'], dy=S['px'])
fig, axs = plt.subplots(1, 4, figsize=(17.6, 5.4), dpi=DPI)
axs[0].imshow(gray(pre_f), cmap='gray', vmin=0, vmax=1, extent=ext); axs[0].set_title('Before (VV)', loc='left', fontsize=19, fontweight='bold')
axs[1].imshow(gray(post_f), cmap='gray', vmin=0, vmax=1, extent=ext); axs[1].set_title('During the flood', loc='left', fontsize=19, fontweight='bold')
axs[2].imshow(rgb, extent=ext); axs[2].set_title('Change composite', loc='left', fontsize=19, fontweight='bold')
axs[3].imshow(shade, cmap='gray', vmin=-0.4, vmax=1.3, extent=ext)
cm = ListedColormap(['#00000000', NAVY, '#4F8FE0', ACC])
axs[3].imshow(np.ma.masked_equal(cls, 0), cmap=cm, vmin=0, vmax=3, extent=ext, interpolation='nearest')
axs[3].set_title('Flood map', loc='left', fontsize=19, fontweight='bold')
for ax in axs:
    ax.set_xticks([]); ax.set_yticks([])
tag(axs[0])
fig.legend([Patch(fc=NAVY), Patch(fc='#4F8FE0'), Patch(fc=ACC)], ['River (permanent)', 'Flood water', 'Flooded forest'],
           loc='lower right', bbox_to_anchor=(0.995, 0.0), frameon=False, fontsize=15, ncol=3)
fig.text(0.01, 0.035, 'Composite: red = before, green and blue = during. Newly flooded land turns red.', ha='left', fontsize=15, color=SOFT)
fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.14, wspace=0.05)
fig.savefig('figs/maps.png', facecolor='white'); plt.close(fig)

# ---------- 2. histogram and Otsu threshold ----------
fig, ax = plt.subplots(figsize=(11.2, 6.2), dpi=DPI)
v_post = post_f.ravel(); v_pre = pre_f.ravel()
bins = np.linspace(-32, 6, 140)
ax.hist(v_pre, bins=bins, color='#C9C4BA', alpha=0.9, label='Before the flood')
ax.hist(v_post, bins=bins, histtype='step', lw=3, color=INK, label='During the flood')
ax.axvline(thr, color=ACC, lw=3, ls='--')
ax.text(thr + 0.4, ax.get_ylim()[1] * 0.92, f'Otsu threshold\n{thr:.1f} dB', color=ACC, fontsize=17, va='top')
ax.text(-27.5, ax.get_ylim()[1] * 0.35, 'Water', fontsize=19, color=BLUE, fontweight='bold')
ax.text(-5.6, ax.get_ylim()[1] * 0.8, 'Land', fontsize=19, color=SOFT, fontweight='bold', ha='left')
ax.text(-1.8, ax.get_ylim()[1] * 0.22, 'Flooded forest\nand town (brighter)', fontsize=15, color=ACC)
ax.set_xlabel('Backscatter, VV (dB)'); ax.set_ylabel('Number of pixels'); ax.set_yticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); ax.spines['left'].set_visible(False)
ax.legend(loc='upper left', frameon=False, fontsize=16)
tag(ax, x=0.99, y=0.03, ha='right')
fig.subplots_adjust(left=0.06, right=0.98, top=0.97, bottom=0.13)
fig.savefig('figs/hist.png', facecolor='white'); plt.close(fig)

# ---------- 3. false alarms: thresholding alone vs change detection + HAND ----------
fa_otsu = m_otsu & ~truth & ~perm
fig, axs = plt.subplots(1, 2, figsize=(14.2, 6.6), dpi=DPI)
for ax, (t, m, fa) in zip(axs, (('Threshold only', m_otsu, fa_otsu), ('Change detection + height above river', m_change_hand, m_change_hand & ~truth & ~perm))):
    ax.imshow(shade, cmap='gray', vmin=-0.4, vmax=1.3, extent=ext)
    c = np.zeros(truth.shape, int); c[m & ~perm] = 1; c[fa] = 2; c[perm] = 3
    ax.imshow(np.ma.masked_equal(c, 0), cmap=ListedColormap(['#00000000', '#4F8FE0', '#E3A008', NAVY]), vmin=0, vmax=3, extent=ext, interpolation='nearest')
    ax.set_title(t, loc='left', fontsize=19, fontweight='bold'); ax.set_xticks([]); ax.set_yticks([])
ay, ax_ = np.where(S['airport']); ya = float(S['Y'][ay[0], 0]); xa = float(S['X'][0, ax_.mean().astype(int)])
sy, sx = np.where(S['shadow'] & (S['Y'] < 3.5) & (S['X'] > 11)); ysh = float(np.median(S['Y'][sy, 0])); xsh = float(np.median(S['X'][0, sx]))
axs[0].annotate('Airport runway', xy=(xa, ya), xytext=(xa - 2.5, ya + 2.6), fontsize=15, color=INK, arrowprops=dict(arrowstyle='->', color=INK),
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85))
axs[0].annotate('Radar shadow\non steep hills', xy=(xsh, ysh), xytext=(xsh - 5.2, ysh + 0.2), fontsize=15, color=INK, arrowprops=dict(arrowstyle='->', color=INK),
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85))
tag(axs[0])
fig.legend([Patch(fc='#4F8FE0'), Patch(fc='#E3A008'), Patch(fc=NAVY)], ['Mapped as flooded, correctly', 'False alarm (not flooded)', 'River'],
           loc='lower center', ncol=3, frameon=False, fontsize=16)
fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.11, wspace=0.04)
fig.savefig('figs/false.png', facecolor='white'); plt.close(fig)
stats['shadow_px_frac'] = round(float(S['shadow'].mean()) * 100, 2)

# ---------- 4. water depth from extent + elevation ----------
r = 330
row_dem = S['dem'][r]; row_fl = (m_change_hand | perm)[r]
xs = S['X'][r]
edge = np.where(np.diff(row_fl.astype(int)) != 0)[0]
from scipy.ndimage import binary_dilation
edges2d = binary_dilation(m_change_hand | perm) & ~(m_change_hand | perm)
ys0, ys1 = r - 15, r + 15
wl = float(np.median(S['dem'][ys0:ys1][edges2d[ys0:ys1]]))
depth = np.clip(wl - row_dem, 0, None) * row_fl
stats['depth'] = {'water_level_m': round(wl, 1)}
fig, ax = plt.subplots(figsize=(11.4, 6.0), dpi=DPI)
sel = (xs > 2) & (xs < 13)
fl_idx = np.where(row_fl & sel)[0]
x_lo, x_hi = xs[fl_idx.min()], xs[fl_idx.max()]
wl = float((row_dem[fl_idx.min()] + row_dem[fl_idx.max()]) / 2)
stats['depth'] = {'water_level_m': round(wl, 1)}
water = (row_dem < wl) & (xs >= x_lo) & (xs <= x_hi)
ax.fill_between(xs[sel], np.where(water[sel], row_dem[sel], wl), np.where(water[sel], wl, wl), color='#8FB3DD', step='mid', label='Floodwater')
ax.fill_between(xs[sel], row_dem[sel].min() - 3, row_dem[sel], color='#D9CBA8', step='mid')
ax.plot(xs[sel], row_dem[sel], color=INK, lw=2)
ax.axhline(wl, color=BLUE, lw=2, ls='--')
ax.text(3.4, wl + 1.0, f'Water level = height of the flood edges: {wl:.1f} m', color=BLUE, fontsize=15)
for xe in (x_lo, x_hi):
    ax.plot([xe, xe], [wl, wl + 3.2], color=ACC, lw=2.5)
ax.text((x_lo + x_hi) / 2, wl + 3.6, 'Flood edges from the SAR map', color=ACC, fontsize=16, ha='center')
ax.text((x_lo + x_hi) / 2, wl - 0.5, 'Depth = water level − ground', color=INK, fontsize=15, ha='center', va='center')
depth_row = np.clip(wl - row_dem, 0, None) * water * ~perm[r]
ax.set_ylim(row_dem[sel].min() - 2, wl + 8); ax.set_xlim(2, 13)
ax.set_xlabel('Distance across the valley (km)'); ax.set_ylabel('Elevation (m)')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
tag(ax, x=0.99, y=0.97, ha='right', va='top')
fig.subplots_adjust(left=0.09, right=0.98, top=0.97, bottom=0.13)
fig.savefig('figs/depth.png', facecolor='white'); plt.close(fig)
stats['depth']['floodplain_max_m'] = round(float(depth_row.max()), 1)

# ---------- 5. inundation frequency from a simulated archive ----------
rng = np.random.default_rng(5)
levels = np.clip(rng.gamma(1.4, 1.3, 240), 0, 7.5)            # 240 simulated images over 10 years
freq = np.zeros(truth.shape)
from scipy.ndimage import label as lbl
for lv in levels:
    f = (S['hand'] < lv) & (S['cover'] != 'urban') | ((S['hand'] < lv - 1.5) & (S['cover'] == 'urban')) | perm
    lab_, n_ = lbl(f)
    f = np.isin(lab_, np.unique(lab_[perm]))
    freq += f
freq = freq / levels.size * 100
fig, ax = plt.subplots(figsize=(9.6, 8.4), dpi=DPI)
ax.imshow(shade, cmap='gray', vmin=-0.4, vmax=1.3, extent=ext)
fm = np.ma.masked_less(freq, 1)
seq = LinearSegmentedColormap.from_list('seq', ['#DCE8F5', '#8FB3DD', '#2F6DB5', '#123B6D'])
im = ax.imshow(fm, cmap=seq, vmin=1, vmax=100, extent=ext)
ax.set_xticks([]); ax.set_yticks([])
cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02); cb.set_label('Share of images flooded (%)', fontsize=16)
tag(ax)
fig.subplots_adjust(left=0.02, right=0.9, top=0.98, bottom=0.02)
fig.savefig('figs/freq.png', facecolor='white'); plt.close(fig)
stats['freq_levels'] = {'median_m': round(float(np.median(levels)), 1), 'max_m': round(float(levels.max()), 1)}

# ---------- 6. scattering schematic ----------
fig, axs = plt.subplots(1, 4, figsize=(17.0, 5.0), dpi=DPI)
def beam(ax, x0, y0, x1, y1, c=INK, lw=2.5, ls='-'):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=18, color=c, lw=lw, ls=ls))
for ax in axs:
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
    beam(ax, 0.6, 6.4, 4.4, 2.1, c=SOFT, lw=2, ls='--')
# open water
a = axs[0]; a.add_patch(Rectangle((0, 0), 10, 2, fc='#8FB3DD')); beam(a, 4.6, 2.1, 9.2, 6.2, c=BLUE, lw=3)
a.set_title('Calm water: mirror-like\nalmost nothing returns: DARK', fontsize=17, loc='left', fontweight='bold')
# rough land
a = axs[1]; xs_ = np.linspace(0, 10, 60); a.fill_between(xs_, 0, 2 + 0.25 * np.sin(xs_ * 4.1) + 0.15 * np.cos(xs_ * 9.7), color='#C9B48A')
for ang in (40, 70, 100, 130, 155):
    t_ = np.radians(ang); beam(a, 4.6, 2.2, 4.6 + 2.2 * np.cos(t_), 2.2 + 2.2 * np.sin(t_), c=SOFT, lw=2)
beam(a, 4.4, 2.3, 2.6, 4.0, c=ACC, lw=3)
a.set_title('Rough land: scattered in all\ndirections, some returns: GREY', fontsize=17, loc='left', fontweight='bold')
# flooded forest
a = axs[2]; a.add_patch(Rectangle((0, 0), 10, 2, fc='#8FB3DD'))
for tx in (2.0, 5.4, 8.4):
    a.add_patch(Rectangle((tx, 2), 0.35, 3.0, fc='#6B4F2A')); a.add_patch(plt.Circle((tx + 0.17, 5.4), 1.0, fc='#5E8C4A'))
beam(a, 4.4, 2.1, 5.35, 3.2, c=BLUE, lw=3); beam(a, 5.35, 3.25, 1.2, 6.2, c=ACC, lw=4)
a.set_title('Flooded forest: water and\ntrunks bounce it back: BRIGHT', fontsize=17, loc='left', fontweight='bold')
# urban flood
a = axs[3]; a.add_patch(Rectangle((0, 0), 10, 2, fc='#8FB3DD'))
a.add_patch(Rectangle((5.3, 2), 2.4, 3.6, fc='#9CA3AF')); a.add_patch(Rectangle((1.0, 2), 1.4, 2.2, fc='#9CA3AF'))
beam(a, 4.4, 2.1, 5.3, 3.0, c=BLUE, lw=3); beam(a, 5.3, 3.05, 1.6, 6.0, c=ACC, lw=4)
a.add_patch(Rectangle((7.7, 2), 2.3, 0.02, fc=INK)); a.text(8.0, 0.8, 'shadow', fontsize=14, color=INK)
a.set_title('Flooded streets: bright\ncorners, shadows: MIXED', fontsize=17, loc='left', fontweight='bold')
axs[0].text(0.6, 6.6, 'radar', fontsize=14, color=SOFT)
fig.text(0.99, 0.02, 'Schematic', fontsize=13, color='white', ha='right', bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none'))
fig.subplots_adjust(left=0.01, right=0.99, top=0.82, bottom=0.03, wspace=0.08)
fig.savefig('figs/scatter.png', facecolor='white'); plt.close(fig)

# ---------- banner: wide change composite ----------
B = make(nx=1920, ny=277, px=25.0, seed=7, flood_level=4.5)
bp, bq = lee(B['pre']), lee(B['post'])
brgb = np.dstack([gray(bp), gray(bq), gray(bq)])
fig = plt.figure(figsize=(19.2, 2.77), dpi=150)
ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(brgb, aspect='auto'); ax.axis('off')
ax.text(0.995, 0.04, 'Simulated data', transform=ax.transAxes, fontsize=11, color='white', ha='right', va='bottom', bbox=dict(boxstyle='square,pad=0.25', fc='#4A5563', ec='none', alpha=0.9))
fig.savefig('figs/banner.png', facecolor='white'); plt.close(fig)

json.dump(stats, open('figs/stats.json', 'w'), indent=1)
print(json.dumps(stats, indent=1))
