# Practical 1: InSAR Processing with ESA SNAP

**Mapping volcano deformation with Sentinel-1** · presented by Akshay Raj Manocha

📄 **Slides:** [InSAR_Processing_with_SNAP_Akshay_Raj_Manocha.pdf](InSAR_Processing_with_SNAP_Akshay_Raj_Manocha.pdf) (43 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)

A hands-on session. Students take two Sentinel-1 radar images and turn them into a map of how many centimetres a volcano's ground moved, working step by step in ESA's free SNAP software. It assumes the [Introduction](../../lectures/00-Introduction/) and Lectures [1](../../lectures/01-SAR-Interferometry/), [2](../../lectures/02-InSAR-Geometry/) and [3](../../lectures/03-InSAR-Theory/).

## What the practical covers

1. **Before you start:** the software (SNAP and SNAPHU), a free data account, and choosing a good pair of images.
2. **Processing in SNAP:** thirteen steps, each with the exact menu path and settings: open, TOPS Split, apply orbits, back-geocoding, interferogram, deburst, topographic phase removal, multilook, Goldstein filter, SNAPHU unwrapping, phase to displacement, terrain correction, and export.
3. **Results and interpretation:** reading the displacement map and a profile, estimating the depth and volume of the magma source (Mogi model), and checking whether a signal is real.
4. **Real example: Kīlauea, Hawaii, 2018:** real Sentinel-1 interferograms of the eruption and the M6.9 earthquake, including magma moving before the eruption, about 55 cm of motion on the south flank, coherence, and the atmosphere over Mauna Loa and Mauna Kea. It ends with an exercise to reproduce the result in SNAP.
5. **Tips and next steps:** automating with the Graph Builder, troubleshooting, a good-practice checklist, and moving on to time series.

## The exercise

Kīlauea, 2 May → 8 May 2018. Search [ASF Vertex](https://search.asf.alaska.edu) for Sentinel-1, IW, L1 SLC, path 124, ascending, and download the images of those two dates (a free NASA Earthdata login is needed). Process them with the thirteen steps, then compare your map with the COMET-LiCSAR result in the slides. Etna (December 2018), Campi Flegrei and Sierra Negra (2018) are suggested as further exercises.

## Folder contents

| Path | What it is |
|------|------------|
| `InSAR_Processing_with_SNAP_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `figures/simulated/` | Step-by-step figures for Parts 2 and 3 (simulated volcano) |
| `figures/kilauea/` | Real Kīlauea 2018 maps and profile for Part 4 |
| `scripts/simulated/` | Python code that makes the simulated data and figures |
| `scripts/kilauea/` | Python code that makes the Kīlauea figures, and a script to download the data |

## Remaking the figures

Requires Python 3 with `numpy`, `matplotlib`, `scipy` and `rasterio`.

```bash
cd scripts/simulated && python3 simulate.py && python3 figures.py
```

```bash
cd scripts/kilauea && ./download_data.sh && python3 kilauea_figures.py
```

The first writes to `scripts/simulated/figs/`. The second downloads about 40 MB of COMET-LiCSAR products into `scripts/kilauea/raw/` and writes to `scripts/kilauea/figs/`.

## About the data

- **Parts 2 and 3** use a **simulated** example, labelled "Simulated data" on every figure. It is a Mogi point source under a synthetic volcano, with Sentinel-1 wavelength and geometry, noise, atmosphere and low-coherence areas, so students can check their results against a known answer.
- **Part 4** uses **real** Sentinel-1 interferograms from COMET-LiCSAR, frame `124A_06996_091406` (track 124, ascending): 20 April → 2 May 2018 and 2 → 8 May 2018. Positive displacement means motion toward the satellite.

## Credits

- **Software:** ESA SNAP ([step.esa.int](https://step.esa.int)); SNAPHU by C. W. Chen and H. A. Zebker (Stanford University).
- **Sentinel-1 data:** EU Copernicus programme / ESA.
- **Kīlauea products:** LiCSAR contains modified Copernicus Sentinel data 2018 analysed by the Centre for the Observation and Modelling of Earthquakes, Volcanoes and Tectonics (COMET). LiCSAR uses JASMIN, the UK's collaborative data analysis environment ([jasmin.ac.uk](http://jasmin.ac.uk)). Citation: Lazecky, M.; Maghsoudi, Y. (2022): LiCSAR interferometry products. NERC EDS Centre for Environmental Data Analysis. [catalogue.ceda.ac.uk/uuid/52cda2e0e6c04272ae15ac836c1e8493](https://catalogue.ceda.ac.uk/uuid/52cda2e0e6c04272ae15ac836c1e8493). Open Government Licence v3.
- **Kīlauea 2018 event facts:** USGS Hawaiian Volcano Observatory.

SNAP menu paths and defaults are as in recent SNAP versions; menus can move slightly between releases.
