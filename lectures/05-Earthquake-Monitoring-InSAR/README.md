# Lecture 5: Earthquake Monitoring with InSAR

**Measuring how the ground moves before, during and after earthquakes** · presented by Akshay Raj Manocha

📄 **Slides:** [Earthquake_Monitoring_InSAR_Akshay_Raj_Manocha.pdf](Earthquake_Monitoring_InSAR_Akshay_Raj_Manocha.pdf) (37 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)
🛰️ **Animation:** [elastic_rebound.html](animations/elastic_rebound.html)

This lecture builds on Lectures [1](../01-SAR-Interferometry/), [2](../02-InSAR-Geometry/) and [3](../03-InSAR-Theory/). It uses the same line-of-sight geometry as [Lecture 4](../04-Landslide-Monitoring-InSAR/).

## What the lecture covers

1. **Earthquakes and the earthquake cycle:** strike-slip, thrust and normal faults, and what InSAR sees for each. The cycle runs from slow build-up between earthquakes (interseismic), to sudden slip (coseismic), to continued motion afterwards (postseismic), shown with an animation of elastic rebound. The part also covers moment magnitude and what InSAR adds to seismology.
2. **Coseismic interferograms:** simulated magnitude 7.0 strike-slip, thrust and normal earthquakes. It shows how east, north and vertical motion combine in the line of sight, and why north–south strike-slip faults are hard to see. It ends with five steps for reading an interferogram, and what to do near the fault (offset tracking, L-band, optical correlation).
3. **From fringes to the fault:** the Okada (1985) fault model, an inversion of noisy simulated data, and what fault models tell us.
4. **Before and after the earthquake:** interseismic strain (slip rate and locking depth), from strain to seismic hazard, postseismic afterslip and relaxation, and triggered landslides, liquefaction and damage.
5. **Case studies:** Gorkha, Nepal (2015); Kahramanmaraş, Türkiye (2023); Mandalay, Myanmar (2025); rapid-response services (COMET-LiCSAR, NASA–JPL ARIA, USGS).
6. **Engineering practice:** fault setback zones, lifelines crossing faults, dams and bridges, damage proxy maps from coherence, limits and good practice, four exercises with answers, recap and references.

## The animation

`animations/elastic_rebound.html` shows a map view of a road crossing a locked strike-slip fault. The road bends while the fault is locked, snaps to a permanent offset in the earthquake, and then strain builds again. It runs live in the online deck. In the PDF it is a single still frame. To show it in class from this repository, download the file and open it in any web browser. It needs no internet connection.

## Folder contents

| Path | What it is |
|------|------------|
| `Earthquake_Monitoring_InSAR_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `animations/elastic_rebound.html` | The elastic-rebound animation as a standalone web page |
| `figures/` | The figures used in the deck |
| `scripts/` | Python code for the fault model and every figure |

## Remaking the figures

Requires Python 3 with `numpy`, `matplotlib` and `scipy`.

```bash
cd scripts && python3 figures.py
```

The figures are written to `scripts/figs/`. Two files can be used on their own in exercises:

- `okada.py` computes the surface displacement from a rectangular fault in an elastic half-space (Okada, 1985). Run `python3 okada.py` to check it against the test values published in Okada's paper. It reproduces all nine.
- `geo.py` holds the Sentinel-1 line-of-sight geometry.

## About the data

- **Simulated** (labelled on every figure): the coseismic interferograms (Okada model, Sentinel-1 wavelength 5.55 cm, incidence 39°), the inversion, the interseismic profile, the postseismic time series and the damage proxy map. The inversion is a real nonlinear least-squares fit to the noisy simulated data.
- **Schematic:** the earthquake-cycle figure.
- **Computed:** the moment-magnitude table and the exercise answers.

## Sources and credits

- Fault model: Okada, Y. (1985). Surface deformation due to shear and tensile faults in a half-space. *Bulletin of the Seismological Society of America* 75, 1135–1154.
- Moment magnitude: Hanks, T. C., Kanamori, H. (1979). A moment magnitude scale. *Journal of Geophysical Research* 84, 2348–2350.
- Elastic rebound: Reid, H. F. (1910). The mechanics of the earthquake. Report of the State Earthquake Investigation Commission on the 1906 California earthquake, vol. 2.
- Interseismic model: Savage, J. C., Burford, R. O. (1973). Geodetic determination of relative plate motion in central California. *Journal of Geophysical Research* 78, 832–845.
- First earthquake InSAR: Massonnet, D. et al. (1993). The displacement field of the Landers earthquake mapped by radar interferometry. *Nature* 364, 138–142.
- Gorkha 2015: Lindsey, E. O. et al. (2015). *Geophysical Research Letters* 42, 6655–6661; and the [ALOS-2 ScanSAR study in Earth, Planets and Space](https://earth-planets-space.springeropen.com/articles/10.1186/s40623-015-0359-z).
- Türkiye 2023: [USGS fault rupture mapping from satellite data](https://www.sciencebase.gov/catalog/item/644ad9afd34e45f6ddccf736); [Geophysical Journal International 236, 1068](https://academic.oup.com/gji/article/236/2/1068/7458664); [NASA JPL ARIA damage proxy map](https://www.jpl.nasa.gov/images/pia25564-satellites-assess-earthquake-damage-in-turkey/).
- Myanmar 2025: [Sustained supershear rupture during the 2025 Mandalay, Myanmar earthquake](https://www.nature.com/articles/s43247-025-02927-5), *Communications Earth & Environment*; [PNAS (2025)](https://www.pnas.org/doi/10.1073/pnas.2514378122).
- Rapid response: Lazecký, M. et al. (2020). LiCSAR: an automatic InSAR tool for measuring and monitoring tectonic and volcanic activity. *Remote Sensing* 12, 2430. Damage proxy maps: Yun, S.-H. et al. (2015). *Seismological Research Letters* 86, 1549–1556.
- Reviews: Bürgmann, R., Rosen, P. A., Fielding, E. J. (2000). *Annual Review of Earth and Planetary Sciences* 28, 169–209; Elliott, J. R., Walters, R. J., Wright, T. J. (2016). *Nature Communications* 7, 13844.
- Sentinel-1: EU Copernicus programme / ESA.

All figures and the animation were made for this lecture.
