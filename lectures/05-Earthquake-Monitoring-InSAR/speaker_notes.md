# Earthquake Monitoring with InSAR — speaker notes

## 1. Earthquake Monitoring with InSAR

This lecture applies InSAR to earthquakes: the sudden displacement of the ground in an earthquake, the slow strain that builds up between earthquakes, and the movement that continues afterwards. The strip at the bottom is a simulated interferogram of a strike-slip earthquake.

## 2. Use satellite radar to map how the ground moved in an earthquake, find the fault that slipped, and measure the strain building up for the next one.

Seismometers record the shaking; InSAR records where the ground ended up. The two together tell us which fault moved, how much, and where stress is still building.

## 3. Outline

Six parts: the earthquake cycle, reading coseismic interferograms, fault modelling, the slow phases before and after, real cases, and engineering use.

## 4. Earthquakes and the earthquake cycle

Part 1: Faults, elastic rebound, magnitude, and what InSAR adds.

## 5. Three ways a fault can move

Rake describes the slip direction on the fault: 0° or 180° is strike-slip, +90° is thrust, −90° is normal. The three simulated interferograms in Part 2 use exactly these three cases.

## 6. The earthquake cycle

This is the elastic rebound idea: the plates move steadily, but the fault is stuck, so the rocks near it bend elastically. When the stress exceeds the fault's strength, it slips and the bent rocks snap back. The next slide animates it.

## 7. Elastic rebound: bend, snap, repeat

Animation in map view: a road crosses a locked right-lateral fault. While the fault is locked, the road bends; in the earthquake it snaps back and is cut by a permanent offset; then strain builds again. Reid proposed this after measuring survey lines across the San Andreas Fault before and after the 1906 San Francisco earthquake.

## 8. How big? Moment magnitude

InSAR gives the fault area and slip directly from the surface displacement, so it gives the moment, and so the magnitude, independently of seismometers. Moment values in the table are computed with μ = 30 GPa.

## 9. What InSAR adds to seismology

Massonnet and colleagues (1993) published the Landers interferogram in Nature: the first time a whole earthquake's deformation field was seen at once. Since then, almost every large shallow continental earthquake has been imaged.

## 10. Coseismic interferograms

Part 2: Reading the fringes of strike-slip, thrust and normal earthquakes.

## 11. What each kind of earthquake looks like

All three are magnitude 7.0 earthquakes. Strike-slip: lobes of opposite sign on each side of the fault. Thrust: a big lobe of uplift over the hanging wall, smaller subsidence beyond. Normal: the reverse, a deep subsidence bowl. The grey areas are where fringes are too dense to count: in real data this is also where coherence is lost.

## 12. One earthquake, many views

The ascending line of sight is mostly east-west plus vertical, with only about 11% of any north-south motion. North-south striking strike-slip faults, such as the Sagaing Fault in Myanmar, are therefore the hardest case for InSAR. Case study in Part 5.

## 13. Reading a coseismic interferogram

A good exercise: give students the three simulated interferograms without titles and ask them to identify the fault type, the side that moved up, and the approximate displacement by counting fringes.

## 14. Near the fault: too many fringes

For the largest earthquakes, offset tracking maps the rupture trace and the metres of slip right at the fault, while interferometry measures the centimetres farther away. The two are combined in the fault model.

## 15. From fringes to the fault

Part 3: Fault models, inversion and magnitude from geodesy.

## 16. A fault model predicts the fringes

Real slip is not uniform: in practice the fault is divided into many small patches, each with its own slip, and the same equations are summed. The ground is not uniform either, so layered-earth models are used for detailed work.

## 17. Inversion: from fringes back to the fault

This is a real inversion run on the simulated data: five unknowns (slip, dip, top and bottom depth, position) fitted by nonlinear least squares. Note the trade-off: a little more slip on a slightly narrower fault fits nearly as well, so individual parameters are uncertain but the moment, and so the magnitude, is well constrained.

## 18. What fault models tell us

Fault models from InSAR feed directly into aftershock forecasts (stress change on nearby faults) and into the next generation of seismic hazard maps.

## 19. Before and after the earthquake

Part 4: Strain build-up, seismic hazard, afterslip and triggered hazards.

## 20. Between earthquakes: measuring the strain

The arctan model is from Savage and Burford (1973). A shallow locking depth gives a sharp step; a deep one a gentle curve. Real signals are only a few mm/yr spread over tens of km, so long time series, atmospheric correction and a stable reference frame are essential.

## 21. From strain to seismic hazard

Example of creeping sections: parts of the central San Andreas Fault and the North Anatolian Fault near İsmetpaşa. Creep shows up in InSAR as a sharp step in velocity right at the fault, rather than a smooth arctan curve. The 10 m figure is simple arithmetic to show the scale, not a forecast for any particular segment.

## 22. After the earthquake, the ground keeps moving

A coseismic pair always includes a few days of afterslip, because the second image comes days after the earthquake. Afterslip matters for engineering: structures across the fault keep moving, and aftershocks often cluster where afterslip is fast.

## 23. Earthquakes trigger other hazards

The 2015 Gorkha earthquake triggered thousands of landslides in Nepal, and the landslide hazard stayed high through the following monsoons. This links back to Lecture 4.

## 24. Case studies

Part 5: Gorkha 2015, Türkiye 2023, Myanmar 2025 and rapid-response services.

## 25. Gorkha, Nepal, 2015

Nearly 9,000 people died. The earthquake shows why InSAR matters in the Himalaya: no surface rupture to map in the field, yet the satellites showed exactly where the fault slipped and where it did not.

## 26. Kahramanmaraş, Türkiye, 2023

Strike-slip ruptures on the East Anatolian Fault system. The Sentinel-1 pixel-offset maps showed the full rupture traces within days, faster than field teams could walk them.

## 27. Mandalay, Myanmar, 2025

A perfect illustration of the geometry slide in Part 2: a north-south strike-slip fault moves mostly in the direction InSAR sees worst. Shaking caused damage as far away as Bangkok.

## 28. Rapid response from space

Within a week of a large earthquake there is now usually a public coseismic interferogram, a rupture map from offsets, a fault model and a damage proxy map. LiCSAR products are free on the COMET-LiCS portal (Lazecký et al., 2020).

## 29. Engineering practice

Part 6: Fault rupture, damage mapping, limits and exercises.

## 30. Where engineers use earthquake InSAR

Fault displacement design is a classic geotechnical problem: a buried pipeline crossing a strike-slip fault must stretch or bend without breaking when the fault moves. InSAR and offset maps from past earthquakes give realistic offsets and widths of the deformation zone.

## 31. Damage proxy maps from coherence

This is the ARIA approach (Yun et al., 2015). It works best in towns, where coherence is normally high and stable. It is a proxy: it says where something changed, not what or how badly.

## 32. Limits and good practice

InSAR cannot predict earthquakes. It measures where strain is building and how a fault moved; the timing of the next earthquake remains uncertain.

## 33. Try these

Sentinel-1: wavelength 5.55 cm, one fringe = 2.8 cm. Ascending line of sight (ground to satellite): about −0.62 east, −0.11 north, +0.78 up. Mw = ⅔ (log₁₀ M₀ − 9.1).

## 34. Answers

Exercise 4 is the Myanmar lesson in numbers: the same motion gives a signal about six times smaller when it is north-south.

## 35. Key points

The whole lecture in five lines.

## 36. References

Elliott, Walters and Wright (2016) is the best single review to start with.

## 37. Thank you. Questions?

Credits and sources are on this slide and the references slide.
