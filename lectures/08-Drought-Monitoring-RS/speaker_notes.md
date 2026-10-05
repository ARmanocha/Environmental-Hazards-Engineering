# Drought Monitoring with Remote Sensing — speaker notes

## 1. Drought Monitoring with Remote Sensing

Floods are fast and visible; droughts are slow and easy to miss until wells and reservoirs run dry. This lecture uses many kinds of satellite measurement, optical, thermal, microwave and gravity, rather than radar alone. The strip at the bottom is a simulated vegetation anomaly map: brown is drier than normal.

## 2. Use satellite data to tell when a drought starts, how severe it is, where it is worst, and which water supplies it reaches.

The key idea is comparison with normal: a drought is defined by how far conditions fall below what is usual for that place and season, so long satellite records are essential.

## 3. Outline

Five parts: what drought is, the satellite measurements, the indices built from them, real droughts and services, and engineering practice.

## 4. Drought and why we monitor it

Part 1: Types of drought, how it spreads, and what satellites add.

## 5. A slow, creeping hazard

Because drought is defined relative to normal, every drought index compares current conditions with a long record for the same place and time of year. That is why long satellite archives matter so much.

## 6. Four kinds of drought

Classification after Wilhite and Glantz (1985). The orange line in each card says what we measure to detect that kind of drought; Part 2 covers the satellite side of each.

## 7. How a drought spreads through the water cycle

Animation with a simple simulated water balance: one monsoon fails. Rain recovers the next year, but soil moisture, river flow and groundwater each lag behind, and groundwater stays low longest. This is why a drought can still hurt water supplies after the rains are back.

## 8. Why satellites for drought

Satellite records are still shorter than the 30-year baseline climatologists prefer for some variables, such as SMAP soil moisture (from 2015). Combining satellites with long gauge records is common.

## 9. What satellites measure

Part 2: Rain, vegetation, temperature, soil moisture and groundwater.

## 10. Rainfall from space

Satellites estimate rain indirectly, from cloud-top temperature (infrared) or from microwave emission and scattering by rain. Blending with gauges, as CHIRPS does, removes much of the bias. Always check against local gauges before trusting small differences.

## 11. Vegetation: how green is the crop?

Tucker (1979) introduced the red and near-infrared combination. Sensors: MODIS (250 m, since 2000), Sentinel-2 (10 m, since 2015), Landsat (30 m). In India, NADAMS uses MODIS NDVI and NDWI.

## 12. Temperature: a thirsty crop runs hot

The Evaporative Stress Index (Anderson et al., 2011) compares actual with potential evapotranspiration. In a flash drought, heat and low humidity dry soils within weeks; thermal data often catch it first.

## 13. Soil moisture from microwaves

Water changes the dielectric constant of soil strongly, so microwave emission and radar backscatter both respond to soil moisture. Vegetation and surface roughness complicate the retrieval. Soil moisture links rainfall (meteorological drought) to crop stress (agricultural drought).

## 14. Groundwater from gravity: GRACE

GRACE flew from 2002 to 2017; GRACE-FO since 2018, leaving a gap of about a year. Results are given as equivalent water height in centimetres. GRACE revealed groundwater depletion in north-west India and California's Central Valley.

## 15. Which satellite for which part of the drought

No single satellite sees the whole drought. Operational systems combine several, as the European Drought Observatory's Combined Drought Indicator does with rainfall, soil moisture and vegetation.

## 16. Drought indices

Part 3: SPI, VCI, TCI, VHI and how to combine them.

## 17. SPI: how unusual is the rain?

SPI uses only rainfall, so it compares well across climates: an SPI of −2 means the same rarity in Rajasthan and Kerala. The Indian drought manual uses SPI and rainfall deviation as mandatory early indicators.

## 18. VCI: greenness against its own history

India's NADAMS, run by the Mahalanobis National Crop Forecast Centre, uses MODIS-based VCI with rainfall and sowing data for district-level agricultural drought assessment.

## 19. Combining greenness and heat: VHI

The vegetation and temperature condition indices and their combination were developed by Kogan for NOAA satellites; they are now computed globally. Classes as on the map: extreme below 10, severe 10 to 20, moderate 20 to 30, mild 30 to 40.

## 20. Which index for which drought

The US Drought Monitor and the European Drought Observatory both combine several indices; the Indian drought manual combines rainfall, remote sensing, crop, soil moisture and hydrological indicators before a drought is declared.

## 21. Case studies and services

Part 4: Marathwada, the Horn of Africa, California, Europe, and who monitors drought.

## 22. Marathwada, Maharashtra, 2015–16

The Jaldoot train ran from Miraj, about 340 km away. The case shows the full propagation from the animation in Part 1: by the time drinking water ran out, satellites and rain gauges had been signalling drought for a long time.

## 23. Horn of Africa, 2020–2023

Famine early warning systems such as FEWS NET rely heavily on CHIRPS rainfall and vegetation indices, because ground stations are sparse in the region. Multiple failed seasons, not one, drove the impacts.

## 24. California’s Central Valley, 2012–2016

This case joins three lectures: drought (less rain), groundwater pumping (GRACE), and subsidence (InSAR, Lecture 6). The water balance and GRACE estimates of groundwater loss agreed closely.

## 25. Europe, summer 2022

The warning and alert categories come from the observatory's Combined Drought Indicator, which steps up as a drought moves from rainfall deficit to soil moisture deficit to visible vegetation stress.

## 26. Who monitors drought

NADAMS began in 1986 at NRSA (now NRSC) and became operational in 1990; since 2012 it has been run by the Mahalanobis National Crop Forecast Centre. It issues warnings (normal, watch, alert) from June to August and assessments (mild, moderate, severe) in September and October.

## 27. Engineering practice

Part 5: Water decisions, a monitoring workflow, limits and exercises.

## 28. Engineering decisions that need drought data

Engineers often design against the worst drought in the record. Satellite records extend and fill in that record, and show where a drought is worst in real time.

## 29. A drought monitoring workflow

A good student project: compute SPI-3 and VCI for their own district for the last 20 years in Google Earth Engine, and compare the driest years with news reports or the state's drought declarations.

## 30. Limits and good practice

Irrigated fields can look perfectly green while groundwater is being used up: vegetation indices alone can hide a groundwater drought, as in north-west India and California.

## 31. Try these

Classes: VHI below 10 extreme, 10–20 severe, 20–30 moderate, 30–40 mild. SPI below −1.5 is severe. A standard normal value is −1.5 or lower about 6.7% of the time.

## 32. Answers

Exercise 4 links the index to probability: SPI is a standard normal score, so the classes correspond to fixed return periods for that season.

## 33. Key points

The whole lecture in five lines.

## 34. References

The WMO and GWP Handbook of Drought Indicators and Indices (2016) is a free, practical companion to this lecture.

## 35. Thank you. Questions?

Credits and sources are on this slide and the references slide.
