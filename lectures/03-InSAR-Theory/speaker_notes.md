# InSAR Theory — speaker notes

## 1. InSAR Theory

Lecture 3 pulls Lectures 1 and 2 together with real examples: how interferograms are formed, what they show about topography and deformation, the main error sources, and how correlation and wavelength control quality.

## 2. Outline

Five parts. Parts 2 and 3 revisit Lecture 2's theory with real data; Parts 4 and 5 are what decide whether an interferogram is usable for geohazard work.

## 3. From SAR to InSAR

Part 1: SAR images, the electromagnetic spectrum, backscatter, and how two images form an interferogram.

## 4. Synthetic Aperture Radar (SAR): a satellite at time t1 views ground pixel A along its line of sight, recording amplitude and phase

A SAR satellite at time t1 views ground pixel A along its line of sight (LOS). Each pixel records an amplitude A1 and a phase Φ1. The amplitude image shows the landscape; the phase of a single image looks random because of speckle.

## 5. Electromagnetic spectrum: atmospheric transmission from visible to microwave, with active and passive sensors

Atmospheric transmission across the spectrum. Optical and thermal sensors are passive and work in transmission windows. Radar (SAR, scatterometers, altimeters) is active and uses microwaves at cm wavelengths (K, X, C, S and L bands), where the atmosphere is almost transparent, so SAR sees through clouds, day and night.

## 6. What's in a SAR image, backscatter: Belle Chasse, Louisiana, on four days in August 2021 under normal, windy and flooded conditions

Belle Chasse, Louisiana, 28–31 August 2021. Calm water is dark because it reflects the radar away like a mirror; wind roughens the water and brightens it; flooding hides land features; as the water recedes they return. The dates span Hurricane Ida's landfall in Louisiana on 29 August 2021.

## 7. Synthetic Aperture Radar (SAR), repeated before the InSAR slide

Back to a single SAR image: amplitude A1 and phase Φ1 for ground pixel A. Next, add a second pass.

## 8. Interferometric SAR (InSAR): two passes at times t1 and t2 view the same ground pixel, giving an interferogram with fringes

A second acquisition from flight path 2 at time t2 gives (A2, Φ2). The amplitudes look alike, but the phase difference Φ2 − Φ1 is no longer random: it shows coherent fringes caused by topography and ground motion.

## 9. Interferogram formation: the phases of two images look random, but their difference shows fringes

Multiply one image by the complex conjugate of the other: C2·C1* = A1·A2·e^{i(φ2 − φ1)} = R + iI. The interferogram phase is tan⁻¹(I/R). The plots show two random-looking phase images whose difference forms clean fringes.

## 10. Interferometry for topography

Part 2: Baselines, the critical baseline, topographic phase and DEM missions.

## 11. Interferometry for topography: the interferometric triangle and the equations to solve for height z

The same triangle as Lecture 2. δρ = λΔφ/(2πp); the law of cosines gives the look angle θ; then h − z = ρ cos θ gives the height z at every pixel, once Δφ is unwrapped and h, B, α and ρ are known. This slide's form of the sin(θ − α) equation matches the figure's geometry.

## 12. Parallel and perpendicular baselines: B parallel = B sin(theta − alpha), B perpendicular = B cos(theta − alpha)

Split the baseline into two parts. The parallel baseline B∥ = B sin(θ − α) lies along the look direction and sets the phase; the perpendicular baseline B⊥ = B cos(θ − α) sets the sensitivity to topography. This uses the parallel-ray approximation.

## 13. Critical baseline: the formula, a table for earlier satellites, and about 5.1 km for Sentinel-1

If the baseline is too large, the phase changes by more than 2π across one range resolution cell: the signal is aliased and the interferogram decorrelates. Check for Sentinel-1: Bc = λρ/(2 Rr cos θ) = 0.055 m × 800 km / (2 × 5 m × cos 30°) ≈ 5.1 km. The table shows that longer wavelengths and wider bandwidths give larger critical baselines.

## 14. Solution for topography from interferometric phase, after subtracting the flat-Earth fringe

After removing the flat-Earth fringe, the phase is proportional to height: φ_topo = −(2πpB/λρ)(cos α / tan θ0 + sin α) dz. Everything in the bracket is known, so phase converts directly to height. Each fringe (one phase cycle) is one ambiguity height.

## 15. Implementation options: the Shuttle Radar Topography Mission and TanDEM-X

Single-pass topographic interferometers. SRTM (2000) carried two antennas on the Space Shuttle, one in the cargo bay and one at the end of a 60 m mast. TanDEM-X flies two satellites in close formation to form the baseline.

## 16. Technology for generation of DEMs: optical stereo, laser profiling, radar interferometry, with a USGS DEM of the United States

DEMs come from optical stereo imaging, laser profiling (lidar) and radar interferometry. The map is a USGS DEM of the conterminous United States.

## 17. Interferometry for surface deformation

Part 3: Deformation phase, the Landers earthquake, sensitivity and phase unwrapping.

## 18. Interferometry for surface deformation: phase difference equals topographic phase plus 4 pi over lambda times line-of-sight deformation

Repeat-pass geometry: from S1 and S2 the radar sees point A move to A′ between passes. The phase difference is the topographic phase plus (4π/λ)Δd, where Δd is the line-of-sight deformation. The example interferogram shows an earthquake's deformation pattern.

## 19. Landers earthquake 1992 interferogram: 20 fringes equal 56 cm of line-of-sight change

The first InSAR map of an earthquake: Landers, California, Mw 7.3, 28 June 1992 (Massonnet et al., 1993). ERS-1 C-band, λ = 5.6 cm, so each fringe is λ/2 = 2.8 cm of line-of-sight change: 20 fringes = 56 cm.

## 20. Interferometry sensitivities: topographic and displacement sensitivity formulas

The same formulas as Lecture 2: metre-level topography versus cm-to-mm-level deformation. With typical numbers, displacement sensitivity is thousands of times larger.

## 21. Phase unwrapping: Three Sisters volcanic uplift, and wrapped versus unwrapped phase diagrams

Wrapped phase repeats every 2π (top diagram), making a sawtooth; unwrapping adds the right multiples of 2π to recover the continuous phase (bottom). Example: uplift near the Three Sisters volcanoes, Oregon. Diagram credit: ESA.

## 22. Phase unwrapping: wrapped interferogram and unwrapped line-of-sight displacement

Wrapped interferogram (left) and the unwrapped line-of-sight displacement in metres, from about −0.2 to +0.2 m (right). The arrows mark the track direction (T) and the look direction (L).

## 23. Phase contributions and error sources

Part 4: Orbits, DEMs, the ionosphere and the troposphere.

## 24. Phase contributions and error sources equation

The measured phase is deformation plus many other terms: DEM error, troposphere, ionosphere, orbits, decorrelation, unwrapping errors and noise. The next slides take them one at a time.

## 25. Orbital errors: an L-band interferogram before and after orbital ramp removal

Orbit errors leave a smooth phase ramp across the scene. Removing a fitted ramp (right) reveals a real signal: uplift from aquifer recharge. Ionospheric and tropospheric delays can also create ramps.

## 26. DEM errors: Mount Etna interferograms with a poor DEM and with SRTM

The Mount Etna example from Lecture 2: a poor DEM leaves fringes that follow the topography; the SRTM DEM removes most of them.

## 27. Ionospheric artifacts: an L-band Iceland interferogram and azimuth misregistration from a TEC gradient

At L-band, gradients in the ionosphere's total electron content (TEC) distort the interferogram (circled) and shift pixels in azimuth by up to about 3 pixels (right). Example from Iceland.

## 28. Tropospheric noise: causes and properties, with a diagram of the radar path through atmospheric layers

The troposphere: pressure, temperature and water vapour. Unlike the ionosphere, it affects all radar wavelengths in the same way. Delays can reach 15 cm or more. Part correlates with topography (stratified); part is turbulent and random in time.

## 29. Atmospheric phase correlated with topography in Hawaii, and simulated turbulent tropospheric phase

Top: the Hawaii example from Lecture 2. The stratified delay correlates with topography and can be modelled and removed. Bottom: turbulent delay between two passes produces random, patchy phase.

## 30. Correlation and wavelength

Part 5: Interferogram quality, decorrelation, and X-, C-, L- and P-band compared.

## 31. Correlation: a decorrelated random interferogram next to a high-correlation interferogram

Correlation (coherence) measures interferogram quality, from 0 to 1. At 0 the phase is random; near 1 the fringes are clean and carry topography and deformation information.

## 32. Correlation definition for a multi-looked interferogram

Correlation is estimated over a window of pixels when the interferogram is multi-looked: the magnitude of the averaged cross product, normalised by the average power of each image.

## 33. Correlation example: 1-day versus 6-month correlation maps over agriculture, sand, alluvium and mountains

One day versus six months. Over six months, agricultural fields and moving sand decorrelate (blue), while alluvium and mountains stay coherent. Water always decorrelates.

## 34. Total correlation is the product of thermal, spatial and temporal correlation

Total correlation = thermal × spatial × temporal. Thermal: noise inside the radar system. Spatial: the change in viewing geometry (baseline). Temporal: change in the surface between acquisitions, such as vegetation growth, farming, erosion or snow.

## 35. SIR-C C-band and L-band interferograms of Kilauea, Hawaii

SIR-C interferograms of Kīlauea, Hawaii (Rosen et al., JGR, 1996). C-band (5.6 cm) decorrelates over vegetation; L-band (24 cm) stays coherent and has a lower fringe rate, so unwrapping is easier, but the ionospheric delay is about 16 times worse. One L-band fringe is 570 m of topography; one C-band fringe is 135 m.

## 36. Wavelengths for different targets: X-, C- and L-band penetration into tree canopies

Longer wavelengths penetrate deeper into vegetation: X-band (3 cm) scatters from the top of the canopy, C-band (6 cm) partly penetrates, and L-band (24 cm) reaches branches, trunks and the ground.

## 37. X-band COSMO-SkyMed interferogram of the 2009 L'Aquila earthquake, Italy

L'Aquila earthquake, central Italy, 6 April 2009 (magnitude 6.3). COSMO-SkyMed X-band interferogram, 19 February to 9 April 2009, perpendicular baseline 480 m, look angle 37°. Fringes are dense and noisy over vegetation. X-band satellites: TerraSAR-X, COSMO-SkyMed, ICEYE, Capella.

## 38. C-band Envisat interferogram of the 2009 L'Aquila earthquake, interpreted by INGV

The same earthquake in an Envisat C-band interferogram interpreted by INGV: clear concentric fringes. C-band satellites: ERS-1/2, Radarsat-1/2, Envisat, Sentinel-1.

## 39. L-band ALOS-1 interferogram of the 2009 L'Aquila earthquake from JAXA

The same earthquake at L-band (ALOS-1, JAXA; 20 July 2008 to 22 April 2009): far fewer fringes for the same deformation, since each fringe is 11.8 cm, and good coherence across the scene. L-band systems: JERS-1, ALOS-1/2, UAVSAR (airborne), NISAR.

## 40. Interferograms and correlation at C-, L- and P-band over the same area

The same area at C-, L- and P-band: longer wavelengths give cleaner interferograms (top row) and higher correlation (bottom row, brighter yellow).

## 41. Key numbers from this lecture

Ask students to derive the first two: λ/2 because the path is two-way; 20 × 2.8 cm = 56 cm. The critical baseline check is in the notes for that slide.

## 42. Geo-SInC: the InSAR short-course repository

For geohazards, the natural next steps are Day 2 (earthquake interferograms) and Days 4–5 (time series for subsidence and slow landslides).

## 43. Thank you. Questions?

Recap the five parts. Credits for the source slides and figures are on this slide.
