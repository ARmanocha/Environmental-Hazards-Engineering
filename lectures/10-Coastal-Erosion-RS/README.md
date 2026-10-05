# Lecture 10: Coastal Erosion Monitoring with Remote Sensing

**Tracking moving shorelines with forty years of satellite images** · presented by Akshay Raj Manocha

📄 **Slides:** [Coastal_Erosion_RS_Akshay_Raj_Manocha.pdf](Coastal_Erosion_RS_Akshay_Raj_Manocha.pdf) (36 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)
🛰️ **Animation:** [harbour_shoreline.html](animations/harbour_shoreline.html)

This lecture uses optical and radar satellites to map shorelines and measure how fast they move. It links to [Lecture 7](../07-Flood-Mapping-SAR/) on separating water from land, and to [Lecture 6](../06-Land-Subsidence-InSAR/) on sinking deltas.

## What the lecture covers

1. **Coastal erosion and why we monitor it:** a beach as a sand budget; short-term swings versus the long-term trend; six causes of erosion (waves and storms, sea-level rise, less river sand, coastal structures, sinking deltas, loss of mangroves); India's eroding coast; what satellites add.
2. **Mapping the shoreline from space:**
   - Which "shoreline": the waterline, a datum shoreline corrected to mean sea level, or the vegetation line.
   - The data: Landsat since 1984, Sentinel-2, Sentinel-1 radar, very-high-resolution images, drones and lidar, old maps.
   - Finding the water's edge with MNDWI and an automatic (Otsu) threshold.
   - Correcting for the tide: shift = tide height ÷ beach slope.
   - Radar for the cloudy monsoon coast.
3. **Measuring shoreline change:**
   - Transects from a baseline, as in DSAS.
   - Three rates: net shoreline movement (NSM), end-point rate (EPR) and linear regression rate (LRR).
   - How sure a rate is, and when to call a shoreline "stable".
   - What a harbour does to the coast: the one-line model and the animation.
   - Beyond the line: beach height and volume from drones, lidar, stereo images and ICESat-2.
4. **Case studies:**
   - The world's sandy beaches, 1984–2016 (Luijendijk et al., 2018).
   - India's national shoreline assessment, 1990–2018 (NCCR).
   - Puducherry: a harbour, a lost beach and its restoration.
   - Satabhaya, Odisha: villages lost to the sea.
5. **Engineering practice:** setback and hazard lines, harbour design, coastal protection, checking projects, infrastructure and disaster response; hard, soft and nature-based protection and retreat; an 8-step workflow; limits and good practice; four exercises with answers; recap and references.

## The animation

`animations/harbour_shoreline.html` shows 30 years of shoreline change beside a breakwater that blocks all longshore drift. It uses the Pelnard-Considère one-line model. Sand piles up on the updrift side and the downdrift beach erodes, and both effects spread further along the coast every year. It runs live in the online deck. In the PDF it is a single still frame. To show it in class from this repository, download the file and open it in any web browser. It needs no internet connection.

## Folder contents

| Path | What it is |
|------|------------|
| `Coastal_Erosion_RS_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `animations/harbour_shoreline.html` | The breakwater animation as a standalone web page |
| `figures/` | The figures used in the deck |
| `scripts/` | Python code that makes every figure |

## Remaking the figures

Requires Python 3 with `numpy`, `matplotlib` and `scipy`.

```bash
cd scripts && python3 figures.py
```

The figures are written to `scripts/figs/`, together with `stats.json`, which holds the numbers quoted on the slides. The analytical one-line model is a small function, `oneline()`. The Otsu threshold, the tide correction and the three rates (NSM, EPR and LRR) are short, commented steps. Students can adapt them for real CoastSat shorelines and for the exercises.

## About the data

- **Computed from the one-line model:** the breakwater figure, the animation, and the exercise answers.
- **Simulated** (labelled "Simulated data" on every figure): the coastal scene and its waterline, the shorelines and transects, the rates along the coast, the tide-corrected transect, and the cover strip.
- **Schematic:** the beach profile shows typical shoreline indicators, not a survey.
- **Real:** the case-study numbers and the descriptions of satellites and methods, from the sources below.

## Sources and credits

- Shoreline indicators: Boak, E. H., Turner, I. L. (2005). Shoreline definition and detection: a review. *Journal of Coastal Research* 21, 688–703.
- MNDWI: Xu, H. (2006). *International Journal of Remote Sensing* 27, 3025–3033.
- CoastSat: Vos, K. et al. (2019). *Environmental Modelling & Software* 122, 104528; code at [github.com/kvos/CoastSat](https://github.com/kvos/CoastSat).
- DSAS: Himmelstoss, E. A. et al. (2021). Digital Shoreline Analysis System (DSAS) version 5.1 user guide. U.S. Geological Survey Open-File Report 2021–1091.
- One-line model: Pelnard-Considère, R. (1956). 4th Journées de l'Hydraulique, Paris; Dean, R. G., Dalrymple, R. A. (2002). *Coastal Processes with Engineering Applications*. Cambridge University Press.
- Sea-level rise: IPCC (2021). AR6 Working Group I, Chapter 9.
- Global beaches: Luijendijk, A. et al. (2018). [The state of the world's beaches](https://www.nature.com/articles/s41598-018-24630-6). *Scientific Reports* 8, 6641.
- India:
  - NCCR (2018). [National Assessment of Shoreline Changes along Indian Coast](https://www.indiaspend.com/wp-content/uploads/2018/11/National-Assessment-of-Shoreline-Changes-NCCR-report.pdf). Ministry of Earth Sciences.
  - Reported by [Down To Earth](https://www.downtoearth.org.in/environment/a-third-of-india-s-coastline-underwent-erosion-in-28-years-bengal-worst-affected-78514) and PIB.
  - The revised coastline length: [Insights on India](https://www.insightsonindia.com/2025/05/26/updated-indias-coastline-length/).
  - The CRZ hazard line: [Vajiram & Ravi](https://vajiramandravi.com/current-affairs/sea-level-rise-indias-eroding-coast/).
- Puducherry: [Frontiers in Marine Science (2024)](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2024.1426627/full), on the hybrid beach restoration; [Earth Journalism Network](https://earthjournalism.net/stories/a-disappearing-beach-in-eastern-india-comes-back-to-life); NIOT.
- Satabhaya: [Down To Earth](https://www.downtoearth.org.in/climate-change/environment-in-elections-sea-erosion-is-key-election-issue-in-odisha-s-satabhaya-95707); [Eco-Business](https://www.eco-business.com/news/resettled-not-rehabilitated-inside-indias-climate-colony/); CEEW.

All figures and the animation were made for this lecture.
