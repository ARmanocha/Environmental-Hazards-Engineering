# Lecture 6: Land Subsidence Monitoring with InSAR

**Measuring sinking ground in cities, farmland and coasts** · presented by Akshay Raj Manocha

📄 **Slides:** [Land_Subsidence_InSAR_Akshay_Raj_Manocha.pdf](Land_Subsidence_InSAR_Akshay_Raj_Manocha.pdf) (33 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)
🛰️ **Animation:** [aquifer_compaction.html](animations/aquifer_compaction.html)

This lecture builds on Lectures [1](../01-SAR-Interferometry/) to [3](../03-InSAR-Theory/). It uses the same two-pass decomposition as [Lecture 4](../04-Landslide-Monitoring-InSAR/) and [Lecture 5](../05-Earthquake-Monitoring-InSAR/).

## What the lecture covers

1. **What land subsidence is and why it happens:** the scale of the problem and six causes (groundwater, oil and gas, mining, drained organic soils, compaction and loading, dissolution). It covers aquifer mechanics: elastic sand, and clay that compacts permanently below its previous lowest water level. It ends with what InSAR adds.
2. **Measuring subsidence with InSAR:** converting line of sight to vertical (v(up) ≈ v(LOS) ÷ cos θ) and why the bowl flanks need both passes. It shows vertical and east–west decomposition, and InSAR techniques with ground checks (GNSS, levelling, borehole extensometers, wells).
3. **Reading the results:** subsidence bowls in a city, time series against groundwater levels, skeletal storage (elastic and permanent), and differential settlement with angular distortion compared with Bjerrum's damage limits.
4. **Case studies:** Mexico City; Jakarta; Delhi National Capital Region; San Joaquin Valley, California; sinking cities worldwide, including Indian megacities and Tokyo.
5. **Engineering practice:** impacts on buildings, pipes, flooding, transport and water supply; slowing and stopping subsidence; limits and good practice; four exercises with answers; recap and references.

## The animation

`animations/aquifer_compaction.html` shows a cross-section of an aquifer system. A pump lowers the water level, the clay layers squeeze, and the houses sink with the ground. When pumping stops the water recovers, but the ground rises only a little. It runs live in the online deck. In the PDF it is a single still frame. To show it in class from this repository, download the file and open it in any web browser. It needs no internet connection.

## Folder contents

| Path | What it is |
|------|------------|
| `Land_Subsidence_InSAR_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `animations/aquifer_compaction.html` | The aquifer-compaction animation as a standalone web page |
| `figures/` | The figures used in the deck |
| `scripts/` | Python code that makes every figure |

## Remaking the figures

Requires Python 3 with `numpy`, `matplotlib` and `scipy`.

```bash
cd scripts && python3 figures.py
```

The figures are written to `scripts/figs/`. `geo.py` holds the Sentinel-1 line-of-sight geometry.

## About the data

- **Simulated** (labelled "Simulated data" on every figure): the city velocity map, the two-pass decomposition, the aquifer-compaction model, the groundwater and settlement time series, and the building settlement profile. They use Sentinel-1 geometry (incidence 39°).
- **Computed:** the exercise answers and the times for the simulated building to reach each damage limit.
- **Real:** the case-study numbers, from the sources below.

## Sources and credits

- Review: Galloway, D. L., Burbey, T. J. (2011). Review: regional land subsidence accompanying groundwater extraction. *Hydrogeology Journal* 19, 1459–1486.
- Global: Herrera-García, G. et al. (2021). Mapping the global threat of land subsidence. *Science* 371, 34–36.
- Mexico City: Cigna, F., Tapete, D. (2021). Present-day land subsidence rates, surface faulting hazard and risk in Mexico City with 2014–2020 Sentinel-1 IW InSAR. *Remote Sensing of Environment*. Chaussard, E. et al. (2021). Over a century of sinking in Mexico City: no hope for significant elevation and storage capacity recovery. *JGR Solid Earth* 126.
- Jakarta: Abidin, H. Z. et al. (2011). Land subsidence of Jakarta (Indonesia) and its relation with urban development. *Natural Hazards* 59, 1753–1771; [Proc. IAHS 372 (2015)](https://piahs.copernicus.org/articles/372/115/2015/).
- Delhi: Garg, S., Motagh, M., Indu, J., Karanam, V. (2022). Tracking hidden crisis in India's capital from space: implications of unsustainable groundwater use. *Scientific Reports* 12. Kumar et al. (2025). [InSAR reveals recovery of stressed aquifer systems in parts of Delhi, India](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024WR037704). *Water Resources Research*.
- Indian megacities: [Building damage risk in sinking Indian megacities](https://www.nature.com/articles/s41893-025-01663-0), *Nature Sustainability* (2025).
- California: Poland, J. F. et al. (1975). Land subsidence in the San Joaquin Valley, California, as of 1972. USGS Professional Paper 437-H; [NASA JPL (2015)](https://www.jpl.nasa.gov/news/nasa-california-drought-causing-valley-land-to-sink/).
- Tokyo and Osaka: [IGES, Land subsidence and groundwater management in Tokyo](https://www.iges.or.jp/system/files/publication_documents/pub/peer/1208/IRES_Vol.6-2_403.pdf).
- Damage limits: Bjerrum, L. (1963). Allowable settlement of structures. Proc. European Conference on Soil Mechanics and Foundation Engineering, Wiesbaden, vol. 2.
- Sentinel-1: EU Copernicus programme / ESA.

All figures and the animation were made for this lecture.
