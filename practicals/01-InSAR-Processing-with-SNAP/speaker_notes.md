# InSAR Processing with SNAP — speaker notes

## 1. InSAR Processing with ESA SNAP

A hands-on practical: from two Sentinel-1 images to a map of volcano deformation, step by step in ESA's free SNAP software. Assumes the introduction lecture and Lectures 1 to 3.

## 2. Turn two Sentinel-1 radar images into a map showing how many centimetres a volcano’s ground moved.

Volcanoes are a good first InSAR target: the signal is often large and circular, the ground is often bare rock (good coherence), and the result has a clear physical meaning: magma moving underground.

## 3. Outline

Five parts. Part 2 is the hands-on core; Part 4 shows the same chain applied to real data from Kīlauea's 2018 eruption.

## 4. Before you start

Part 1: Software, data, and choosing a good pair of images.

## 5. What you need

Install SNAP before the class: the installer is large. On Windows, SNAPHU is easiest through SNAP itself or a Linux environment such as WSL.

## 6. The workflow at a glance

This is the standard Sentinel-1 TOPS interferometry chain in SNAP. Steps 2 to 9 can later be chained into a single graph (Part 4).

## 7. Our example and choosing a pair

The simulation uses the real Sentinel-1 wavelength (5.55 cm) and a 39° incidence angle. The magma source is a Mogi point source: a standard first model for volcano inflation.

## 8. Downloading the two images

If the baseline tool shows a partner with a very large perpendicular baseline (several hundred metres), pick another date: large baselines mean more topographic phase and lower coherence.

## 9. Processing in SNAP

Part 2: Thirteen steps from raw images to a map of ground motion.

## 10. Open the two images and check them

Use the World Map tab to check that both images cover the volcano. For a descending pass the image appears mirrored east–west in radar geometry; that is normal and is fixed in step 12.

## 11. Split: keep only the bursts you need

If the volcano straddles two subswaths, split both and merge them after deburst with Radar › Sentinel-1 TOPS › S-1 TOPS Merge.

## 12. Apply precise orbits

SNAP downloads the orbit files automatically. If you are offline, it will fall back to the orbits stored in the product, which are less accurate.

## 13. Coregister the images (Back-Geocoding)

Enhanced Spectral Diversity (ESD) uses the overlap between bursts to remove tiny azimuth misalignments, which would otherwise show up as phase jumps at burst boundaries.

## 14. Form the interferogram

The flat-earth phase (the fringes a perfectly flat Earth would produce) is removed here. Topography is removed in step 7.

## 15. Deburst

Deburst is quick. From here on the product is a normal single image in radar geometry.

## 16. Remove the topographic phase

In the simulation the true line-of-sight uplift peaks at 13.6 cm, which is 4.9 fringes of 2.8 cm: count them with the students.

## 17. Multilook

Sentinel-1 IW pixels are about 2.3 m in range and 14 m in azimuth; 4 range looks makes them roughly square on the ground.

## 18. Filter the phase (Goldstein)

The exponent ranges from 0 (no filtering) to 1 (strongest). Use the coherence image from step 5 to decide where to trust the fringes.

## 19. Unwrap the phase with SNAPHU

The number at the end of the snaphu command is the image width in pixels; SNAP writes the correct command for your image. Unwrapping fails in low-coherence areas: masking coherence below about 0.3 first (Band Maths) often helps.

## 20. Convert phase to displacement

Unwrapped phase is relative: SNAPHU's zero is arbitrary. That is why a reference area is essential before quoting numbers.

## 21. Terrain correction (geocoding)

Compare with step 11: the image is flipped back east–west and stretched to its true shape. The dashed line A–B is the profile used in Part 3.

## 22. Export and make a map

KMZ export is a quick way to show students their result draped over Google Earth. GeoTIFF keeps the actual numbers for analysis in QGIS.

## 23. Results and interpretation

Part 3: Reading the volcano deformation and estimating the magma source.

## 24. The volcano is inflating

Ask students to read these numbers off their own map. A circular bulge centred on the summit is the classic signature of magma accumulating in a chamber below.

## 25. A profile across the volcano

This asymmetry is a nice teaching point: a single LOS measurement mixes vertical and horizontal motion. Ascending and descending data together would separate them.

## 26. How deep is the magma, and how much?

For a Mogi source the uplift falls to half its peak at r = 0.77 d, hence d ≈ 1.3 r½. ν is Poisson's ratio of the crust. Real studies fit the full model to ascending and descending data together, but these hand estimates are within about 10 per cent here.

## 27. Is the signal real?

The atmospheric trap is the most common mistake on volcanoes: water vapour layering with height creates a delay that looks exactly like a bulge centred on the summit.

## 28. Real example: Kīlauea, Hawaii, 2018

Part 4: Real Sentinel-1 interferograms of the 2018 eruption and earthquake.

## 29. What happened at Kīlauea in 2018

One of the best-observed volcanic crises ever: GNSS, tiltmeters, drones and satellites all recorded it. InSAR shows the whole system at once: the draining summit, the intruding dike and the earthquake on the south flank.

## 30. The data: two real Sentinel-1 pairs

Frame names: 124 is the relative orbit, A means ascending. Anyone can download these products from the COMET-LiCS portal, which makes them a good check for students' own SNAP results.

## 31. Deformation or atmosphere?

This is the 'Is the signal real?' slide from Part 3 in action. On tall volcanoes the stratified atmosphere can produce several fringes on its own.

## 32. Before the eruption: magma on the move

This pair ends on 2 May, the day before lava reached the surface. InSAR caught the magma moving underground: a few tens of centimetres of motion along the rift before the first fissure opened.

## 33. Eruption and earthquake: phase and coherence

Compare with SNAP steps 5 and 9. Low-coherence areas are where unwrapping will leave gaps, which you see on the next slide.

## 34. The displacement map: 2 → 8 May 2018

Seaward (south-east) motion moves the ground away from an ascending satellite, which sits to the west; subsidence also moves it away. Both add up on the south flank.

## 35. Profile A–B across the south flank

Counting fringes on the wrapped image and comparing with the unwrapped values is the quickest way to catch unwrapping errors.

## 36. Your turn: reproduce Kīlauea in SNAP

Kīlauea is a demanding first real pair because of the dense fringes and low coherence on the forested east; Etna is gentler. Either way, students can check their result against the COMET-LiCSAR product.

## 37. Tips and next steps

Part 5: Automating with graphs, fixing common problems, and where to go next.

## 38. Automate with the Graph Builder

Once a graph works for one pair, the same XML file processes a whole year of pairs: the first step towards time-series analysis.

## 39. Troubleshooting

Most first-time problems come from mismatched inputs: different tracks, different bursts or different polarisations between the two images.

## 40. Good-practice checklist

Print this checklist for the lab session; students tick it off for their own pair.

## 41. Key steps

The whole practical in five lines.

## 42. From one interferogram to a time series

A volcano that inflates by a few centimetres a year needs a time series: dozens of pairs, processed the same way, then inverted for displacement through time.

## 43. Thank you. Questions?

Credits for software and data are on this slide.
