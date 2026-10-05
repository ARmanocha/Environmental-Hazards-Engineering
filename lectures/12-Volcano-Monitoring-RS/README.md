# Lecture 12: Volcano Monitoring with Remote Sensing

**Watching the ground swell, the lava glow and the gas and ash spread, from space** · presented by Akshay Raj Manocha

📄 **Slides:** [Volcano_Monitoring_RS_Akshay_Raj_Manocha.pdf](Volcano_Monitoring_RS_Akshay_Raj_Manocha.pdf) (36 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)
🛰️ **Animation:** [magma_inflation.html](animations/magma_inflation.html)

This lecture brings together tools from across the course:
- InSAR from Lectures 1 to 6, with the Okada model of [Lecture 5](../05-Earthquake-Monitoring-InSAR/).
- Thermal infrared from [Lecture 9](../09-Wildfire-Monitoring-RS/).
- The volcanic tsunami of [Lecture 11](../11-Tsunami-Monitoring-RS/).

The Kīlauea case study links to [Practical 1](../../practicals/01-InSAR-Processing-with-SNAP/).

## What the lecture covers

1. **Volcanoes and why we monitor them:**
   - The hazards: lava flows, pyroclastic flows, ash fall, lahars, gases, and collapse and tsunamis.
   - The four warning signs of unrest, and which can be seen from space.
   - India's volcano, Barren Island.
   - Which satellite measures what, including NISAR (NASA–ISRO, 2025).
2. **The ground moves:**
   - The Mogi magma-chamber model and its interferogram.
   - InSAR at more than 1,000 volcanoes (COMET LiCSAR).
   - The animation.
   - A dyke under a town, using the Okada model, linked to Grindavík 2023.
   - Combining uplift, heat and gas records.
3. **Heat and lava:** Planck's law and short-wave infrared images of lava; the MODVOLC and MIROVA hot-spot systems; lava volume from before-and-after elevation models.
4. **Gas and ash:** sulfur dioxide from TROPOMI on Sentinel-5P; the split-window test for ash; ash and aircraft, plume heights and the Volcanic Ash Advisory Centres.
5. **Case studies:** Kīlauea 2018, Eyjafjallajökull 2010, La Palma 2021 and Grindavík 2023–24.
6. **Engineering practice:**
   - Where engineers use volcano data: hazard zoning, lahar paths, ash loads on roofs, lava barriers, lifelines and geothermal energy.
   - An 8-step monitoring workflow.
   - Limits and good practice.
   - Four exercises with answers, a recap and references.

## The animation

`animations/magma_inflation.html` shows magma flowing into a chamber 4 km deep, up to 20 million m³.

- **Left:** the ascending Sentinel-1 interferogram, computed live from the Mogi model. It gains one fringe for every 2.8 cm of movement towards the satellite.
- **Right:** a cross-section shows the ground rising, greatly exaggerated.
- **Eruption:** magma then leaves the chamber, and the ground and the fringes go back down.
- **Readouts:** the volume added, the uplift at the centre and the number of fringes.

It runs live in the online deck. In the PDF it is a single still frame. To show it in class from this repository, download the file and open it in any web browser. It needs no internet connection.

## Folder contents

| Path | What it is |
|------|------------|
| `Volcano_Monitoring_RS_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `animations/magma_inflation.html` | The magma-chamber animation as a standalone web page |
| `figures/` | The figures used in the deck |
| `scripts/` | Python code that makes every figure |

## Remaking the figures

Requires Python 3 with `numpy`, `matplotlib` and `scipy`.

```bash
cd scripts && python3 figures.py
```

The figures are written to `scripts/figs/`, together with `stats.json`, which holds the numbers quoted on the slides. `okada.py` is the same Okada (1985) model used in Lecture 5. Run it on its own to check it against the test values in Okada's paper.

`figures.py` contains small functions that students can reuse for the exercises:
- `mogi()`: the Mogi point source;
- `dyke_enu()`: a vertical dyke from Okada's tensile solution;
- `los()`: projects ground movement onto the Sentinel-1 line of sight;
- `planck()`: Planck's law.

It also shows how to convert Dobson units to SO₂ mass.

## About the data

- **Computed:**
  - The magma-chamber deformation and interferogram (Mogi, 1958).
  - The dyke deformation (Okada, 1985).
  - The Planck curves.
  - The animation and the exercise answers.
- **Simulated** (labelled "Simulated data" on every figure):
  - The combined uplift, heat and SO₂ records.
  - The Sentinel-2 lava scene.
  - The before-and-after elevation models.
  - The SO₂ plume.
  - The ash scene.
- **Cover strip:** computed fringes over a simulated volcano.
- **Real:** the case-study numbers and the descriptions of satellites, systems and services, from the sources below.

## Sources and credits

- Deformation models:
  - Mogi, K. (1958). Relations between the eruptions of various volcanoes and the deformations of the ground surfaces around them. *Bulletin of the Earthquake Research Institute* 36, 99–134.
  - Okada, Y. (1985). *Bulletin of the Seismological Society of America* 75, 1135–1154.
- InSAR at volcanoes:
  - Biggs, J. et al. (2014). [Global link between deformation and volcanic eruption quantified by satellite imagery](https://www.nature.com/articles/ncomms4471). *Nature Communications* 5, 3471.
  - Lazecký, M. et al. (2020). LiCSAR. *Remote Sensing* 12, 2430; [COMET-LiCS portal](https://comet.nerc.ac.uk/comet-lics-portal/).
- Thermal monitoring:
  - Wright, R. et al. (2004). MODVOLC. *Journal of Volcanology and Geothermal Research* 135, 29–49.
  - Coppola, D. et al. (2016). MIROVA. *Geological Society, London, Special Publications* 426, 181–205.
- Sulfur dioxide: Theys, N. et al. (2019). [Global monitoring of volcanic SO₂ degassing with unprecedented resolution from TROPOMI](https://www.nature.com/articles/s41598-019-39279-y). *Scientific Reports* 9, 2643.
- Pinatubo: [USGS Fact Sheet 113-97](https://pubs.usgs.gov/fs/1997/fs113-97/).
- Ash:
  - Prata, A. J. (1989). *International Journal of Remote Sensing* 10, 751–761.
  - Proud, S. R. et al. (2022). [The January 2022 eruption of Hunga Tonga-Hunga Ha'apai volcano reached the mesosphere](https://www.science.org/doi/10.1126/science.abo4076). *Science* 378, 554–557.
  - [Volcanic Ash Advisory Centres](https://en.wikipedia.org/wiki/Volcanic_Ash_Advisory_Center).
- Ash loads on buildings:
  - Spence, R. J. S. et al. (2005). [Residential building and occupant vulnerability to tephra fall](https://nhess.copernicus.org/articles/5/477/2005/nhess-5-477-2005.pdf). *Natural Hazards and Earth System Sciences* 5, 477–494.
  - [USGS volcanic ash: roof loading](https://volcanoes.usgs.gov/volcanic_ash/roof_loading.html).
- Global exposure: Loughlin, S. C. et al., eds. (2015). *Global Volcanic Hazards and Risk*. Cambridge University Press.
- India:
  - Barren Island: Global Volcanism Program; [Down To Earth](https://www.downtoearth.org.in/science-technology/barren-island-volcanos-activity-is-purely-due-to-magmatic-processes-hetu-sheth); [Insights on India (September 2025)](https://www.insightsonindia.com/2025/09/23/barren-island-volcano/).
  - NISAR: [NASA mission overview](https://science.nasa.gov/mission/nisar/mission-overview/).
- Kīlauea 2018: [USGS Hawaiian Volcano Observatory](https://usgs.gov/volcanoes/kilauea/science/2018-lower-east-rift-zone-eruption-and-summit-collapse-kilauea); [Hawai‘i County](https://recovery.hawaiicounty.gov/resources/2018-eruption).
- Eyjafjallajökull 2010: IATA and Eurocontrol figures, summarised in [Air travel disruption after the 2010 Eyjafjallajökull eruption](https://en.wikipedia.org/wiki/Air_travel_disruption_after_the_2010_Eyjafjallaj%C3%B6kull_eruption).
- La Palma 2021: [Copernicus EMS activation EMSN119](https://mapping.emergency.copernicus.eu/activations/EMSN119/); [ESA](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/La_Palma_volcano_How_satellites_help_us_monitor_eruptions); [Scientific Reports (2024)](https://www.nature.com/articles/s41598-023-50982-9).
- Grindavík 2023–24: Icelandic Meteorological Office; [Natural Hazards (2026)](https://link.springer.com/article/10.1007/s11069-026-08084-y); [Reykjavík Grapevine](https://grapevine.is/news/2024/01/14/eruption-has-begun-north-of-grindavik/).

All figures and the animation were made for this lecture.
