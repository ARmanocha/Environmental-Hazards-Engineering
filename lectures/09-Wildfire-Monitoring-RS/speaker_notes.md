# Wildfire Monitoring with Remote Sensing — speaker notes

## 1. Wildfire Monitoring with Remote Sensing

Wildfire monitoring uses infrared light: hot fires glow strongly at middle-infrared wavelengths, and burned land reflects light differently from living vegetation. The strip at the bottom is a simulated false-colour image: green forest, a dark red burn scar and a bright fire front.

## 2. Use satellite data to detect fires as they burn, map what burned and how badly, and judge where the next fire is likely.

Before, during and after a fire, satellites answer different questions: where is it dry enough to burn, where is it burning now, and what has burned and how badly.

## 3. Outline

Six parts: the hazard, active-fire detection, burned areas and their aftermath, fire danger, real fires, and engineering practice.

## 4. Wildfire and why we monitor it

Part 1: Fire behaviour, fires in India, and the before–during–after cycle.

## 5. What drives a wildfire

The fire triangle (heat, fuel, oxygen) explains burning; the fire behaviour triangle (fuel, weather, terrain) explains spread. Satellites can measure fuel dryness, track the weather and map terrain, but not ignitions, which is why fire danger is a probability.

## 6. Fires in India

FSI's alerts use the polar-orbiting MODIS and VIIRS sensors, combining several passes a day. Most Indian forest fires are ground fires that burn litter and undergrowth rather than crown fires, but they still damage regeneration, soil and air quality.

## 7. Before, during and after

This lecture follows the same order in reverse importance for response: Part 2 is during (active fires), Part 3 is after (burned areas), Part 4 is before (fire danger).

## 8. Why satellites for fires

FIRMS is NASA's Fire Information for Resource Management System: free active-fire data from MODIS and VIIRS, in near real time, with maps and email alerts.

## 9. Detecting active fires

Part 2: Seeing heat, sub-pixel fires, satellites and fire radiative power.

## 10. Hot things glow at shorter wavelengths

This is the same physics as Lecture 1's discussion of radiation, applied to emission rather than reflection. In daylight the 3.9 micrometre channel also contains reflected sunlight, which is why daytime detection needs extra tests for sun glint and bright surfaces.

## 11. Small fires, big pixels

The calculation mixes radiance, not temperature: the pixel radiance is the area-weighted sum of fire and ground radiance, converted back to a brightness temperature. Operational algorithms (MODIS: Giglio et al., 2003 and 2016; VIIRS: Schroeder et al., 2014) use contextual tests against neighbouring pixels plus checks for clouds, sun glint and hot bare ground.

## 12. Grow a fire inside one pixel

Animation: the fire grows from 1 square metre to 1 hectare inside a 1 km pixel. The 3.9 micrometre brightness temperature climbs steeply while the 11 micrometre value hardly moves. The detection test shown is simplified from the published algorithms, which use thresholds that depend on the background and on day or night.

## 13. Satellites that watch fires

Polar orbiters pass at fixed local times, around 10:30 and 13:30 and the matching night passes. A fire lit and burned out between passes is missed, which matters for crop-residue burning (case study in Part 5).

## 14. Following a fire from pass to pass

In practice, responders overlay FIRMS detections on roads, villages and terrain. A detection marks a hot pixel, not a point: the fire can be anywhere within the 375 m square, and smoke or thick cloud can hide it.

## 15. Fire radiative power: how much is burning

Satellites estimate FRP from the excess 3.9 micrometre radiance of the fire pixel, without needing to know the fire's area or temperature separately (the middle-infrared method of Wooster et al., 2003). Exercise 3 uses the Stefan–Boltzmann form.

## 16. Mapping burned areas and what follows

Part 3: NBR, burn severity, radar, recovery and post-fire hazards.

## 17. Burned land has a different spectrum

The normalized burn ratio uses Sentinel-2 bands 8 and 12, or Landsat 8 and 9 bands 5 and 7. It is far more sensitive to burning than NDVI, which uses red instead of short-wave infrared.

## 18. Burn severity from before and after

Use images from the same season, a year apart if possible, so that seasonal greening does not look like burn severity. Clouds and smoke must be masked first. Field plots using the Composite Burn Index are the standard check.

## 19. Radar sees through the smoke

Radar burn-scar signals depend on vegetation type, soil moisture and rain after the fire, so they are less consistent than NBR. Sentinel-1 is commonly used; L-band (NISAR) responds better to changes in woody biomass.

## 20. Watching the forest recover

Comparing with a nearby unburned control removes the seasonal cycle and year-to-year weather. Recovery rates depend on severity, forest type and rainfall; repeated fires can turn forest into scrub.

## 21. After the fire: new hazards

Burn-severity maps from dNBR are the main input to post-fire hazard assessment: the US Geological Survey uses them with slope and rainfall to estimate debris-flow likelihood within days of a fire. This links wildfire to the landslide and flood lectures.

## 22. Before the fire: fire danger

Part 4: Dry vegetation, fire seasons and danger ratings.

## 23. Fires follow dryness

In Uttarakhand and much of central India the fire season runs from February to June, peaking in April and May. A dry winter, little pre-monsoon rain and heat waves make a bad season.

## 24. Fire danger ratings

Danger ratings are probabilities, not predictions of a fire: they say how easily a fire would start and spread if lit. They guide patrols, fire lines, burning bans and where to pre-position crews.

## 25. Case studies

Part 5: Uttarakhand, Punjab, Australia, Canada and Los Angeles.

## 26. Uttarakhand, India, 2023–24 fire season

Figures differ between reports and dates, so use them as orders of magnitude. Several people died fighting the fires in 2024. Smoke affected air quality across the hills.

## 27. Crop-residue burning, Punjab

This case shows a key limit of polar-orbiting detection: the overpass time. Geostationary sensors and burned-area mapping give a fuller picture than hot-spot counts alone.

## 28. Black Summer, Australia, 2019–20

Black Summer links drought (Lecture 8) to fire: years of low rainfall left fuel extremely dry. About 3 billion animals were estimated to have been killed or displaced.

## 29. Canada, 2023

Geostationary satellites tracked smoke plumes hour by hour, feeding air-quality forecasts for millions of people far from the fires.

## 30. Los Angeles, January 2025

This case is about the wildland–urban interface. Detection was not the problem; spread was. Satellite and aerial damage maps supported recovery and insurance, and burn-severity maps fed debris-flow warnings for the following rains.

## 31. Engineering practice

Part 6: Uses, a workflow, limits and exercises.

## 32. Where engineers use fire data

Power lines both start wildfires and are damaged by them; utilities increasingly use fire-danger forecasts to plan preventive shut-offs. In India, forest fire lines and community fire watchers are the main tools, guided by satellite alerts.

## 33. A wildfire monitoring workflow

A good class exercise: download FIRMS detections for Uttarakhand for April 2024, then compute dNBR for one large burn scar in Google Earth Engine and compare the two.

## 34. Limits and good practice

False alarms come from hot bare ground, sun glint, gas flares and industry. Most systems give each detection a confidence level; use it.

## 35. Try these

Severity classes for dNBR (Key and Benson, 2006): below 0.10 unburned, 0.10–0.27 low, 0.27–0.44 moderate-low, 0.44–0.66 moderate-high, above 0.66 high.

## 36. Answers

Exercise 4 is approximate: real fires change intensity through the day, which is why geostationary FRP every few minutes gives better fire radiative energy than two polar passes.

## 37. Key points

The whole lecture in five lines.

## 38. References

Chuvieco et al. (2019) is a good review of burned-area mapping; Giglio et al. (2016) describes the MODIS active-fire algorithm used in FIRMS.

## 39. Thank you. Questions?

Credits and sources are on this slide and the references slide.
