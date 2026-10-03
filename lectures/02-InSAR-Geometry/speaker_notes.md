# Geometric Aspects of InSAR — speaker notes

## 1. Geometric Aspects of InSAR

Lecture 2 builds on the SAR lecture: how the phase of two radar images measures topography and ground displacement.

## 2. Key concepts

These five concepts are the backbone of the lecture. Return to them at the end as a recap.

## 3. Review the SAR lecture

s(ρ, x) is the complex SAR image as a function of range ρ and along-track position x. Quick check: ask students to define two or three of these before moving on.

## 4. Interferometry

Part 1: what interferometric phase is and how an interferogram is formed.

## 5. Phase is proportional to distance

The phase of a propagating wave is directly proportional to the distance propagated: 2π radians for every wavelength.

## 6. The use of phase measurements to find the relative distance to an object imaged by SAR from two or more observations, separated in time or in space.

Worked check: a change in range Δρ changes the two-way phase by 4πΔρ/λ, so 1° of phase is λ/720 of range: about 0.3 mm at L-band (24 cm), 0.04 mm at 3 cm and 1.1 mm at 80 cm.

## 7. Wave interference

If the observing surface could record phase differences, each point would hold a fixed value between −π and π. The figure is the classic double-slit experiment (© 2006 Encyclopædia Britannica).

## 8. SAR interferometry

In the figure, SAR 1 and SAR 2 are separated by the baseline B. The phase contours (mod 2π) follow the terrain, which is why the relative phase carries topography.

## 9. The SAR interferogram

The image on the right is an interferogram: one colour cycle represents 2π of relative phase. The interferogram is itself a complex image.

## 10. Interferometry for topography

Part 2: using two vantage points to measure topography.

## 11. The interferometric triangle

Height of the ground point: z = h − ρ cos θ. (The notebook writes this as z = h = ρ cos θ, a typo.) The law-of-cosines step is sin(θ − α) = (ρ² + B² − (ρ + δρ)²) / 2ρB, which matches the figure; the notebook prints this fraction with the opposite sign. The baseline, its angle and the range must all be known accurately for good topography.

## 12. How the data are collected sets p

In ping-pong mode each path is a full round trip from its own antenna, so the phase difference doubles: p = 2.

## 13. Interferometer methods

Hint: assume the surface is static over time. The answer is on the next slide: D.

## 14. D: p = 2

This is why repeat-pass differential interferometry uses 4π/λ (that is, 2πp/λ with p = 2) later in the lecture.

## 15. Phase and the interferometric baseline

Figure: the dotted line drops the baseline b onto the look direction ℓ̂. That projection, the parallel baseline, sets the phase.

## 16. The phase gradient

The gradient tells us how densely packed the fringes will be, which matters for planning baselines and for unwrapping.

## 17. Fringe rate across and along track

ψ_c is the local slope across track and ψ_s the slope along track. b⊥ = b cos(θ − α) is the perpendicular baseline.

## 18. Flattened phase

Flattening removes the predictable phase ramp due to the flat (or spherical) Earth, leaving only the phase due to height.

## 19. Flattened phase maps topography

This is the key result for topographic mapping: flattened phase is a scaled height map, with the scale set by b⊥, λ, ρ and θ.

## 20. Ambiguity height

Hint: check the units! The answer is on the next slide: B.

## 21. B: the ambiguity height

Example uses the values from the sensitivity calculation later in the lecture. Equivalently, h_amb = 2π divided by the topographic sensitivity (0.00907 rad/m) = 693 m.

## 22. Differential interferometry

Part 3: using two times to measure ground displacement, the part most relevant to geohazards.

## 23. Repeat-pass interferometry

Note the 4π/λ factor: repeat-pass is a two-way measurement on each date (p = 2).

## 24. Deformation phase convention

Left: range and phase decrease over time, caused by motion toward the radar along the line of sight (for example inflation). Right: range and phase increase, motion away from the radar (for example deflation). Always check which convention a software package uses.

## 25. Displacement and topography together

Without extra information, the two terms are hard to separate. This is why InSAR processing subtracts a DEM before interpreting displacement.

## 26. Line-of-sight displacement

Hint: most spaceborne radars point closer to nadir than to the horizon to maximise the signal return. The answer is on the next slide: A.

## 27. A: east and up

Whether the horizontal part is east or west depends on whether the pass is ascending or descending. North–south motion is nearly invisible to a single interferogram from a polar orbit.

## 28. Interferometric sensitivities

Computed in the notebook: 0.00906899682 rad per metre of elevation and 52.3598776 rad per metre of line-of-sight range change. One full fringe is about 693 m of height but only 12 cm of line-of-sight motion.

## 29. Sensitivity

Hint: set b = 0 in the notebook's code cell and recalculate. The answer is on the next slide: C.

## 30. C: topographic sensitivity vanishes

A zero baseline is ideal for measuring deformation: no topographic phase to remove, so DEM errors do not leak into the result.

## 31. Phase unwrapping and error sources

Part 4: why real interferograms are harder to read than the ideal equations suggest.

## 32. Phase is measured only modulo 2π

Only the fractional part of the phase cycle is measured. The integer number of cycles has to be recovered: that is phase unwrapping.

## 33. Unwrapping reconstructs the phase

Unwrapping errors are one of the intrinsic InSAR error sources on the next slide.

## 34. Interferometric error sources

Ambiguities come from design constraints; sidelobes from bandwidth and resolution limits; multipath and cross-talk act as low-level interference.

## 35. Residual errors after removing topography

Note: the notebook places the 'linear or quadratic phase variation' remark next to the DEM term; it describes the baseline error, which produces smooth ramps (see the next quiz).

## 36. Baseline error

Hint: is the line-of-sight vector constant across the swath? The answer is on the next slide: C.

## 37. C: about 4π, varying smoothly across range

Smooth ramps like this are usually removed by fitting a plane or low-order polynomial to the interferogram, or by using precise orbits.

## 38. DEM error example: Mount Etna

Why is b⊥ non-zero somewhere? Because the look angle varies across the swath, b⊥ = b cos(θ − α) also varies, so it can't be zero everywhere.

## 39. Tropospheric noise

This error is particularly confounding because it has similar spatial patterns to real displacement. Persistent patterns across many interferograms may be the deformation, unless the deformation itself is changing over time.

## 40. Tropospheric noise example: Hawaii

Since these volcanoes are active, one might conclude they are deforming. The tropospheric model shows that the signal, correlated with topography, is mostly atmospheric.

## 41. Flat-Earth fringe rate

Solution (not in the notebook; state p for students, here both cases). Flat Earth: ρ = h / cos θ, so ρ_nr = 692.8 km and ρ_fr = 848.5 km. b⊥ = b cos(θ − α): near range θ − α = 90°, so b⊥ = 0 and the fringe rate is 0. Far range θ − α = 105°, b⊥ = −25.9 m; ρ tan θ = 848.5 km. Fringe rate = (2πp/λ) b⊥ / (ρ tan θ) = −0.80 rad/km for p = 1 (one fringe per 7.9 km) or −1.60 rad/km for p = 2 (one fringe per 3.9 km). The near-range result is a nice talking point: there the baseline is parallel to the look direction.

## 42. Other resources

Simons & Rosen (2015) is freely available from Caltech: web.gps.caltech.edu/~simons/publications/pdfs/Simons_etal_2015.pdf. Rosen et al. (2000) is the classic review paper.

## 43. Geo-SInC: the InSAR short-course repository

All the material in this lecture comes from this repository; use the EarthScope2024 folder, the newest. For geohazards, Day 2 (earthquake interferograms) and Days 4–5 (time series for subsidence and slow landslides) are the most useful next steps.

## 44. Thank you. Questions?

Recap the five key concepts from the start. Credits for the source material are on this slide.
