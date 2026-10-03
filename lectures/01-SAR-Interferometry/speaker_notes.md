# Synthetic Aperture Radar Interferometry — speaker notes

## 1. Synthetic Aperture Radar Interferometry

Welcome. Today: the basics of synthetic aperture radar (SAR) and SAR interferometry (InSAR), the technique we use to map ground deformation from space.

## 2. What you will learn

These are the seven questions this notebook-based lecture answers. Return to this list at the end as a recap.

## 3. First segment: radar imaging fundamentals

Two parts: how a SAR forms an image, then what a radar image actually shows us.

## 4. How can a radar that lights up a huge footprint on the ground deliver very fine-resolution images, and measure ground motion over time to mm–cm accuracy?

We are interested in the geodetic side of SAR, especially interferometric SAR (InSAR). The next seven slides build up the whole idea in pictures.

## 5. Motivation – understanding the processes and phenomenology of radar interferometry

Motivation. Over the next few slides we follow one idea: how raw radar echoes become images, and how two images become an interferogram that shows ground motion.

## 6. Motivation: satellite observation, raw data from the first pass

A satellite observes the ground. The raw radar data from the first pass looks like noise: the echo from every point on the ground is spread over many pulses.

## 7. Motivation: raw data from a first and a later pass

A second pass at a later time gives another raw data set over the same area. It also looks like noise.

## 8. Motivation: the magic of imaging turns raw data into amplitude images

The magic of imaging: SAR processing focuses each raw data set into an amplitude image in which we can recognise the landscape.

## 9. Motivation: the phase of each image looks random

Each focused image also has a phase. On its own, the phase of a single image looks random.

## 10. Motivation: the magic of interferometry reveals fringes

The magic of interferometry: differencing the phases of the two images reveals coherent fringes. Each full colour cycle is a change of half a wavelength in the radar-to-ground distance.

## 11. Motivation: fringes are modelled to understand the process

Finally, the fringes are modelled to understand what moved the ground, for example an earthquake, a volcano or subsidence.

## 12. Basic principles of radar and SAR

Part 1: how a radar measures distance and how a moving antenna synthesizes a long aperture.

## 13. Wave properties of light

Radar waves, like light waves, are electromagnetic energy that propagates. A plane wave travels in direction k, with wavenumber k = 2π/λ. The phase term tells us where we are in the wave cycle.

## 14. Radar and light waves, radar frequency bands and the electromagnetic spectrum

λ = c/f. Radars use microwaves, with wavelengths from millimetres to metres. Like lasers, radars are coherent, so we can measure the signal's phase. Common bands: X ≈ 3 cm, C ≈ 6 cm, S ≈ 12 cm, L ≈ 24 cm, P ≈ 75 cm.

## 15. The radar concept

Like an echo in a canyon: the transmitter sends a pulse at the speed of light, objects scatter energy back, the time delay of the echo gives the distance, and changes in the echo tell us about the object.

## 16. Parameters used in the examples

Velocity and altitude are assumed constant. Pulse duration sets average power; pulse rate sets average power and ambiguity levels; peak power, noise temperature and corner-reflector size set the SNR. Note: the notebook's table lists a 20 μs pulse, but its range-resolution calculation uses 10 μs (next slides). The speed of light is shown correctly as 299,792,458 m/s; the notebook had a typo (…456) that changes no result.

## 17. Radar geometric terminology

Key terms: look angle θ (at the platform, from nadir), incidence angle ψ (at the ground, from the local surface normal), range ρ, beamwidth, swath width S, Earth radius r_e and platform height h_p. Because the Earth curves, the incidence angle is larger than the look angle.

## 18. Achieving resolution in range

Two point targets ΔR apart in range return echoes 2ΔR/c apart in time. To separate them the pulse must be shorter than that, so a narrow pulse resolves close targets.

## 19. Coding the pulse buys resolution

Computed in the notebook: range ρ = 866,025 m; resolution from a 10 μs pulse = 1,498.96 m; resolution from a 20 MHz coded pulse = 7.49 m. Coding (for example a chirp) keeps a long pulse for high average power while getting fine resolution.

## 20. Ground resolution

Ground resolution Δg = Δρ / sin θ_i, where θ_i is the local incidence angle. On a slope τ_p facing the radar, θ_i = θ_l − τ_p, so the ground resolution gets coarser.

## 21. Ground resolution, look angle and slope

Recomputed from the notebook: Δg = Δρ / sin(θ − τ_p) with Δρ = 7.5 m, for slopes of 0°, 10° and 20°. Steep slopes facing the radar and small look angles both degrade ground resolution. At 45° look angle the three cases are 10.6 m, 13.1 m and 17.7 m.

## 22. Radar on a moving platform

Pulses are transmitted as the platform moves along its flight path; each pulse lights a strip of ground the size of the antenna beam. Beamwidth ≈ λ/L: a small antenna gives a big beam, a big antenna a small beam. Footprint ≈ ρλ/L.

## 23. Example beam dimensions

The 0.866 factor is more representative of the actual 3 dB point than λ/L alone. Notebook values: azimuth beamwidth 1.19°, elevation 5.95°, azimuth extent 17,999 m, elevation extent 103,920 m. A long antenna gives a narrow beam in azimuth; the short antenna height gives a wide beam across track, which sets the swath.

## 24. Doppler shift

Objects moving relative to the radar see a Doppler shift: higher frequency when moving toward the radar, lower when moving away. The shift is set by the velocity component along the line of sight: f_d = 2⟨v, l⟩/λ.

## 25. SAR imaging in action

NISAR mission animation, 45 seconds. It plays when you present this slide; click it to pause. Sound is off.

## 26. Azimuth resolution from aperture synthesis

Each target stays in the beam over ΔX_az ≈ λR₀/L_a. The synthetic aperture is about twice that, and its beamwidth shrinks as range grows, so the azimuth resolution is about L_a/2, independent of range.

## 27. Azimuth resolution from a synthetic aperture

Notebook values: beam extent 17,999 m, synthetic aperture 35,999 m, effective beamwidth 0.331 millidegrees, resolution 5.000 m. A longer range gives a longer synthetic aperture, which exactly cancels out, so the resolution stays at L_a/2.

## 28. Radar resolution

Give students a minute. Hint: what matters in the flight direction is the antenna length. The answer is on the next slide: D.

## 29. D: 3 m in range, 6 m along track

Range resolution depends only on bandwidth: c/(2B) ≈ 3.75 m, which the question rounds to 3 m. Azimuth resolution is about half the antenna length: 6 m.

## 30. Range-Doppler coordinates

Points at equal range from the platform lie on circles (lines of equidistance); points with equal Doppler lie on hyperbola-like curves (lines of equi-Doppler). Together they locate every pixel on the ground.

## 31. Doppler and squint

If the beam points forward or backward (squint), the Doppler spectrum shifts away from zero. A broadside (unsquinted) beam has its Doppler spectrum centred on zero.

## 32. Zero Doppler processing: closer to a planimetric grid

Zero-Doppler geometry is closer to a planimetric (map) grid, so many prefer this output even when the data were naturally squinted forward or backward.

## 33. Zero Doppler processing: output as if acquired broadside

Zero-Doppler processors output the data as though they were acquired broadside. This is becoming the standard.

## 34. Learning more about SAR processing

Optional for students who want the mathematics behind SAR focusing.

## 35. SEASAT – SAR in space in 1978, with a SEASAT image of Death Valley

SEASAT (1978) was the first civilian SAR in space. The image shows Death Valley.

## 36. Conventional SAR modes: stripmap and ScanSAR

Stripmap: send a pulse, receive the echo, repeat; swath width is limited by ambiguities. ScanSAR repoints the beam across several sub-swaths for a wider swath, trading azimuth resolution for coverage.

## 37. Other wide-swath SAR modes: TOPS and SweepSAR

TOPS (terrain observation by progressive scans) steers the beam forward in azimuth during each burst to improve radiometry. SweepSAR (scan-on-receive) uses several receive beams to cover a wide swath.

## 38. Properties of radar images

Part 2: what a radar image actually shows, and why it looks so different from a photograph.

## 39. What radar can tell us

The radar transmits a known signal (amplitude, polarization, phase and time reference, wavelength). An object changes these differently at different wavelengths; comparing the received and transmitted signals tells us about the object.

## 40. Surface and volume scattering models for radar: particles and surfaces

Simple scattering models: a sphere moves through Rayleigh, resonant and optical scattering regimes as it grows relative to the wavelength. A large flat facet scatters like a mirror.

## 41. Surface and volume scattering models for radar: Rayleigh roughness

Combining smooth, rough, faceted and volume elements builds intuition. Rayleigh criterion: a surface looks smooth if its height variation δh < λ / (8 cos θ_i).

## 42. Surface and volume scattering models for radar: facet and Bragg scattering

Near nadir, facet (mirror-like) scattering dominates. At larger incidence angles, Bragg scattering from roughness at the scale of the wavelength dominates.

## 43. Radar imaging properties: foreshortening, layover and shadow

Radar images are distorted relative to a map: slopes facing the radar are foreshortened, very steep slopes collapse into layover, and areas hidden behind slopes are in shadow. Radar is sensitive to structure, optical images to chemistry; roughness relative to the wavelength sets brightness.

## 44. Wavelength – a measure of surface scale

Light interacts most strongly with objects about the size of the wavelength. Forest leaves reflect X-band (3 cm) but not L-band (24 cm); dry soils and ice look rough to X-band but not to L-band.

## 45. Polarization – a measure of surface orientations and properties

Vertically and horizontally polarized waves interact differently with surface orientation. A flat surface mostly reflects horizontal polarization. Colour composites of different polarizations reveal surface properties.

## 46. Radar equation in remote sensing

SNR = P_T · G_T · 1/(4πR²) · σ · 1/(4πR²) · A_R · ε / (kTB). Transmit power, antenna gain and area, range, target reflectivity σ, losses, noise temperature and bandwidth set the measurement sensitivity.

## 47. SAR imagery and speckle

Each resolution cell holds many scatterers. The received signal is their coherent sum, which varies randomly from pixel to pixel and gives SAR images their grainy look, called speckle.

## 48. Speckle and radiometric accuracy

Speckle masks the true backscatter, whatever the SNR. Averaging neighbouring pixels (multi-looking) reduces speckle and reveals the natural reflectivity, at the cost of resolution.

## 49. Geo-SInC: the InSAR short-course repository

All the material in this lecture comes from this repository. Point students to the EarthScope2024 folder, the newest version of the course. Most useful for geohazards: Day 2 (earthquake interferograms) and Days 4–5 (InSAR time series for subsidence and slow landslides with ARIA-tools and MintPy). The roadmap shown is from the 2024 course README.

## 50. Thank you. Questions?

Recap the seven questions from the start. Credits for the source material are on this slide.
