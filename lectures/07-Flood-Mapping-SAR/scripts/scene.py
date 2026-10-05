"""A simulated river valley seen by Sentinel-1 (VV, dB) before and during a flood. Everything here is synthetic."""
import numpy as np
from scipy.ndimage import gaussian_filter, uniform_filter, binary_dilation, label

def sn(rng, shape, sigma):
    """Smooth random field scaled to unit standard deviation."""
    g = gaussian_filter(rng.normal(0, 1, shape), sigma)
    return g / g.std()


ENL = 4.4                        # equivalent number of looks of Sentinel-1 IW GRD
SIGMA = {'crop': -10.5, 'forest': -7.5, 'urban': -2.0, 'water': -22.0, 'tarmac': -19.5, 'sand': -17.5}


def make(nx=600, ny=600, px=25.0, seed=1, flood_level=3.5, steep=True):
    rng = np.random.default_rng(seed)
    x = np.arange(nx) * px / 1000.0; y = np.arange(ny) * px / 1000.0            # km
    X, Y = np.meshgrid(x, y)
    W = nx * px / 1000.0
    cx = W * 0.47 + 1.2 * np.sin(Y / 1.9) + 0.5 * np.sin(Y / 0.7 + 1.0)        # meandering river centreline
    d = np.abs(X - cx)                                                          # km from the river
    bed = 40.0 - 1.2 * Y                                                        # river bed falls downstream (south = larger y)
    flood_plain = 1.0 + 0.9 * d + sn(rng, X.shape, 6) * 0.35
    hills = np.clip(d - 3.6, 0, None) ** 1.6 * 55
    dem = bed + flood_plain + hills + gaussian_filter(rng.normal(0, 1, X.shape), 3) * 1.5 * (d > 3.2)
    if steep:   # a few steep, rocky hills: their slopes facing away from the radar fall in shadow
        for hx, hy in ((W * 0.86, 2.2), (W * 0.93, 3.6), (W * 0.83, 13.3), (W * 0.07, 7.5)):
            r = np.hypot(X - hx, Y - hy)
            dem = dem + np.clip(1 - r / 0.5, 0, None) * 900
    airport = (np.abs(Y - 9.4) < 0.22) & (X > cx + 3.0) & (X < cx + 6.2) & (d > 3.0)
    dem = np.where(gaussian_filter(airport.astype(float), 3) > 0.05, np.maximum(dem, bed + 6.5), dem)
    channel = d < 0.09 + 0.03 * np.sin(Y)
    dem = np.where(channel, bed - 2.0, dem)
    hand = dem - bed                                                            # height above the river (simplified HAND)
    cover = np.full(X.shape, 'crop', dtype=object)
    forest = (sn(rng, X.shape, 14) > 0.6) & (d < 3.3) & (d > 0.4)
    cover[forest] = 'forest'
    cover[d > 3.6] = 'forest'
    town = ((X - (cx + 1.8)) ** 2 / 1.0 + (Y - 4.0) ** 2 / 0.8) < 1
    cover[town] = 'urban'
    cover[airport] = 'tarmac'
    sand = (d < 0.35) & ~channel & (sn(rng, X.shape, 5) > 1.0)
    cover[sand] = 'sand'
    cover[channel] = 'water'
    # local slope towards / away from a radar looking east (ascending): shadow on steep slopes facing west->east away
    gy, gx = np.gradient(dem, px)
    slope_away = np.degrees(np.arctan(-gx))                                     # ground falling eastwards = facing away
    shadow = slope_away > 51.0
    layover = np.degrees(np.arctan(gx)) > 39.0
    base = np.vectorize(SIGMA.get)(cover).astype(float)
    base += sn(rng, X.shape, 2) * 0.8
    base = np.where(layover, base + 6.0, base)
    pre = np.where(shadow, -26.0, base)
    flooded = (hand < flood_level) & ~channel & (cover != 'urban') | ((hand < flood_level - 1.5) & (cover == 'urban'))
    lab, n = label(flooded | channel)
    keep = np.isin(lab, np.unique(lab[channel]))                                # only areas connected to the river
    flooded = flooded & keep
    post = pre.copy()
    open_f = flooded & np.isin(cover, ['crop', 'sand', 'tarmac'])
    veg_f = flooded & (cover == 'forest')
    urb_f = flooded & (cover == 'urban')
    post[open_f] = SIGMA['water'] + rng.normal(0, 1.0, open_f.sum())
    post[veg_f] = pre[veg_f] + 4.5                                             # double bounce: brighter
    post[urb_f] = pre[urb_f] + 2.5
    wind = sn(rng, X.shape, 25) > 1.4                 # a patch of wind-roughened water
    post[open_f & wind] = -13.0

    def speckle(db, s):
        lin = 10 ** (db / 10.0) * np.random.default_rng(s).gamma(ENL, 1.0 / ENL, db.shape)
        return 10 * np.log10(lin)
    return dict(X=X, Y=Y, dem=dem, hand=hand, cover=cover, channel=channel, flooded=flooded, veg_f=veg_f, open_f=open_f, urb_f=urb_f,
                shadow=shadow, airport=airport, sand=sand, wind=wind & open_f, pre=speckle(pre, seed + 10), post=speckle(post, seed + 20), px=px)


def lee(db, size=5):
    """Simple box-car speckle filter in linear power, back to dB."""
    lin = 10 ** (db / 10.0)
    return 10 * np.log10(uniform_filter(lin, size))


def otsu(values, bins=256):
    v = values[np.isfinite(values)]
    h, e = np.histogram(v, bins=bins)
    c = (e[:-1] + e[1:]) / 2
    w0 = np.cumsum(h); w1 = w0[-1] - w0
    m0 = np.cumsum(h * c) / np.maximum(w0, 1); m1 = (np.sum(h * c) - np.cumsum(h * c)) / np.maximum(w1, 1)
    between = w0 * w1 * (m0 - m1) ** 2
    return c[np.argmax(between)]
