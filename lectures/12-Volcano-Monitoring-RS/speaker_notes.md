# Volcano Monitoring with Remote Sensing — speaker notes

## 1. Volcano Monitoring with Remote Sensing

Most of the world's volcanoes have no instruments on the ground, so satellites are often the first to notice that one is waking up. The strip at the bottom shows computed interferogram fringes over a simulated volcano whose magma chamber is filling: each colour cycle is 2.8 cm of movement towards the satellite.

## 2. Use satellites to spot a volcano waking up, follow an eruption as it happens, and measure what it leaves behind.

This lecture brings together almost every tool from the course: InSAR from Lectures 1 to 6, thermal infrared from Lecture 9, and change detection throughout.

## 3. Outline

Six parts: the hazard, ground deformation, heat, gas and ash, real eruptions, and engineering practice.

## 4. Volcanoes and why we monitor them

Part 1: Hazards, warning signs, India’s volcano, and which satellite sees what.

## 5. What volcanoes threaten

About 800 million people live within 100 km of an active volcano, in 86 countries (Loughlin et al., 2015). The Global Volcanism Program counts between about 60 and 90 volcanoes in eruption in a typical year.

## 6. Signs that magma is moving

Three of the four classic signs of unrest can be seen from space. Earthquakes need seismometers on the ground, which is why satellite and ground monitoring work together. Not all deformation leads to eruption: magma often stalls underground.

## 7. India’s volcano: Barren Island

Barren Island has erupted many times since 1991, including 1994 to 1995, 2005 to 2007, 2008 to 2010, 2013 to 2014, 2017 and 2022, with two small eruptions reported on 13 and 20 September 2025. Ash from eruptions elsewhere in Asia, for example Indonesia, can also affect flights over India.

## 8. Which satellite sees what

Radar for deformation, infrared for heat, ultraviolet for sulfur dioxide, and geostationary weather satellites for ash: each signal has its own satellites and its own repeat time. NISAR combines NASA's L-band and ISRO's S-band radars and covers the globe every 12 days.

## 9. The ground moves

Part 2: Magma chambers and dykes, InSAR at every volcano, and combining signals.

## 10. A swelling magma chamber

The Mogi model treats the magma chamber as a small sphere under pressure in an elastic half-space. It is simple but fits many volcanoes surprisingly well. Deeper sources make a smaller, wider bulge, so the shape of the deformation tells us where the magma is. The ground also moves outwards from the centre, which the ascending radar sees, making the fringes slightly lopsided.

## 11. InSAR at every volcano

The COMET LiCSAR system makes interferograms automatically for over a thousand volcanoes as each new Sentinel-1 image arrives, and the products are free to download. Atmospheric water vapour is the main source of false signals at tall volcanoes, because the radar path through the air changes with height. Long time series and weather-model corrections reduce it.

## 12. Fringes appear as magma arrives

Animation computed with the Mogi model: magma flows into a chamber 4 km deep, up to 20 million cubic metres. The interferogram on the left gains a fringe for every 2.8 cm of movement towards an ascending Sentinel-1 pass; the cross-section shows the ground rising, greatly exaggerated. Then the volcano erupts, magma leaves, and the ground and fringes go back down. Counting fringes is a quick way to estimate how much the ground moved.

## 13. Magma on the move: a dyke

Not all magma stays in a chamber. A dyke is a thin, nearly vertical sheet of magma that splits the crust. Near the dyke the fringes become too dense to count, and the radar loses coherence, shown in grey. In Iceland, interferograms produced within a day showed a subsiding graben running right through Grindavík, which guided the evacuation and later the building of lava barriers.

## 14. Combine the signals

Volcano observatories combine satellite records with seismometers, ground GNSS and field gas measurements before raising an alert level. The pattern here, accelerating uplift and then a burst of heat and gas, is common but not universal; some eruptions give only days of warning, as at La Palma in 2021.

## 15. Heat and lava

Part 3: Thermal infrared, hot-spot systems, and lava volumes from elevation models.

## 16. Seeing hot lava

Wien's law: peak wavelength in micrometres is about 2898 divided by temperature in kelvin. In a Sentinel-2 image with SWIR 2, SWIR 1 and near-infrared as red, green and blue, active lava glows yellow and orange while vegetation looks green. The same physics was used for wildfire detection in Lecture 9.

## 17. Hot-spot systems

These systems run without human input and publish results within hours of each satellite pass, so a small volcano anywhere can trigger an alert. At remote volcanoes such as Barren Island, they may be the only regular record of activity. Cloud and thick plumes can hide hot spots, so a missing alert does not mean all is quiet.

## 18. How much lava? Subtract elevation models

The true volume of the simulated flow is 8.0 million cubic metres; the estimate is close because the DEM errors partly cancel and thin changes below 2.5 m are ignored. Dividing volume by eruption time gives the average eruption rate, which helps forecast how far future flows may travel.

## 19. Gas and ash

Part 4: Sulfur dioxide from space, finding ash, and keeping aircraft safe.

## 20. Sulfur dioxide from space

TROPOMI has 3.5 by 5.5 km pixels since August 2019, fine enough to see small degassing plumes almost daily (Theys et al., 2019). Carbon dioxide from volcanoes is much harder to measure from space because the atmosphere already contains so much of it. Pinatubo's sulfate aerosols lowered global temperatures for about two years (USGS).

## 21. Finding ash: the split-window test

The test fails when the ash cloud is thick and opaque, when it is mixed with ice, or over very cold or hot surfaces, so analysts combine it with other channels, true-colour images and dispersion models. India's INSAT-3D and 3DR imagers carry the two thermal channels needed for this test.

## 22. Keeping aircraft out of ash

Volcanic ash melts at roughly 1,100 degrees or lower, while jet engine combustion chambers run hotter, so ash melts and sticks to turbine parts. In 1982 a British Airways Boeing 747 lost all four engines in ash from Galunggung, Indonesia, and restarted them only after descending out of the cloud. The 57 km height of the Hunga Tonga plume came from the parallax between GOES-17 and Himawari-8.

## 23. Case studies

Part 5: Kīlauea 2018, Eyjafjallajökull 2010, La Palma 2021 and Grindavík 2023.

## 24. Kīlauea, Hawai‘i, May–August 2018

This was the largest lower East Rift Zone eruption and summit collapse at Kīlauea in at least 200 years. The summit caldera floor dropped by hundreds of metres in a series of collapse events, each recorded as ground deformation and an earthquake.

## 25. Eyjafjallajökull, Iceland, April 2010

The disruption came less from the size of the eruption than from the weather: steady north-westerly winds carried the ash straight to Europe's busiest airspace. The episode drove better measurement of ash concentration, from satellites and research aircraft, and new rules on how much ash engines can tolerate.

## 26. La Palma, Canary Islands, 2021

The precursors lasted only about eight days, which is short for a basaltic eruption, so fast satellite and GNSS processing mattered. Damage maps from Copernicus EMS were used for evacuation, insurance claims and reconstruction planning.

## 27. Grindavík, Iceland, 2023–2024

This is the clearest recent example of remote sensing driving engineering decisions: where to build barriers, which roads and pipes to protect, and when it was safe to return. Uplift at Svartsengi, measured by InSAR and GNSS, was used to anticipate each new magma intrusion.

## 28. Engineering practice

Part 6: Where engineers use volcano data, a workflow, limits and exercises.

## 29. Where engineers use volcano data

Roof damage from ash typically starts at loads of about 100 to 400 kg per square metre for roofs with timber supports, and higher for reinforced concrete (Spence et al., 2005). Clearing ash from roofs early, and before rain, is a simple, effective measure.

## 30. A volcano monitoring workflow

Steps 1 to 4 are continuous background work; steps 5 to 8 happen around an eruption. The decisions in step 5 belong to the volcano observatory and civil protection, but engineers supply many of the inputs.

## 31. Limits and good practice

Satellites have made it possible to watch every volcano on Earth, but interpreting what they see still needs local knowledge and ground instruments.

## 32. Try these

Use: uplift at the centre = (1 − ν) ΔV ÷ (π d²); one Sentinel-1 fringe = 2.8 cm; load = thickness × density × g.

## 33. Answers

Exercise 2 shows why a single number, the uplift, is not enough: the width of the deformation is needed to separate a small shallow source from a large deep one.

## 34. Key points

The whole lecture in five lines.

## 35. References

Biggs et al. (2014) and Lazecký et al. (2020) for InSAR at volcanoes worldwide; Wright et al. (2004) and Coppola et al. (2016) for thermal monitoring; Theys et al. (2019) for SO₂; Loughlin et al. (2015) for the global picture of volcanic risk.

## 36. Thank you. Questions?

Credits and sources are on this slide and the references slide.
