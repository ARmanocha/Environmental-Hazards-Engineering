"""Surface displacement from a rectangular dislocation in an elastic half-space (Okada, 1985, BSSA 75, 1135-1154)."""
import numpy as np


def _terms(xi, eta, q, sd, cd, a):
    R = np.sqrt(xi ** 2 + eta ** 2 + q ** 2)
    yt = eta * cd + q * sd
    dt = eta * sd - q * cd
    X = np.sqrt(xi ** 2 + q ** 2)
    with np.errstate(divide='ignore', invalid='ignore'):
        ath = np.where(np.abs(q) < 1e-12, 0.0, np.arctan(xi * eta / (q * R)))
        lnRe = np.log(R + eta)
        I5 = np.where(np.abs(xi) < 1e-12, 0.0,
                      a * 2 / cd * np.arctan((eta * (X + q * cd) + X * (R + X) * sd) / (xi * (R + X) * cd)))
        I4 = a / cd * (np.log(R + dt) - sd * lnRe)
        I3 = a * (yt / (cd * (R + dt)) - lnRe) + sd / cd * I4
        I2 = a * (-lnRe) - I3
        I1 = a * (-xi / (cd * (R + dt))) - sd / cd * I5
        ss = (xi * q / (R * (R + eta)) + ath + I1 * sd,
              yt * q / (R * (R + eta)) + q * cd / (R + eta) + I2 * sd,
              dt * q / (R * (R + eta)) + q * sd / (R + eta) + I4 * sd)
        ds = (q / R - I3 * sd * cd,
              yt * q / (R * (R + xi)) + cd * ath - I1 * sd * cd,
              dt * q / (R * (R + xi)) + sd * ath - I5 * sd * cd)
        tf = (q ** 2 / (R * (R + eta)) - I3 * sd ** 2,
              -dt * q / (R * (R + xi)) - sd * (xi * q / (R * (R + eta)) - ath) - I1 * sd ** 2,
              yt * q / (R * (R + xi)) + cd * (xi * q / (R * (R + eta)) - ath) - I5 * sd ** 2)
    return ss, ds, tf


def okada85(x, y, d, dip, L, W, U1=0.0, U2=0.0, U3=0.0, nu=0.25):
    """Okada's own frame: x along strike, fault from x=0..L, lower edge at depth d, width W up-dip.
    U1 strike-slip (positive = left-lateral), U2 dip-slip (positive = reverse), U3 opening. Returns (ux, uy, uz)."""
    dip = np.radians(dip)
    if abs(np.cos(dip)) < 1e-6:
        dip -= 1e-6
    sd, cd = np.sin(dip), np.cos(dip)
    a = 1 - 2 * nu                     # mu / (lambda + mu)
    p = y * cd + d * sd
    q = y * sd - d * cd
    out = np.zeros((3,) + np.shape(x))
    for xi, eta, s in ((x, p, 1), (x, p - W, -1), (x - L, p, -1), (x - L, p - W, 1)):
        ss, ds, tf = _terms(xi, eta, q, sd, cd, a)
        for k in range(3):
            out[k] += s * (-U1 / (2 * np.pi) * ss[k] - U2 / (2 * np.pi) * ds[k] + U3 / (2 * np.pi) * tf[k])
    return out


def fault_enu(E, N, xc, yc, strike, dip, rake, slip, top, bottom, length, nu=0.25):
    """Map-frame wrapper. Fault centred along strike at (xc, yc) (km), top edge trace at (xc, yc); dips to the right of strike.
    rake: 0 left-lateral, 180 right-lateral, 90 reverse (thrust), -90 normal. Depths in km, slip in m. Returns (ue, un, uu) in m."""
    st = np.radians(strike)
    di = np.radians(dip)
    W = (bottom - top) / np.sin(di)
    # Okada's x along strike from the fault's start, y across (positive to the left of strike, the hanging wall is at -y)
    # Okada's origin is the start of the LOWER edge projected... build it from the top-edge trace
    ue_s, un_s = np.sin(st), np.cos(st)          # unit vector along strike (east, north)
    ue_n, un_n = -np.cos(st), np.sin(st)         # unit vector 90 deg left of strike
    # point on the lower edge at the start of the fault, projected to the surface
    off = (bottom - top) / np.tan(di)            # horizontal offset of the lower edge, towards the dip side (right of strike)
    x0 = xc - ue_s * length / 2 - ue_n * off
    y0 = yc - un_s * length / 2 - un_n * off
    dx, dy = E - x0, N - y0
    xo = dx * ue_s + dy * un_s
    yo = dx * ue_n + dy * un_n
    r = np.radians(rake)
    ux, uy, uz = okada85(xo, yo, bottom, dip, length, W, slip * np.cos(r), slip * np.sin(r), 0.0, nu)
    ue = ux * ue_s + uy * ue_n
    un = ux * un_s + uy * un_n
    return ue, un, uz


if __name__ == "__main__":
    print("Okada 1985 Table 2 check (x=2, y=3, d=4, dip=70, L=3, W=2):")
    for name, U in (("strike", (1, 0, 0)), ("dip", (0, 1, 0)), ("tensile", (0, 0, 1))):
        print(name, ["%.3e" % v for v in okada85(np.array(2.0), np.array(3.0), 4.0, 70, 3.0, 2.0, *U)])
    print("expected strike [-8.689e-03, -4.298e-03, -2.747e-03]; dip [-4.682e-03, -3.527e-02, -3.564e-02]; tensile [-2.660e-04, 1.056e-02, 3.214e-03]")
