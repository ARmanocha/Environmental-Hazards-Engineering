# SAR and InSAR for Geohazards — speaker notes

## 1. SAR and InSAR for Geohazards

An introduction for the whole module: what radar satellites are, how InSAR measures ground motion, which satellites exist, and how all this helps us monitor hazards and engineer safer infrastructure. Lectures 1 to 3 then go deeper into the theory.

## 2. The ground is always moving. Landslides creep, cities sink, faults slip and volcanoes swell, often by only millimetres a year.

Ask: how would you measure 5 mm a year of movement on a hillside above a town? Surveying and GNSS give a few points; InSAR gives a map of millions of points, repeated every few days.

## 3. Outline

Six parts, from the physics of radar to practical engineering use.

## 4. Remote sensing and radar basics

Part 1: Passive and active sensors, radar bands, and fifty years of radar satellites.

## 5. Passive and active sensors

Optical images are easy to read but need clear skies and daylight. Radar brings its own illumination at centimetre wavelengths, which pass through clouds.

## 6. Radar wavelengths and bands

Band letters come from wartime radar codes and have no deeper meaning. For InSAR the main trade-off is precision (shorter wavelength) against coherence over vegetation (longer wavelength).

## 7. Longer waves see deeper

This is why L-band keeps working over vegetated hillslopes, where many landslides are. Figure from the EarthScope InSAR short-course slides.

## 8. Fifty years of radar satellites

The big change came in 2014: Sentinel-1 made regular, free radar data available everywhere, which turned InSAR from a research tool into a monitoring tool.

## 9. What is SAR?

Part 2: How a radar satellite takes a picture, what the picture shows, and its distortions.

## 10. How a radar satellite takes a picture

Why sideways? If the radar looked straight down, echoes from the left and right of the track would arrive at the same time and could not be separated.

## 11. The “synthetic aperture” trick

The surprise: the resolution along track is about half the antenna length, no matter how far away the satellite is. Lecture 1 works through this in detail.

## 12. What a SAR image shows

A radar image shows structure and moisture, not colour. Ask students: why would a city look so bright? (Corner reflections between walls and streets.)

## 13. Side-looking geometry distorts mountains

Why engineers care: landslide-prone valleys are steep. Always check the viewing geometry: a slope hidden from an ascending pass may be visible from a descending one.

## 14. What is InSAR?

Part 3: Phase, fringes, line of sight, time series and coherence.

## 15. Two radar images, one measurement of change

Half a wavelength, because the signal travels to the ground and back: moving the ground by λ/2 changes the round-trip path by a whole wavelength.

## 16. Watch fringes form

A simulated volcano swelling and relaxing, seen by a C-band satellite like Sentinel-1 (λ = 5.6 cm). Every 2.8 cm of uplift toward the satellite adds one full colour cycle. Count the rings: at 14 cm there are 5. This is exactly how real volcano and subsidence interferograms look.

## 17. Reading a real interferogram: Landers, 1992

Mw 7.3 Landers earthquake, California, 28 June 1992. Figure modified from Massonnet et al. (1993), via the EarthScope InSAR theory slides.

## 18. InSAR sees motion in one direction only

A landslide sliding due north or south can be almost invisible to InSAR. Always ask: which direction is the slope moving, and which direction is the satellite looking?

## 19. From one interferogram to a time series

Time series are what make InSAR useful for engineering: they reveal slow, steady creep and its seasonal ups and downs, which single interferograms miss.

## 20. When InSAR works, and when it doesn’t

Left: 1-day correlation. Right: 6-month correlation; agricultural fields and moving sand have lost coherence. Figure from the EarthScope InSAR theory slides.

## 21. Satellites and orbits

Part 4: How radar satellites circle the Earth, Sentinel-1, NISAR and other missions.

## 22. How a radar satellite circles the Earth

Watch the orange swaths: each new orbit lands west of the previous one because the Earth has turned about 25° in the meantime. In one day the swaths leave wide gaps; it takes the full 12-day cycle to cover every point, and then the pattern repeats exactly. The counter resets each simulated day.

## 23. Sentinel-1 in numbers

Sentinel-1A launched in 2014 and Sentinel-1C in December 2024; Sentinel-1B failed in December 2021. C-band wavelength 5.55 cm, so one fringe is 2.8 cm.

## 24. NISAR: the NASA–ISRO radar mission

NISAR is the first satellite to fly two radar frequencies. The L-band radar keeps coherence over vegetation, which makes it especially useful for landslide-prone hillslopes in the tropics and the Himalaya.

## 25. Radar satellites you can use

For teaching and most research, start with Sentinel-1 and NISAR: free, global and regular. Commercial X-band satellites can revisit daily and resolve metre-scale features, useful for emergencies and individual structures.

## 26. Hazards and engineering

Part 5: Earthquakes, landslides, subsidence, infrastructure, floods and the workflow.

## 27. What InSAR does for hazards and engineering

The next slides take a closer look at each. All of these are geohazard problems where the key question is: where is the ground moving, how fast, and is it speeding up?

## 28. Earthquakes: L’Aquila, Italy, 2009

For engineers, coseismic deformation maps show where foundations, pipelines and roads were stretched or offset, and help assess the risk from aftershocks on the same fault.

## 29. Landslides and unstable slopes

InSAR does not replace inclinometers and field mapping; it tells you where to put them. A slope creeping at 2 cm a year that suddenly speeds up to 10 cm a year deserves urgent attention.

## 30. Land subsidence: groundwater, mining and cities

Example from the EarthScope InSAR theory slides: an L-band interferogram before (left) and after (right) removing an orbital ramp, revealing uplift from aquifer recharge.

## 31. Infrastructure and engineering monitoring

The big advantage is history: because the Sentinel-1 archive goes back to 2014 (and ERS to 1992), you can look back at how a structure behaved before a problem was noticed.

## 32. Floods and damage mapping

Wind roughens open water and makes it brighter (day 2), which can hide floods: one reason analysts compare several dates. Disaster agencies use exactly this through the International Charter Space and Major Disasters.

## 33. From satellite data to engineering decisions

Steps 1–3 are covered by the course software; step 4 is classic engineering geology; step 5 is essential before acting on any InSAR result.

## 34. Getting started

Part 6: Strengths and limits, free data and tools, and a quick check.

## 35. Strengths and limitations

Use InSAR as a wide-area screening and monitoring tool, and combine it with ground measurements for any decision.

## 36. Free data and tools

A good first exercise: open EGMS or COMET-LiCSAR, find a city or volcano you know, and look at its ground-motion map. No processing needed.

## 37. Three quick questions

Give students two minutes in pairs. Answers on the next slide.

## 38. Three quick answers

Follow-up for question 2: if the slope faces east and the pass is ascending (looking east), the satellite sees mostly the downslope and downward motion; from a descending pass the same slide may look very different.

## 39. Key ideas

If students remember only one number, make it this: one Sentinel-1 fringe is 2.8 cm.

## 40. The rest of this module

Each lecture builds on this introduction; the course software (ISCE2, MintPy) comes after Lecture 3.

## 41. Thank you. Questions?

Credits for reused figures are on this slide.
