"""Sentinel-1 line-of-sight (LOS) sensitivity to downslope landslide motion."""
import numpy as np
THETA = 39.0                      # incidence angle, degrees (mid-swath Sentinel-1 IW)
G2S = {"asc": 260.0, "desc": 100.0}  # azimuth from ground towards the satellite (asc looks east, desc looks west)


def los(geom, theta=THETA):
    """Unit vector from ground to satellite, (east, north, up)."""
    t, a = np.radians(theta), np.radians(G2S[geom])
    return np.array([np.sin(t) * np.sin(a), np.sin(t) * np.cos(a), np.cos(t)])


def downslope(aspect, slope):
    """Unit vector of downslope motion for a slope facing `aspect` (deg from north) and dipping `slope` (deg)."""
    a, b = np.broadcast_arrays(np.radians(aspect), np.radians(slope))
    return np.stack([np.cos(b) * np.sin(a), np.cos(b) * np.cos(a), -np.sin(b)], -1)


def sens(aspect, slope, geom, theta=THETA):
    """C = LOS component of a unit downslope motion; positive = towards the satellite."""
    return downslope(aspect, slope) @ los(geom, theta)


if __name__ == "__main__":
    for name, a in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
        print(name, {g: round(float(sens(a, 30, g)), 3) for g in ("asc", "desc")})
