# Lecture 11: Tsunami Monitoring with Remote Sensing

**Detecting the wave at sea, warning the coast, and mapping what it leaves behind** · presented by Akshay Raj Manocha

📄 **Slides:** [Tsunami_Monitoring_RS_Akshay_Raj_Manocha.pdf](Tsunami_Monitoring_RS_Akshay_Raj_Manocha.pdf) (40 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)
🛰️ **Animation:** [tsunami_crossing.html](animations/tsunami_crossing.html)

This lecture combines ocean sensors, GNSS, satellite altimetry, the ionosphere, and optical and radar images. It uses the Okada fault model from [Lecture 5](../05-Earthquake-Monitoring-InSAR/). Its radar damage maps build on the coherence ideas of Lectures 1 to 3, and its water mapping links to [Lecture 7](../07-Flood-Mapping-SAR/).

## What the lecture covers

1. **Tsunamis and why we monitor them:**
   - The four causes: earthquakes, landslides, volcanoes and weather.
   - Speed = √(g × depth), and Green's law for the growth in height near the coast.
   - How a megathrust earthquake lifts the seafloor (the Okada model).
   - India's threat from the Andaman–Sumatra and Makran subduction zones.
   - What is monitored before, during and after a tsunami.
2. **Detecting a tsunami at sea:**
   - The warning chain, and India's Tsunami Early Warning Centre at INCOIS.
   - GNSS for measuring great earthquakes quickly.
   - Bottom-pressure sensors (DART).
   - Satellite altimetry, from Jason-1 in 2004 to SWOT in 2025.
   - GNSS detection of tsunamis in the ionosphere (NASA's GUARDIAN).
   - The animation, and travel-time maps.
3. **Mapping what it leaves behind:** optical before-and-after images, radar coherence damage maps, inundation distance, run-up height and flow depth, and land that rose or sank.
4. **Preparing for the next one:** why elevation models matter for inundation maps; hazard and evacuation maps; UNESCO-IOC Tsunami Ready communities in Odisha.
5. **Case studies:** Indian Ocean 2004, Tōhoku 2011, Palu 2018 and Hunga Tonga–Hunga Ha'apai 2022.
6. **Engineering practice:**
   - Where engineers use tsunami data: critical facilities, ports, vertical evacuation, design loads, lifelines and land-use planning.
   - An 8-step hazard workflow.
   - Limits and good practice.
   - Four exercises with answers, a recap and references.

## The animation

`animations/tsunami_crossing.html` follows a tsunami from an earthquake across 4000 m of ocean, over the continental slope and shelf, to a tide gauge on the coast.

- **Speed and height:** the wave moves at √(g × depth) and its height follows Green's law.
- **Readouts:** the time, the depth under the crest, the speed and the height are shown live.
- **Detections:** a DART buoy detects the wave, and a satellite altimeter measures it as it passes overhead.
- **On the shelf:** the wave slows to about 25 km/h and grows to about 2.7 m, reaching the coast nearly three hours after the earthquake.
- **Scales:** wave heights are greatly exaggerated, and depths are drawn on a square-root scale so that the shelf can be seen.

It runs live in the online deck. In the PDF it is a single still frame. To show it in class from this repository, download the file and open it in any web browser. It needs no internet connection.

## Folder contents

| Path | What it is |
|------|------------|
| `Tsunami_Monitoring_RS_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `animations/tsunami_crossing.html` | The tsunami animation as a standalone web page |
| `figures/` | The figures used in the deck |
| `scripts/` | Python code that makes every figure |

## Remaking the figures

Requires Python 3 with `numpy`, `matplotlib` and `scipy`.

```bash
cd scripts && python3 figures.py
```

The figures are written to `scripts/figs/`, together with `stats.json`, which holds the numbers quoted on the slides. It takes a few seconds. `okada.py` is the same Okada (1985) fault model used in Lecture 5. Run it on its own to check it against the test values in Okada's paper.

`figures.py` also contains a small tsunami model that students can experiment with. It solves the linear long-wave equations on a 4 km grid over a simulated ocean basin. The earthquake's seafloor uplift starts the wave, and the model records arrival times and wave records at chosen points.

## About the data

- **Computed:**
  - The wave-speed and Green's law curves.
  - The seafloor uplift: Okada model, a thrust fault 320 km long with 8 m of slip, about Mw 8.7.
  - The animation and the exercise answers.
- **Computed on a simulated basin:** the ocean basin is invented, but the tsunami crossing it is computed with the long-wave equations. The travel-time map, the cover strip and the sea surface in the altimeter figure come from this model.
- **Simulated** (labelled "Simulated data" on every figure):
  - The bottom-pressure record.
  - The altimeter measurements.
  - The ionosphere signals.
  - The radar coherence and damage scene.
  - The coastal elevation profiles.
- **Schematic:** the run-up diagram and the ionosphere sketch.
- **Real:** the case-study numbers and the descriptions of sensors, satellites and services, from the sources below.

## Sources and credits

- Fault model: Okada, Y. (1985). Surface deformation due to shear and tensile faults in a half-space. *Bulletin of the Seismological Society of America* 75, 1135–1154.
- Warning systems: Bernard, E., Titov, V. (2015). [Evolution of tsunami warning systems and products](https://royalsocietypublishing.org/rsta/article/373/2053/20140371/114943/Evolution-of-tsunami-warning-systems-and). *Philosophical Transactions of the Royal Society A* 373, 20140371.
- DART: NOAA National Data Buoy Center, [DART description](https://www.ndbc.noaa.gov/dart/brief.shtml).
- India:
  - INCOIS, [Indian Tsunami Early Warning Centre user guide](https://tsunami.incois.gov.in/itews/web/NTWC-Userguide.pdf).
  - 2004 figures from the Government of India.
  - 1945 Makran tsunami: [UNESCO (2015)](https://unesdoc.unesco.org/ark:/48223/pf0000232549).
  - Tsunami Ready in Odisha: [Mongabay India (2020)](https://india.mongabay.com/2020/08/indias-first-two-tsunami-ready-villages/) and [ANI (December 2024)](https://www.aninews.in/news/national/general-news/odishas-26-villages-get-recognition-as-tsunami-ready-by-intergovernmental-oceanographic-commission-of-unesco20241222060700/).
- 2004 Indian Ocean:
  - [EERI Special Earthquake Report (2005)](https://www.iitk.ac.in/nicee/RP/2005_SumatraEQ_EERI.pdf).
  - Ablain, M. et al. (2006). [High resolution altimetry reveals new characteristics of the December 2004 Indian Ocean tsunami](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2006GL027533). *Geophysical Research Letters* 33, L21602.
  - Meltzner, A. J. et al. (2006). [Uplift and subsidence associated with the great Aceh-Andaman earthquake of 2004](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2005JB003891). *Journal of Geophysical Research* 111, B02407.
- 2011 Tōhoku:
  - Ozaki, T. (2011). [Outline of the 2011 off the Pacific coast of Tohoku Earthquake (Mw 9.0): tsunami warnings/advisories and observations](https://link.springer.com/article/10.5047/eps.2011.06.029). *Earth, Planets and Space* 63, 827–830.
  - Mori, N., Takahashi, T. et al. (2012). *Coastal Engineering Journal* 54, 1250001.
  - Japan National Police Agency figures, reported by [nippon.com](https://www.nippon.com/en/features/h00004/).
- 2018 Palu: NASA JPL, [ARIA damage maps](https://www.jpl.nasa.gov/news/nasas-aria-maps-indonesia-quake-tsunami-damage/); Carvajal, M. et al. (2019). Nearly instantaneous tsunamis following the Mw 7.5 2018 Palu earthquake. *Geophysical Research Letters* 46.
- 2022 Hunga Tonga: [NOAA NCEI](https://www.ncei.noaa.gov/news/january-15-2022-tonga-volcanic-eruption-and-tsunami); Omira, R. et al. (2022). [Global Tonga tsunami explained by a fast-moving atmospheric source](https://www.nature.com/articles/s41586-022-04926-4). *Nature* 609, 734–740.
- 2025 Kamchatka:
  - NASA, [SWOT satellite measures tsunami](https://www.nasa.gov/missions/swot/us-french-swot-satellite-measures-tsunami-after-massive-quake/).
  - Sepúlveda, I. et al. (2026). [SWOT detects dispersive tsunami tied to a near-trench source in the 2025 Kamchatka earthquake](https://www.science.org/doi/10.1126/science.aeb8634). *Science*.
  - NASA JPL, [GUARDIAN tsunami detection](https://www.jpl.nasa.gov/news/nasas-guardian-tsunami-detection-tech-catches-wave-in-real-time/) (September 2025).

All figures and the animation were made for this lecture.
