# Flood Mapping with SAR — speaker notes

## 1. Flood Mapping with SAR

This lecture uses radar images themselves, the brightness of each pixel, rather than interferometry. Floods are the most common application of SAR in disaster response. The strip at the bottom is a simulated change composite: newly flooded land appears red.

## 2. Use radar images to map where a flood is, how much land it covers, and how often it happens, even under cloud.

Floods are the most frequent natural disaster. During a flood the sky is usually cloudy, which is exactly when optical satellites fail and radar works.

## 3. Outline

Five parts: the physics, the methods, checking and sharing maps, real floods, and engineering use.

## 4. Floods and why radar sees them

Part 1: Flood types, clouds, how water scatters radar, and the satellites.

## 5. Four kinds of flood

India sees all four: monsoon river floods in Assam and Bihar, flash floods in the Himalaya, cyclone surges on the east coast, and urban floods in Mumbai, Chennai and Bengaluru.

## 6. Why radar for floods

Optical images (Sentinel-2, Landsat) are excellent for floods when the sky clears, and are often used to check radar maps afterwards.

## 7. Why floodwater looks dark, and when it does not

VV polarisation shows the most contrast for open water; VH is less affected by wind. L-band penetrates forest canopies better than C-band, so it sees flooding under trees more reliably.

## 8. Radar satellites for flood mapping

For a big flood, agencies combine many satellites to get an image as often as possible. Through the International Charter, space agencies share images free of charge for major disasters.

## 9. Timing: will the satellite catch the peak?

Animation: a simulated flood rises to a peak on day 7 and drains. A satellite passing every 6 days, on days 3, 9 and 15, never sees the peak: the map it makes shows less than the maximum flooded area. More satellites, and models, fill the gaps.

## 10. Mapping water in SAR images

Part 2: Preparing images, thresholds, change detection and false alarms.

## 11. Preparing the images

GRD (ground range detected) images carry only the brightness, not the phase, so they are smaller and simpler than the SLC images used for interferometry. Decibels: σ⁰(dB) = 10 log₁₀ σ⁰.

## 12. Thresholding: separating water from land

Split-based thresholding (Martinis et al., 2009) computes the threshold only in tiles that contain both water and land, which makes the histogram bimodal even when floods cover a small part of a large scene.

## 13. Change detection: before and during

The difference in dB is the log of the ratio of the two images, which cancels most of the speckle and terrain effects. The UN-SPIDER Google Earth Engine method uses this approach with VH images. The change composite (before in red, during in green and blue) is the quickest visual check for anyone.

## 14. False alarms: dark but not flooded

HAND, height above nearest drainage (Nobre et al., 2011), is computed from a DEM. The threshold of 15 or 20 m is a common choice; check it against local flood history.

## 15. The hard cases

In the simulated scene, change detection alone finds 68% of the flooded area; adding a rule for brighter flooded forest raises this to 87%. The rest, under a wind-roughened patch and in town, is still missed.

## 16. A flood-mapping workflow

Using the same track and pass for the reference image keeps the viewing geometry identical, so terrain effects cancel in the change detection. A minimum mapping unit (removing patches of a few pixels) cleans up speckle.

## 17. Accuracy, services and tools

Part 3: Checking a flood map, and the free services and software.

## 18. How good is each method?

CSI, the critical success index, is hits divided by hits plus misses plus false alarms: 1 is perfect. These numbers come from the simulated scene used in Part 2, where the true flood is known exactly.

## 19. Checking a flood map

The biggest source of disagreement between flood maps is often timing, not method: two maps made a day apart can both be correct.

## 20. Who makes flood maps in a disaster

The Global Flood Monitoring product combines algorithms from TU Wien, DLR and LIST by majority vote, and also provides the whole archive from 2015. It is part of the Global Flood Awareness System (GloFAS).

## 21. Free software for flood mapping

For a class exercise, the UN-SPIDER Earth Engine recommended practice runs in a web browser with a free account and maps a flood in minutes.

## 22. Case studies

Part 4: Kerala 2018, Pakistan 2022, Valencia 2024 and Assam’s flood atlas.

## 23. Kerala, India, August 2018

Studies afterwards showed that automatic thresholds in Google Earth Engine could reproduce the flood extent from Sentinel-1 quickly, making this a good exercise case for students.

## 24. Pakistan, 2022

Headlines said a third of the country was under water. Radar maps of open water at any one time show a much smaller area. Both numbers can be true for different definitions; always say what a flood area means.

## 25. Valencia, Spain, October 2024

Valencia shows the limits of satellite radar for flash floods in towns: by the time of the next pass the water had largely gone. The damage, mud and debris still showed in high-resolution optical and aerial images, and in coherence loss.

## 26. Assam, India: a flood atlas

This is the same idea as the inundation-frequency map in Part 5: stacking many flood maps from the archive to show which land floods every year and which only rarely.

## 27. Engineering practice

Part 5: Water depth, flood frequency, model calibration, limits and exercises.

## 28. From flood extent to water depth

This is the idea behind the FwDET tool (Cohen et al., 2018). LiDAR elevation models give the best results; global 30 m DEMs can be several metres wrong in flat floodplains.

## 29. How often does each place flood?

A frequency from satellite images is not the same as a return period from river-gauge statistics: images miss short floods. The two are best used together, as in the Assam atlas.

## 30. Calibrating flood models with SAR

Flood forecasting centres also assimilate SAR flood extents and water levels into their models to correct forecasts as a flood develops.

## 31. Where engineers use SAR flood maps

In the first days of a disaster, the most valuable output is often simple: which villages and roads are under water today.

## 32. Limits and good practice

A flood map without a date and time is misleading: water can rise or fall by metres within a day.

## 33. Try these

dB = 10 log₁₀(linear). One 10 m pixel = 100 m². CSI = hits ÷ (hits + misses + false alarms).

## 34. Answers

Exercise 4: the hit rate alone looks good, but the CSI, which counts every kind of error, is the fairer single score.

## 35. Key points

The whole lecture in five lines.

## 36. References

Schumann and Moller (2015) is a good review to start with; the UN-SPIDER recommended practice is the best hands-on starting point.

## 37. Thank you. Questions?

Credits and sources are on this slide and the references slide.
