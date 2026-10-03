# Lecture 2: Geometric Aspects of InSAR

**Synthetic Aperture Radar Interferometry** · presented by Akshay Raj Manocha

📄 **Slides:** [InSAR_Geometry_Akshay_Raj_Manocha.pdf](InSAR_Geometry_Akshay_Raj_Manocha.pdf) (44 slides)
🗒️ **Speaker notes:** [speaker_notes.md](speaker_notes.md), including the homework solution

Builds on [Lecture 1](../01-SAR-Interferometry/), so students should review it first.

## What the lecture covers

1. **Interferometry:** phase and distance, wave interference, SAR interferometry, the interferogram.
2. **Interferometry for topography:** the interferometric triangle, single-pass modes (classic p = 1, ping-pong p = 2), the parallel baseline, phase gradient and fringe rates, flattened phase, ambiguity height (worked example: 693 m).
3. **Differential interferometry:** repeat-pass phase, the deformation sign convention, separating topography from displacement, line-of-sight sensitivity, topographic vs displacement sensitivity (0.0091 vs 52.36 rad/m).
4. **Phase unwrapping and error sources:** wrapped and unwrapped phase, the error budget (phase noise, DEM, atmosphere, baseline), with the Mount Etna DEM and Hawaii troposphere examples.
5. **Homework** (flat-Earth fringe rate), further reading and the Geo-SInC repository.

It has five quizzes, each followed by an answer slide.

## Folder contents

| Path | What it is |
|------|------------|
| `InSAR_Geometry_Akshay_Raj_Manocha.pdf` | The full slide deck |
| `speaker_notes.md` | Talking points for every slide, with the homework solution |
| `figures/` | The notebook's 16 diagrams (wave interference, baselines, unwrapping, DEM and troposphere examples) |
| `equations/` | Every equation in the lecture, rendered as a transparent PNG for reuse |

## Notes on the source

- The notebook writes the height of the ground point as "z = h = ρ cos θ"; the slides use the intended z = h − ρ cos θ.
- The notebook places the "linear or quadratic phase variation" remark next to the DEM error term. The slides attach it to the baseline-calibration error, which produces those smooth ramps (as the baseline-error quiz shows).
- The homework does not state p. The solution in the speaker notes gives both p = 1 and p = 2. At near range the perpendicular baseline is zero, so the fringe rate is zero.
- Author names in the reading list are corrected to Rodríguez and Bürgmann.

## Credits

Content adapted from Paul A. Rosen and Scott Hensley, *Geometric Aspects of InSAR*, a notebook from the EarthScope (formerly UNAVCO) InSAR short course, 2021: [github.com/parosen/Geo-SInC](https://github.com/parosen/Geo-SInC) (`1.3_InSAR_theory/InSAR.ipynb`).
Wave-interference figure © 2006 Encyclopædia Britannica, Inc.

The figures remain the work of their original authors. They are shared here for teaching only.
