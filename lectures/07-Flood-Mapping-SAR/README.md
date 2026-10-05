# Lecture 7: Flood Mapping with SAR

**Seeing floodwater through clouds, day and night** · presented by Akshay Raj Manocha

📄 **Slides:** [Flood_Mapping_SAR_Akshay_Raj_Manocha.pdf](Flood_Mapping_SAR_Akshay_Raj_Manocha.pdf) (37 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)
🛰️ **Animation:** [flood_timing.html](animations/flood_timing.html)

This lecture uses the brightness of radar images (backscatter), not interferometry. It builds on the SAR basics in the [Introduction](../00-Introduction/) and [Lecture 1](../01-SAR-Interferometry/).

## What the lecture covers

1. **Floods and why radar sees them:** river, flash, coastal and urban floods, and why radar works under cloud. It explains why calm water is dark while flooded forest and towns can be bright, lists the radar satellites (Sentinel-1, NISAR, EOS-04/RISAT-1A, RADARSAT Constellation, ALOS-2/4, commercial X-band), and asks whether a satellite catches the flood peak.
2. **Mapping water in SAR images:** preparing GRD images, Otsu thresholding, change detection with a change composite, and false alarms (radar shadow, runways) removed with change detection and HAND masks. It covers the hard cases (flooded vegetation, urban floods, wind and rain, fast floods) and an 8-step workflow.
3. **Accuracy, services and tools:** four methods compared on a simulated scene, and checking a flood map with hit rate, false alarm ratio and the critical success index (CSI). It lists Copernicus Global Flood Monitoring and EMS Rapid Mapping, the International Charter and NRSC (ISRO), plus free tools (Google Earth Engine with the UN-SPIDER script, SNAP, QGIS, Python, HEC-RAS).
4. **Case studies:** Kerala (2018), Pakistan (2022), Valencia (2024), and NRSC's Flood Hazard Zonation Atlas of Assam (1998–2023).
5. **Engineering practice:** water depth from flood extent and elevation, flood frequency from the archive, calibrating hydraulic models with SAR, uses, limits and good practice, four exercises with answers, recap and references.

## The animation

`animations/flood_timing.html` shows a simulated flood rising to a peak on day 7 and draining again. A satellite passing every 6 days (days 3, 9 and 15) never catches the peak. It runs live in the online deck. In the PDF it is a single still frame. To show it in class from this repository, download the file and open it in any web browser. It needs no internet connection.

## Folder contents

| Path | What it is |
|------|------------|
| `Flood_Mapping_SAR_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `animations/flood_timing.html` | The flood-timing animation as a standalone web page |
| `figures/` | The figures used in the deck |
| `scripts/` | Python code for the simulated scene and every figure |

## Remaking the figures

Requires Python 3 with `numpy`, `matplotlib` and `scipy`.

```bash
cd scripts && python3 figures.py
```

The figures are written to `scripts/figs/`. `scene.py` builds a simulated river valley seen by Sentinel-1 before and during a flood. It includes speckle (4.4 looks), crops, forest, a town, an airport runway, steep hills with radar shadow, flooded forest that gets brighter, and a patch of wind-roughened water. It also contains a simple Otsu threshold function. Students can use it to try their own mapping rules and score them against the known truth.

## About the data

- **Simulated** (labelled "Simulated data" on every figure): the radar scene, the change composite, the flood maps, the histogram and Otsu threshold, the false-alarm comparison, the accuracy scores, the depth profile and the flood-frequency map.
- **Schematic:** the scattering diagram.
- **Computed:** the exercise answers.
- **Real:** the case-study numbers and the descriptions of services, from the sources below.

## Sources and credits

- Thresholding: Otsu, N. (1979). A threshold selection method from gray-level histograms. *IEEE Transactions on Systems, Man, and Cybernetics* 9, 62–66. Martinis, S., Twele, A., Voigt, S. (2009). *Natural Hazards and Earth System Sciences* 9, 303–314.
- HAND: Nobre, A. D. et al. (2011). Height Above the Nearest Drainage: a hydrologically relevant new terrain model. *Journal of Hydrology* 404, 13–29.
- Flooded forest: Hess, L. L., Melack, J. M., Simonett, D. S. (1990). Radar detection of flooding beneath the forest canopy: a review. *International Journal of Remote Sensing* 11, 1313–1325.
- Depth: Cohen, S. et al. (2018). Estimating floodwater depths from flood inundation maps and topography. *Journal of the American Water Resources Association* 54, 847–858.
- Review: Schumann, G. J.-P., Moller, D. K. (2015). Microwave remote sensing of flood inundation. *Physics and Chemistry of the Earth* 83–84, 84–95.
- Copernicus Global Flood Monitoring: Salamon, P. et al. (2021). IGARSS 2021; [GFM technical information](https://global-flood.emergency.copernicus.eu/technical-information/glofas-gfm/).
- Kerala 2018: [ISRO flood inundation maps](https://www.isro.gov.in/Flood-Inundation-Kerala); [Geomatics, Natural Hazards and Risk (2019)](https://www.tandfonline.com/doi/full/10.1080/19475705.2018.1543212); [PLOS ONE (2020)](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0237324).
- Pakistan 2022: Roth, F. et al. (2023). [Sentinel-1-based analysis of the severe flood over Pakistan 2022](https://nhess.copernicus.org/articles/23/3305/2023/). *NHESS* 23, 3305–3317; [UNOSAT](https://unosat.org/products/3346).
- Valencia 2024: [Copernicus EMS (ESA)](https://www.esa.int/ESA_Multimedia/Images/2024/11/The_Copernicus_Emergency_Management_Service_monitors_the_floods_in_Valencia_Spain); [European Geographical Journal](https://eurogeojournal.eu/index.php/egj/article/view/897).
- Assam: [NRSC (ISRO), Flood Hazard Zonation Atlas of Assam, 1998–2023](https://www.nrsc.gov.in/nrscnew/assets/pdf/Flood_Hazard_Zonation_Atlas_of_Assam_using_multi_sensor_satellite_data1998_2023.pdf).
- Hands-on: [UN-SPIDER Recommended Practice: flood mapping with Sentinel-1 in Google Earth Engine](https://un-spider.org/advisory-support/recommended-practices/recommended-practice-google-earth-engine-flood-mapping).
- Sentinel-1: EU Copernicus programme / ESA.

All figures and the animation were made for this lecture.
