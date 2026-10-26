# Practical 1: InSAR processing in SNAP, step by step

**Kīlauea, Hawai‘i, 2 → 8 May 2018** · Akshay Raj Manocha

In this practical you turn two Sentinel-1 radar images into a map of how far the ground moved at Kīlauea when the 2018 eruption began and a magnitude 6.9 earthquake struck its south flank. Follow the steps in order. Each step gives:
- the menu path;
- the settings to use;
- the name SNAP gives the output;
- a check to make before you move on.

The slides for this session are [InSAR_Processing_with_SNAP_Akshay_Raj_Manocha.pdf](InSAR_Processing_with_SNAP_Akshay_Raj_Manocha.pdf). Steps 1–13 below match steps 1–13 in the slides.

| | |
|---|---|
| **Software** | ESA SNAP 12 with the Microwave Toolbox, and SNAPHU. Menus are almost the same in SNAP 10 and 11. |
| **Data** | Two Sentinel-1 IW SLC images, track 124, ascending: 2 May 2018 (reference) and 8 May 2018 (secondary) |
| **Computer** | 16 GB of memory recommended (8 GB minimum), about 30 GB of free disk space, internet access |
| **Time** | 2 to 3 hours for a first pair; download the data before the session |

---

## Contents

- [Part A: Before the session](#part-a-before-the-session)
- [Part B: Processing, steps 1 to 13](#part-b-processing-steps-1-to-13)
- [Part C: Check your result](#part-c-check-your-result)
- [Part D: Automate with the Graph Builder](#part-d-automate-with-the-graph-builder)
- [Part E: Troubleshooting](#part-e-troubleshooting)
- [Part F: What to hand in](#part-f-what-to-hand-in)

---

## Part A: Before the session

### A1. Install SNAP

1. Download the installer for your system from [step.esa.int](https://step.esa.int/main/download/snap-download/). Choose the version that includes the Microwave Toolbox (for Sentinel-1).
2. Run the installer and accept the defaults. At the end, allow SNAP to update itself.
3. Open SNAP and run **Help › Check for Updates**. Older versions can fail to download orbit files, because the orbit servers moved in 2023.
4. Give SNAP more memory: **Tools › Options › Performance**. Set the memory to about 70% of your computer's RAM, then restart SNAP.

### A2. Install SNAPHU, the phase-unwrapping program

**Windows and Linux: use the SNAP plugin**

1. Go to **Tools › Plugins › Available Plugins**, search for **SNAPHU Unwrapping**, tick it and click **Install**. Restart SNAP.
2. The first time you run **Snaphu-unwrapping** (step 10), SNAP asks for a working folder and downloads the SNAPHU program. Accept.
3. Linux only: make the program executable once:

```bash
chmod +x $HOME/.snap/auxdata/snaphu-v1.4.2_linux/bin/snaphu
```

The folder name may differ slightly with the version.

**macOS, or if the plugin fails:** install SNAPHU yourself, for example with conda:

```bash
conda install -c conda-forge snaphu
```

You can also download it from the [SNAPHU page on the STEP website](https://step.esa.int/main/snap-supported-plugins/snaphu/). In step 10 you will then run SNAPHU from a terminal. The exact command is given there.

### A3. Get a free data account

Create a free **NASA Earthdata** login at [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov). It is used by ASF Vertex. A Copernicus Data Space account ([dataspace.copernicus.eu](https://dataspace.copernicus.eu)) also works.

### A4. Download the two images

1. Open **ASF Vertex**: [search.asf.alaska.edu](https://search.asf.alaska.edu). Sign in.
2. **Dataset:** Sentinel-1.
3. **Area:** zoom to the Island of Hawai‘i and draw a small box over Kīlauea. The summit is at about 19.41° N, 155.28° W, and Leilani Estates at about 19.47° N, 154.91° W.
4. **Filters:**

   | Filter | Value |
   |---|---|
   | Start date | 1 May 2018 |
   | End date | 9 May 2018 |
   | Beam mode | IW |
   | File type | L1 Single Look Complex (SLC) |
   | Direction | Ascending |
   | Path | 124 |

5. You should see one scene on **2 May 2018** and one on **8 May 2018**. Check that both have **Path 124**, the same frame, and cover Kīlauea's summit and East Rift Zone.
6. Add both to the queue, then download them. Each is a zip file of a few gigabytes.
7. **Do not unzip them.** SNAP opens the .zip files directly.

> **Choosing your own pair later:** use the same track and pass direction, a short time gap (6–24 days), a small perpendicular baseline (under about 150 m; use the **Baseline** tool in Vertex), and no snow.

### A5. Set up a working folder

Make one folder with a short path and **no spaces**, for example `C:\insar\kilauea` or `~/insar/kilauea`. Put both zip files in it. Save every output product there.

---

## Part B: Processing, steps 1 to 13

SNAP adds a suffix to the file name at each step. The table shows the defaults, so you can always tell which product to use next.

| Step | Operator | Suffix added |
|---|---|---|
| 2 | S-1 TOPS Split | `_split` |
| 3 | Apply Orbit File | `_Orb` |
| 4 | Back-Geocoding (+ ESD) | `_Stack` (`_esd`) |
| 5 | Interferogram Formation | `_ifg` |
| 6 | TOPS Deburst | `_deb` |
| 7 | Topographic Phase Removal | `_dinsar` |
| 8 | Multilooking | `_ML` |
| 9 | Goldstein Phase Filtering | `_Flt` |
| 10 | SNAPHU Import | add `_unw` yourself |
| 11 | Phase to Displacement | `_dsp` |
| 12 | Terrain Correction | `_TC` |

Keep **BEAM-DIMAP** as the output format until step 13.

### Step 1 · Open the two images and check them

**Menu:** File › Open Product

1. Select both zip files and click **Open**.
2. In the Product Explorer, expand each product and open **Metadata › Abstracted_Metadata**.
3. Check the values in this table.

| Check | Expected |
|---|---|
| `MISSION` | SENTINEL-1A or SENTINEL-1B |
| `ACQUISITION_MODE` | IW |
| `PRODUCT_TYPE` | SLC |
| `REL_ORBIT` | 124 for both |
| `PASS` | ASCENDING for both |
| `first_line_time` | 2 May and 8 May 2018 |

4. Open **View › Tool Windows › World View** (or World Map) to check that both footprints cover Kīlauea.

✅ **Check:** same relative orbit and pass for both images. The 2 May image is the **reference**; the 8 May image is the **secondary**.

### Step 2 · TOPS Split: keep only the bursts you need

**Menu:** Radar › Sentinel-1 TOPS › S-1 TOPS Split

1. **I/O Parameters:** the 2 May product as source.
2. **Processing Parameters:**

   | Setting | Value |
   |---|---|
   | Subswath | The one covering Kīlauea's summit, East Rift Zone and south flank |
   | Polarisations | VV |
   | Bursts | 3–4 bursts covering the summit to Leilani Estates and the coast |

3. Find the right subswath: try IW1, IW2 and IW3 in turn and look at the burst outlines in the preview map.
4. Drag the two grey triangles to keep only the bursts over the target. Write down the subswath and burst numbers.
5. Click **Run**. Then repeat for the 8 May product with **exactly the same subswath and bursts**.

✅ **Check:** two `_split` products. The area should be a few tens of kilometres across, not the whole image.

> If the target falls across two subswaths, split and process both. Then join them after step 6 with **Radar › Sentinel-1 TOPS › S-1 TOPS Merge**.
>
> **Sentinel-1A and 1B:** these images can be shifted along track, so the same place may have different burst numbers in the two images. Always check the preview.

### Step 3 · Apply precise orbits

**Menu:** Radar › Apply Orbit File

| Setting | Value |
|---|---|
| Source | The `_split` product |
| Orbit State Vectors | Sentinel Precise (Auto Download) |
| Polynomial Degree | 3 |
| Do not fail if new orbit file is not found | Ticked |

Run it once for each `_split` product.

✅ **Check:** two `_split_Orb` products. Open the Processing_Graph metadata. If it says the orbit file was not found, SNAP fell back to less accurate orbits. Retry later or update SNAP.

### Step 4 · Coregister the images (Back-Geocoding, then ESD)

**Menu:** Radar › Coregistration › S1 TOPS Coregistration › S1 Back Geocoding

| Tab / setting | Value |
|---|---|
| ProductSet-Reader | Add both `_split_Orb` products; the **2 May** product first |
| Digital Elevation Model | SRTM 1Sec HGT (Auto Download) or Copernicus 30m Global DEM |
| DEM resampling | BICUBIC_INTERPOLATION (default) |
| Resampling type | BISINC_5_POINT_INTERPOLATION (default) |
| Mask out areas without elevation | Ticked |

Then, because you kept more than one burst:

**Menu:** Radar › Coregistration › S1 TOPS Coregistration › S1 Enhanced Spectral Diversity, with the default settings, on the `_Stack` product.

✅ **Check:** the `_Stack_esd` product has i, q and Intensity bands for both dates (names ending in `_02May2018` and `_08May2018`).

Make an RGB image to check the alignment:
1. Right-click the product › **Open RGB Image Window**.
2. Choose the reference intensity for red and green, and the secondary intensity for blue.
3. Zoom in on the coast.

A sharp grey image means the alignment is good. Coloured fringes at edges mean it failed. The exception is new lava, which really did change between the dates.

### Step 5 · Form the interferogram

**Menu:** Radar › Interferometric › Products › Interferogram Formation

| Setting | Value |
|---|---|
| Source | The `_Stack_esd` product |
| Subtract flat-earth phase | Ticked |
| Subtract topographic phase | **Not ticked** (we do it in step 7). If you tick it, choose the same DEM and skip step 7. |
| Include coherence estimation | Ticked |
| Coherence window | 10 (range) × 3 (azimuth) |

✅ **Check:** open the `Phase_ifg_…` and `coh_…` bands. You will see fringes that follow the volcano's shape, which is topography, and black lines between bursts. Coherence should be bright over the summit and old lava, and dark over forest and the sea.

### Step 6 · Deburst

**Menu:** Radar › Sentinel-1 TOPS › S-1 TOPS Deburst

| Setting | Value |
|---|---|
| Source | The `_ifg` product |
| Polarisations | VV |

✅ **Check:** one continuous image with no black lines between bursts. If you processed two subswaths, merge them now with **S-1 TOPS Merge**.

### Step 7 · Remove the topographic phase

**Menu:** Radar › Interferometric › Products › Topographic Phase Removal

| Setting | Value |
|---|---|
| Source | The `_deb` product |
| Digital Elevation Model | The same DEM as in step 4 |
| Output elevation band | Ticked (useful for checking atmospheric effects later) |

✅ **Check:** the fringes that followed the topography have gone. What remains is deformation, atmosphere and noise. For 2 → 8 May 2018, expect dense fringes over the south flank and along the East Rift Zone.

### Step 8 · Multilook

**Menu:** Radar › SAR Utilities › Multilooking (in some versions under Raster › SAR Utilities)

| Setting | Value |
|---|---|
| Source | The `_dinsar` product |
| Source bands | Leave all bands selected: SNAP averages the complex i and q bands and recomputes the phase. Never average the wrapped phase on its own. |
| Looks | Independent Looks |
| Range × azimuth looks | **8 × 2** for Kīlauea (4 × 1 for cleaner, smaller areas) |

✅ **Check:** the image is smaller and less noisy. Pixels are now about 30 m. The fringes must still be clearly separated; if they blur together, use fewer looks.

### Step 9 · Filter the phase (Goldstein)

**Menu:** Radar › Interferometric › Filtering › Goldstein Phase Filtering

| Setting | Value |
|---|---|
| Source | The `_ML` product |
| Adaptive filter exponent | 1.0 |
| FFT size | 64 |
| Window size | 3 |
| Use coherence mask | Optional; threshold 0.2 |

✅ **Check:** the fringes are smoother, with sharp edges. Compare with the unfiltered phase from step 8. A fringe that appears only after filtering is probably noise.

**Optional subset:** to speed up unwrapping, use **Raster › Subset** on the `_Flt` product to keep just the area of interest.
1. Draw a box in the preview.
2. Save the subset with **File › Save Product As** before continuing.

### Step 10 · Unwrap the phase with SNAPHU

Unwrapping has three parts: export, unwrap, import.

**10a. Export**

**Menu:** Radar › Interferometric › Unwrapping › Snaphu Export

| Setting | Value |
|---|---|
| Source | The `_Flt` product (or your saved subset) |
| Target folder | Your working folder (short path, no spaces) |
| Statistical-cost mode | DEFO |
| Initial method | MCF |
| Number of tile rows × columns | 1 × 1 for images under about 3,000 × 3,000 pixels; otherwise 4 × 4 or more |
| Row and column overlap | 200 pixels (when using tiles) |
| Number of processors | The number of cores on your computer |

SNAP creates a folder named after the product. It contains:
- the wrapped phase (.img and .hdr);
- the coherence (.img and .hdr);
- an empty unwrapped-phase header;
- `snaphu.conf`.

**10b. Unwrap: with the plugin**

**Menu:** Radar › Interferometric › Unwrapping › Snaphu-unwrapping
1. **Source product:** the same product you exported.
2. **Output folder:** the folder that Snaphu Export created.
3. Tick **Display execution output** and click **Run**. Wait for "Finished tool execution".

**10b. Unwrap: by hand, in a terminal (macOS, or if the plugin fails)**
1. Open `snaphu.conf` in a text editor. Near the top, a commented line gives the command, for example:

```bash
snaphu -f snaphu.conf Phase_ifg_VV_02May2018_08May2018.snaphu.img 2843
```

2. In a terminal, go to the export folder and run that line without the `#`:

```bash
cd ~/insar/kilauea/<export folder>
snaphu -f snaphu.conf Phase_ifg_VV_02May2018_08May2018.snaphu.img 2843
```

The last number is the image width in pixels. Use the one in **your** file.

**10c. Import**

**Menu:** Radar › Interferometric › Unwrapping › Snaphu Import

| Tab | Setting |
|---|---|
| 1-Read-Phase | The product you exported (the `_Flt` product or subset) |
| 2-Read-Unwrapped-Phase | The `UnwPhase_ifg_…snaphu.hdr` file in the export folder |
| 3-SnaphuImport | Leave "Do NOT save Wrapped interferogram" **unticked** |
| 4-Write | Add `_unw` to the name |

✅ **Check:** open `Unw_Phase_ifg_…`. It should change smoothly, with no 2π jumps.
- Sudden steps or a blocky pattern mean unwrapping errors. Mask low coherence, filter more, or change the tiles, then delete the old `UnwPhase…img` and run again.
- You can also try the SMOOTH cost mode or the MST initial method.

### Step 11 · Convert phase to displacement

**Menu:** Radar › Interferometric › Products › Phase to Displacement

- **Source:** the `_unw` product. There are no other settings.
- **Output:** line-of-sight (LOS) displacement in metres, d = −λ·φ/4π, with λ = 5.55 cm. One fringe = 2.8 cm.
- **Sign:** positive values mean motion **towards** the satellite, for example uplift. Negative values mean motion **away**, for example subsidence or eastward motion for this ascending pass.

**Carry the coherence across.** Phase to Displacement does not copy the coherence band, but you need it for masking.
1. Right-click the `_dsp` product › **Band Maths**.
2. Name the band `coherence` and **untick Virtual**.
3. Click **Edit Expression**. Switch the product list to the `_unw` product and double-click its `coh_…` band.
4. Click OK twice, then **File › Save Product**.

**Set a reference area.** SNAPHU's zero is arbitrary.
1. Draw a rectangle on stable ground with good coherence, far from Kīlauea's summit, rift zones and south flank. For example, use an area north of the East Rift Zone, towards Hilo, if it is inside your bursts.
2. Open **Analysis › Statistics**, tick **Use ROI mask** and read the **mean** of the displacement band.
3. Use **Band Maths** to make a new, non-virtual band: `displacement - (mean)`. Use the mean you just read, and your band's exact name.

✅ **Check:** values near zero in the reference area. On the south flank, expect tens of centimetres of LOS motion **away** from the satellite (negative).

### Step 12 · Terrain correction (geocoding)

**Menu:** Radar › Geometric › Terrain Correction › Range-Doppler Terrain Correction

| Setting | Value |
|---|---|
| Source | The `_dsp` product (with the referenced displacement and coherence bands) |
| Source bands | The referenced displacement band and coherence |
| Digital Elevation Model | The same DEM as in step 4 |
| Pixel spacing | 30 m (or 15 m) |
| Map projection | WGS84 (geographic) for Google Earth; UTM Zone (automatic) for QGIS |

✅ **Check:** the image is now north-up and matches the real shape of the island. Turn on **World View** or a coastline layer to confirm.

### Step 13 · Export and make a map

1. **Mask low coherence:** right-click the displacement band › **Properties** › **Valid-Pixel Expression** = `coherence > 0.3`.
2. **Colours:** in **Colour Manipulation**, choose a blue–white–red palette, set it symmetric around zero, and set the range to about −0.5 to +0.5 m.
3. **GeoTIFF for QGIS:** File › Export › GeoTIFF. Choose the displacement and coherence bands.
4. **KMZ for Google Earth:** File › Export › Other › View As Google Earth KMZ. This needs the WGS84 projection.
5. **In QGIS:**
   - Add the GeoTIFF over a hillshade or satellite basemap.
   - Draw the profile A–B from the summit to the south coast with the **Profile Tool** plugin.

A good InSAR map shows:
- [ ] the two dates (2 May → 8 May 2018);
- [ ] the satellite, track 124 and the ascending pass;
- [ ] an arrow for the line of sight (looking east from the west);
- [ ] a colour bar in cm, with the sign explained;
- [ ] low-coherence areas masked;
- [ ] a scale bar and a north arrow.

---

## Part C: Check your result

Compare your map with the automatic COMET-LiCSAR result for the same pair: frame `124A_06996_091406`, interferogram `20180502_20180508`. Download its unwrapped phase and coherence (GeoTIFF, free, Open Government Licence):

- [20180502_20180508.geo.unw.tif](https://data.ceda.ac.uk/neodc/comet/data/licsar_products/124/124A_06996_091406/20180502_20180508/20180502_20180508.geo.unw.tif)
- [20180502_20180508.geo.cc.tif](https://data.ceda.ac.uk/neodc/comet/data/licsar_products/124/124A_06996_091406/20180502_20180508/20180502_20180508.geo.cc.tif)

LiCSAR's unwrapped phase is in radians. Multiply it by −0.0555 / (4π) to get metres, with positive meaning towards the satellite, as in SNAP. Then subtract the mean of the same stable area you used in step 11.

What you should see:
- **South flank:** a broad area moving **away** from the satellite, up to about half a metre. This is the M6.9 earthquake on 4 May, with the flank sliding seaward and sinking.
- **East Rift Zone:** a narrow, sharp pattern along the rift near Leilani Estates, where magma pushed the ground apart.
- **Low coherence:** fresh lava, dense forest on the east, and the sea.
- **Mauna Loa and Mauna Kea:** fringes that follow height on these tall volcanoes are probably atmospheric (water vapour), not deformation.

If your pattern matches but the values are offset, check your reference area (step 11). If the patterns differ, check the unwrapping (step 10).

---

## Part D: Automate with the Graph Builder

Once one pair works, save the chain so the next pair takes minutes.

1. Open **Tools › GraphBuilder**.
2. Right-click › **Add** the operators in this order:
   - `Read` (×2)
   - `TOPSAR-Split` (×2)
   - `Apply-Orbit-File` (×2)
   - `Back-Geocoding`
   - `Enhanced-Spectral-Diversity`
   - `Interferogram`
   - `TOPSAR-Deburst`
   - `TopoPhaseRemoval`
   - `Multilook`
   - `GoldsteinPhaseFiltering`
   - `Write`
3. Connect them by dragging from each operator to the next. The two Read → Split → Orbit branches join at Back-Geocoding.
4. Set each tab with the values from steps 2–9. Click **Save** to write the graph as an XML file, for example `kilauea_steps2-9.xml`.
5. To run the same graph on many pairs, use **Tools › Batch Processing**. Or run it from a terminal with SNAP's Graph Processing Tool:

```bash
gpt kilauea_steps2-9.xml
```

A second graph can do steps 11–12: Read → Phase to Displacement → Terrain Correction → Write.

---

## Part E: Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| Back-Geocoding fails, or the images do not overlap | Different tracks, or different bursts kept | Check `REL_ORBIT`; redo TOPS Split with matching bursts (check the preview) |
| Orbit or DEM download error | No internet, server busy, or an old SNAP version | Retry later; run Help › Check for Updates; try the Copernicus 30m DEM |
| SNAP runs out of memory or is very slow | Too many bursts for the RAM | Keep fewer bursts; raise memory in Tools › Options › Performance; close other programs |
| Phase jumps at burst edges | ESD skipped | Run Enhanced Spectral Diversity after Back-Geocoding |
| Interferogram is pure noise | Low coherence: long gap, vegetation or snow, or wrong pair | Check the dates; multilook more; choose a shorter pair |
| Snaphu-unwrapping does nothing | Plugin not set up, or a path with spaces | Tools › Manage External Tools › Snaphu-unwrapping › check the paths; use a folder without spaces; or run SNAPHU by hand (step 10b) |
| Snaphu Import fails | Wrong product in tab 1, or the unwrapped .img is missing | Select the same product you exported; check that `UnwPhase…img` exists in the export folder |
| Unwrapped result has steps or blocks | Unwrapping errors in noisy areas or at tile edges | Mask coherence below 0.3, filter more, change the tiles or overlap, delete the old output and unwrap again |
| Displacement looks shifted overall | No reference area | Subtract the mean of a stable area (step 11) |
| Map is mirrored or slanted | Step 12 not done | Run Range-Doppler Terrain Correction |

---

## Part F: What to hand in

1. **Your map** (Step 13), with all six items in the checklist.
2. **A profile** from the summit to the south coast, with distance in km and LOS displacement in cm.
3. **Short answers:**
   1. What is the largest LOS displacement on the south flank, and in which direction? What two kinds of motion could cause it for an ascending pass?
   2. How many fringes did you count on the wrapped phase along your profile? Does fringes × 2.8 cm agree with your unwrapped values?
   3. Where is coherence low, and why?
   4. How does your map compare with the COMET-LiCSAR result? Explain any difference.
   5. Why would a descending pair over the same dates help you separate vertical from horizontal motion?

**Going further:**
- Process the earlier pair, **20 April → 2 May 2018**. It shows magma moving along the rift before the eruption.
- Try another volcano: Etna, December 2018; Sierra Negra, June 2018; or Campi Flegrei.

---

**Credits.**
- Software: ESA SNAP ([step.esa.int](https://step.esa.int)); SNAPHU by C. W. Chen and H. A. Zebker, Stanford University.
- Sentinel-1 data: EU Copernicus programme and ESA.
- COMET-LiCSAR products: modified Copernicus Sentinel data 2018, analysed by the Centre for the Observation and Modelling of Earthquakes, Volcanoes and Tectonics (COMET). Lazecký and Maghsoudi (2022), LiCSAR interferometry products, NERC EDS CEDA, Open Government Licence v3.
- Event facts: USGS Hawaiian Volcano Observatory.

The workflow follows ESA's *TOPS Interferometry Tutorial*. Menu names can move slightly between SNAP versions; if a menu is not where this guide says, use the search box at the top right of SNAP.
