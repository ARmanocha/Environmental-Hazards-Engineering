# Coastal Erosion Monitoring with Remote Sensing — speaker notes

## 1. Coastal Erosion Monitoring with Remote Sensing

Shorelines move all the time: with tides, storms and seasons, and over years as sand is gained or lost. Satellites since 1984 let us measure the long-term trend for any coast on Earth. The strip at the bottom is a simulated coast with shorelines from several years around a harbour.

## 2. Use satellite images to find the shoreline, measure how fast it moves, and judge what that means for people and structures on the coast.

This is one of the most practical remote-sensing applications for civil engineers: shoreline-change rates feed directly into setback lines, coastal protection design and planning decisions.

## 3. Outline

Five parts: processes, extracting shorelines, measuring change, real coasts, and engineering practice.

## 4. Coastal erosion and why we monitor it

Part 1: Processes, causes, India’s coast, and what satellites add.

## 5. A beach is a sand budget

Waves arriving at an angle push sand along the shore: longshore drift. Anything that interrupts it, such as a harbour or groyne, changes the budget on both sides. On India's east coast the net drift is mostly northward, from about March to October; on the west coast it changes direction with the monsoon.

## 6. Why coasts erode

Natural and human causes usually act together. On many Indian coasts, harbours and sand mining matter more today than sea-level rise, but sea-level rise adds a slow, steady push landward everywhere.

## 7. India’s eroding coast

India's coastline was recently re-measured at about 11,099 km including islands, up from the old figure of 7,517 km, because more detailed maps capture more creeks and islands: the coastline paradox. The NCCR study covers the mainland coast. Percentages differ slightly between the report and press summaries depending on the coast length used.

## 8. Why satellites for coasts

The great strength is the time span: long records let us separate a real trend from seasonal and storm-driven swings.

## 9. Mapping the shoreline from space

Part 2: Shoreline indicators, satellites, water indices, tides and radar.

## 10. Which ‘shoreline’?

Boak and Turner (2005) list dozens of shoreline indicators. Mixing indicators between years, for example a vegetation line from an old map and a waterline from a satellite image, produces fake erosion or accretion.

## 11. Data for shoreline mapping

Most national and global studies combine Landsat for the long record with Sentinel-2 for recent detail. Survey of India toposheets and old air photos extend records further back, but bring larger errors.

## 12. Finding the water’s edge

This is the same thresholding idea as flood mapping (Lecture 7), applied to optical images. CoastSat (Vos et al., 2019) combines a classifier with a sub-pixel contour and reaches about half a pixel: around 15 m for Landsat and 5 m for Sentinel-2.

## 13. Tides move the waterline

The correction moves each waterline horizontally by the tide height divided by the beach slope. Beach slope can be measured in the field or estimated from the satellite waterlines themselves. Wave run-up adds a further offset on exposed beaches.

## 14. Radar for the monsoon coast

Sentinel-1 shorelines are noisier than optical ones on wave-exposed sandy beaches but work well on muddy, mangrove and tidal-flat coasts where optical water indices struggle.

## 15. Measuring shoreline change

Part 3: Transects and rates, uncertainty, structures, and elevation change.

## 16. Transects from a baseline

DSAS (Himmelstoss et al., USGS) runs in ArcGIS; free alternatives include CoastSat's own transect tools in Python and QGIS plugins. Transect spacing should match the detail you need; closer near structures.

## 17. Rates of shoreline change

Negative rates mean erosion (landward movement), positive accretion. EPR depends heavily on the two end dates: a storm just before the last image can make the whole trend look worse.

## 18. How sure is a rate?

Luijendijk et al. (2018) used ±0.5 m/yr as the threshold for calling a sandy beach eroding or accreting in their global Landsat study. Linear regression has its own confidence interval; DSAS reports it for each transect.

## 19. What a harbour does to the coast

Animation computed with the one-line model: a breakwater that stops all longshore drift. Sand piles up on the updrift side and the downdrift beach starves and erodes, and both effects spread further along the coast every year. This is the Puducherry story in Part 4.

## 20. The one-line model

The one-line model treats the beach as a single line whose position y changes with the gradient of longshore transport (Pelnard-Considère, 1956). The analytical solution for a structure that blocks all drift is shown; real harbours bypass some sand, and the diffusivity depends on wave height and sediment size.

## 21. Beyond the line: height and volume

Relative sea-level rise equals global sea-level rise plus local land subsidence. On sinking deltas such as parts of the Ganges–Brahmaputra and Godavari–Krishna, subsidence can exceed the global rate.

## 22. Case studies

Part 4: The world’s beaches, India’s coast, Puducherry and Satabhaya.

## 23. The world’s sandy beaches

The study ran on Google Earth Engine, which holds the whole Landsat archive. The same tools are free for students; CoastSat makes this practical for a single beach.

## 24. India’s coast, 1990–2018

Odisha showed the strongest accretion of any state in the same study, much of it near river mouths. Erosion and accretion often sit side by side along the same stretch of coast, exactly as around a harbour.

## 25. Puducherry: a harbour and a lost beach

Exactly the pattern of the one-line model and the animation: accretion updrift (south) and erosion downdrift (north). The restoration by the National Institute of Ocean Technology combined a submerged artificial reef with beach nourishment.

## 26. Satabhaya, Odisha: villages lost to the sea

Satabhaya has been called India's 'climate colony'. It shows the human side of shoreline-change numbers: resettled families lost both land and livelihoods.

## 27. Engineering practice

Part 5: Uses, coastal management, a workflow, limits and exercises.

## 28. Where engineers use shoreline change

A simple setback rule: rate of erosion times design life, plus a buffer for storms and sea-level rise. Exercise 4 works one example.

## 29. Managing an eroding coast

Puducherry used a hybrid of hard (submerged reef) and soft (nourishment). Satellite shorelines before and after are the standard way to judge which option works on a given coast.

## 30. A shoreline-change workflow

CoastSat downloads images, extracts shorelines with sub-pixel accuracy and computes time series on transects. A complete beach analysis is a realistic one-week student project.

## 31. Limits and good practice

Muddy and mangrove coasts, rocky shores and cliffs need different indicators and methods from sandy beaches.

## 32. Try these

Use: shift = tide height ÷ slope; EPR = NSM ÷ years; σ(rate) = √(σ₁² + σ₂²) ÷ years. In exercise 2 the baseline is on land, so a smaller distance means the shoreline moved landward.

## 33. Answers

Exercise 3 shows why long records matter: longer time spans shrink the rate uncertainty, which is why the 40-year Landsat archive is so valuable despite its coarser pixels.

## 34. Key points

The whole lecture in five lines.

## 35. References

Boak and Turner (2005) for shoreline indicators; Vos et al. (2019) and the CoastSat code for hands-on work; Dean and Dalrymple for the engineering background.

## 36. Thank you. Questions?

Credits and sources are on this slide and the references slide.
