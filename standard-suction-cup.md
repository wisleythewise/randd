# The Standard Suction Cup — From Measured Load to a Simulation Curve

*Engineering reference · 2026-10-28 · Source: the local `gripper-config` working tree.*

[Open the interactive 3D explanation](suction-cup-curve.html) · [R&D index](index.html)

## What this note describes

Our standard cup is the **office cup**, profile ID `office`: the existing Ø41 mm cup used in the gripper. The source stores an axial loading fit at approximately −60 kPa gauge vacuum, a separate pull-off observation, and a simulator model derived from them. It does not identify the cup as a particular VMECA product.

The useful distinction is between **the measured loading fit**, **the change of reference made for simulation**, and **the provisional contact laws**. A smooth curve is not evidence that every point on it was measured.

The READMEs describe the model and its measurement limits. The actual coefficients live in `gripper_sim/settings.py`; the contact law lives in `gripper_sim/physics.py`. No original mass/height sample table, fit script, residuals, uncertainty estimates, repeated trials, or complete bench protocol was found in the inspected source files. Consequently this note reconstructs the equations from the stored coefficients; it cannot reproduce the original regression or claim a fitting algorithm or fit quality.

## Standard cup specifications and their status

| Property | Value | Meaning / source status |
| --- | --- | --- |
| Profile ID | `office` | Default simulator profile |
| Display name | Office cup · Ø41 mm · measured | `catalog.py` |
| Nominal diameter | 41 mm | Office profile |
| Outside lip diameter | 41 mm | Office profile |
| Packing envelope diameter | 41 mm | Maximum of lip and visual bellows diameter; GEO-03 requirement |
| Free height | 47 mm | Unloaded, without a box; GEO-03 and stored model input |
| Working height for design | 28 mm | With a box attached; GEO-03 packaging requirement |
| Simulator sealed reference | 27.351 mm | Stored calibration reference, not interchangeable with the 28 mm design requirement |
| Original fit zero-load height | 28.723 mm | Stored original-fit reference |
| Reference shift | 1.372 mm | Original fit translated downward for the simulation; explicitly UNVALIDATED |
| Bellows diameter in the renderer | 38 mm | Illustrative legacy geometry, not a measured/vendor dimension |
| Number of folds | Unconfirmed | `folds=0` means unspecified, not a zero-fold cup |
| Catalogue overall height | 47 mm | Same as free height in the office profile; no separate fitting dimension established |
| Catalogue lip stroke | Unspecified | `lip_stroke_mm=0` is a placeholder; not evidence of zero physical travel |
| Approximate test vacuum | −60 kPa gauge | Stored reference; magnitude is entered as positive 60 kPa in the simulator |
| Loading fit range | Through 3.77 kg equivalent / 36.9710705 N | Source-reported measured range |
| Pull-off observation | 4.2 kg equivalent / 41.18793 N | Separate observation, interpreted per cup in the simulator; fixture/surface applicability remains unconfirmed |
| Gravity used | 9.80665 m/s² | Mass-to-force conversion |
| Brand, part number, rubber material, hardness | Not recorded | Do not infer these from the shape or diameter |
| Thread, fitting, wall thickness, rated stroke, temperature range, lifetime | Not recorded | Need physical inspection or manufacturer documentation |

The 47 mm free height and 28 mm working height imply about **19 mm of packaging compression**. They do not establish a permissible tensile stroke. The curve can extend past the free height; no physical travel limit is calibrated in the current simulation.

## 1. How the measured relationship becomes an equation

The stored constants are `A = 0.001372 m`, `B = g / 0.7669 N`, original fit zero height `0.028723 m`, and sealed reference `0.027351 m`. Since `28.723 − 27.351 = 1.372 mm`, the original exponential height law consistent with these constants can be reconstructed as:

```text
h_original_cm(m) = 2.7351 + 0.1372 × exp(0.7669 × m)
```

Here `m` is equivalent suspended mass in **kg**, not force in newtons; the coefficient 0.7669 has units kg⁻¹. This expression is reconstructed from the stored model, not quoted from an original regression sheet. At zero load it predicts **2.8723 cm = 28.723 mm**.

Converting `F = m × g`, using metres throughout:

```text
A = 0.001372 m
B = 9.80665 / 0.7669 = 12.787390794106 N
h_original(F) = 0.027351 + A × exp(F / B)
```

The experiment therefore supplies a nonlinear axial relationship: equal additions of force produce progressively larger extensions. It is not a single constant spring stiffness.

## 2. Why the simulator uses log1p

The simulation starts attached cups at the sealed reference and needs **force from displacement**, rather than height from an applied mass. It translates the original fit down by `A`:

```text
h_sim(F) = h_original(F) − A
         = 0.027351 + A × (exp(F / B) − 1)

d = h_sim − 0.027351
F_elastic(d) = B × ln(1 + d / A),  d ≥ 0
```

`log1p(d/A)` implements `ln(1+d/A)` accurately near zero. For the inverse, `expm1(F/B)` implements `exp(F/B)−1`. Positive `d` is extension along the cup normal from mount toward carton.

**This 1.372 mm translation is explicitly unvalidated.** It makes the simulated force zero at the sealed state but does not preserve the absolute measured height at a given load. Both curves have the same incremental compliance; every simulator height is 1.372 mm shorter. Do not silently treat the two height references as one measurement.

The local tangent stiffness is:

```text
k(d) = dF/dd = B / (A + d)             [N/m when A and d are metres]
k_mm(d_mm) = B / (1.372 + d_mm)        [N/mm]
k_mm(0) ≈ 9.32026 N/mm
```

## 3. Calculated checkpoints, not raw measurement points

Values below come from the equations, using the unscaled, static office model at the reference vacuum. The corresponding points in the interactive plot are calculated checkpoints. **No synthetic point is presented as a bench sample.**

| Equivalent mass (kg) | Force (N) | Simulator extension (mm) | Simulator height (mm) | Original-fit height (mm) | Tangent stiffness (N/mm) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.00000 | 0.000 | 27.351 | 28.723 | 9.320 | Calculated from stored fit |
| 1 | 9.80665 | 1.582 | 28.933 | 30.305 | 4.329 | Calculated from stored fit |
| 2 | 19.61330 | 4.988 | 32.339 | 33.711 | 2.011 | Calculated from stored fit |
| 3 | 29.41995 | 12.322 | 39.673 | 41.045 | 0.934 | Calculated from stored fit |
| 3.77 | 36.97107 | 23.345 | 50.696 | 52.068 | 0.517 | Calculated from stored fit |
| 4.2 | 41.18793 | 33.000 | 60.351 | 61.723 | 0.372 | Extrapolated to pull-off |

The fit ends at 36.9710705 N. From there to the 41.18793 N pull-off threshold, the simulator is extrapolating. The extension of approximately 33.000 mm at pull-off is an **extrapolated model prediction**, not measured travel. Pull-off is an event; it does not establish the shape of the curve between the last loading measurement and separation.

## 4. What is added for a dynamic simulation

For extension `d ≥ 0`, with normal relative velocity `v_n`:

```text
T = max(0, B_i × log1p(d / A_i) + c × v_n)
```

For compression `d < 0`:

```text
C = max(0, −k_compression × d − c × v_n)
```

The default office cup uses `A_i=A`, `B_i=B`. The stiffness multiplier scales `B`, not `A`. The following are simulator defaults, **not experimentally established cup specifications**:

| Parameter | Default | Interpretation |
| --- | --- | --- |
| Axial stiffness multiplier | 1 | Multiplies the logarithmic force coefficient |
| Damping `c` | 8 N·s/m | Velocity contribution to axial and tangential force |
| Compression stiffness | 12,000 N/m = 12 N/mm | Linear compression branch, uncapped |
| Shear stiffness | 4,000 N/m = 4 N/mm | Trial elastic tangential response |
| Friction coefficient | 0.5 | Sets shear capacity |
| Peeling threshold | 20° | Detach above this cup tilt |
| Sliding travel limit | 5 mm | Detach after accumulated slip exceeds this |
| Pull-off threshold | 41.18793 N | Detach when total tensile force reaches or exceeds it |
| Vacuum scaling | Off | Changing office vacuum otherwise changes metadata only |
| Cup gap | 2 mm | Layout default, not a material property |

Shear capacity is `μ × max(0, F_limit − T + C)`. Trial shear is reduced to this capacity by a plastic slip correction; accumulated slip can break the seal. Failure is evaluated in order: pull-off, peeling, sliding seal. Failure removes the cup force on the same step. There is no reattachment until a fresh test. Damping can reach pull-off earlier than the static curve predicts.

The solver already accounts for attachment through the contact law. Adding a separate `Δp × area` attraction on top would double count suction in this model.

## 5. Pressure and other cups

Only the approximately −60 kPa office loading curve is described as measured. Optional office vacuum scaling assumes a constant effective area and multiplies `B` and the pull-off limit by `vacuum_kPa / 60`; `A`, sealed height, and compression stiffness do not change. This is a **hypothesis**, not a pressure calibration.

VMECA profiles in `catalog.py` are a separate family. Their loading curves and compressed heights were not measured: the implementation estimates `A` by free-height ratio and `B` by catalogue force ratio at 60 kPa; their sealed height begins at `H × 27.351/47`. Their catalogue limit is pressure-interpolated. Do not label those estimated curves as office measurements or treat the Ø41 mm office cup as a VMECA model.

## 6. What the 3D view represents

The interactive page shows a schematic revolved bellows at the correct office lip diameter and selected model height. Its fold count, wall profile, neck and fitting are illustrative. The page has a free-height reference view and a loaded view, a choice of original-fit versus simulator reference, and a slider up to the recorded pull-off load. It shows the fitted-range boundary separately from extrapolation and detaches the schematic at the threshold. It is a static axial explanation: no dynamic box motion, shear, pressure build-up or rubber strain is solved.

The full model also omits leakage, shared-chamber pressure, pump capacity, vacuum build-up, cardboard porosity and bending, crushing, hysteresis, calibrated rubber travel and torsional capacity. In particular, uncapped compression is not a cardboard crushing or payload rating.

## 7. What to record in the next bench test

To make the calibration reproducible, record the cup identity and material, fixture and surface, actual pressure at the cup, height datum, raw mass/height pairs, loading and unloading cycles, repeat count and spread, and pull-off height/force. Measure the zero-load sealed height in the same fixture. Fit and compare the original and rebased laws against those points; report residuals and separate measurement uncertainty from model assumptions. Then test lateral loading and peel rather than inferring them from axial data.

## Source trail

The snapshot was read from sibling directory `../gripper-config` on 2026-10-28, whose HEAD was `3de5f597641fd2010423e5548c309937a7c36989`. That repository has local modifications, including its simulator README; this note reflects the **working tree**, not a claim that all text is committed. No remote URL was configured. Paths below are relative to that repository; hashes identify the exact text read.

| File | Role |
| --- | --- |
| `GRIPPER_REQUIREMENTS.md`, GEO-03 | Design envelope and free/working heights |
| `gripper_sim/README.txt`, Physics / Frame Mapping and Assumptions / Limits | Conversion, measured range, rebase caveat and limitations |
| `gripper_sim/settings.py`, constants and `Settings` | Coefficients, measured input metadata, defaults and optional scaling |
| `gripper_sim/catalog.py`, `OFFICE` | Profile identity, dimensions and unspecified fields |
| `gripper_sim/physics.py`, cup update | Dynamic forces, failure order and extrapolation tracking |

| Source file | SHA-256 of working-tree contents |
| --- | --- |
| `GRIPPER_REQUIREMENTS.md` | `f500bc2109ad3aa25cf7a6c28f0f4f5a9f2611374e13adcabdb275f87a26d2be` |
| `gripper_sim/README.txt` | `a3e93cea7ba243c225f342e544f354de4cd71523225f6426f0d699938345e58e` |
| `gripper_sim/settings.py` | `955e5fc8eb7dce66ccfcd8edf9290cbd69a7fd6ef2c5ec8a82184f4a1aa59bec` |
| `gripper_sim/catalog.py` | `cbc4e30a7b03fe6db67e4708b07914862ca7f60583ae72263a7278de35b71f39` |
| `gripper_sim/physics.py` | `05af24f468293e46d82ebfbc5bb56f455ae84df576d9c228e497d2af01c2a88b` |
