# Lecture 4: Landslide Monitoring with InSAR

**Measuring slow slope movements from space** · presented by Akshay Raj Manocha

📄 **Slides:** [Landslide_Monitoring_InSAR_Akshay_Raj_Manocha.pdf](Landslide_Monitoring_InSAR_Akshay_Raj_Manocha.pdf) (40 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)
🛰️ **Animation:** [slope_aspect.html](animations/slope_aspect.html)

This lecture applies the InSAR ideas from Lectures [1](../01-SAR-Interferometry/), [2](../02-InSAR-Geometry/) and [3](../03-InSAR-Theory/) and the [SNAP practical](../../practicals/01-InSAR-Processing-with-SNAP/) to landslides.

## What the lecture covers

1. **Landslides and why we monitor them:** landslide types and which ones InSAR can see, the Cruden and Varnes velocity scale with the range each technique covers, and what InSAR adds.
2. **Seeing slopes from space:** InSAR measures only the line-of-sight part of the motion. This part covers layover and shadow on ridges, which slope directions each pass sees, converting line-of-sight velocity to downslope velocity, and the phase-aliasing speed limit of each satellite.
3. **Techniques and processing:** differential InSAR, persistent scatterers, small baselines, offset tracking, corner reflectors and ground-based radar; what reflects radar on a hillside; a landslide workflow; open tools; atmosphere and seasons in mountains.
4. **Reading the results:** one valley seen from two passes, decomposing into vertical and east–west motion, time series against monsoon rainfall, the inverse-velocity method for forecasting failure, and the limits of early warning.
5. **Case studies:** Mud Creek, California (2017); Xinmo, China (2017); Joshimath, India (2023); national ground-motion services (EGMS, InSAR Norway) and NISAR.
6. **Engineering practice:** uses in roads, dams, mines and towns; combining InSAR with field instruments; limits and good practice; four exercises with answers; recap and references.

## The animation

`animations/slope_aspect.html` shows a slope turning through every direction. Two bars show how much of its downslope motion the ascending and descending Sentinel-1 passes measure. It runs live in the online deck. In the PDF it is a single still frame. To show it in class from this repository, download the file and open it in any web browser. It needs no internet connection.

## Folder contents

| Path | What it is |
|------|------------|
| `Landslide_Monitoring_InSAR_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `animations/slope_aspect.html` | The slope-direction animation as a standalone web page |
| `figures/` | The figures used in the deck |
| `scripts/` | Python code that computes the geometry and makes every figure |

## Remaking the figures

Requires Python 3 with `numpy`, `matplotlib` and `scipy`.

```bash
cd scripts && python3 figures.py
```

The figures are written to `scripts/figs/`. `geo.py` holds the line-of-sight sensitivity calculation. It can be used on its own for the exercises.

## About the data

- **Simulated** (labelled "Simulated data" on every figure): the two-pass velocity maps, the cover strip, the monsoon time series and the failure-forecast example. They use Sentinel-1 wavelength and geometry, so students can check calculations against a known answer.
- **Computed:** the sensitivity chart, the animation and the speed-limit table. They come from Sentinel-1 geometry (incidence 39°, ascending heading about 350°, descending about 190°) and published wavelengths and revisit times.
- **Indicative:** the technique ranges on the velocity-scale chart depend on the sensor and the site.

## Sources and credits

- Velocity classes: Cruden, D. M., Varnes, D. J. (1996). Landslide types and processes. TRB Special Report 247, 36–75.
- Landslide types: Hungr, O., Leroueil, S., Picarelli, L. (2014). The Varnes classification of landslide types, an update. *Landslides* 11, 167–194.
- Inverse-velocity method: Fukuzono, T. (1985). A new method for predicting the failure time of a slope. Proc. 4th International Conference and Field Workshop on Landslides, Tokyo, 145–150.
- Mud Creek: Handwerger, A. L. et al. (2019). A shift from drought to extreme rainfall drives a stable landslide to catastrophic failure. *Scientific Reports* 9, 1569; and [NASA](https://science.nasa.gov/earth/natural-disasters/drought-deluge-turned-stable-landslide-into-disaster/).
- Xinmo: Intrieri, E. et al. (2018). The Maoxian landslide as seen from space: detecting precursors of failure with Sentinel-1 data. *Landslides* 15, 123–133; and [COMET](https://comet.nerc.ac.uk/sentinel-1-satellites-reveal-pre-event-movements-source-areas-maoxian-landslides-china/).
- Joshimath: National Remote Sensing Centre (ISRO), preliminary report on land subsidence, January 2023.
- Prediction from satellite InSAR: Carlà, T. et al. (2019). *Scientific Reports* 9, 14137.
- Review: Lacroix, P., Handwerger, A. L., Bièvre, G. (2020). Life and death of slow-moving landslides. *Nature Reviews Earth & Environment* 1, 404–419.
- Hotspot detection: Bekaert, D. P. S. et al. (2020). *Remote Sensing of Environment* 249, 111983.
- Slope visibility: Notti, D. et al. (2014). *International Journal of Remote Sensing* 35, 2186–2214.
- Ground-motion services: [European Ground Motion Service](https://land.copernicus.eu/en/products/european-ground-motion-service) (Copernicus Land Monitoring Service); NISAR ([NASA](https://science.nasa.gov/mission/nisar/), ISRO).
- Sentinel-1: EU Copernicus programme / ESA.

All figures and the animation were made for this lecture.
