# Lecture 8: Drought Monitoring with Remote Sensing

**Watching rain, crops, soil and groundwater dry out from space** · presented by Akshay Raj Manocha

📄 **Slides:** [Drought_Monitoring_RS_Akshay_Raj_Manocha.pdf](Drought_Monitoring_RS_Akshay_Raj_Manocha.pdf) (35 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)
🛰️ **Animation:** [drought_propagation.html](animations/drought_propagation.html)

This lecture goes beyond radar to optical, thermal, microwave and gravity satellites. Its California case links to [Lecture 6](../06-Land-Subsidence-InSAR/) on land subsidence.

## What the lecture covers

1. **Drought and why we monitor it:** a slow, relative, wide-area hazard; meteorological, agricultural, hydrological and groundwater drought; how a drought spreads through the water cycle; what satellites add.
2. **What satellites measure:**
   - Rainfall (CHIRPS, GPM IMERG, INSAT-3D).
   - Vegetation: NDVI from red and near-infrared reflectance.
   - Land surface temperature and evapotranspiration.
   - Soil moisture (SMAP, SMOS, Sentinel-1).
   - Groundwater from gravity (GRACE and GRACE-FO).
   - A table matching satellites to each part of a drought.
3. **Drought indices:** SPI (rainfall), VCI (greenness against its own history), TCI and VHI (greenness and temperature), and which index suits which kind of drought.
4. **Case studies and services:**
   - Marathwada, Maharashtra (2015–16), including the Latur water train.
   - Horn of Africa (2020–2023).
   - California's Central Valley (2012–2016), with groundwater loss measured by GRACE.
   - Europe (2022).
   - Who monitors drought: IMD and NADAMS (MNCFC) in India, the Copernicus European and Global Drought Observatories, FEWS NET, and the US Drought Monitor.
5. **Engineering practice:** reservoir operation, water supply planning, irrigation, insurance and relief, energy and groundwater; an 8-step monitoring workflow; limits and good practice; four exercises with answers; recap and references.

## The animation

`animations/drought_propagation.html` follows one failed monsoon through a simple simulated water balance. Rain recovers the next year, but soil moisture, river flow and groundwater each stay low for longer. It runs live in the online deck. In the PDF it is a single still frame. To show it in class from this repository, download the file and open it in any web browser. It needs no internet connection.

## Folder contents

| Path | What it is |
|------|------------|
| `Drought_Monitoring_RS_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `animations/drought_propagation.html` | The drought-propagation animation as a standalone web page |
| `figures/` | The figures used in the deck |
| `scripts/` | Python code that makes every figure |

## Remaking the figures

Requires Python 3 with `numpy`, `matplotlib` and `scipy`.

```bash
cd scripts && python3 figures.py
```

The figures are written to `scripts/figs/`. The script contains small, readable versions of the SPI calculation (gamma fit, then a standard normal score, for each calendar month) and the VCI calculation. Students can adapt them for real CHIRPS and MODIS data.

## About the data

- **Simulated** (labelled "Simulated data" on every figure): the monsoon rainfall and SPI series, the NDVI and VCI curves, the VCI, TCI and VHI maps, the water-storage series, and the cover strip.
- **Schematic:** the reflectance spectra show typical shapes, not measurements.
- **Computed:** the exercise answers.
- **Real:** the case-study numbers and the descriptions of satellites and services, from the sources below.

## Sources and credits

- Drought types: Wilhite, D. A., Glantz, M. H. (1985). Understanding the drought phenomenon: the role of definitions. *Water International* 10, 111–120.
- SPI: McKee, T. B., Doesken, N. J., Kleist, J. (1993). The relationship of drought frequency and duration to time scales. Proc. 8th Conference on Applied Climatology, 179–184.
- SPEI: Vicente-Serrano, S. M., Beguería, S., López-Moreno, J. I. (2010). *Journal of Climate* 23, 1696–1718.
- NDVI: Tucker, C. J. (1979). Red and photographic infrared linear combinations for monitoring vegetation. *Remote Sensing of Environment* 8, 127–150.
- VCI, TCI and VHI: Kogan, F. N. (1995). Application of vegetation index and brightness temperature for drought detection. *Advances in Space Research* 15(11), 91–100.
- Evaporative Stress Index: Anderson, M. C. et al. (2011). *Journal of Climate* 24, 2025–2044.
- CHIRPS: Funk, C. et al. (2015). *Scientific Data* 2, 150066.
- GRACE: Tapley, B. D. et al. (2004). *Science* 305, 503–505.
- India: Government of India (2016, updated 2020). [Manual for Drought Management](https://nidm.gov.in/pdf/manuals/drought_manual.pdf); NADAMS, Mahalanobis National Crop Forecast Centre.
- Marathwada and the Latur water train (April 2016): news reports ([ABP Live](https://abplive.in/india-news/first-train-with-5-lakh-litres-of-potable-water-reaches-drought-latur-320241), [Al Jazeera](https://www.aljazeera.com/gallery/2016/4/14/drought-suicide-and-indias-water-train)); Indian Railways.
- Horn of Africa: [WMO](https://wmo.int/media/news/catastrophic-consequences-of-horn-of-africa-drought-will-continue-2023); World Weather Attribution (2023), reported by [Carbon Brief](https://www.carbonbrief.org/deadly-drought-in-horn-of-africa-would-not-have-happened-without-climate-change).
- California: Xiao, M. et al. (2017). [How much groundwater did California's Central Valley lose during the 2012–2016 drought?](https://agupubs.onlinelibrary.wiley.com/doi/10.1002/2017GL073333) *Geophysical Research Letters* 44; [NASA JPL (2015)](https://www.jpl.nasa.gov/news/nasa-california-drought-causing-valley-land-to-sink/).
- Europe 2022: European Commission Joint Research Centre, European Drought Observatory (reported by [CBS News](https://www.cbsnews.com/news/europe-drought-worst-in-500-years-report/) and others).
- Further reading: WMO and GWP (2016). [Handbook of Drought Indicators and Indices](https://www.droughtmanagement.info/literature/GWP_Handbook_of_Drought_Indicators_and_Indices_2016.pdf).

All figures and the animation were made for this lecture.
