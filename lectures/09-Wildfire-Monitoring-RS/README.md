# Lecture 9: Wildfire Monitoring with Remote Sensing

**Finding fires, mapping burn scars and judging fire danger from space** · presented by Akshay Raj Manocha

📄 **Slides:** [Wildfire_Monitoring_RS_Akshay_Raj_Manocha.pdf](Wildfire_Monitoring_RS_Akshay_Raj_Manocha.pdf) (39 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)
🛰️ **Animation:** [subpixel_fire.html](animations/subpixel_fire.html)

This lecture uses thermal and optical satellites, plus radar for burned areas. It links to [Lecture 8](../08-Drought-Monitoring-RS/) on drought and fuel dryness, and to [Lecture 4](../04-Landslide-Monitoring-InSAR/) on hazards after a fire.

## What the lecture covers

1. **Wildfire and why we monitor it:** fuel, weather, terrain and ignition; forest fires and crop-residue burning in India; the Forest Survey of India's satellite alerts; what satellites tell us before, during and after a fire.
2. **Detecting active fires:**
   - Planck's law and why fire sensors use a 3.9 µm channel.
   - How a fire much smaller than a pixel is still detected.
   - The satellites: MODIS, VIIRS, geostationary, Sentinel-3, Sentinel-2 and Landsat.
   - Following a fire from pass to pass.
   - Fire radiative power and biomass burned.
3. **Mapping burned areas and what follows:** the normalized burn ratio (NBR), burn severity from dNBR (Key and Benson classes), radar through smoke, recovery, and post-fire hazards (debris flows, floods, landslides, water supply).
4. **Before the fire:** vegetation dryness and the fire season, and fire-danger ratings, including the Canadian Fire Weather Index and FSI pre-fire alerts.
5. **Case studies:**
   - Uttarakhand, 2023–24 season.
   - Crop-residue burning in Punjab.
   - Black Summer, Australia, 2019–20.
   - Canada, 2023.
   - Los Angeles, January 2025.
6. **Engineering practice:** the wildland–urban interface, lifelines, post-fire hazards, water supply, air quality and fire management; an 8-step workflow; limits and good practice; four exercises with answers; recap and references.

## The animation

`animations/subpixel_fire.html` grows a 1000 K fire from 1 m² to 1 hectare inside one 1 km pixel of 300 K ground. Two bars show the pixel's brightness temperature at 3.9 µm and 11 µm. The pixel is flagged once a simplified detection test is passed, at about 0.1% of the pixel. It runs live in the online deck. In the PDF it is a single still frame. To show it in class from this repository, download the file and open it in any web browser. It needs no internet connection.

## Folder contents

| Path | What it is |
|------|------------|
| `Wildfire_Monitoring_RS_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `animations/subpixel_fire.html` | The sub-pixel fire animation as a standalone web page |
| `figures/` | The figures used in the deck |
| `scripts/` | Python code that makes every figure |

## Remaking the figures

Requires Python 3 with `numpy`, `matplotlib` and `scipy`.

```bash
cd scripts && python3 figures.py
```

The figures are written to `scripts/figs/`. The script includes small functions for Planck's law and its inverse (brightness temperature), the sub-pixel mixing calculation, NBR and dNBR, and the Stefan–Boltzmann FRP example. Students can reuse them for the exercises.

## About the data

- **Computed from physics:** the Planck curves, the sub-pixel brightness temperatures, the animation, and the exercise answers.
- **Simulated** (labelled "Simulated data" on every figure): the fire detections over three days, the burn-severity scene, the recovery time series, the fire-season chart, and the cover strip.
- **Schematic:** the forest and burned-land spectra show typical shapes, not measurements.
- **Real:** the case-study numbers and the descriptions of satellites and services, from the sources below.

## Sources and credits

- Active-fire detection: Giglio, L., Schroeder, W., Justice, C. O. (2016). *Remote Sensing of Environment* 178, 31–41. Schroeder, W. et al. (2014). *Remote Sensing of Environment* 143, 85–96.
- Burn severity: Key, C. H., Benson, N. C. (2006). [Landscape assessment: the Normalized Burn Ratio](https://www.fs.usda.gov/rm/pubs_series/rmrs/gtr/rmrs_gtr164/rmrs_gtr164_13_land_assess.pdf). USDA Forest Service RMRS-GTR-164-CD.
- Fire radiative power and biomass: Wooster, M. J. et al. (2005). *Journal of Geophysical Research* 110, D24311.
- Fire danger: Van Wagner, C. E. (1987). Development and structure of the Canadian Forest Fire Weather Index System. Canadian Forestry Service, Forestry Technical Report 35.
- Burned-area mapping review: Chuvieco, E. et al. (2019). *Remote Sensing of Environment* 225, 45–64.
- NASA FIRMS: [Fire Information for Resource Management System](https://www.earthdata.nasa.gov/news/feature-articles/data-tool-focus-fire-information-resource-management-system).
- India: Forest Survey of India, [Forest Fire Alert System (FAST 3.0)](https://fsi.nic.in/uploads/documents/technical_information_series_vol1_no2.pdf).
- Uttarakhand 2023–24: state forest department figures reported by [India Water Portal](https://www.indiawaterportal.org/climate-change/disasters/unravelling-escalating-forest-fire-crisis-uttarakhand) and [Newslaundry](https://www.newslaundry.com/2024/05/18/uttarakhand-forests-across-1500-hectares-burned-in-a-year-were-fire-lines-drawn-to-prevent-it) (May 2024).
- Punjab: Punjab government satellite counts as reported in the press; [CEEW](https://www.ceew.in/publications/how-can-satellite-borne-remote-sensing-capture-crop-burning-and-farm-fires).
- Australia: [CSIRO](https://www.csiro.au/en/news/all/articles/2021/november/bushfires-linked-climate-change); Filkov, A. I. et al. (2020). [Impact of Australia's catastrophic 2019/20 bushfire season](https://www.sciencedirect.com/science/article/pii/S2666449620300098). *Journal of Safety Science and Resilience* 1, 44–56.
- Canada: [Natural Resources Canada](https://natural-resources.canada.ca/stories/simply-science/canada-s-record-breaking-wildfires-2023-fiery-wake-call); Jain, P. et al. (2024). [Nature Communications 15, 6764](https://www.nature.com/articles/s41467-024-51154-7); Kirchmeier-Young, M. C. et al. (2024). [npj Climate and Atmospheric Science 7, 316](https://www.nature.com/articles/s41612-024-00841-9).
- Los Angeles 2025: CAL FIRE and news reports (January 2025).

All figures and the animation were made for this lecture.
