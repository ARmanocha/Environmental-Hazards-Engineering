"""Simulated Sentinel-1 interferometric pair over an inflating volcano (for teaching figures)."""
import numpy as np, json, os
os.makedirs("sim", exist_ok=True)
rng = np.random.default_rng(42)
N = 600; L = 40.0                                  # 600 x 600 pixels over 40 x 40 km
x = np.linspace(-L/2, L/2, N); X, Y = np.meshgrid(x, -x)   # km, north up
lam = 0.0555; theta = np.radians(39.0); nu = 0.25
def fractal(beta, seed):
    r = np.random.default_rng(seed); k = np.fft.fftfreq(N)[:, None]**2 + np.fft.fftfreq(N)[None, :]**2
    k[0, 0] = 1; f = (r.normal(size=(N, N)) + 1j*r.normal(size=(N, N))) * k**(-beta/4); f[0, 0] = 0
    z = np.real(np.fft.ifft2(f)); return (z - z.mean())/z.std()
# topography: volcano with a summit crater, rough flanks, sea to the east
xc, yc = 0.0, 2.0; R = np.hypot(X-xc, Y-yc)
h = 2600*np.exp(-(R/9.0)**1.6) - 120*np.exp(-(R/1.0)**2) + 60*fractal(3.2, 1) * np.exp(-(R/14)**2) + 40
sea = (X > 13 + 2*np.sin(Y/4)); h[sea] = 0
# amplitude: descending, right-looking -> satellite to the east; slopes facing east are bright
gy, gx = np.gradient(h/1000.0, x[1]-x[0]); nx, ny, nz = -gx/1, gy/1, np.ones_like(h)   # y axis flipped (north up)
nrm = np.sqrt(nx**2+ny**2+nz**2); los = np.array([np.sin(theta), 0, np.cos(theta)])
inc = np.clip((nx*los[0]+ny*los[1]+nz*los[2])/nrm, 0.02, 1)
rough = np.gradient(fractal(2.2, 9))[1]
amp = (inc**6) * np.exp(0.6*rough) * rng.gamma(4.0, 0.25, size=h.shape); amp[sea] *= 0.05
# coherence: rock near the summit high, vegetated lower flanks lower, sea ~0
coh = 0.88 - 0.45*np.clip((R-5)/9, 0, 1) + 0.06*fractal(2.5, 3); coh = np.clip(coh, 0.12, 0.95); coh[sea] = 0.04 + 0.04*rng.random(sea.sum())
# deformation: Mogi point source, depth 3 km, volume change 6e6 m3
d = 3000.0; dV = 6e6; rm = R*1000; Rs = np.sqrt(rm**2 + d**2)
uz = (1-nu)*dV/np.pi * d/Rs**3; ur = (1-nu)*dV/np.pi * rm/Rs**3
ue = ur*(X-xc)*1000/np.maximum(rm, 1e-6)
los_def = uz*np.cos(theta) + ue*np.sin(theta)          # metres, positive = toward the satellite
atm = 0.006*fractal(8/3, 7) - 0.004*h/1000.0            # turbulent + stratified delay, metres
hamb = 150.0                                             # ambiguity height for B_perp ~ 100 m
phi_topo = 2*np.pi*h/hamb
phi_sig = 4*np.pi/lam*(los_def + atm)
noise = rng.normal(size=h.shape) * (1.9*(1-coh)); noise[sea] = rng.uniform(-np.pi, np.pi, sea.sum())
wrap = lambda p: np.angle(np.exp(1j*p))
ifg_topo = wrap(phi_topo + phi_sig + noise)
ifg = wrap(phi_sig + noise)
def smooth(z, s):
    k = np.fft.fftfreq(N)[:, None]**2 + np.fft.fftfreq(N)[None, :]**2
    return np.fft.ifft2(np.fft.fft2(z)*np.exp(-2*(np.pi**2)*(s**2)*k))
filt = np.angle(smooth(np.exp(1j*ifg)*coh, 2.2))
mask = (coh < 0.3) | sea
unw = phi_sig.copy(); unw[mask] = np.nan
disp = (los_def + atm)*100; disp[mask] = np.nan                       # cm
np.savez_compressed('sim/sim.npz', X=X, Y=Y, h=h, amp=amp, coh=coh, ifg_topo=ifg_topo, ifg=ifg, filt=filt, unw=unw, disp=disp,
                    los_def=los_def*100, uz=uz*100, sea=sea)
row = np.argmin(np.abs(x - 0)); prow = np.argmin(np.abs(-x - yc))
stats = {"peak_uz_cm": float(uz.max()*100), "peak_los_cm": float(np.nanmax(los_def)*100),
         "peak_obs_cm": float(np.nanmax(disp)), "fringes_topo": float(h.max()/hamb),
         "fringes_def": float(np.nanmax(los_def)/(lam/2)), "half_width_km": float(0.766*d/1000),
         "dV_check": float(uz.max()*np.pi*d**2/(1-nu)), "atm_std_cm": float(np.nanstd(atm[~sea])*100),
         "hmax": float(h.max())}
json.dump(stats, open('sim/stats.json', 'w'), indent=1); print(json.dumps(stats, indent=1))
