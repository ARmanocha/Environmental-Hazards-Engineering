# Lecture 1: Synthetic Aperture Radar Interferometry

**SAR principles and phenomenology** · presented by Akshay Raj Manocha

📄 **Slides:** [SAR_Interferometry_Akshay_Raj_Manocha.pdf](SAR_Interferometry_Akshay_Raj_Manocha.pdf) (50 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)

## What the lecture covers

1. **Introduction and motivation:** from raw radar echoes to amplitude images, phase, interferograms and modelling.
2. **Part 1: Basic principles of radar and SAR**
   - Waves and radar, radar frequency bands
   - Range resolution and range coding (worked example: 1,499 m uncoded vs 7.5 m coded)
   - Ground resolution against look angle and terrain slope (chart)
   - Beam dimensions, Doppler shift, aperture synthesis (worked example: 5 m azimuth resolution)
   - Quiz: radar resolution, with the answer
   - Range-Doppler coordinates, squint and zero-Doppler processing
   - SEASAT, and stripmap, ScanSAR, TOPS and SweepSAR modes
3. **Part 2: Properties of radar images:** scattering models, foreshortening, layover and shadow, wavelength, polarization, the radar equation, and speckle.
4. **Further resources:** the Geo-SInC InSAR short-course repository.

## Folder contents

| Path | What it is |
|------|------------|
| `SAR_Interferometry_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `figures/slides/` | The original course slide images, with the NASA and JPL logos removed |
| `figures/ground_resolution_chart.png` | Ground-range resolution vs look angle for 0°, 10° and 20° slopes |
| `figures/banner.png` | Title-slide banner of example SAR images |
| `media/SAR_imaging_animation.mp4` | NISAR animation of SAR imaging (45 s), shown on the "SAR imaging in action" slide |

## Notes on the source

- The notebook's parameter table lists a 20 μs pulse, but its range-resolution calculation uses 10 μs. The slides show both as in the notebook, and the speaker notes point this out.
- The notebook gives the speed of light as 299,792,456 m/s (a typo). The slides use 299,792,458 m/s; no result changes.
- In the quiz, the exact range resolution is c / (2 × 40 MHz) ≈ 3.75 m; option D's "3 m" is the closest choice.

## Credits

Content adapted from Paul A. Rosen, *SAR Principles and Phenomenology*, a notebook from the EarthScope (formerly UNAVCO) InSAR short course, 2021: [github.com/parosen/Geo-SInC](https://github.com/parosen/Geo-SInC) (`0.8_SAR_Theory_Phenomenology/SAR.ipynb`).
Contributors to the original content: Scott Hensley, Anthony Freeman, Jakob van Zyl, Piyush Agram and Howard Zebker.
Animation: NISAR mission.

The slide images and animation remain the work of their original authors. They are shared here for teaching only.
