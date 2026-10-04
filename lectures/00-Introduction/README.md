# Introduction: SAR and InSAR for Geohazards

**Radar satellites, ground motion and engineering** · presented by Akshay Raj Manocha

📄 **Slides:** [SAR_InSAR_Geohazards_Introduction_Akshay_Raj_Manocha.pdf](SAR_InSAR_Geohazards_Introduction_Akshay_Raj_Manocha.pdf) (41 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md)
🛰️ **Animations:** [satellite_orbit.html](animations/satellite_orbit.html) and [interferogram_fringes.html](animations/interferogram_fringes.html)

The starting point for the module, before [Lecture 1](../01-SAR-Interferometry/). It assumes no prior knowledge of radar.

## What the lecture covers

1. **Remote sensing and radar basics:** passive and active sensors, radar bands from X to P, how far each penetrates vegetation, and fifty years of radar satellites.
2. **What SAR is:** side-looking imaging, the synthetic-aperture idea, what makes a radar image bright or dark, and foreshortening, layover and shadow.
3. **What InSAR is:** phase and fringes (one Sentinel-1 fringe = 2.8 cm), the 1992 Landers earthquake, line-of-sight limits, time series (PS-InSAR and SBAS), and coherence.
4. **Satellites and orbits:** how radar satellites circle the Earth, Sentinel-1 in numbers, NISAR, and the satellites available today.
5. **Hazards and engineering:** earthquakes, volcanoes, landslides, land subsidence, infrastructure, floods and damage, and the workflow from data to decisions.
6. **Getting started:** strengths and limitations, free data and tools, a short quiz with answers, a recap, and how Lectures 1–3 follow on.

## The animations

Both run live on the online deck and in Present mode. In the PDF they appear as a single still frame. To show them in class from this repository, download the file and open it in any web browser. They need no internet connection.

| File | What it shows |
|------|---------------|
| `animations/satellite_orbit.html` | A near-polar radar satellite circling a rotating Earth: ascending and descending passes, the ground track, and the radar swath building up orbit by orbit (one orbit in about 5 seconds; satellite height and swath width exaggerated) |
| `animations/interferogram_fringes.html` | A simulated volcano swelling and relaxing, with its interferogram: every 2.8 cm of uplift adds one colour fringe (Sentinel-1 wavelength) |

The NISAR imaging animation shown on the NISAR slide is in [`../01-SAR-Interferometry/media/`](../01-SAR-Interferometry/media/).

## Folder contents

| Path | What it is |
|------|------------|
| `SAR_InSAR_Geohazards_Introduction_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide |
| `animations/` | The two animations as standalone web pages |
| `figures/` | Figures used in the deck, cropped from the course materials of Lectures 1 and 3 |

## Credits

Figures are reused from the EarthScope InSAR short-course materials ([github.com/parosen/Geo-SInC](https://github.com/parosen/Geo-SInC)): the InSAR theory slides by Molly Zebker and Ann Chen (after Paul A. Rosen and Scott Hensley) and the SAR lecture by Paul A. Rosen. Image credits include DLR, ESA, INGV and Massonnet et al. (1993). NISAR animation: NISAR mission. The orbit and fringe animations were made for this lecture.

Satellite details (launch dates, repeat cycles, data access) reflect the situation at the time of writing; check the mission websites for updates.
