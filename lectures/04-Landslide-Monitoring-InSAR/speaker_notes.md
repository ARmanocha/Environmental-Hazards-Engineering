# Landslide Monitoring with InSAR — speaker notes

## 1. Landslide Monitoring with InSAR

This lecture applies the InSAR ideas from Lectures 1 to 3 and the SNAP practical to one of the most common geohazards: landslides. The strip at the bottom is simulated data: blue clusters are slopes moving away from the satellite.

## 2. Use satellite radar to find slopes that are moving, measure how fast, and judge when that matters.

Many large landslides creep for years before they fail, at millimetres to centimetres per year. That is too slow to notice on the ground but exactly the range InSAR measures well.

## 3. Outline

Six parts: the hazard, the geometry, the techniques, interpreting results, real cases, and engineering use.

## 4. Landslides and why we monitor them

Part 1: Types, speeds, and what InSAR adds.

## 5. What moves, and how

Classification after Varnes, updated by Hungr, Leroueil and Picarelli (2014). The key question for InSAR is speed: anything that fails within seconds or minutes is invisible in images taken days apart, but many slides, spreads and earthflows move slowly for years.

## 6. Landslide speeds, and where InSAR fits

Satellite InSAR covers the extremely slow and very slow classes, below about a metre per year. Faster movements need offset tracking, ground-based radar or field instruments. The scale is logarithmic: each step is a factor of about 100.

## 7. Why use InSAR for landslides?

The free Sentinel-1 archive is the big change: since 2014 most land areas have been imaged every 6 to 12 days, so we can go back and check whether a slope was moving before a failure. Sentinel-1C (launched December 2024) restored the 6-day repeat after Sentinel-1B failed in 2021.

## 8. Seeing slopes from space

Part 2: Line of sight, slope direction, layover, shadow and the speed limit.

## 9. InSAR measures only one direction

Write the sign convention on the board: in this lecture positive LOS values mean motion towards the satellite. A landslide moving downhill can therefore appear positive, negative or almost zero, depending on the slope and the pass. This is the single most important idea for landslide InSAR.

## 10. Mountains are hard for a side-looking radar

These are the same distortions met in Lecture 1, now on the slopes we care about. A slope that is in layover for ascending is often well seen from descending, which is another reason to process both.

## 11. Which slopes does each pass see?

Values are computed for a 30 degree slope, Sentinel-1 geometry, ascending heading about 350 degrees and descending about 190 degrees. Steeper slopes change the numbers, so in practice C is computed pixel by pixel from the elevation model.

## 12. Turn the slope: what does each pass see?

Animation: the arrow shows the direction of downslope motion as the slope turns through every direction. Watch the bars swap as the slope turns from east-facing to west-facing, and both stay low near north and south. Pause on a few directions and ask the class which pass they would use.

## 13. From line of sight to downslope velocity

Numbers from the simulated example on the velocity-map slide later: the true downslope velocity in the centre of landslide A is about 34 to 42 mm/yr, so the projected 38 mm/yr is right. The same landslide seen from descending has C close to zero and must not be projected.

## 14. The speed limit: phase aliasing

Worked out as wavelength over four, divided by the revisit time, converted to metres per year. It is a limit on the velocity difference between neighbouring pixels, so a fast landslide next to stable ground is the worst case. Low coherence lowers the practical limit further.

## 15. Techniques and processing

Part 3: Point targets, small baselines, offset tracking and the open tools.

## 16. Choosing a technique

For most landslide work the choice is a multi-image time series (PS and SBAS families). Single interferograms are useful after a sudden event. Offset tracking takes over when phase aliases. Ground-based radar is the tool for a slope in crisis.

## 17. What reflects radar on a hillside?

This explains the patchy point maps: on a forested Himalayan or Western Ghats slope, C-band Sentinel-1 may give almost no points, while L-band (NISAR, ALOS-2) penetrates the canopy and keeps coherence. Snow cover in winter breaks coherence completely.

## 18. A landslide InSAR workflow

Dark steps are the outputs people use: the hotspot map, the time series compared with rainfall, and the report. Hotspot detection is often automated, for example by flagging clusters of points faster than a velocity threshold (Bekaert et al. 2020 did this for Nepal).

## 19. Open tools and ready-made products

For a first landslide project, start from ready-made products (EGMS in Europe, LiCSAR elsewhere) before processing your own. All of these are free; HyP3 and the Sentinel-1 data need a free Earthdata or Copernicus account.

## 20. Mountains add atmosphere and seasons

A classic mistake: a signal that correlates with elevation across the whole image is atmosphere, not a landslide. A real landslide has sharp edges at its boundaries and does not depend on the weather on the day of each image.

## 21. Reading the results

Part 4: Velocity maps, two passes, time series and forecasting failure.

## 22. One valley, two passes

Both landslides move straight downhill at similar speeds. Each is obvious from one pass and almost invisible from the other. With only one pass, half the landslides in a valley would be missed. Points are missing in forest (green-tinted) and where geometry is poor.

## 23. Two passes, two components

The decomposition needs the two passes to cover the same period. The vertical and east-west components are easier to explain to engineers and planners than line-of-sight values.

## 24. Time series: the landslide breathes with the monsoon

This seasonal pattern is typical of slow landslides in monsoon climates and in Mediterranean winters. Groundwater rises after heavy rain, effective stress on the slip surface drops, and the landslide speeds up. Mud Creek (Part 5) behaved like this for years before it failed.

## 25. Before failure: the inverse-velocity method

The method is widely used with ground-based radar and extensometers, where readings come every few minutes. From satellites it works only for slow final accelerations lasting weeks to months (Carlà et al., 2019). The forecast is a window, not a date: update it with every new image.

## 26. Can satellite InSAR give early warning?

A sensible system uses satellite InSAR for screening and long-term trends, and switches to ground-based radar, extensometers and alarms once a slope is known to be accelerating.

## 27. Case studies

Part 5: Mud Creek, Xinmo and Joshimath, and national ground-motion services.

## 28. Mud Creek, Big Sur, California, 2017

Handwerger and colleagues combined eight years of NASA's airborne radar (UAVSAR) with Sentinel-1 to show the landslide's seasonal rhythm, then its acceleration in 2017. Repairs to Highway 1 cost about 54 million US dollars.

## 29. Xinmo, Maoxian, Sichuan, China, 2017

This is the case that showed what Sentinel-1 could do for landslides: a clear precursor sat in free data that nobody was watching. It also shows the revisit limit: the last image before failure was taken five days earlier.

## 30. Joshimath, Uttarakhand, India, 2023

The NRSC preliminary report was widely reported in January 2023 and withdrawn from its website shortly after. Families were moved out of the worst-affected areas. The case shows both the value of InSAR and the care needed when sharing results during a crisis.

## 31. From one slope to a whole country

Ground-motion services turn InSAR from a research project into routine screening. Engineers can check any slope against the map before designing a road or a building, then look closer where points are moving.

## 32. Engineering practice

Part 6: Uses, field instruments, limits and exercises.

## 33. Where engineers use landslide InSAR

The common thread: InSAR covers large areas cheaply, so it is used to decide where detailed, expensive investigation is needed, and to check afterwards whether drainage or stabilisation works have slowed the slope.

## 34. InSAR works best with field instruments

InSAR says where and how fast at the surface. Boreholes say how deep, piezometers say why, and continuous sensors say what is happening right now. A monitoring plan uses all of them.

## 35. Limits and good practice

A point that is not moving in the InSAR map may simply be a point the satellite cannot see well. Absence of evidence is not evidence of stability.

## 36. Try these

Give students five to ten minutes in pairs. Sentinel-1 wavelength: 5.55 cm. All four use only ideas from this lecture.

## 37. Answers

For exercise 4, stress that the forecast must be updated with every new reading: real inverse-velocity plots are noisy and can bend.

## 38. Key points

The whole lecture in five lines.

## 39. References

Lacroix et al. (2020) is the best single review to start with; it is written for a broad audience.

## 40. Thank you. Questions?

Credits and sources are on this slide and the references slide.
