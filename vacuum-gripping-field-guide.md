# Vacuum Gripping: The Complete Field Guide

*Compiled 2026-08-14 from seven parallel research passes (all claims web-verified against manufacturer datasheets, standards, and vendor documentation — sources inline as URLs), the OnRobot VGP20 datasheet v1.7, and measured data from our own warehouse cell.*

## How to read this document

This is source material for a technical podcast about upgrading the vacuum system of a container-unloading robot cell. It is deliberately dense — the storyteller should pick the thread, but every number in here is real and cited.

**The narrative spine, in one paragraph:** A warehouse robot picks cardboard boxes with suction grippers fed by two small compressors, and the compressors keep overheating. Investigating why leads through the physics of the atmosphere (suction doesn't pull — the sky pushes), the strange economics of compressed air (the most expensive utility in any factory), a venturi device with no moving parts that turns pressure into vacuum, ball check valves that mechanically "notice" a hole and shut themselves, the discovery that every mobile picking robot on Earth (Boston Dynamics, Pickle, Anyware, XYZ Robotics) abandoned compressed air entirely, and finally a shopping trip to Shenzhen. The punchline: the fix isn't a bigger compressor — it's understanding that on leaky cardboard, *flow* is the currency, not vacuum depth, and electricity buys flow 5–10× cheaper when it skips the compressed-air detour.

**Chapters:**

0. The cell we actually have — measured baseline
1. Vacuum physics: units, force, flow
2. Ejectors: vacuum from compressed air, no moving parts
3. Electric vacuum: pumps, blowers, and what the picking-robot companies run
4. Smart gripper heads: how a gripper "recognizes a hole"
5. The energy ledger: wall watts to suction
6. Failure modes: surviving thousands of hours
7. Case study: decoding the OnRobot VGP20 datasheet
8. Buying it in China: the Shenzhen sourcing guide
9. Synthesis: the decision for our cell

---

# Chapter 0 — The cell we actually have (measured baseline)

Everything in this guide is anchored to one real machine, so here it is, with measured numbers.

**The robot.** A Fairino FR20 arm (20 kg payload) unloads shipping containers of mixed-size corrugated cardboard boxes. On the flange: a 500 mm rail carrying two large-area foam suction pads, 140 × 340 mm each. Top-down picks and front-face (wall) picks.

**The vacuum source.** Each pad is fed by a compressed-air venturi ejector. The compressed air comes from two Kippers Rijssen oil-free direct-drive piston compressors: 40 L tank each, 2600 W max each, nameplate 410 l/min intake displacement, 240 l/min free-air delivery (FAD) at 4 bar, 180 l/min at 8 bar.

**Measured consumption (tank drawdown test, 2026-08-12).** One 40 L tank falling 7 → 6 bar in 9 seconds while feeding one gripper: **one ejector gripper consumes ~265 l/min of free air at ~6.5 bar**. Two grippers ≈ 530 l/min at 6.5 bar (~425 l/min if regulated to 5 bar) versus the compressor pair's ~420–440 l/min flat-out. During dual-gripper bursts the cell is at or over 100% of its air supply ceiling and survives only on the off-time between picks.

**The failure.** The compressors' thermal protectors (klixons) trip mid-shift, killing the air supply for 15–30 minutes at a time. Measured: **~120 compressor motor starts per hour** — roughly one start per pick, because the 40 L tank's pressure band holds less air than one pick draws.

**The diagnosis (2026-08-12, confirmed by this research).** Not air starvation. Three stacked electrical/setup problems: (1) sagging motor starts — both compressors, the robot, and a long coiled extension cord shared one 230 V / 16 A group; (2) no regulator — the ejectors were fed raw tank pressure (7–8 bar), and choked-nozzle consumption scales with absolute pressure, wasting ~25%+ versus a 5 bar feed; (3) simultaneous pressure-switch starts slamming two motor inrushes onto a sagging line at once. The interim fix already agreed: Y-manifold sharing both 40 L tanks, staggered pressure-switch bands (lead 6.0→7.5 bar, lag 5.5→7.0), a 5 bar filter-regulator on the ejector feed, unrolled 2.5 mm² cords, circuits split across groups.

**The electrical ceiling.** Warehouse sockets are 230 V single-phase only; each group is 16 A ≈ **3600 W**. Measured all-on steady draw: ~3400 W. The compressor pair's combined nameplate (5200 W) cannot legally coexist with the robot on one group. Three-phase 400 V may exist in the panel (unverified) — if it does, a whole class of bigger machines opens up.

**Grip performance history.** An earlier measurement put total effective suction at ~300 N — *leak-starved*, not area-limited: one perfectly sealed 140 × 340 mm pad at a mere −30 kPa would theoretically hold ~1,400 N. Front-face carries peeled off at ~7 kg, which the physics predicts exactly (Chapter 1, load case III); the industry fix — used by Copal, Anyware, Honeywell — is a mechanical rest that carries the box weight so suction only has to hold, not lift.

**The constraint set for any upgrade:** drop-in parts, few failure modes, must run thousands of hours, 3600 W per outlet group, mixed and sometimes leaky/torn cardboard, and a Shenzhen trip coming up.

---

# Chapter 1 — Vacuum physics: units, force, flow

## 1.1 Pressure units and what "negative kPa" means

**Absolute vs gauge.** Absolute pressure is measured from a perfect vacuum (0 kPa abs); gauge pressure is measured relative to local atmospheric pressure. Vacuum specs in industrial pneumatics are almost always **negative gauge** numbers: −60 kPa means "60 kPa below ambient," i.e. ~41.3 kPa absolute at sea level. Reference: 1 atm = 101.325 kPa = 1.01325 bar = 1013.25 mbar = 760 mmHg (Torr) = 29.92 inHg = 14.696 psi (https://www.tawi.com/en-us/insights/how-to-measure-vacuum-methods-units-and-scales, https://www.sensorsone.com/vacuum-conversion-table/).

**Why negative?** A vacuum gripper only cares about the *differential* between ambient and cup interior — that differential is what pushes the part against the cup. Writing −60 kPa (gauge) directly states the usable differential, whereas "41 kPa absolute" would require knowing local ambient to compute force.

**The "% vacuum" convention.** 0% = atmospheric pressure, 100% = perfect vacuum. Formula: `V% = (P₀ − P_abs)/P₀ × 100`, e.g. 300 mbar abs → (1013−300)/1013 = 70% vacuum (https://www.vacuum-guide.com/english/equipment/conversion_pascal_bar.htm). In the rough-vacuum range used for gripping, % vacuum is the common shorthand, and conveniently **−kPa ≈ % vacuum** ("about 80% vacuum" ≈ −80 kPa) since 1 atm ≈ 101 kPa (https://fluidpowerjournal.com/vacuum-measurement-a-basic-guide/, https://www.industrialspec.com/images/files/vacuum-pressure-unit-conversions-chart-from-ism.pdf).

**Conversion table** (gauge vacuum; % vacuum referenced to 101.325 kPa; inHg/mmHg are "vacuum" scales counting up from 0 at atmosphere):

| Gauge kPa | bar (g) | mbar (g) | abs. kPa | inHg vac | mmHg vac | psi vac | % vacuum |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 101.3 | 0 | 0 | 0 | 0% |
| −20 | −0.20 | −200 | 81.3 | 5.9 | 150 | 2.9 | 19.7% |
| −40 | −0.40 | −400 | 61.3 | 11.8 | 300 | 5.8 | 39.5% |
| −60 | −0.60 | −600 | 41.3 | 17.7 | 450 | 8.7 | 59.2% |
| −80 | −0.80 | −800 | 21.3 | 23.6 | 600 | 11.6 | 79.0% |
| −90 | −0.90 | −900 | 11.3 | 26.6 | 675 | 13.1 | 88.8% |
| −101.325 | −1.013 | −1013 | 0 | 29.92 | 760 | 14.7 | 100% |

(Conversion constants: 1 inHg = 3.386 kPa, 1 mmHg = 0.1333 kPa, 1 psi = 6.895 kPa; cross-checked against https://www.industrialspec.com/images/files/vacuum-pressure-unit-conversions-chart-from-ism.pdf and https://www.sensorsone.com/vacuum-conversion-table/.)

## 1.2 The physical ceiling: ~101 kPa is all you ever get

Suction does not "pull" — the atmosphere *pushes* the part onto the cup. The maximum possible differential at sea level is ambient pressure itself: **≈101.3 kPa**. No pump, however powerful, exceeds it. Consequences:

- **Max theoretical holding pressure ≈ 10.13 N/cm² ≈ 1.03 kgf/cm²** at perfect vacuum. The "1 kg per cm²" rule of thumb.
- At a realistic industrial working level of **−60 kPa: 6.0 N/cm² ≈ 0.61 kgf/cm²**.
- At porous-load levels of **−40 kPa: 4.0 N/cm² ≈ 0.41 kgf/cm²**.
- Going from −60 to −90 kPa gains only 50% more force at steeply rising energy/time cost; going from −90 to −101 kPa is practically unreachable with ejectors (typical max 85–90% vacuum). Past ~−60 kPa, **adding area is almost always cheaper than adding vacuum depth** (https://www.pneumatictips.com/size-vacuum-cup/, https://fluidpowerjournal.com/vacuum-lifting-fundamentals/).

## 1.3 Holding force: F = ΔP × A, safety factors, friction, peel

**Base law:** `F = ΔP × A` (ΔP in Pa, A effective sealed area in m², F in N). Example: one Ø40 mm cup at −60 kPa: A = 12.6 cm² → F = **75 N ≈ 7.7 kg theoretical**; with safety factor 2 → ~3.8 kg usable per cup. Note A is the *effective* area at the sealing lip under load, which for bellows cups is smaller than the nominal diameter suggests (https://www.schmalz.com/en/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/vacuum-suction-cups/design-of-the-suction-cup).

**Schmalz load-case formulas** (https://www.schmalz.com/en/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/system-design-calculation-example/theoretical-holding-force-of-a-suction-cup):

| Load case | Geometry | Required theoretical holding force |
|---|---|---|
| I | Cup horizontal, force vertical (lift straight up) | F = m·(g + a)·S |
| II | Cup horizontal, force horizontal (lift then move sideways) | F = m·(g + a/μ)·S |
| III | Cup vertical, force vertical (face/wall pick, gravity in shear) | F = (m/μ)·(g + a)·S |

- **Safety factors:** Schmalz: minimum **S = 1.5** for smooth dense parts, **S ≥ 2.0** for critical, porous, rough or oiled parts — and always **S ≥ 2 for load case III** (vertical cup, load held by friction alone). EN 13155 (non-fixed load lifting attachments) requires vacuum lifters be dimensioned to hold **2× the working load limit**, and where holding is by friction the factor shall be at least 2 (https://www.aerolift.nl/en/standards-and-safety-regulations-vacuum-lifting/, https://standards.iteh.ai/catalog/standards/cen/78d516a5-5967-407e-affd-4654ba0a0f3a/en-13155-2020). EN 13155 also distinguishes self-priming vs non-self-priming lifters (the latter need vacuum reserve to survive power loss).
- **Friction coefficients (cup on workpiece):** μ ≈ **0.5** for dry wood/metal/glass/stone (commonly extended to dry cardboard in practice), 0.6 rough surfaces, 0.2–0.3 wet, 0.1–0.3 oiled. Schmalz cautions there is no universally valid μ — measure it for your part.
- **Worked example** (Schmalz): 61.3 kg steel sheet, a = 5 m/s², μ = 0.5 → case I: 1363 N (S=1.5); case II: 1822 N; case III: 3633 N (S=2). Case III needs ~2.7× the force of case I for the same part — **face picks are expensive**. This is exactly why our front-face carries peeled at ~7 kg on 300 N of suction, and why the industry answer is a mechanical rest, not more vacuum.
- **Worked example, cardboard box:** 5 kg sealed box, lift with a = 5 m/s², S = 2: case I → 148 N; at −40 kPa that needs ≥37 cm² → e.g. four Ø35 mm cups. Adding a horizontal robot move (case II, μ = 0.5): 198 N → ~50 cm².
- **Peel moments:** F = ΔP·A holds only for centric normal loads. Cups fail in *peel* at a fraction of their normal-pull rating: an offset centre of gravity creates a moment M = m·g·d that concentrates load on one lip edge; the lip lifts locally, leakage spikes, vacuum collapses. On face picks any torque about the cup array is reacted by the outermost cups over the array's lever arm — a 5 kg box whose CoG sits 150 mm behind a vertical face pick produces M = 7.4 N·m; with a cup array of 100 mm vertical span, the top cups see an extra ~74 N pulling them off. Best practice: place cups so the CoG lies inside the cup pattern, maximize array span, and use bellows sparingly on face picks (https://www.pneumatictips.com/size-vacuum-cup/, https://blog.robotiq.com/best-practices-for-cup-selection).

## 1.4 Vacuum level vs flow: the curve, and leaky vs sealed loads

A vacuum generator is not a single number, it is a **curve**: maximum suction flow at 0 kPa (free flow) falling monotonically to zero flow at its maximum vacuum. Datasheet "suction capacity" is the free-flow endpoint; datasheet "max vacuum" is the zero-flow endpoint; the working point is wherever the load's leak rate intersects the curve (https://www.coval.com/en-us/technologies/vacuum-technology/vacuum-generation).

- **Sealed load (glass, steel sheet, plastic tote):** leak ≈ 0, so any generator eventually reaches its max vacuum; you size for **depth** and evacuation speed, not steady-state flow.
- **Leaky/porous load (corrugated cardboard, ventilated boxes):** air flows through/past the load continuously; the achieved vacuum is where the generator curve equals the leak flow. A deep-vacuum, low-flow generator stalls at a few −kPa on such loads. You size for **flow**. Manufacturers recommend **−20 to −40 kPa** working levels for cardboard — deeper vacuum mostly increases airflow through the pores (and can delaminate/dimple single-face board) rather than force (https://www.airbestpractices.com/industries/food/handling-corrugated-cardboard-optimized-pressure-regulation-air-driven-vacuum-pumps). Smaller cups leak less than one big cup on porous board.
- Coval offers exactly this split as two mixer profiles: **60%-max-vacuum venturis for porous** loads (operate at 30–55%) and **85%-max-vacuum venturis for airtight** loads (operate at 55–80%) (https://www.coval.com/en-us/technologies/vacuum-technology/vacuum-generation).

**"Suction capacity" vs "air consumption" — different numbers.** For a compressed-air ejector (venturi):

- *Suction capacity / suction rate (l/min)* = air drawn **in at the vacuum port** (at zero vacuum). This is what fights leaks.
- *Air consumption (l/min)* = **compressed air burned by the drive nozzle** to run the ejector. It exits the exhaust; none of it touches your cup.

Verified datasheet examples (Schmalz, 0.7 mm nozzle class): inline ejector VR 07 — suction 14 l/min, consumption 21 l/min; compact ejector SCPS 07 — suction 16 l/min, consumption 22 l/min; multi-stage SBP HV 3-07 — suction 76.8 l/min from the same nozzle class (multi-stage venturis reuse the drive jet across stages, multiplying free-flow capacity for the same consumption) (https://www.schmalz.com/en/products/vacuum-technology-for-automation-301607/vacuum-components-301608/vacuum-generators-307617/pneumatic-vacuum-generators-739752/inline-ejectors-307817/inline-ejectors-vr-307818/10.02.01.00001). Consumption typically runs ~1.4–6× suction capacity depending on design (https://rodlesspneumatic.com/blog/the-physics-of-venturi-ejectors-and-vacuum-control-valves/). Beginners routinely read "21 l/min" on an ejector and assume that flow is available to fight leaks — it is not; only the suction-capacity number is. **Our grippers' 265 l/min figure is air consumption** — the compressed air burned, not the suction produced.

## 1.5 Deep vs shallow vacuum: when each wins

| | Deep vacuum, small area | Shallow vacuum, large area |
|---|---|---|
| Typical level | −60…−90 kPa | −15…−40 kPa |
| Generator | ejector / vacuum pump | blower or high-flow multi-stage ejector; Schmalz vacuum blowers max out at ~40% vacuum by design (https://www.schmalz.com/en-us/products/automation-743270/vacuum-generators-307617/electric-vacuum-generators-738973/vacuum-blowers-308520) |
| Flow | low (l/min–tens of l/min) | huge (hundreds–thousands of l/min) |
| Load | airtight, smooth, stiff | porous, rough, leaky, floppy (cardboard, sacks, wood, ventilated crates) |
| Gripper | discrete cups | foam-mat area grippers with per-cell check valves so uncovered cells don't kill the vacuum (https://www.schmalz.com/en/additional-infos-shop/vacuum-area-gripping-system-fxp-with-foam-su, https://www.piab.com/en-us/news/kenosflexigrip) |
| Failure mode | peel, surface damage (dimpling thin board at high ΔP) | insufficient force per cm² if area is limited |

The arithmetic: a foam gripper at −20 kPa needs 5× the area of a cup at −100 kPa for the same force — but on a ventilated box the −100 kPa system might actually achieve −5 kPa while the blower system holds its −20 kPa against the leaks. Depth wins on sealed, small-contact-area parts; area+flow wins whenever the load leaks or the top surface is large, uneven, or fragile.

## 1.6 Evacuation time

Cup grip is not instantaneous: the generator must evacuate the **dead volume** — cup interiors, fittings, hoses, manifold, filter, valve — down to working vacuum. Schmalz sizing formula (https://www.schmalz.com/en-us/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/system-design-calculation-example/calculation-of-evacuation-times):

`t = V_G × ln(p_a / p_e) × 1.3 / V̇`  (t in hours with V_G in m³ and V̇ in m³/h; the 1.3 is an empirical correction for suction rate falling off as vacuum deepens)

Worked Schmalz example: 6 cups + fittings + hoses + distributor → V_G = 564 cm³; generator suction 116 l/min; target 400 mbar abs (−60 kPa): **t = 0.35 s**. The general pump-down law is t = (V/S)·ln(p₀/p₁) (https://www.engineeringtoolbox.com/vacuum-evacuation-time-d_844.html); the crude estimate t ≈ V/Q underestimates because Q collapses as vacuum rises.

Practical implications: every metre of Ø9 mm hose adds ~64 cm³ that must be pumped down *every cycle*; decentralizing (generator at the cup) beats one remote pump through long lines both in evacuation time and leak response. For fast pick cycles, evacuation time budget caps allowable dead volume.

## 1.7 Altitude and temperature (brief)

- **Altitude:** ambient pressure drops ≈12.5 mbar per 100 m near sea level; at 2000 m ambient is ~763 mbar, so a generator rated "80% vacuum" that achieves −810 mbar at sea level only reaches **−610 mbar at 2000 m** — holding force drops ~25%. Vacuum switches and % settings must be re-tuned (https://www.schmalz.com/en/vacuum-knowledge/basic-knowledge/the-atmosphere-and-its-effects-on-vacuum-technology/, https://www.wpg.com/elevation-affects-vacuum-cup-performance).
- **Temperature:** gas volume scales with absolute temperature (a sealed evacuated volume heated 20→50 °C rises ~10% in pressure); more practically, cup elastomers stiffen and seal poorly in cold (NBR below ~+10 °C) and soften/mark parts when hot.

## 1.8 Nl/min vs l/min, FAD, and the "7× volume" rule

- **Nl/min (normal litres per minute):** flow converted to *normal conditions* — DIN 1343: 0 °C, 1013.25 mbar (vendors also use ANR per ISO 8778: 20 °C, 1000 mbar). It is a **mass-flow statement in volume clothing**: 1 Nl of air is the same number of molecules regardless of pipe pressure (https://www.engineeringtoolbox.com/rating-air-compressors-d_848.html).
- **l/min (actual):** the geometric volume passing per minute at local pressure. At 6 bar gauge = 7 bar absolute, the same gas occupies ~1/7 the volume: **1 l/min actual at 6 barg ≈ 7 Nl/min of free air** (https://www.air-compressor-guide.com/question/calculation-to-convert-nlmin-to-lmin). This is why "compressed air at 6 bar contains ~7× atmospheric volume" and why ejector *air consumption* specs (given in free-air l/min) translate to modest actual pipe flow.
- **FAD (Free Air Delivery):** compressor output *converted back to inlet (ambient) conditions* per ISO 1217 — the honest "how much atmosphere-equivalent air does this machine deliver at rated pressure" number, always below theoretical displacement because of volumetric efficiency losses (https://nigen.com/how-to-calculate-compressor-free-air-delivery-fad/). Retail listings love quoting intake displacement instead of FAD — our compressors' "410 l/min" is displacement; the real number is 240 l/min FAD at 4 bar, 180 at 8 bar.
- **Sizing chain example:** an ejector consuming 66 Nl/min run at 50% duty needs 33 l/min FAD from the compressor — but only ~4.8 l/min of actual volume flows in the 6 barg supply line. Mixing up Nl/min and actual l/min gives 7× errors; mixing up suction capacity and air consumption gives a gripper that can't fight leaks.

---

# Chapter 2 — Ejectors: vacuum from compressed air, no moving parts

## 2.1 Working principle: converging–diverging nozzle, momentum transfer

A vacuum ejector feeds compressed air through a converging–diverging (de Laval / venturi) nozzle. The air accelerates to sonic velocity at the throat (the nozzle **chokes**) and expands supersonically past it; static pressure in the jet falls well below atmospheric. Ambient air from the vacuum port is entrained into the jet by shear/momentum transfer, mixed in a diffuser section, recompressed, and exhausted through a silencer. Suction persists as long as motive air flows (https://insights.globalspec.com/article/18359/vacuum-ejector-understanding-its-working-principle-and-some-design-parameters, https://www.schmalz.com/en/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/vacuum-generators/vacuum-ejectors).

**No moving parts:** the only "mechanism" is a shaped hole. Consequences: no wear surfaces, no lubrication, no motor/bearings/vanes to overheat, unlimited duty cycle, insensitive to vibration and mounting orientation, ~30–900 g mass so it can ride on the end-effector, and near-instant on/off (vacuum in tens of ms). Practically all failure modes are contamination-related (§2.9), not mechanical. Festo specifies 100% duty cycle and "any" mounting position for OVEM (https://ftp.festo.com/Public/PNEUMATIC/SOFTWARE_SERVICE/Datasheet/EN_US/539074.pdf).

## 2.2 Single-stage vs multi-stage

- **Single-stage:** one nozzle. Ratio of suction flow (at 0 kPa vacuum) to compressed-air consumption is typically **≤1:1**, often 0.4–0.9:1. Verified examples (SMC ZH at 0.45 MPa): ZH10 S: 24 l/min suction / 46 l/min air = 0.52; ZH20 L: 135/185 = 0.73 (https://content.smcetech.com/pdf/ZH_EU.pdf).
- **Multi-stage (Piab COAX, Schmalz eco-nozzle/SEM/SBPL, Vmeca cartridges, Coval CMS, SMC ZK2 2-stage):** the exhaust of the first nozzle still has kinetic energy; downstream nozzles/stages entrain additional "free" ambient air through check-valve flaps, adding suction flow at low vacuum levels without extra motive air. Industry references put the improvement at roughly **1:3 or better** near 0 kPa vs ~1:1 single-stage (https://www.blowervacuumbestpractices.com/system-assessments/vacuum-generation/utilizing-venturi-vacuum-generators-efficiently, https://fluidpowerjournal.com/vacuum-venturis-air-powered-generators/). Three stages is the practical maximum.
- Verified ratios: Piab COAX MIDI Xi40-3 (3-stage): 354 l/min suction for 110 l/min air = **3.2:1** (https://www.piab.com/globalassets/productimages/0118724_datasheet_coax_cartridge_midi_xi40_3_en-gb.pdf). Schmalz SBPL 25 HF: 290/80 = **3.6:1**; SBPL 150 HV: 1140/545 = 2.1:1 (https://media.schmalz.com/MAM_Library/Dokumente/Datenblatt_Produktfamilie/0_/050/05050/ff4cfffb7ff4_Datasheet_Basic%20Ejectors%20SBPL_en-EN.pdf). Schmalz SEM-C 100: 673/246 = **2.7:1**. SMC ZK2 (2-stage): ZK2-10: 56/40 = 1.4:1 — SMC states +50% suction flow and −30% air vs their single-stage (https://content2.smcetech.com/pdf/16-e678-zk2.pdf). Piab markets COAX as "up to three times the vacuum flow of a conventional system" (https://www.piab.com/vacuum-pumps-and-ejectors).
- **The catch:** the multi-stage advantage lives at **low vacuum (0…−30 kPa)**. As vacuum deepens, auxiliary-stage check valves close and flow converges toward the first stage alone — Xi40-3 falls from 354 l/min at 0 kPa to 78 l/min at −40 kPa and 11 l/min at −80 kPa. For porous loads (cardboard) you operate at −20…−40 kPa where the multiplier is largest — exactly the pick-cell case.

## 2.3 Product comparison table

Manufacturer data; suction flow at 0 kPa; air consumption at rated pressure.

| Brand / model | Type | Air cons. (l/min) | Suction (l/min) | Ratio | Max vac (kPa) | Rated supply | Street price |
|---|---|---|---|---|---|---|---|
| SMC ZH07-S | 1-stage, 0.7 mm | 23 | 12 | 0.52 | −88 | 0.45 MPa | ~$30–60 |
| SMC ZH10-S / ZH10-L | 1-stage, 1.0 mm | 46 | 24 / 34 | 0.52/0.74 | −88 / −48 | 0.45 MPa | ~$30–60 |
| SMC ZH20-S / ZH20-L | 1-stage, 2.0 mm | 185 | 85 / 135 | 0.46/0.73 | −88 / −48 | 0.45 MPa | — |
| SMC ZK2-07 (2-stage, air-save) | 2-stage | 24 | 34 | 1.42 | −91 | 0.35 MPa | $292 (Zoro) |
| SMC ZK2-15 | 2-stage | 90 | 89 | 0.99 | −91 | 0.35 MPa | ~A$730 w/ valve+switch |
| Schmalz SBP 10 S02 | 1-stage, 1.0 mm | 48 | 37.7 | 0.79 | ~−85 | 4.5 bar | ~$75–190 |
| Schmalz SBP 20 S03 | 1-stage, 2.0 mm | 197 | 127 | 0.64 | ~−85 | 4.5 bar | — |
| Schmalz SBPL 25 HF / HV | eco-nozzle multi-stage | 80 / 105 | 290 / 300 | 3.6/2.9 | −60 / −90 | 2–6 bar | — |
| Schmalz SBPL 100 HF / HV | eco-nozzle multi-stage | 300 / 395 | 860 / 870 | 2.9/2.2 | −60 / −90 | 2–6 bar | — |
| Schmalz SCPi 20 | compact, pulse-valve air-save | 180 | 140 | 0.78 | −85 | 4.5 bar | — |
| Piab COAX MIDI Xi40-3 | 3-stage cartridge | 110 | 354 | 3.2 | −95 | 0.45 MPa | — |
| Piab piCOMPACT23 SMART | all-in-one, ES + blow-off | ~110–140 | ~350 | ~3 | −95 | 0.4–0.5 MPa | — |
| Festo VN-10-H / VN-14 | 1-stage Laval | — | 21.8 / 48.8 | — | −93 | 3–3.6 bar opt. | — |
| Festo OVEM (family) | 1-stage + air-save + blow-off | — | 6–348 | — | −93 | 3.5–5.3 bar | — |
| Coval LEMAX (1.0–1.4 mm) | mini pump, ASC air-save + regulator | 44–90 | 29–70 | ~0.7 | −90 | integr. regulator | — |
| Coval CMS M 90X30 / HD 90X150 | multi-stage | — | 550 / 1600 | ~2–3 typ. | −80 | ~5 bar | — |
| Vmeca VTM / Turtle pumps | 3-stage cartridge + filter, Eco = air-save | — | — | ~2–3 typ. | ~−90 | — | — |

Sources: SMC ZH catalog PDF, SMC ZK2 leaflet PDF, Schmalz SBP/SBPL family datasheets, Festo OVEM datasheet, Piab Xi40-3 datasheet, Coval LEMAX/CMS product pages, Vmeca Eco Turtle page (URLs as cited above and: https://www.schmalz.com/en-us/products/vacuum-technology-for-automation-301607/vacuum-components-301608/vacuum-generators-307617/pneumatic-vacuum-generators-739752/compact-ejectors-307841/compact-ejectors-scpi-smpi-307880/10.02.02.03359, https://www.festo.com/media/catalog/203880_documentation.pdf, https://www.coval.com/en-us/ejectors-and-vacuum-pumps/intelligent-vacuum-pumps/integrated-mini-vacuum-pumps-with-asc-air-saving-control-lemax-seriesp_158734, https://vmeca.com/en/shop/vacuum-pump-en/eco-turtle-pump-en/eco-turtle-pump/).

## 2.4 The efficiency picture: the full electric→vacuum chain

Compressed air is the expensive part. Good screw compressors deliver ~**6.4–7.2 kW per m³/min FAD** (https://www.hpccompressors.co.uk/news-resources/blog/what-is-your-air-compressor-s-specific-power-get-more-output-use-less-energy-lower-your-costs/). Small oil-free piston compressors are far worse: 2.6 kW for ~250 l/min FAD ≈ **10.4 kW per m³/min** — every l/min of compressed air costs ~10.4 W electric.

Chain math (electric W per l/min of suction at 0 kPa):

- **Single-stage ejector** (ratio 0.5, screw compressor at 7 kW/m³/min): 7/0.5 ≈ **14 W per l/min suction**. On a piston compressor: ~21 W.
- **Multi-stage ejector** (ratio 3.2, screw): 7/3.2 ≈ **2.2 W per l/min**; piston: ~3.3 W.
- **Electric dry pump reference:** a 0.55 kW dry vane/claw pump at ~165 l/min ≈ **3.3 W per l/min**, continuously, with no compressor losses upstream.

So a multi-stage ejector on a decent compressor is competitive with an electric pump *per unit flow*; a single-stage on a piston compressor is ~5–7× worse. "Energy-hungry ejector" is really "single-stage ejector fed from an inefficient compressor at too-high pressure, running 100% duty". Energy is up to ~75% of a compressed-air system's lifecycle cost (https://www.fs-elliott.com/blog/how-to-calculate-your-compressed-air-energy-costs). Applied to our cell: 2 × ~250–265 l/min at 6–6.5 bar ≈ the full rated FAD of both 2600 W piston compressors — that is the overheating, not a compressor defect.

## 2.5 Max vacuum: −85 to −95 kPa, and high-flow vs high-vacuum nozzles

Standard ejectors reach deeper vacuum than most dry-running mechanical pumps: SMC ZH-S **−88 kPa**, ZK2 **−91 kPa**, Festo VN/OVEM **−93 kPa**, Piab Xi40-3 **≥−95 kPa**, Coval LEMAX 90%, Schmalz HV −90 kPa. Most dry vane/diaphragm pumps top out around −75…−85 kPa; ejectors give depth "for free" but with vanishing flow near max vacuum.

All vendors sell a flow/depth trade-off via nozzle geometry:

- SMC **S** ("standard/high-vacuum", −88 kPa) vs **L** ("large flow", −48 kPa but ~40–60% more suction flow at the same air consumption, e.g. ZH13: 70 vs 40 l/min at 78 l/min air) (https://content.smcetech.com/pdf/ZH_EU.pdf).
- Schmalz **HV** (90% vacuum) vs **HF** (60% vacuum, air consumption ~25–35% lower at equal suction; explicitly "optimized for airtight (HV) or porous (HF) workpieces").
- Festo **H** (high vacuum) vs **L** (high flow) Laval nozzles.

Rule: porous/leaky loads (corrugate) → high-flow nozzle at −20…−40 kPa; sealed rigid loads → high-vacuum nozzle + air saving.

## 2.6 Supply pressure: there is an optimum, and tank pressure wastes air

The motive nozzle is **choked** whenever upstream absolute pressure exceeds ~1.9× downstream — always true above ~1 bar g. Choked mass flow scales linearly with upstream **absolute** pressure (ṁ ∝ p_abs·A/√T), independent of vacuum side (https://www.morrisejectors.com/operation.html, https://epcland.com/ejector-working-principle/). The diffuser is designed for one expansion ratio, so above the design pressure you pump in proportionally more air and get **no more vacuum** — often slightly less, because the over-expanded jet chokes the mixing section (https://croll.com/library/vacuum-systems-ejectors-operations/).

Verified optima: SMC ZH rated at **0.45 MPa**, ZK2 at **0.35 MPa**; Festo OVEM max vacuum at 3.5–5.3 bar; Schmalz specifies **4.5 bar** optimal; Piab Xi40-3 at 0.6 MPa consumes **27% more air (140 vs 110 l/min) for identical 354 l/min suction** vs 0.45 MPa, and slightly worse max vacuum. Feeding a 4.5 bar-optimal ejector from a 6.5 bar line ≈ (7.5/5.5) = **36% wasted air**; from an 8 bar tank ≈ 55–60%. Mitigation: a point-of-use regulator per ejector — Coval LEMAX integrates the regulator (ASR) precisely so the ejector always runs at its own optimum regardless of line pressure. **This is why the 5 bar filter-regulator in our fix plan is free money.**

## 2.7 Air-saving ("energy-saving") ejectors

Architecture: ejector + **vacuum sensor** + **supply solenoid valve** + **check valve** in one block. Sequence: evacuate to setpoint H1 → close supply valve → check valve holds vacuum in the (sealed) cup circuit → on leak-down to threshold H2, re-fire. Air consumption during hold is zero; savings scale with hold-time fraction.

- **SMC ZK2**: digital pressure switch cuts supply at setpoint; claims **90–93% air reduction** (SMC conditions); N.O.-supply-valve variant keeps holding through power loss (https://www.smcworld.com/products/subject/en-jp/air_saving/vacuum/zk2.html).
- **Festo OVEM**: electric air-saving function + check valve + pulse valve, IO-Link diagnostics.
- **Piab piCOMPACT ES**: energy saving with adjustable hysteresis, Automatic Condition Monitoring, Self-Adhesion Control (https://www.piab.com/en-us/vacuum-pumps-and-ejectors/compact-and-stackable-ejectors/picompact10x2).
- **Coval LEMAX/LEMAX+ ASC**: claims **75–99%** savings, "90% for airtight products".
- **Schmalz** compact ejectors interrupt generation at safe vacuum, restart below minimum; SCPSi eco-nozzle + air-save claims up to **80%**. Vmeca Eco Turtle: same idea.

**Why they fail on leaky loads:** with porous cardboard the cup circuit never leak-tightens; vacuum never holds between setpoints, the controller detects the leak and reverts to continuous generation — savings ≈ 0, and vendor firmware does this automatically (https://ar-vacuum.com/en/fab_vacuum_ejector). For hole-riddled corrugate the correct lever is not air-save alone but a **high-flow multi-stage stage at reduced pressure** (Schmalz HF, COAX, CMS) — more l/min suction per l/min air at shallow vacuum — **plus a check-valved gripper head that removes the uncovered-cell leak** (Chapter 4), which is what lets air-save engage at all.

## 2.8 Distributed vs centralized

- **Centralized** (one large ejector/pump at robot base): one air feed, one control point, easy silencer maintenance; but evacuation time scales with total hose+manifold volume, one leaking cup degrades all cups, and vacuum lines must be large-bore.
- **Decentralized** (small ejector per cup or cup group, e.g. Piab COAX cartridges in the gripper): evacuates only the cup dead volume → **fastest response (ms–tens of ms)**, no false vacuum signals from line losses, per-cup leak isolation (a missed cup doesn't drop the carton), and a small compressed-air line replaces large vacuum plumbing. Cost: more units, more valves/IO, silencers on the arm. Piab claims decentralized COAX inline gives ≥40–50% lower energy than competing single-stage inline units (https://www.piab.com/en-us/vacuum-pumps-and-ejectors/decentralized-ejectors).

## 2.9 Failure modes and mitigations

- **Silencer clogging** (the #1 real-world failure): exhaust silencer felt/sinter loads up with dust, oil mist, and debris drawn through the vacuum port; back pressure rises, max vacuum and flow drop silently. Treat silencers as consumables; prefer straight-through designs; monitor evacuation-time drift (OVEM/piCOMPACT do this natively) (https://hifi-filter.com/en/reduce-noise-in-industry-with-pneumatic-silencers/).
- **Nozzle/stage contamination**: throat diameters are 0.5–2 mm; supply-side pipe scale or suction-side dust (cardboard fibers!) erode or block them and jam multi-stage check-valve flaps. Mitigation: supply filtration (Festo builds in 40 µm), suction-side inline filter at the cup (Vmeca Turtle integrates one), cleanable nozzle cartridges.
- **Freezing/condensate**: expanding air cools sharply; moisture in supply air condenses and can ice the nozzle/diffuser and silencer. Mitigation: dried air, drain legs; oil-free piston compressors without dryers (our cell) are the worst-case moisture source.
- **Supply-pressure sag**: below design pressure the diffuser un-chokes and vacuum collapses non-linearly. Piab COAX is marketed as tolerant of low/fluctuating feed (works from ~3 bar) — relevant when a sagging compressor is the reality.

## 2.10 Blow-off and cycle time

Releasing a part is not free: the cup + tubing volume sits at −60…−90 kPa and vents only through the cup orifice; passive release takes 100s of ms and light parts stay stuck. **Blow-off** routes a positive-pressure pulse into the vacuum port, collapsing the vacuum and pushing the part off. Typical blow-off actuation ~20–25 ms; usually set near 50–150 ms (https://shop.gimatic.com/en/ej-blowoff). Variants: PLC-timed, automatic-timed on vacuum-off (Coval GEM), Piab Intelligent Blow-Off (fires only what's needed) and Self-Adhesion Control (periodic micro-puffs to stop thin parts re-adhering). In a 1–2 s pick cycle, 100–300 ms of passive release is 10–25% of cycle time. Blow-off also back-flushes dust out of check valves and foam (Chapter 4) — on a dusty cardboard cell this cleaning function alone justifies it.

## 2.11 Implications for our cell

1. 240–265 l/min continuous per gripper at 6–6.5 bar is single-stage-with-no-controls behavior run above optimal pressure. Two immediate, cheap levers: **regulate down to 4.5–5 bar at the ejector** (−25–35% air, no vacuum loss) and **switch to high-flow multi-stage** (COAX Xi40-3: 354 l/min suction for 110 l/min air; SBPL 25/50 HF: 290–500 l/min suction for 80–160 l/min air). Together these plausibly cut compressor demand 50–70% at equal or better grip — likely below one compressor's continuous rating.
2. Air-saving ejectors only pay off if the load surface seals. On porous corrugate they revert to continuous flow — unless paired with a check-valved gripper head (Chapter 4). Test leak-down per SKU before buying "smart".
3. If loads are mostly porous and duty is high, the honest comparison is multi-stage ejector (~2–3 W electric per l/min suction via a screw compressor; ~3.3 W via our piston units) vs an electric dry pump/blower (~1–3 W per l/min, no idle-compressor overhead, but adds moving parts and slower response). Ejectors stay compelling for fast cycling and depth; blowers/pumps win for continuous high-leak flow at shallow vacuum.

---

# Chapter 3 — Electric vacuum: pumps, blowers, and what the picking-robot companies run

## 3.0 Framing

An ejector converts ~7 bar compressed air into suction; every liter of that air costs compressor shaft power upstream. An electric vacuum source converts wall (or battery) power into suction directly and skips the two lossiest stages (compression to 7 bar, then throwing that pressure away across a venturi). Every major container-unload robot on the market (Stretch, Pickle, Pixmo, RockyOne, Contoro) has converged on onboard electric vacuum for exactly this reason — a mobile base cannot carry a 7-bar compressor, and porous cardboard rewards flow, not depth.

Unit conversions used throughout: 1 m³/h = 16.7 l/min; 1 CFM = 28.3 l/min; 1 inH2O = 0.249 kPa; ultimate pressure in mbar(abs) → gauge vacuum ≈ −(1013 − p_abs)/10 kPa.

## 3.1 Taxonomy of electric vacuum sources

### Dry rotary vane (Becker VT/VX, Busch Seco, Gast oil-less)

Sliding graphite-composite vanes in an eccentric rotor; self-lubricating, oil-free, air-cooled. The classic "electric ejector replacement" for woodworking/pick-and-place.

- **Becker VT 4.25**: 25 m³/h (417 l/min) @ 50 Hz, 0.75 kW, ultimate 150 mbar abs (≈ −86 kPa), continuous duty (https://www.becker-international.com/in/products/vacuum-pumps/rotary-vane-vacuum-pumps-oil-free/vt-series/vt-4.25.htm).
- **Becker VT 4.40** (US datasheet): 28.3 CFM (800 l/min) @ 60 Hz, 1.5 kW, ultimate 150 mbar abs ≈ −86 kPa, 67/72 dB(A), ~38–41 kg, **vane lifetime "up to 8,000 operating hours"** printed on the sheet (https://beckerpumps.com/wp-content/uploads/2022/01/VT_4.40_Vacuum_pumps_us.pdf).
- Specific power ≈ **1.8–1.9 W per l/min** of displacement.
- Maintenance: no oil ever, but vanes are a wear part — OEM figure 8k h; premium vanes are marketed to ~20k h (https://elitevak.com/carbon-vs-fiber-vanes-which-does-your-vacuum-pump-need/). Vane dust and seizure-on-humidity are the known failure modes.

### Claw pumps — the low-maintenance industrial choice

Two claw-shaped rotors counter-rotate in a housing, synchronized by an external timing gearbox, **never touching each other or the housing**; air is trapped, internally compressed and expelled. No vanes, no oil in the compression chamber, no contacting wear parts at all — the only maintenance item is gearbox oil (order-of-years interval) (https://www.buschvacuum.com/us/en/products/vacuum-pumps/claw/claw-technology/, https://www.ohiomedicalparts.com/services/how-to/maintain-a-rotary-claw-vacuum-pump.php).

- **Busch Mink MM 1104 BV**: 62/75 m³/h (1,030/1,250 l/min) @ 50/60 Hz, 1.5/1.7 kW, **ultimate 60 mbar abs ≈ −95 kPa**, 66/70 dB(A). Top of the same frame (MM 1142 BV): 140/175 m³/h at 3.5/4.8 kW (https://www.buschvacuum.com/global/en/products/vacuum-pumps/claw/mink/).
- **Busch Mink MV 0040**: 40 m³/h class, ~1.3–2.1 kW, ultimate ~40 mbar (https://www.buschvacuum.com/us/en/products/mink-mv-0040-0080-d-synchro.html).
- Specific power ≈ **1.3–1.5 W per l/min** — better than vane because internal compression + no friction. Busch markets Mink as "highly energy-efficient and nearly maintenance-free"; the contact-free principle means pumping speed does not degrade over life (https://www.buschvacuum.com/global/en/technology/dry-claw-vacuum-pumps).
- This is what you buy when you want ejector-class depth (−90 kPa+) plus 2–4× the flow per watt, running 16 h/day for years with no consumables. Downsides: cost (claw ≈ 2× vane for same flow), weight (25–100 kg, floor-mounted only).

### Screw pumps (brief — overkill)

Dry twin-screw (Busch COBRA): ultimate ≤ 0.1 mbar, 100–650 m³/h, 1.1–7.6 kW (https://www.buschvacuum.com/global/en/products/vacuum-pumps/screw/cobra-industry/). Process-vacuum class. For box gripping the extra two decades of vacuum depth buy nothing — force saturates at −101 kPa — and you pay in cost and complexity. Not relevant here.

### Side-channel / regenerative blowers (Becker SV/VASF, Elmo Rietschle G-BH)

A bladed impeller regenerates momentum transfer around a toroidal channel. **No internal contact, no wear parts, bearings are the only maintenance item** — Elmo Rietschle quotes a **20,000 h service interval** for G-BH1 (https://www.elmorietschle.com/en/side-channel/g-bh1/).

- Depth: single-stage typically −150…−300 mbar; two-stage to ~−450 mbar; the largest G-BH1 frames reach Δp up to 780 mbar at multi-kW sizes. Flow: up to 2,500 m³/h at the top of the range.
- **Becker SV 201/1**: 2.7 kW, 3,820 l/min open flow → **≈ 0.7 W per l/min** (https://beckerpumps.com/products/compressors/side-channel-blowers/single-stage-compressor-pumps/sv-series/sv-201-1/).
- **Becker VASF 2.80/1** (VARIAIR Speed Flow — Becker's side-channel line with integrated variable-frequency drive to 300 Hz): 750 l/min open flow, max vacuum ≈ −28 kPa, 0.82 kW → ≈ 1.1 W/(l/min), oil-free, contact-free (https://www.beckerpumpsales.com/becker-vasf-1-stage-vac.php). The two-stage VASF 2.80/2 (1.1 kW, 45 m³/h, quoted to us at ~€2–3.5k, also in 24/48 V DC variants) reaches substantially deeper — earlier research recorded −500 mbar class at low flow thanks to the 300 Hz drive.
- Mains-powered, ~70 dB(A), essentially fit-and-forget. The classic centralized source for foam/large-area grippers on porous product.

### BLDC blower cartridges (Ametek Windjammer, Domel) — the Stretch/Pickle class

Multi-stage centrifugal blower + brushless EC motor in a 4–6" cartridge. 24/48 VDC, battery-native, 0–10 V or PWM speed control, mass ~2–4 kg.

- **Ametek Windjammer 5.7" family**: pressures up to 170 inH2O (−42 kPa) and flows to 275 CFM (7,790 l/min) (family maxima, not simultaneous). Concrete units: 150420-51, 48 VDC, 2-stage, **375 W**, 0–10 V speed control (https://optimaldist.com/collections/thru-flow/products/150420-51-ametek-windjammer-brushless-blower-5-7-48-vdc); 150418-50, 48 VDC, 3,100 l/min, −32 kPa; 24 V 3-stage 150402-50: 1,750 l/min, −20 kPa (https://www.thevacuumfactory.com/product/ametek-windjammer-150402-50-brushless-24-volt-blower-motor/).
- **Domel**: 1–3 stage brushless blowers with integrated controller, thermal/overcurrent/soft-start protection (https://www.domel.com/products/brushless-blowers-pumps-54). Life caveat: Domel's appliance-grade cartridges are specified 1,000–5,000 h depending on series — treat as consumables; Windjammer's industrial line is rated 20,000 h continuous (https://optimaldist.com/products/116638-58-ametek-windjammer-brushless-blower-5-7-120vac-48-9cfm-64-92-in-h2o-bypass-elec-cl).
- Specific power at working point ≈ **0.1–0.5 W per l/min** — an order of magnitude below any positive-displacement pump, because they only sustain −20…−40 kPa.
- Brushless motor life 10,000–25,000 h (bearing-limited) vs 1,000–3,000 h for brushed vacuum motors (https://blog.bisonametek.com/oem-air-moving-blog/brushed-vs-brushless-motors).
- Light enough to mount **on the arm or inside the gripper**, killing the hose-conductance problem entirely.

### Diaphragm & piston pumps (mobile/cobot class)

Small oil-free displacement pumps, 10–60 l/min per head, banked for more. Deep vacuum (−60…−85 kPa) but tiny flow → only for sealed surfaces. The canonical example is the OnRobot VGP20's integrated pump bank: ~110 W max, up to ~48 l/min total, −61 kPa — works because each cup is individually managed and it never has to fight a big leak (full teardown of its datasheet in Chapter 7). Not the container-unload class.

## 3.2 What the picking-robot companies actually run

| Company / robot | Vacuum source | Depth/flow class | Mounted | Power |
|---|---|---|---|---|
| Boston Dynamics **Stretch** | "New, quieter **onboard vacuum pump**" (BD's own wording); high-flow class, per-cup valving ("Smart Gripper": cups with good contact get full suction, bad ones are shut off; pressure sensor per cup assembly, patent US 12,441,002 "Robotic gripper with seal detection") | Boxes to 23 kg; 600–800 cases/h | Pump onboard robot body; sensors + pneumatic valves in gripper | **Battery only**, up to 16 h runtime, no facility air or power tether (https://bostondynamics.com/blog/idea-to-application-with-stretch/, https://patentsgazette.uspto.gov/week41/OG/html/1539-2/US12441002-20251014.html) |
| **Pickle Robot** | "Powerful **vacuum motor** that **sounds like an aircraft engine**" (press description) — i.e., high-flow blower stack, not ejectors; large-contact-area suction plate | Boxes to 50–60 lb; up to 1,500 boxes/h | On the manipulator platform at the dock | Dock/facility electric power (https://newatlas.com/robotics/mit-pickle-one-armed-warehouse-robot-suction-unloading/) |
| **Anyware Robotics Pixmo** | Vacuum end-effector on a FANUC cobot + **mechanical rest**: patented vertical-lift conveyor between robot and wall **supports the box weight so suction only has to translate, not carry** — this is how a cobot-class arm and modest vacuum reach 65 lb boxes | 65 lb boxes, 1,000/h with add-on | AMR base | Battery (https://anyware-robotics.com/anyware-robotics-unveils-unloading-add-on-for-its-pixmo-robots-that-further-increases-container-unloading-throughput/) |
| **XYZ Robotics RockyOne** | "Multimodal smart gripper," suction pick from top or side; self-contained mobile manipulator ("no additional infrastructure") → onboard electric vacuum | 30 kg boxes; >800 cases/h multi-pick | Mobile base | Battery (https://www.xyzrobotics.com/rocky-mmr/rockyone) |
| **Contoro** | "Fully **self-contained and battery-powered, including the vacuum pump** for the gripper"; articulated two-sided suction gripper on a KUKA arm | 80 lb boxes; 300–350 cases/h; 8 h per charge | Mobile base | Battery (https://www.automatedwarehouseonline.com/contoro-robotics-raises-series-a-funding-to-scale-trailer-unloading-automation/) |
| RightHand Robotics RightPick | Suction cup + underactuated fingers, item-picking class; generation method not published | Small items | Workcell | Mains |
| Dexterity DexR/Mech | Suction case gripper on dual arms, mobile trailer loader; mobile chassis implies onboard electric | Cases | Mobile chassis | Onboard (https://www.therobotreport.com/dexterity-launches-mech-dual-armed-mobile-manipulator-for-truck-unloading/) |
| Copal C2 (fixed container unloader) | Vacuum plate grippers (PullPlate/PushPlate, 8 modules × 4 cups) on a mains-powered gantry — fixed installation, free choice of industrial pump | Mixed cases/trays | Machine frame | Mains (https://www.copalhandlingsystems.com/pullplate) |

Pattern: **every battery/mobile machine uses an onboard electric vacuum source; nobody ships a compressor + ejector on a mobile base.** The two published descriptions that leak implementation detail (Stretch "quieter pump", Pickle "aircraft-engine vacuum motor") both point at the high-flow blower class, with per-cup/zone valving to concentrate flow where the seal is good. (Data-quality note: Stretch/Pickle/RockyOne internals aren't published as datasheets — attributions rest on vendors' own press wording plus the physical constraint that battery platforms preclude compressors.)

## 3.3 Why electric instead of compressor + ejector

1. **End-to-end energy.** Becker's worked example: a 3-ejector station at −600 mbar consumes 341 l/min of 6-bar air = **2.28 kW of compressor electrical power**; the single VT 4.16 vane pump that replaces it draws **0.75 kW** — **3× at like-for-like depth and duty** (https://www.becker-international.com/uk/good-to-know/mechanical-vacuum-pump-vs-ejector.htm). Industry surveys put the general figure at electric pumps needing **1/4 to 1/10 the energy** of venturi generators for the same suction duty (https://www.plantservices.com/articles/2005/530/). Against blowers on shallow-vacuum duty the gap widens further.
2. **Concrete gripper-level illustration** (Schmalz's own datasheet, same gripper two ways): FXP-60 (integrated ejectors) consumes **165–300 l/min of 5-bar compressed air** to generate 270–425 l/min suction; the FMP-60 (external-vacuum variant of the same gripper) needs only **61–176 l/min of flow at −250 mbar** delivered by any electric source (https://media.schmalz.com/MAM_Library/Dokumente/Technical_Information/30/3030/303001/30300103662/d1c166458522_DS_30.30.01.03662_en-EN.pdf).
3. **Battery viability.** 341 l/min of 6-bar air is a ~2.3 kW continuous compressor — hours of a mobile robot's entire battery. A 375 W Windjammer providing more suction flow than five ejectors is trivially battery-fed at 48 V. This alone decides it for Stretch/Pixmo/Contoro/RockyOne.
4. **Curve shape matches cardboard.** A blower holds −20…−30 kPa while swallowing thousands of l/min of leak; an ejector's suction flow collapses toward zero as it approaches rated depth — on a leaky box it never gets there and just burns air.
5. **No infrastructure.** No compressor room, dryer, drops, FRLs, or leaking fittings at the customer site — a major sales argument for every vendor above.
6. **Noise.** Ejector exhaust can be up to 16× louder than an electromechanical pump (Becker, same source); measured pump values: VT 4.40 67–72 dB(A), Mink MM 1104 66–70 dB(A). BD explicitly advertised the *quieter* pump as a Stretch improvement.

## 3.4 Depth, honestly (the "ejector draws deeper than a pump" question)

| Source | Achievable gauge vacuum |
|---|---|
| Multi-stage ejector | −85…−95 kPa easily, instantly |
| Dry vane / claw | −85…−95 kPa (VT: 150 mbar abs; Mink: 60 mbar abs) |
| Two-stage side channel | −30…−45 kPa (big frames / 300 Hz VASF deeper) |
| BLDC blower cartridge | −20…−42 kPa |
| Diaphragm/piston | −60…−85 kPa at tiny flow |

So the gut feeling "ejectors draw a deeper vacuum than a vacuum pump" is *half right*: a €50 ejector out-deepens most cheap dry pumps and every blower — but an industrial claw pump matches or beats it (−95 kPa), and **for porous cardboard depth beyond ~−40 kPa is unusable anyway**. Holding force = ΔP × effective sealed area. A large-area foam gripper with 0.08–0.15 m² engaged at a mere −20 kPa gives 1,600–3,000 N — versus ~400 N for four Ø75 cups at −60 kPa. On porous faces the *achieved* vacuum is set by the intersection of the leak curve and the pump curve: a deep-vacuum, low-flow source sits on the steep part of its curve and collapses to near-zero ΔP once leakage exceeds its flow; a blower barely notices the leak and keeps ΔP pinned near its stall pressure. Where you genuinely need −80 kPa (sealed glossy boxes, small cups, high acceleration), claw/vane delivers it — blowers do not; that's the one honest reservation.

## 3.5 Centralized pump + vacuum line to the gripper

- **Hose conductance is the whole game.** Turbulent pressure drop scales ~1/d⁵: going 25 mm → 32 mm ID cuts line loss ~3.4×; → 50 mm by ~32×. Blower systems move thousands of l/min at only 200–400 mbar of total budget, so 32 mm ID is the practical floor and 38–50 mm is typical (https://www.thinkvacuums.com/size-of-vacuum-pipe). Becker's piping rule: never neck below the pump inlet diameter; a single short-radius 2" elbow adds ~60 inches equivalent length (https://beckerpumps.com/news/sizing-pipes-for-a-vacuum-pump/).
- **External-vacuum gripper heads exist off the shelf:** Coval **MVG "G0"** — the modular foam/cup gripper with a G1"-F flange specifically for an external source ("impeller [blower], electric vacuum pump, or multi-stage pump"), flow-control nozzles or patented check valves per cell, sizes 150×150 to 1200×1000 mm (https://doc.coval.com/g/MVG/doc/mvg_doc_coval_2025_v07-01_us.pdf). Schmalz **FMP** (external-vacuum twin of FXP) "ideal for operation with high performance pumps and blowers". AIRBEST TXM foam bar grippers are offered explicitly in "external blower" variants (https://www.airbest.com/products/txm-series-blower-type-vacuum-grippers/).
- **Response time pattern:** the electric pump runs continuously; a per-gripper valve (and optionally a vacuum reservoir between pump and valve) gives grip response comparable to an ejector — the reservoir supplies the initial evacuation surge, the pump handles steady leak. For blowers, many integrators skip the valve entirely and modulate blower speed (spin-up <1 s), since a dead-headed blower draws minimum power.
- Coval's own numbers show what the ejector alternative costs at this scale: the largest integrated-ejector MVG (D3, 2× CMSHDE 100) consumes **840 l/min of compressed air** to produce 2,200 l/min of suction. Two such grippers ≈ 1,700 l/min of 5-bar air ≈ a 10+ kW compressor.

## 3.6 Power budget under 3600 W (230 V / 16 A)

Current state: 2 grippers × 265 l/min of ~6.5-bar air implies ~5.2 kW of piston compressor running near 100% duty — **already over the 3600 W group** — for perhaps 350–450 l/min of usable suction via the ejectors.

Electric scenarios, all inside 3600 W with room to spare:

- **A. One claw pump, ejector-class depth:** Busch Mink MM 1104 BV, 1.5 kW → 1,030 l/min at up to −95 kPa, shared via 2 zone valves + reservoir. Matches today's depth, roughly triples usable flow, uses ~42% of the wall budget, near-zero maintenance.
- **B. Two vane/claw pumps (one per gripper):** 2× VT 4.25 (0.75 kW each, 417 l/min, −86 kPa) = 1.5 kW; or 2× Mink MM 1104 = 3.0–3.4 kW for 2,100–2,500 l/min at full depth — the maximum-performance mains option, still ≤ 3.4 kW.
- **C. Side-channel, flow-optimized:** one Becker SV 2.7 kW class → ~3,800 l/min open flow at −200…−300 mbar into a manifold feeding both heads; or 2× VASF 2.80/1 (0.82 kW each, 750 l/min, −28 kPa, integrated VFD) = 1.65 kW total.
- **D. BLDC blowers at the grippers:** 2× Windjammer 48 V, 375 W each → **750 W total** for 2,500–7,800 l/min-class flow at −18…−42 kPa, **no vacuum hose runs at all** (blower in the gripper head), speed-servoed per pick. This is the Stretch/Pickle architecture and the only one that also survives a future move to a mobile base.

Every scenario delivers more suction flow per gripper than the ejectors do today, at 20–90% less wall power, and options A/B keep full −86…−95 kPa depth for sealed boxes.

## 3.7 VFD / EC-motor control — the electric analog of "air saving"

Ejector installations save air with on/off air-saving valves; the electric equivalent is speed control, and it is better because blower power scales roughly with the cube of speed and displacement-pump power near-linearly. Becker's **VARIAIR** program: KVT vane pumps with integrated frequency converter (30–60 Hz window) and VASF side-channel units driven to 300 Hz, holding constant vacuum setpoint under fluctuating leakage and idling down between picks (https://www.becker-international.com/de/en/products/vacuum-pumps/rotary-vane-vacuum-pumps-oil-free/variair-kvt-series.htm); typical VSD retrofit savings on vane pumps ~25% (https://vac-cube.com/blog/post/vacuum-generators-vs-electric-pumps-which-one-fits-your-industrial-needs). BLDC cartridges get this for free (0–10 V/PWM, closed-loop) — hold a −10 kPa "search" vacuum, ramp to full the instant cup-pressure sensors detect seal: exactly the per-cup logic Boston Dynamics patented at the valve level.

## 3.8 Technology comparison table

| Technology | Example | Max depth | Flow class (this size) | Wall power | W per l/min | Noise dB(A) | Maintenance | Cost class | Battery-viable? |
|---|---|---|---|---|---|---|---|---|---|
| Compressor→ejector (our baseline) | 2×2.6 kW piston + 265 l/min ejectors | −90 kPa | ~350–450 l/min suction (2 heads) | ~5.2 kW | ~4–10+ (chain) | loudest (exhaust) | Compressor service, dryers, leaks | Low capex, high opex | **No** |
| Dry rotary vane | Becker VT 4.40 | −86 kPa | 800 l/min | 1.5 kW | 1.9 | 67–72 | Vanes ~8k h (to 20k premium), filters | €€ | Marginal |
| **Claw** | Busch Mink MM 1104 BV | **−95 kPa** | 1,030–1,250 l/min | 1.5–1.7 kW | 1.3–1.5 | 66–70 | Gearbox oil only; no wear parts | €€€ | Marginal |
| Dry screw | Busch COBRA | −101 kPa | 100–650 m³/h | 1.1–7.6 kW | n/a | — | Low, process-class | €€€€ | No — overkill |
| Side-channel blower | Becker SV / VASF | −20…−45 kPa | 750–3,800 l/min | 0.8–2.7 kW | 0.7–1.1 | ~70 | ~20,000 h bearings | €€ | Marginal (VASF VFD-native) |
| **BLDC blower cartridge** | Ametek Windjammer 5.7" 48 V | −20…−42 kPa | 1,750–7,800 l/min | **0.375 kW** | **0.1–0.5** | moderate | 10k–25k h, zero service | € | **Yes — the Stretch/Pickle class** |
| Diaphragm/piston bank | OnRobot VGP20 internal | −61 kPa | ~48 l/min | 0.11 kW | ~2.3 | 67–71 | Diaphragms ~5k h | €€ (as gripper) | Yes, sealed surfaces only |

Caveat on the W-per-l/min column: it compares displacement/open-flow ratings, not equal-depth working points — blowers only look 10× better while you stay above ≈ −40 kPa, which leaky cardboard does.

---

# Chapter 4 — Smart gripper heads: how a gripper "recognizes a hole"

## 4.1 The core problem: uncovered cells are a giant calibrated leak

A large-area ("mat" or "foam") gripper is a plenum with dozens to hundreds of suction apertures. Pick a small box with a 130×400 mm head and 60–80% of the apertures stay open to atmosphere. Each open Ø12–16 mm hole flows tens of l/min at 400–600 mbar differential, so an uncovered gripper needs *thousands* of l/min to hold any vacuum — either the vacuum collapses below holding threshold or the vacuum source (and compressor) is sized for the worst case and runs there permanently. That is exactly the 240–265 l/min-per-head, always-on regime of a plain foam pad on a plain ejector. Three counter-mechanisms exist, in increasing sophistication:

**a. Per-cell check valves — the "recognizes a hole" mechanism.** A small ball (or poppet/flap) sits in each cell's bore. A *covered* cell sees low flow: the ball hangs off its seat and vacuum reaches the box. An *uncovered* cell sees high-velocity flow; drag lifts the ball onto the seat and the cell self-closes, preserving plenum vacuum. The threshold is set by orifice geometry, ball mass, and seat design — i.e., the valve closes when flow through the cell exceeds a calibrated value, which is functionally "detecting a hole," with zero electronics. Users: Schmalz (SVK ball-seat valves in FXP/FMP area grippers; the standalone SVV has a screw-adjustable closing flow), Coval (patented check valves in CVG/MVG/CVGC foam plates: "valves transfer the suction flow only when the part is present and close automatically if it is absent"), AIRBEST (TXM "-V" option = ball-valve structure, "built-in check valve automatically blocks free suction ports"), VMECA (check valve + filter integrated in every V-Grip orifice, ordered in two calibrated classes: type 1 for airtight parts, type 2 for 1–10% leakage parts — the threshold is explicitly spec'd against workpiece porosity), Piab Kenos (configurable option on KVG/KFG), and Joulin (the original patentee: one auto-regulated valve per opening, "closes where there is no product," no reprogramming between layer patterns).
Failure modes: cardboard dust and shrink-wrap shreds lodging between ball and seat (valve leaks or sticks); a stuck-closed valve permanently dead-ends a cell until blown open; and closed valves need a re-open event — most vendors solve this with the blow-off pulse at release, which also back-flushes dust (Coval explicitly: blow-off "ensures the cleaning of the network, the flow resistors or check valves"). Check valves also mis-trigger on very porous boxes: a heavily perforated or torn carton can flow enough air to slam its own cells shut — this is why VMECA sells threshold classes and Schmalz sells the adjustable SVV.
https://www.schmalz.com/en-us/vacuum-technology-for-automation/vacuum-components/valve-technology/check-valves-and-flow-restrictors/check-valves-svk-svkg-svv-308721/ · https://www.trolmation.com/wp-content/uploads/2021/04/cvm_cvg.pdf · https://www.airbest.com/uploads/file/txm-series-vacuum-gripper-blower-standard-type.pdf · https://www.pkfluid.com/data/web-pages/attachments/orig/vmeca-gm-gripper.pdf · https://www.joulin.com/company/vacuum-technology.html

**b. Flow restrictors (orifices) per cell.** A fixed 0.6–1.1 mm orifice in each cell caps the leak of every uncovered hole to a few l/min. Simpler, nothing to jam, tolerant of dusty air — but *every* uncovered cell leaks forever, so the vacuum source never rests, and evacuation of covered cells is slower (throttled both ways). Piab's standard Kenos technology is "Flow Reduction 0.6 mm"; Coval's suction-cup plates use Ø0.7/0.9/1.1 mm restrictors; Schmalz's SW option is the same idea. AIRBEST's TXM default (no -V) is a "throttling hole structure." Restrictors are preferred where parts swivel/peel during motion (a briefly unloaded cup re-primes instantly; a check valve would latch shut).
https://neffautomation.com/hubfs/Resources/Piab/Piab%20Kenos%20Vacuum%20Gripper%20Datasheet.pdf · https://www.powermotiontech.com/packaging/suction-cups-hold-tight

**c. Active zone switching.** Solenoids shut whole zones based on the pick plan or sensing. Coval MVG offers factory-configured independent zones ("multizoning"); Schmalz's FMG MATRIX-GRIPPER is the extreme: modules of 12 suction points on a 30 mm grid, each point individually activated by pilot air, orchestrated over IO-Link — the gripper energizes only the cells over the box. Biggest savings and true "pick one box out of a layer" capability, at the cost of valves, controls, and integration with vision/pose data.
https://www.schmalz.com/en-us/career-company/latest/news/fmg-matrix-area-gripper-easy-to-operate-and-flexible-to-use · https://www.coval-inc.com/news/product-news/MVG-Modular-vacuum-gripper_2272.htm

## 4.2 Foam vs bellows cups vs flat cups on corrugated cardboard

- **Sealing foam** (EPDM/NBR, typically 20–40 mm thick, apertures punched through) conforms to box ribs, tape ridges, staples, wrap wrinkles and crushed corners; it grips across gaps and undefined pick positions. The default for mixed corrugated. Downside: it is an abrasive-wear **consumable**. AIRBEST states flatly "sponges are consumables… replace in time or adsorption suffers"; Piab sells KCS foam as a one-line spare (EPDM 30 mm); Schmalz sells quick-change sealing foam plates with adhesive backing so a swap is minutes, and notes service life depends on surface roughness, vacuum level, cycle rate — corrugated is the fast-wear case. Plan foam plates as a stocked wear part (tens of € for Chinese spares to low hundreds for Schmalz/Piab); in high-cycle depalletizing, weekly-to-monthly swaps are normal, driven by visible glazing/tearing and rising leak flow.
- **Bellows cups (1.5–2.5 folds)** are the alternative interface on the same bodies (Schmalz SPB2 40 on FXCB; Coval bellows plates). They tolerate height steps and tilted boxes, seal better than foam on smooth intact carton, last longer — but each cup lip is a point-seal that fails on ribs/tears exactly where foam succeeds.
- **Flat cups** need flat, closed surfaces — wrong answer on container corrugate except as reinforcement on known-good faces.
https://www.schmalz.com/en/vacuum-technology-for-automation/vacuum-components/area-gripping-systems-and-end-effectors/sealing-foams-for-area-gripping-systems/

## 4.3 Product deep-dive

**Schmalz FXCB/FMCB (cobot large-area line).** FXCB = integrated SEP ejector modules, FMCB = external vacuum. Example FXCB-SW150 297: 297×123×158 mm, 2.2 kg, 15 cells, 354 l/min max suction, flow-restrictor cells, bellows or foam, integrated VSi vacuum switch with IO-Link, rounded cobot housing; ~35 kg payload class; street price ≈ €3,242 (https://unchainedrobotics.de/en/products/end-of-arm-effectors/grippers/vacuum-grippers/flaechengreifsystem-fxcb-sauggreifer).

**Schmalz FXP/FMP with SVK (the classic industrial mat).** 130 mm wide, lengths 442–1432 mm; foam or cups; SVK ball check valves ("porous workpieces, gaps, undefined pick position") or SW restrictors; SEMP multi-stage ejectors, 250–875 l/min drive air. Example FXP-SVK 442 3R18: 442×130×70 mm, 2.2 kg, 66 cells, **1050 l/min max suction from 250 l/min drive air**, 550 N suction force at −250 mbar. Note: FXP/FMP is phasing out (orderable to 12/2027, successor FA-X/FA-M); FXP-i/FMP-i variants add IO-Link condition monitoring and digital air-saving (https://www.schmalz.com/en/vacuum-technology-for-automation/vacuum-components/area-gripping-systems-and-end-effectors/10.01.38.00680).

**Coval MVG (our shortlisted candidate).** Modular made-to-measure gripper, any size 150×150 to 1200×1000 mm; interface = foam plate, suction-cup plate, or COVAL-Flex; per-hole flow restrictors or patented check valves (check valves only on foam plates); factory multizoning; VA electronic vacuum switch (two PNP thresholds, adjustable hysteresis). Vacuum generation: **G0 = no generator** (external vacuum via large flange — the version to pair with a remote pump/blower), or integrated multi-stage venturi modules. The sibling CVG catalog gives hard numbers at 130 mm width: lengths 424/624/824 mm; foam plates Ø12 "mini" (98 holes on 424) or Ø16 "maxi"; holding force 1100/1650/2200 N at 85% vacuum (600/900/1200 N at 45%); integrated CMSE50 generator = 900 Nl/min suction from 190 Nl/min drive, CMSE100 = 1800 from 380 Nl/min; weights 2.1–5.75 kg (https://doc.coval.com/g/MVG/doc/mvg_doc_coval_2025_v07-01_us.pdf).

**Coval CVGC (carbon cobot line).** Same plate/valve tech in a carbon monocoque (2.5× lighter than aluminum, 6× stiffer): 240×120, 320×160, 350×250 mm; G0 (external) or M2 (integrated venturi); max 85% vacuum; UR+/CRX certified (https://www.coval.com/vacuum-grippers/carbon-vacuum-grippers-for-cobots-cvgc-series).

**Piab Kenos KCS / KVG.** KCS: 110×110 mm cobot gripper, 0.62 kg, EPDM foam 30 mm, 0.6 mm flow reduction, 1–2 COAX SX42 cartridges (~132 l/min drive at 4.7 bar; 440 Nl/min free suction, max ~90% vacuum), ~8 kg payload. KVG: the large-area line — widths 60/120/150 mm, length 300–2000 mm, integrated COAX or external vacuum, configurable **check valves, flow restrictors, solenoid zone valves and piSAVE sense** per application (https://www.piab.com/robot-and-cobot-gripping-solutions/kenos-vacuum-gripping-systems/kvg/kenos-vacuum-gripper-kvg150).

**AIRBEST TXM (our second candidate) / TXC.** TXM = external-vacuum "blower standard type" aluminum body, 130 mm wide, lengths 400–1400 mm; sponge plates in 1/3/5-row hole patterns (A1/A3/A5) or Ø30/Ø40 cup plates; **suffix -V = ball non-return valve per hole; default = throttling holes — order the -V.** TXM130×400-A3-V: 434×130 mm, 2.3 kg, 65 suction holes, φ32 blower port, theoretical force 227 N at −40 kPa (344 N at −60 kPa); the 130×400 footprint is a near drop-in for our 140×340 pads. Sponge spare plates sold by size. One vacuum port + 8 G1/8 vacuum-detecting ports for switches; T-slots for sensors. TXC = same head with integrated venturi. Sold direct and via Alibaba at Chinese-market pricing (https://www.airbest.com/products/txm-series-blower-type-vacuum-grippers/).

**OnRobot VGP20 (the no-compressed-air all-in-one).** Full teardown in Chapter 7. Integrated electric pump, ~$6,925. Zero compressor air — but ~48 l/min of total flow is two orders of magnitude below an ejector-fed foam mat; it works because each channel is individually managed. Best for clean-ish boxes, not leak-dominated container unloading.

**VMECA V-Grip GM130 (Magic Gripper family).** Aluminum body, 130 mm wide, 220–1200 mm long, EPDM foam with oval or round holes, **check valve + filter in every orifice** with two calibrated threshold classes; integrated Magic multi-stage cartridges. GM130X400-L4: 416 Nl/min drive at 6 bar, up to 1448 Nl/min suction, −75 kPa max, 2.2 kg — and uniquely honest partial-coverage data: **1005 N held at just 40% coverage** (2472 N at 100%). GMF variant = same head, external vacuum (https://www.pkfluid.com/data/web-pages/attachments/orig/vmeca-gm-gripper.pdf).

**Joulin (the OG).** Invented and patented the auto-regulating foam-gripper valve for lumber handling; Valve Gripper, Port Gripper, Foam-Valve and Bag variants; auto-regulated "Wave System" claims up to 50% energy savings; handles full layers, partial layers and single boards with no re-setup. Now the layer-gripper specialist inside Piab Group (https://www.joulin.com/company/vacuum-technology.html).

### Comparison table (foam-interface, ~130–150 mm wide class)

| Product | Size (example) | Cell shutoff | Vacuum source | Drive/suction flow | Force (example) | Weight | Sensing | Price signal |
|---|---|---|---|---|---|---|---|---|
| Schmalz FXP-SVK 442 | 442×130 mm, 66 cells | Ball check valves (SVK) | Integrated SEMP ejector | 250 → 1050 l/min | 550 N @ −250 mbar | 2.2 kg | VSi switch, FXP-i IO-Link | phase-out 2027; FA-X successor |
| Schmalz FXCB 297 | 297×123 mm, 15 cells | Restrictor | Integrated SEP | ~160 → 354–526 l/min | 350 N horiz. | 2.2 kg | VSi + IO-Link | €3,242 |
| Coval MVG (G0) | 150×150–1200×1000 custom | Patented check valves (foam) or restrictors | External (G0) or 1–2 venturis | CMSE100: 380 → 1800 Nl/min | CVG624: 1650 N @ 85% | ~2–6 kg | VA switch, 2 thresholds | quote |
| Piab Kenos KVG150 | 150 mm × 300–2000 mm | Check valves or restrictors (config) | COAX integrated or external | config | config | config | piSAVE sense | quote |
| AIRBEST TXM130×400-A3-V | 434×130 mm, 65 holes | Ball non-return valves (-V) | External blower/ejector, φ32 port | user-sized | 227 N @ −40 kPa | 2.3 kg | 8× G1/8 sensor ports | low (Alibaba) |
| VMECA GM130X400-L4 | 406×130 mm | Check valve + filter every hole, 2 threshold classes | Integrated cartridges (or GMF external) | 416 → 1448 Nl/min | 1005 N @ 40% coverage | 2.2 kg | Digital switch | mid |
| OnRobot VGP20 | 16 cups | Per-channel electric control | On-board electric pump | ~48 l/min | 20 kg payload | 2.55 kg | Airflow monitoring | $6,925 |
| Joulin VG/EGB | layer-size custom | Patented auto valves | Blower/pump | application | layer loads | custom | option | quote |

## 4.4 Why check valves + air-saving ejector is the actual money combo

The savings come from a *system* interaction, not from either part alone. An air-saving ejector stops driving air once setpoint vacuum is reached and re-fires only when vacuum decays below a floor; Piab's Vacustat check valve additionally traps the vacuum so a sealed pick consumes "virtually no air." This only works if the gripper-side leak is small enough that vacuum *holds* between top-ups. Plain foam mat + plain ejector: uncovered holes leak hundreds of l/min, the setpoint is never reached, air saving never engages, consumption = 100% duty at full flow — **our current 240–265 l/min**. Foam mat *with per-cell check valves*: uncovered cells latch shut within the first evacuation, residual leak is only the covered-but-imperfect cells plus carton porosity, the ejector reaches setpoint and drops to intermittent pulses — this is where the routinely quoted 60–90% consumption cuts come from (and multi-stage ejectors add another ~2–4× suction per drive-liter at the low vacuum levels cardboard needs). Guard rail: corrugate itself is porous, so on bad boxes the control can start hunting; Schmalz's regulation auto-disables air saving if it switches more than 6 times in 3 s and falls back to continuous suction — the correct failure direction (https://www.schmalz.com/en-us/solutions/media-center/explanation-of-the-air-saving-regulation-in-compact-ejectors).

## 4.5 Sizing rule

Required suction flow ≈ Σ(covered-cell imperfection leak, dominated by carton porosity and seal quality on ribs) + Σ(uncovered-cell threshold leak: ~0 for latched check valves, orifice-capped for restrictors) + margin for the evacuation transient. Manufacturers refuse to publish universal l/min-per-cm² for corrugated because porosity varies carton-to-carton; Schmalz's published per-cup table (8.3 l/min per cup ≤Ø60, 16.6 ≤Ø120, 33.3 ≤Ø215, 66.6 ≤Ø450) applies to airtight surfaces only, with an explicit instruction to run a suction trial on the real workpiece for porous material (https://www.schmalz.com/en/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/system-design-calculation-example/vacuum-generator-selection). Coval's guidance: size porous picks in the economical 30–55% vacuum zone (deep vacuum on cardboard wastes air and crushes boxes; hold force comes from area). Practical anchors: vendors pair a 400 mm foam head with roughly **900–1800 Nl/min of free suction capacity** (CMSE50/100, VMECA 1448 Nl/min, Schmalz 1050 l/min) — an order of magnitude more *available* flow than a plain single-stage ejector delivers, achieved from 190–420 l/min of drive air, and throttled back to near zero on sealed picks by the check-valve/air-saving pair.

## 4.6 Vacuum sensing: grip-confirm, part-present, drop detection

Every serious head carries an analog/digital vacuum switch on the plenum: threshold 1 = "grip confirmed, start move" (e.g., −250 to −400 mbar on cardboard), threshold 2 (lower, with hysteresis) = "losing the box" for in-motion drop detection and e-stop/slow-down. Coval's VA switch gives two PNP outputs with 0–99% adjustable hysteresis; Schmalz's VSi does the same over IO-Link so the PLC can read the analog vacuum curve (leak trending also predicts foam wear); AIRBEST exposes 8 G1/8 detection ports so you can zone your own sensors across the plate — useful for crude part-present-per-zone on a dumb head. OnRobot instead monitors pump airflow continuously (flow ≈ leak = grip quality). Part-present before lift = vacuum reaches threshold within a timeout; with check valves the plenum still pulls down on a missed pick — so use time-to-threshold or a zone sensor, not just level.

## 4.7 The pattern worth internalizing

The intelligence that matters operationally is (1) per-cell passive shutoff (no software), (2) plenum vacuum telemetry with two thresholds, (3) air-saving generation, (4) optionally, zone valves driven by the picking plan. For an FR20 container cell with mixed boxes, a 130–150 mm-wide check-valved foam head (Coval MVG G0 or AIRBEST TXM-V as the budget twin) fed by a multi-stage air-saving ejector or an electric pump, with an IO-Link vacuum switch wired to grip-confirm/drop-detect, captures ~80% of the benefit at ~20% of the MATRIX-style complexity.

---

# Chapter 5 — The energy ledger: wall watts to suction

## 5.1 Specific power: what a watt of wall power buys in air

Specific power = electrical input per unit Free Air Delivery, quoted as kW per m³/min at 7 bar (1 m³/min = 1000 l/min).

| Generation path | Specific power @ ~7 bar | l/min FAD per kW | Source |
|---|---|---|---|
| **Theoretical isothermal minimum** | ~3.5 kW/(m³/min) (`W = p₀·ln(p₂/p₀)`) | ~285 | https://www.womackmachine.com/engineering-toolbox/design-data-sheets/horsepower-required-for-compressing-air.aspx |
| Theoretical adiabatic (n=1.4) | ~4.8 kW/(m³/min) | ~210 | same |
| Modern industrial screw (premium) | 6.0–6.8 kW/(m³/min) | 147–167 | https://www.hpccompressors.co.uk/news-resources/blog/what-is-your-air-compressor-s-specific-power-get-more-output-use-less-energy-lower-your-costs/ |
| Industrial screw (typical) | 6.5–8.5 kW/(m³/min) | 118–154 | https://www.aivyter.com/blog/9-performance-parameters-for-industrial-compressor-machine-selection-rotary-screw-vs-reciprocating/ |
| Good oil-lube belt-drive piston (ABAC 2.2 kW: 264 l/min FAD @ 7 bar) | ~8.3 kW/(m³/min) | ~120 | https://www.abacaircompressors.com/content/dam/brands/ABAC/products/piston-compressors/piston-compressors-pad-tech/leaflet/int/ABAC_Tech_leaflet_web.pdf.coredownload.pdf |
| **Our oil-free direct-drive units** | 2600 W / 180 l/min @ 8 bar = **14.4 kW/(m³/min)**; 10.8 @ 4 bar | 69 @ 8 bar | measured/nameplate |

Our compressors run at **~4× the isothermal minimum** and ~2× a decent screw. Beware retail "l/min" figures: many listings quote displacement (intake), not FAD — ABAC's own leaflet shows 504 l/min intake vs 264 l/min FAD for the same 2.2 kW pump.

**Why "most expensive utility":** US DOE tip sheet — "compressed air is one of the most expensive sources of energy in a plant… overall efficiency of a typical compressed air system can be as low as 10–15%", and "only 10 to 20 percent of the electric energy input reaches the point of end-use"; running a 1 hp air motor takes ~7–8 hp of electrical input (https://www1.eere.energy.gov/manufacturing/tech_assistance/pdfs/compressed_air1.pdf). The loss stack: motor (~10–15%), compression heat rejected (~40–50% vs isothermal ideal), leaks/pressure drop (10–30% typical), then the end-use conversion (an ejector converts pressure flow to suction flow at well under unity).

## 5.2 Duty cycle, starts, and why the klixons trip

- **Duty rating.** Cheap oil-free direct-drive piston compressors are rated ~50% duty (S3 50%): run ≤5 min in 10 so heat can leave the head and windings. Exceeding it accelerates ring/seal degradation; sustained over-cycling cuts pump life 30–50% (https://aircompressorzone.com/blogs/resources/air-compressor-duty-cycle).
- **Design life.** Oil-free piston rings (PTFE, no oil film): ~2000–3000 h service life, hobby-grade toward or below the bottom; oil-lubricated piston pumps 5000+ h, industrial recips 10,000–15,000 h; rotary screw 40,000–80,000+ h at 100% duty (https://www.airsupply.co.uk/blogs/what-is-the-life-expectancy-of-an-air-compressor/).
- **Starts.** Each direct-on-line start draws 5–7× rated current and dumps 25–49× normal heating rate into the windings; NEMA MG-1 allows small motors only ~10–30 starts/hour *with mandated rest between starts* (https://www.decaturindustrial.com/how-many-starts/). Compressor practice is stricter: size storage/pressure band for **~6–8 starts/hour** (https://www.airbestpractices.com/technology/compressor-controls/your-air-compressor-may-be-smarter-you-think).
- **Our measured 120 starts/hour is 4–20× over spec.** The klixon tripping is the motor repeatedly reaching insulation-limit temperature; every trip cycle restarts into a hot winding — the canonical kill mechanism for these units.

## 5.3 The full chain: wall W → FAD → suction

**Ejector conversion ratio (verified, single-stage).** Schmalz SBP datasheet at optimal pressure (https://media.schmalz.com/MAM_Library/Dokumente/Datenblatt_Produktfamilie/0_/032/03270/5a6e7118417c_Datasheet_Basic%20Ejectors%20SBP_en-EN.pdf):

| Model | Max suction (l/min) | Air consumption (l/min) | Ratio |
|---|---|---|---|
| SBP 10 | 37.7 | 48 | 0.79 |
| SBP 15 | 71 | 105 | 0.68 |
| SBP 20 | 127 | 197 | 0.64 |
| SBP 25 | 215 | 311 | 0.69 |

Single-stage ejectors deliver **~0.65–0.8 l/min of free-flow suction per l/min of compressed air** — at zero vacuum; suction falls toward zero as vacuum deepens (SBP 25: 215 l/min at 0 mbar → ~half at −300 mbar). Multistage (Piab COAX) ≈ 1.5–3.2:1 — better, but the air itself still costs 8–14 kW per m³/min to make.

**Chain math for our cell (6.5-bar piston air, single-stage ejectors):**

| Stage | Value |
|---|---|
| 2 grippers demand | ~530 l/min compressed air @ 6.5 bar |
| Wall power at our units' specific power (~12–14 W per l/min) | **6.4–7.6 kW** (good piston: 4.4 kW; screw: 3.7 kW) |
| Suction delivered (×0.65–0.8, free-flow) | ~350–420 l/min |
| Net wire→suction | **~0.06–0.08 l/min suction per W** |

**Direct electric vacuum (verified datapoints):**

- Busch Mink MM 1104 BV dry claw: 1,033 l/min at 1.5 kW, −95 kPa: **~0.7 l/min per W — roughly 10× the ejector chain** (https://adara-bg.com/wp-content/uploads/2017/08/Mink_MM-1104-1142-BV.pdf).
- Small dry-vane units in the 1.1–1.5 kW class: 420–670 l/min, still 5–8×.
- Schmalz GCPi electric pump: 46 l/min at 55 W = 0.84 l/min per W (https://www.schmalz.com/en/career-company/latest/news/energy-saving-in-vacuum-automation-pump-instead-of-ejector).

This 5–10× gap **for continuous suction** is the whole argument, and manufacturers on both sides concede it: Piab's own FAQ states that "when operating continuously, the vacuum ejector pump actually uses more energy than a mechanical pump" (https://www.piab.com/faq/vacuum-pumps/does-an-ejector-pump-use-more-energy-than-a-mechanical-pump/).

## 5.4 When ejectors still win (both sides, fairly)

Piab's counter-argument: most vacuum applications are **intermittent** — grip, hold, release. An ejector is massless-response (full vacuum in tens of ms), can be valved off instantly, and with air-save/ES on sealed workpieces it only tops up between hysteresis thresholds; Schmalz itself credits ejector air-save with "savings of up to 95 percent" and calls ejectors converters that turn overpressure into vacuum "almost optimally". Ejectors also win on: zero maintenance, gram-level mass on the end-effector, decentralised generation at each cup (leak isolation, no long vacuum lines), built-in blow-off, and marginal cost ≈ 0 if plant air already exists. **The catch for our cell:** ~265 l/min per gripper means porous/leaky loads — exactly the case where air-save can't idle and the ejector runs continuously, i.e. the case Piab concedes to the mechanical pump.

## 5.5 The cheap fix: oil-lubricated belt-drive piston

A slow-running (≈1000–1400 rpm) belt-drive, oil-lubricated, cast-iron twin on 100 L: 2.2 kW single-phase 230 V gives ~264 l/min FAD @ 7 bar (ABAC leaflet); duty typically 60%+ and far more heat-tolerant (oil film, low rpm, big iron thermal mass), 5,000–15,000 h life class. Street prices: single-phase 100 L 3 hp from ~€370–900 (https://www.agrieuro.de/kompressoren-100-riemenantrieb/einphasige-kompressoren-100-riemenantrieb-3-ps-c-110_1869_504_1411.html). **Oil carryover is a non-issue for ejectors:** Schmalz operating instructions accept "oiled or non-oiled" air, 5 µm filtered (https://media.schmalz.com/MAM_Library/Dokumente/Bedienungsanleitung/30/3030/303001/30300100078/929a10c8b2d6_BAL_30.30.01.00078_en-EN.pdf); a filter-regulator handles it. (Oil mist in blow-off air onto product is the only real concern — coalescing filter on that branch.)

## 5.6 Receiver sizing vs starts/hour

Standard formula: **t = V·(p₁ − p₂)/(q·p₀)** — the time a receiver of volume V bridges demand q across pressure band p₁→p₂ (https://www.engineeringtoolbox.com/compressed-air-receivers-d_846.html). Starts/hour follows from cycle time: t_on = VΔp/(S − D), t_off = VΔp/D (S = supply FAD, D = demand).

| Tank | Band | Demand | Cycle | Starts/h |
|---|---|---|---|---|
| 40 L (current) | 1 bar | 150 l/min avg, S≈240 | ~43 s | **~85–120** — matches our measurement; the tank *is* the cause |
| 200 L | 2 bar | same | ~6 min | **~10** — inside the 6–8/h design zone |

Key subtlety: the tank does **not** change average duty (run fraction = D/S regardless of volume); it converts 120 thermal-shock starts into ~10 long runs — which is what the motor and klixon actually care about — and buys ~90 s of full-draw ride-through per 2-bar band for pick bursts.

## 5.7 Scenarios on one 3600 W / 16 A outlet

| Scenario | Peak wall draw | Continuous air/suction | Verdict |
|---|---|---|---|
| (a) Current 2× 2600 W oil-free pair | 5200 W — **exceeds outlet**; must interlock, so effectively one unit | one unit at ≤50% duty → ~90–120 l/min FAD sustained → ~60–95 l/min suction | Supports **less than half of one gripper** sustained; klixon trips and 120 starts/h are structural, not tuning |
| (b) 1× 2.2 kW belt-drive + 200 L receiver | ~2.6 kW running; ~1 kW left for robot — tight | ~264 l/min FAD at ~100% duty → ~170–210 l/min suction | One gripper continuously (at its ceiling), two only intermittent-with-air-save; ~10 starts/h; €500–900 |
| (c) 1.5 kW dry claw/vane pump | ~1.5 kW; ~2 kW headroom | **~600–1000 l/min suction direct** | Both grippers continuously with margin; add per-gripper solenoid + check valve + small vacuum reservoir; −95 kPa available |
| (d) Hybrid: small compressor (blow-off/tools) + electric pump for vacuum | ~1.5 kW pump + compressor at <10% duty | pump as (c) | Best of both: instant blow-off, compressor back inside its S3 rating |

**Bottom line:** at this cell's flows, compressed-air vacuum costs ~0.06–0.08 l/min suction per wall watt through the full chain, consistent with DOE's 10–20% wire-to-work figure for compressed air generally; a dry claw/vane pump delivers ~0.4–0.7 l/min per watt — a 5–10× gap that only closes when duty is genuinely intermittent and air-save ejectors can idle, which leaky 265 l/min grippers prevent (unless a check-valved head fixes the leak first — Chapter 4).

---

# Chapter 6 — Failure modes: surviving thousands of hours

Context: fine cardboard dust everywhere, target runtime in the thousands of hours, prototype budget but must not silently degrade.

## 6.1 Oil-free direct-drive piston compressors: the wrong tool

The cheap hardware-store compressor (direct-drive, oil-free, aluminum pump) is designed around a 25–50% duty cycle. Compression heat has no oil circuit to carry it away — only cylinder fins and a shaft fan. Sustained running past the rating follows a predictable failure sequence: reed/valve fatigue, then PTFE piston-ring wear, then bearings (https://aircompressorzone.com/blogs/resources/air-compressor-duty-cycle).

- **Klixon behavior:** the winding-mounted thermal overload trips at unsafe temperature and auto-resets after 15–30 min of cooling. In a robot cell this looks like the air supply randomly disappearing mid-shift. Repeated tripping = fundamental sizing mismatch, and each trip/restart further cooks the windings (https://fluidairedynamics.com/blogs/articles/is-it-normal-if-an-air-compressor-shuts-off-when-it-gets-hot).
- **PTFE rings:** without oil, the self-lubricating ring deposits a transfer film on the cylinder; wear rate and frictional heat are inherently higher, and the film degrades fast at high temperature — exactly what continuous duty creates (https://www.sciencedirect.com/science/article/abs/pii/S1350630725000585).
- **Service life:** consumer oil-free pumps ~500–2,000 h (cheapest) to 2,000–5,000 h; oil-lubricated piston 10,000–15,000 h. A container line logs 1,500+ h/yr (https://aircompressorzone.com/blogs/resources/oil-vs-oil-free-air-compressor).
- **Unloader valve:** vents the head at shutoff so the motor restarts unloaded. Stuck closed → start against tank pressure trips the overload; stuck open → continuous hiss, runs forever (https://aircompressorzone.com/blogs/resources/air-compressor-unloader-valve).
- **Tank condensate:** ~10% of ingested moisture settles in the receiver; condensate can be acidic (pH < 5) and is the primary corrosion driver. Drain daily or fit a €30–80 auto-drain — a rusted-through receiver is a pressure-vessel failure (https://www.quincycompressor.com/blog/avoiding-rust-with-air-compressor/).
- **Noise:** oil-free piston units reach ~90 dB(A) — above the 85 dB action level.

**Verdict:** everything about this machine class assumes intermittent DIY duty. For thousands of hours feeding ejectors, it is consumable-grade.

## 6.2 Belt-drive oil-lubricated piston & small screw compressors

- **Belt-drive cast-iron piston:** slower pump rpm, splash-oil lubrication, 60–75% realistic duty, 10,000–15,000 h pump life. Service: oil every 500–1,000 h, intake filter, belt, valve plates mid-life. Still 82–90 dB(A) — enclosure or separate room (https://www.atlascopco.com/en-uk/compressors/products/air-compressor/piston-compressor/professional-piston-compressor/at-belt-drive-cast-iron).
- **Small rotary screw:** true 100% duty, 30,000–40,000 h before overhaul; oil + three filters on schedule; 65–75 dB(A). Caveat: screws hate low duty (short cycling → condensate in oil) — only right if the cell consumes air continuously (https://dhhcompressors.com/how-many-hours-is-a-screw-compressor-good-for/).

## 6.3 Dry rotary vane vacuum pumps

- **Vane life:** inspect at ≥500 h intervals; standard Becker vanes ~2,000 h in hard service, 10,000–20,000 h expectation in normal service, Becker X-series rated to 20,000 h (https://www.becker-international.com/uk/good-to-know/becker-vacuum-pump-vanes.htm). Replacement is a bench job. Cost caveat: an OEM 8-vane set for a 60 m³/h frame lists at $911; small-frame (VT 4.4/4.8) sets far less; aftermarket ~25% cheaper (https://www.supervane.com/becker-vanes). Still cheap versus a new pump.
- **Dust is the killer:** cardboard dust ingested into the chamber accelerates vane and housing wear dramatically — the #1 cause of premature failure. Inlet filtration is non-negotiable: 5 µm, 99%+, generously sized canister (Solberg CSL/ST style, replaceable polyester element), checked weekly in cardboard environments (https://www.solbergmfg.com/pages/inlet-vacuum-filters).
- **Dead-head is fine — verified, with mechanism:** a vacuum pump's power draw peaks at intermediate pressure (~400 mbar abs for rotary vane per Leybold) and falls toward ultimate vacuum, where mass flow → ~0 and the drive needs only ~⅓ of installed power. Blocked inlet = lowest load, coolest running — the exact opposite of a compressor (https://www.leybold.com/en-us/knowledge/vacuum-fundamentals/vacuum-generation/how-does-an-oil-sealed-rotary-displacement-pump-work). A vane pump holding a sealed gripper against a switch setpoint is loafing, not straining.
- **Bearings:** grease/replace at overhaul; motor amps vs nameplate FLA is the health indicator (https://beckerpumps.com/news/how-to-test-a-vacuum-pump/).

## 6.4 Claw vacuum pumps

Claw rotors are non-contact: no vanes, no wear parts in the chamber. Maintenance ≈ "change the gearbox oil every 20,000 operating hours" (Busch Mink MV claim) (https://www.buschvacuum.com/global/en/products/vacuum-pumps/claw/mink/). Higher up-front price than vane, recovered via zero vane changes and lower energy; Becker's own comparison concedes claw wins on total cost of ownership in continuous duty (https://beckerpumps.com/news/claw-vs-rotary-vane-vacuum-pumps/). Dust tolerance is better (nothing rubbing) but not magic: the same 5 µm inlet filtration applies. Right answer if budget stretches and the cell runs multi-shift for years; vane + spare vane kits is the pragmatic prototype answer.

## 6.5 Side-channel blowers / BLDC blower cartridges

- **Side-channel:** impeller never touches housing; sealed bearings are the only wear part; ~20,000 h maintenance-free standard claim (https://www.atlanticblowers.com/regenerative-blowers). Shallow vacuum only.
- **Ametek Windjammer 5.7" BLDC:** rated 20,000 h continuous — genuinely fit-and-forget.
- **Domel caveat:** appliance-grade cartridges are specified 1,000–5,000 h depending on series — treat small Domel units as consumables (https://www.domel.com/product/729-bypass-101).

## 6.6 Ejectors: no moving parts, one silent failure mode

The venturi is nearly immortal; the **exhaust silencer is not**. In dusty air the silencer felt loads up over weeks/months, back pressure rises, and suction falls with no visible symptom — the canonical "the gripper got weak over months" root cause. SMC's ZK2 manual: replace silencer and filter element when pressure drop reaches ~5 kPa, or immediately on any vacuum-level drop or slower adsorption (https://static.smc.eu/binaries/content/assets/smc_global/product-documentation/installationmaintenance-manuals/en/im_zk2_tf2z424en.pdf). Nozzle/diffuser contamination from dirty *compressed air* is the other path — both sides must be clean.

**Mitigations:** pipe the exhaust open (bare elbow pointed down, accepting the hiss) or fit a grossly oversized straight-through silencer on the PM schedule; filter both the compressed-air feed (5 µm FR minimum) *and* the suction side; log vacuum-reached time as the clog indicator. A high-flow silencer can improve suction ~20% over a packed stock one (https://control.com/news/smc-releases-new-vacuum-ejector-and-vacuum-pump-systems/).

## 6.7 Suction-side filtration & gripper consumables

- **Inline vacuum filters:** transparent dust-cup/canister filter (Piab/SMC ZFA/ZFB at the gripper, Solberg CSL G1 canister at the pump, 5 µm) between cup and vacuum source. Elements are €10–40 and take minutes; weekly checks to start, then let trend data set the interval (https://www.solbergmfg.com/collections/csl-series).
- **Sealing foam is a consumable, period.** Schmalz stocks replacement foams as spare parts with peel-and-stick replacement and states replacement can be needed "even if there is no visible indication of wear" — micro-abrasion raises leakage before it looks damaged (https://www.schmalz.com/en-us/support/know-how/vacuum-knowledge/sealing-elements-fxp-fmp). Abrasive corrugate at high pick rates: plan foam swaps in weeks-to-months, keep 2–3 in stock, watch the vacuum-level trend as the true wear gauge.
- **Check-valve balls:** cardboard dust glues balls in place (stuck open = permanent leak mimicking worn foam; stuck closed = dead zone dropping one corner). Blow the gripper through in reverse periodically; include "all zones pull down" in the weekly check.

## 6.8 Compressed-air side (if ejectors stay)

- **Condensate:** unregulated, undried lines feed water straight into nozzles and valves; fit a filter-regulator with auto-drain at the cell.
- **PU hose at robot joints:** excellent flex life but fails by micro-fissures near fittings where stress concentrates; route in the dresspack with tubing+cable ≤60% of carrier bore; treat joint-adjacent sections as periodic replacements (https://igus.com/robot-dress-pack/resources/robot-cable-management-solutions).
- **Push-in fittings:** nearly all leaks occur at the fitting seal; vibration and hose motion shorten O-ring life; >5 cm³/min per fitting already affects response (https://www.airbestpractices.com/system-assessments/leaks/choosing-durable-no-air-leak-pneumatic-tubing-fittings).
- **Leak economics:** a 1 mm pinhole at 7 bar ≈ £300/yr in electricity; 3 mm ≈ £2,600–10,000/yr; Kaeser: 1/16" at 100 psig = $468/yr (https://us.kaeser.com/compressed-air-resources/kaeser-talks-shop/fix-air-leaks.aspx). More importantly, every leak-l/min raises compressor duty and start frequency. **Audit practice:** monthly soapy-water spray on every fitting; read "receiver decay time with everything off" as a whole-system leak number.

## 6.9 Duty-cycle system design: make the source cycle calmly

The architecture, not component choice, is what kills or saves motors:

- **Vacuum receiver + check valve:** a 10–60 L reservoir between pump and gripper with a check valve at the pump port. Picks draw from the tank; the pump runs long strokes between hysteresis setpoints (on at −500 mbar, off at −750 mbar) instead of once per pick.
- **The 120-starts/hour problem, fixes in order of cheapness:** (a) bigger receiver + wider hysteresis band; (b) let the vacuum pump idle continuously at deep vacuum — legitimate because dead-head is its minimum-load state — and switch flow with a valve at the gripper; (c) VFD/soft-start, which removes the 5–7× inrush and tracks demand; Busch ships Mink MVs with a factory VFD for exactly this (https://www.buschvacuum.com/us/en/news-media/busch-mink-dry-claw-vacuum-pumps.html).
- Corollary: with a properly sized reservoir, even a modest pump gives fast gripper response (tank delivers the surge), and pump sizing becomes about average demand, not peak.

## 6.10 Monitoring for long unattended runs

Two cheap trend signals catch nearly every failure mode above before it drops a box:

- **Vacuum level + time-to-vacuum:** a digital vacuum switch at the gripper (SMC ZSE30A class, ~€70–95, analog + 2 switch outputs) wired to the robot controller as go/no-go per pick, with the analog value logged. Slowly rising "seconds to setpoint" = silencer/filter clogging; slowly falling plateau = foam wear or fitting leak; sudden per-zone failure = stuck check ball. **Alarm on trend, not just threshold.**
- **Motor current trend:** amps vs nameplate FLA is the standard pump-health check — rising current at constant vacuum = bearing/vane wear or dust packing. A €20 CT clamp or the VFD's own readout into the PLC suffices.
- Log pump duty cycle (on-time fraction) too: creeping duty at constant throughput is the earliest whole-system leak/wear indicator, before any pick fails.

**Bottom-line architecture for this cell:** dry rotary vane (budget) or claw pump (long-run) + generous 5 µm inlet filter + vacuum receiver with check valve and wide hysteresis + ZSE30A-class per-pick verification with trend logging + foam and filter elements stocked as consumables. If ejectors stay: screw or cast-iron belt-drive air source, open-pipe or oversized silencers on a PM schedule, monthly leak walks. The direct-drive oil-free compressor should not survive the prototype phase.

---

# Chapter 7 — Case study: decoding the OnRobot VGP20 datasheet

The datasheet that kicked off this research (OnRobot VGP20, v1.7) is worth reading line-by-line with everything above in mind, because it's an honest datasheet — and with Chapters 1–5 absorbed, every number in it now tells a story.

## 7.1 The headline numbers

| Spec | Value | What it means in field-guide terms |
|---|---|---|
| Vacuum | 5–60% (−0.05 to −0.607 bar, 1.5–17.95 inHg) | −5 to −61 kPa gauge. Tops out at 60% vacuum — the "porous-load zone" of Chapter 1. No deep-vacuum pretension at all. |
| Air flow in total | 0–48 l/min | This is *suction capacity* (Chapter 1.4). 48 l/min vs the 900–1800 Nl/min vendors pair with a foam bar head (Chapter 4.5): **two orders of magnitude less flow.** |
| Air flow per channel | 0–12 l/min | 4 independent channels × 12 l/min. The flow is rationed per zone — this is the design trick. |
| Vacuum pump | "Integrated, electric BLDC" | A small electric pump bank (diaphragm class, Chapter 3.1) living inside the gripper housing. |
| Power | 24 V, 50 mA idle / 2.5 A typical / 4.5 A max | **~60 W typical, ~108 W absolute max.** The entire gripper uses less power than one LED floodlight — and replaces a compressor circuit. |
| Payload | 10 kg typical on cardboard (all 16 cups); 20 kg at low acceleration with the 24-cup bracket | With F = ΔP×A (Chapter 1.3): 16 cups × 450 mm² gripping area × −60 kPa ≈ 430 N ≈ 44 kg theoretical — they rate it at 10 kg, i.e. a real-world factor ~4 for leakage, peel, and acceleration. |
| Gripping time | 0.25 s (at 40% target vacuum) | Small dead volume + small cups = fast evacuation despite tiny pump (Chapter 1.6 arithmetic). |
| Noise | 67 dB(A) average / 71 worst box | Externally measured, 4 cardboard types, 1 m distance. Quieter than any compressor; the noise depends on box leakage — leakier box, more flow, more noise. |
| Dust filters | Integrated 50 µm, field replaceable | Chapter 6.7 in miniature: suction-side filtration as a designed consumable. |
| Warranty | 3 years or 3,000,000 cycles | An honest duty statement: 3M grip-releases. |
| Weight, IP | 2.55 kg, IP54, 264×184×92 mm | Cobot-class. |

## 7.2 The clever bits

**Four channels, sixteen holes.** The 16 cup positions map to 4 independently-controlled vacuum channels (A–D). Unused holes get blind screws; channels that don't engage a box are simply not commanded. This is Chapter 4's "active zone switching" (mechanism c) done electrically — the software equivalent of check valves.

**The pump runs to target, then throttles.** "The pump will run at full speed until the target vacuum is achieved, and then run at a lower speed necessary to maintain the target vacuum." That is the electric analog of an air-saving ejector (Chapter 2.7) and VFD-on-demand (Chapter 3.7) in one sentence — and it's why typical draw is 60 W, not 108 W.

**They tell you not to crank the vacuum.** Direct quote: "A high vacuum percentage setting does not give a higher lifting capacity on corrugated cardboard. In fact, a lower setting is recommended, e.g. 20%." And: "A low vacuum setting results in less air flow and less friction below the vacuum cups. This means that the filters and the vacuum cups will last longer." This is Chapter 1.4's leaky-load physics, stated by a vendor against their own spec-sheet vanity. Their porousness-vs-vacuum graph puts uncoated brown cardboard at roughly 20–35 kPa achievable, paper lower, coated board/metal/glass up to 60.

**"Airflow is the amount of air that must be pumped to maintain the target vacuum."** Their definition section is a compact restatement of the whole leak-vs-flow model: a tight system has zero airflow; real systems leak at the cup lips and *through* the workpiece ("things that look completely tight might not be tight at all — a typical example is coarse cardboard boxes"). Their airflow-performance graph is exactly the generator curve of Chapter 1.4: 48 Nl/min at 0% vacuum falling to zero at 60%, scaled by channel count.

**Altitude compensation.** The gripper auto-compensates to 2 km altitude ("where the pressure is about 80% of sea level") — Chapter 1.7 handled in firmware.

**External vacuum assist — even OnRobot concedes the flow ceiling.** The High-payload Bracket (accessory #113922) adds 8 more cups (24 total) *and four vacuum inlets for an external vacuum source*. Their recommended booster: a solenoid valve of ≥100 l/min capacity and — notably — **an SMC ZU07SA compressed-air ejector**. One-way valves let unused external channels hold vacuum. Translation: when the box is heavy or leaky, even the all-electric flagship gripper reaches for a venturi and a compressed-air line. The 48 l/min on-board pump is sized for management, not brute force.

## 7.3 What the VGP20 is and isn't (for our cell)

It is: the cleanest existence proof that ~100 W of well-managed electric vacuum replaces a compressor circuit for cooperative loads — sealed-ish boxes, ≤10 kg, cups individually zoned. At ≈ $6,925 it's also proof that "drop-in and integrated" carries a 5–10× price premium over assembling the same functions (pump + head + valves + sensing) yourself.

It isn't: a container-unload gripper. Torn, wet, open-flute, or heavily vented cartons out-leak 48 l/min instantly, and OnRobot says so themselves via the external-vacuum bracket. Our workload needs the same architecture at 10–20× the flow: exactly what a claw/vane pump or blower + check-valved foam head provides (Chapters 3–4).

---

# Chapter 8 — Buying it in China: the Shenzhen sourcing guide

Scope: prototype-grade but multi-thousand-hour parts; 230 V single-phase constraint; drop-in compatibility with European Festo/SMC gear at home.

## 8.1 The Chinese pneumatics brand landscape and quality tiers

| Tier | Brands | Notes |
|---|---|---|
| Japanese/global (benchmark) | SMC (China plants), CKD | Genuine SMC made in China is the same part as in EU; heavily counterfeited. |
| Taiwanese (near-benchmark) | **AirTAC**, Mindman, Chelic | AirTAC has ~28% China market share, second only to SMC (https://www.iwapneumatic.com/blog/top-10-most-popular-chinese-pneumatic-parts-brands-247771.html). Fit/finish a notch below SMC/Festo but seal and coil quality fine for thousands of hours. |
| Respected mainland | **AIRBEST** (vacuum specialist, Zhejiang — **a Piab Group brand since 2022**, Swedish-audited QC: https://www.airbest.com/about-airbest/), XCPC (Ningbo, est. 1991, ISO9001/CE/TUV), E.MC, STNC, SNS | Fine for prototypes and light production. Design lineage is openly SMC/Festo-pattern, so specs read across. |
| Clone/commodity tier | Unbranded 1688 cylinders, "SMC-type" fittings, no-name solenoids | Usable for fittings and manifolds; avoid for anything with a dynamic seal you want 1000+ h from. |

**Spotting fake SMC:** SMC itself warns non-authorized sellers ship imitation product with faked certificates (https://www.smc-vietnam.com.vn/news-promo/warning-about-imitation-product/). Tells: price far below AirTAC (genuine SMC never undercuts AirTAC), pad-printed vs laser-etched markings, missing lot/date code. In a market stall, assume any "SMC" at 30% of list is fake — at which point honest AirTAC/AIRBEST at the same price with a real warranty is the better buy.

## 8.2 Vacuum-specific suppliers

**AIRBEST (airbest.com)** is the main event — Schmalz/Coval/Piab-pattern products at mainland prices, with Piab ownership:

| Family | What it is | Key specs |
|---|---|---|
| TXM 130 series | Blower/external-pump bar gripper (Coval MVG pattern) | 130 mm wide × 400–1400 mm; foam in 1/3/5-row patterns or B30/B40 cups; **check valves: throttling-hole standard or ball-check "-V" option**; φ32 port (400–600) / φ60 (800–1400); 170–3129 N at −30 to −60 kPa; 2.3–10.1 kg; replaceable foam (https://www.airbest.com/products/txm-series-blower-type-vacuum-grippers/) |
| TXC / TXD / TXH / TXL / TXN | Same head with integrated ejector (TXC), light/heavy/combined/mini variants |
| AM/AL/AH multistage ejectors | AM universal −92 kPa, AL large-flow −81 kPa (360–1230 NL/min suction), AH high-vac −100 kPa; air consumption 105–810 NL/min; **ES air-saving option on AM-25L/50L** (https://www.airbest.com/products/ah-series-multistage-vacuum-generator/) |
| AGE series | Mechanical energy-saving generator, claims up to 99% air saving on sealed parts (https://www.airbest.com/products/age-series-mechanical-energy-saving-vacuum-generator/) |
| SOP / SNP / SPF | Foam suction cups, flat pads |

AIRBEST sells direct on Alibaba (https://airbestcn.en.alibaba.com/) and Made-in-China with MOQ 1 on most items.

**Other makers:** Zhejiang CKT does straight SMC-ZL multistage clones (https://www.cktworld.com/product/zl-series-multistage-vacuum-generator/zl1-series-multistage-vacuum-ejector.html). Alibaba lists ~19 multistage-generator suppliers and 900+ foam-gripper listings; 1688 has ~2,150 sponge-suction-cup makers.

**Prices vs Europe:** European street price for a configured 600–1000 mm foam bar gripper: €1,500–4,000 (Coval MVG is quote-only). Alibaba: small sponge grippers $59–135; a TXM-class 600–1000 mm bar typically lands $200–500 on quote. That's the 5–10× gap. On 1688, knock another 20–40% off but everything is RMB/domestic-only. **MOQ:** branded makers take MOQ 1; no-name factories want 2–10 pcs but cave for a "sample order" at +20%. Lead time: catalogue sizes ex-stock to 1 week; custom foam layouts 2–3 weeks.

## 8.3 Electric vacuum pumps from China

| Type | China reality | Price | 230 V single-phase? |
|---|---|---|---|
| Dry rotary vane (Becker pattern) | Mature clone ecosystem: "XD-040"-style 40 m³/h units everywhere (https://www.alibaba.com/countrysearch/CN/dry-rotary-vane-pump.html); Guangdong Wordfik VD40 $526–688. **Many cheap "XD" pumps are actually oil-lubricated — specify "oil-free / dry running, graphite vanes."** Shanghai EVP is a serious Alibaba-native vacuum house (https://evppump.en.alibaba.com/); better-factory oil-free dry vane $1,625–2,125. | $500–2,100 for 40 m³/h class | Default motor is 380 V 3-phase; 220 V 1-phase is a standard option to ~1.5–2.2 kW. Or take the 3-phase motor + a 230 V-in VFD ($60–100 on Alibaba, gives soft start + speed trim). |
| Claw | Available but skewed industrial-large (18.5 kW class); small single-phase claw pumps are rare — skip for this trip | $3k+ | Rarely |
| BLDC blowers (Windjammer/Domel analogs) | Strong Ningbo cluster: **Wonsmart** (https://www.wonsmartmotor.com/), Rongtron (24 V 22 kPa BLDC), BG Motor, CDM/Guomeng (supplies Roborock/Midea) | **$20–80/module in singles** | N/A (24/48 V DC) — ideal for foam-gripper blower duty and flies in luggage |

**Receipt inspection checklist (at the factory or forwarder):** dead-head vacuum test — dry vane should pull ≥ −85 kPa blanked off within seconds, and hold; listen for bearing rumble and vane chatter; confirm vane material (carbon/graphite, not phenolic); take a spare vane set (+$20–40, always); check the nameplate actually says 220 V 50 Hz 1-phase; run 30 min and touch-check bearings (<70 °C); confirm inlet screen and correct G-thread. BLDC blowers: bench-test at rated voltage, verify stall/overtemp protection.

## 8.4 Physically shopping in Shenzhen/PRD

Honest answer: **pneumatics has no Huaqiangbei.** Walking the electronics markets for vacuum parts wastes a day. What exists:

- **Dongguan-Shenzhen Intelligent Manufacturing Equipment Trade City, Chang'an Town, Dongguan** — automation-component mall on the Shenzhen border; distributor storefronts for AirTAC, SMC(-ish), fittings, hose by the roll. Chang'an is mold town; its hardware streets carry pneumatic staples.
- **Bao'an hardware/electromechanical markets (五金机电城)** around Xixiang/Fuyong — hose, fittings, solenoids, filters same-day. Vacuum grippers and dry pumps you will not find on a shelf.
- Trade-show timing bonus: automation exhibitions at Shenzhen World (Bao'an) put AirTAC, XCPC, E.MC in one hall.

**Recommended practice:** treat markets as fittings/hose/valve runs, and buy the grippers/ejectors/pump on **1688 or Alibaba shipped to your hotel** — domestic 1688 shipping is 1–3 days, so order on arrival day. 1688 is RMB/domestic-only; foreigners normally use an agent that pays, inspects and consolidates (https://yiwuagent.com/buy-from-1688-as-a-foreigner/) — but since 2023 Alipay/WeChat Pay accept foreign Visa/Mastercard, so in-person buying and some 1688 checkouts work with just your phone; hotels accept parcels routinely (give the front desk name + phone in Chinese). AIRBEST/EVP-class vendors will quote EXW and hand the box to your hotel via SF Express.

## 8.5 Fittings and standards gotchas

| Item | China default | Gotcha / what to standardize on |
|---|---|---|
| Port threads | "PT" on Chinese datasheets = Rc/BSPT taper (also written ZG); "G" = BSPP parallel with face seal | Rc and G in the same size half-engage then leak or jam; NPT (60°) vs BSPT (55°) cross-thread. **Standardize on G (BSPP) with face seal** — matches Festo/SMC EU practice; many Chinese push-in fittings ship "universal" short-taper threads sealing in both. Avoid NPT entirely (https://www.huiyivalve.com/a-comprehensive-guide-to-npt-bspp-bspt-zg-r-and-rc-threads-and-how-to-choose-the-correct-thread.html). |
| Tube | Metric OD 4/6/8/10/12 mm push-in, same as EU | Fully drop-in with Festo QS / SMC KQ2. Buy Chinese fittings freely; buy spare collets. No inch-OD stock. |
| Hose | PU (soft, kink-resistant) vs PA/nylon (stiff, high temp) | PU 8×5 and 12×8 for signal/supply. For the 32 mm vacuum trunk: **PU with embedded steel wire** (smooth bore, crush-proof under vacuum), $2–6/m on Alibaba (https://www.alibaba.com/showroom/32mm-vacuum-hose.html). |
| Silencers | G1/8–G1/2 sintered bronze/plastic | Buy a bag; they clog and are near-free. |
| Solenoid coils | AC220V and DC24V offered on everything | **Standardize on 24 V DC** — PLC-friendly, identical to EU stock, nothing mains-rated in luggage. AirTAC 4V210-08 in bulk: $1–10. |

## 8.6 Import and logistics (EU)

- **Duty:** vacuum pumps HS 8414 10 (~1.7–2.2%); pneumatic valves 8481 (~2.2%); plastic fittings/hose 3917 (~6.5%); brass 7412 (~5.2%). Then **21% VAT (NL) on CIF + duty**. On a €1,500 haul, total landed uplift ~24–26% — the 5–10× price gap survives easily (https://www.tariffnumber.com/2026/84141089).
- **CE:** Chinese vendors print CE on anything; XCPC/AIRBEST-class firms have genuine TUV/SGS files, no-name 1688 sellers don't. Passive pneumatics aren't CE-directive items anyway; the pump motor and any 230 V electrics are (LVD/EMC) — for lab/prototype use this is your own responsibility, not a customs blocker, but don't resell.
- **Luggage vs shipping:** grippers, ejectors, switches, fittings, hose, BLDC blowers — all fine in checked luggage (a 1000 mm TXM is 6–8 kg and 1 m long: oversize-ish but flyable). The 40 m³/h vane pump is 30–50 kg — ship it: air express DDP ~$4–6/kg or a 1688 agent consolidates for ~$100–200.
- **Warranty reality:** nominally 12 months from branded makers; in practice "send photos on WeChat, they express replacement parts, you fit them." The spare vane set and spare foam plate you buy up front ARE the warranty. Keep the seller's WeChat.

## 8.7 Concrete shopping list and budget

| Item | Spec / source | Qty | Est. unit (USD) | Ext. |
|---|---|---|---|---|
| Foam bar gripper w/ ball check valves | AIRBEST TXM130×600-A3-V + one TXM130×1000-A3-V, spare foam skirts | 2 | 250–450 | 500–900 |
| Multi-stage air-saving ejector | AIRBEST AM-25L-ES (or CKT ZL1 clone) | 2 | 60–150 | 120–300 |
| Dry vane pump 40 m³/h, oil-free, 220 V 1-ph (or 380 V + 230 V VFD) | Wordfik VD40 class / EVP + spare vane set | 1 | 550–900 | 550–900 |
| BLDC blower module 24 V, 20+ kPa (bonus, luggage-friendly) | Wonsmart / Rongtron | 2 | 30–60 | 60–120 |
| Digital vacuum switches | ZSE30-pattern clones ($12–25 vs genuine SMC $80) | 4 | 15 | 60 |
| G1 inline vacuum dust filter + spare elements | AIRBEST vacuum filter line | 1+3 | 30 | 50 |
| 32 mm PU wire-reinforced vacuum hose | 10 m roll | 10 m | 3/m | 30 |
| Fittings kit: G-thread push-in 6/8/12, Y/T, ball valves, silencers, PU tube | Market run or XCPC store | lot | — | 80–120 |
| Solenoid valves 24 V DC | AirTAC 4V210-08 + a 3/2 for ejector pilot | 4 | 8 | 32 |

**Total: roughly $1,480–2,560 (~€1,400–2,400) ex-shipping; ~€1,800–3,000 landed in the EU with VAT/duty/freight** — versus €8,000–15,000 for the equivalent Coval/Schmalz/Becker basket at European list. Buy switches, valves, fittings, hose, blowers, and one gripper for luggage; ship the pump and the second gripper via an agent.

---

# Chapter 9 — Synthesis: the decision for our cell

## 9.1 The original questions, answered in one place

**"What is one atmosphere / what do the negative kilopascals mean?"** One atmosphere = 101.325 kPa = 1.013 bar pushing on everything, always. A vacuum spec of −60 kPa means the gripper's interior is 60 kPa below that ambient, so the atmosphere pushes the box against the cup with 60 kPa × the sealed area — 0.6 kg of force per cm². 100% vacuum (−101.3 kPa) is the hard physical ceiling; nothing pulls harder than the sky pushes. (Chapter 1.)

**"Why does a gripper consume 240 l/min?"** Because it's a plain single-stage venturi ejector on an uncontrolled foam pad: the 240–265 l/min is *compressed air blown through the drive nozzle continuously*, converted at ~0.7:1 into suction that mostly fights the leaks of uncovered foam holes and porous cardboard — fed at tank pressure (7–8 bar) instead of the nozzle's 4.5–5 bar optimum, which alone wastes ~25–35%. Air consumption ≠ suction capacity; the confusion between those two numbers is the most common beginner mistake in vacuum datasheets. (Chapters 1.4, 2.6.)

**"Why do Boston Dynamics / Pickle / Anyware / XYZ use vacuum pumps?"** Your gut feeling was right on both counts, and there's a third reason: (1) **battery** — a mobile base cannot carry a 7-bar compressor; 341 l/min of compressed air costs ~2.3 kW while a 375 W blower out-sucks it; (2) **efficiency** — electric vacuum is 1/4 to 1/10 the energy of the compressor→ejector chain for continuous duty, per both Becker's worked examples and Piab's own admission; (3) **the flow curve matches cardboard** — blowers hold −20…−30 kPa while swallowing thousands of l/min of leak, which is exactly what porous corrugate demands. Stretch runs an onboard pump with a patented per-cup seal-detection gripper; Contoro is "battery-powered including the vacuum pump"; nobody ships ejectors on wheels. (Chapter 3.)

**"How deep is a vacuum — can an ejector out-pull a vacuum pump?"** Cheap ejectors reach −88…−95 kPa, deeper than most cheap dry pumps (−75…−85) and every blower (−20…−45) — so yes, the gut feeling holds at the low end of the market. But an industrial claw pump matches it (−95 kPa), and more importantly **depth is the wrong axis for our workload**: on corrugated cardboard anything past ~−40 kPa just pulls more air through the pores (and dents the box) without adding holding force. OnRobot's own datasheet says to run 20% on cardboard. Flow is the currency; depth is for glass and steel. (Chapters 1.4, 2.5, 3.4, 7.)

**"Why not keep the compressor and use a gripper that doesn't eat 240 l/min — one that recognizes holes?"** Completely legitimate, and the "recognizes a hole" part exists as a purely mechanical ball check valve in each foam cell (Schmalz SVK, Coval MVG, AIRBEST TXM-V, VMECA, Joulin — Chapter 4.1a). Paired with a multi-stage air-saving ejector at 5 bar, the routinely quoted result is a 60–90% consumption cut on decent boxes. That path keeps the compressors and is the smallest change. Its limits: savings evaporate on genuinely porous/torn boxes (air-save can't idle against a real leak), and the compressors remain 50%-duty, 2,000-hour, 120-starts/hour consumables unless the receiver/regulator/stagger fixes land too. (Chapters 2.7, 4.4, 5.2, 6.1.)

## 9.2 The three viable architectures, ranked by change size

**Architecture 1 — "Fix the air, smarten the ends" (smallest change, all drop-in).**
Keep both compressors with the already-planned fixes (Y-manifold, staggered switches, 5 bar filter-regulator, split circuits, receiver later if needed). Replace the gripper heads with check-valved foam bars (AIRBEST TXM130-…-A3-V ≈ our pad size; Coval MVG G0 as the premium twin) and the plain ejectors with multi-stage air-saving units (AIRBEST AM-…-ES, Piab COAX/piCOMPACT ES, Schmalz SBPL-HF class). Expected: consumption drops from ~530 l/min to plausibly 150–250 l/min average — inside one compressor's comfortable duty; klixon problem gone via electrics + duty relief. Cost: €400–1,200 in parts (Shenzhen prices). Risk: on the worst torn boxes consumption spikes back toward continuous; compressors remain the wear item.

**Architecture 2 — "Electric vacuum, industrial" (the robustness endgame, still mostly drop-in).**
One dry vane pump (budget: used Becker VT 4.25/4.40 at €300–850 or Chinese 40 m³/h clone; long-run: Busch Mink claw) + 24 L vacuum reservoir + check valve + one solenoid valve and vacuum switch per gripper + 32 mm wire-reinforced hose + G1 dust filter (cardboard dust is the #1 pump killer) + the same check-valved foam heads (external-vacuum G0/TXM-V versions — same heads as Architecture 1, so the two paths share parts). Runs both grippers continuously at ~1.5 kW total against today's ~5.2 kW, leaves 2 kW of outlet headroom for the robot, ~10 calm pump cycles per hour instead of 120 motor starts, and the pump *cools down* at dead-head instead of overheating. Cost: ~€1.5k budget / €2.7k proper (previous research), confirmed by this pass. Keep one compressor at <10% duty for blow-off pulses (which also back-flush the check valves and foam — Chapter 2.10).

**Architecture 3 — "Stretch-class blowers" (most flow per watt, best future story).**
2× 48 V BLDC blower cartridges (Ametek Windjammer class, or $20–80 Ningbo analogs from the Shenzhen list) mounted at or near the gripper heads: 750 W total, thousands of l/min at −20…−40 kPa, zero vacuum plumbing, PWM speed-servoed per pick. This is literally the Boston Dynamics/Pickle architecture and the only one that survives a future mobile base. Risk: −40 kPa ceiling means the check-valved foam area must carry the whole load (it can: 0.09 m² of engaged foam at −25 kPa ≈ 2,200 N); cheap cartridges are 5,000 h consumables (industrial Windjammers 20,000 h).

**Recommendation for the prototype that must "just run":** Architecture 2, with the Shenzhen shopping list (Chapter 8.7) deliberately covering Architectures 1 and 3 too — the TXM-V heads work with all three vacuum sources, the AM-ES ejectors make Architecture 1 testable the day the parts arrive, and two $30 BLDC blowers make Architecture 3 a weekend experiment. Total outlay ~€1,400–2,400 buys the ability to A/B all three with the same gripper heads.

## 9.3 Non-negotiables regardless of architecture (from the failure-mode research)

1. **5 µm inlet filtration on any electric pump** — cardboard dust kills vanes; transparent-bowl filters so loading is visible.
2. **A vacuum switch per gripper (ZSE30A-class, €15–80) wired to the controller** — grip-confirm threshold, drop-detect threshold, and *logged* analog value; alarm on trend (rising time-to-vacuum = clogging; falling plateau = foam wear/leak).
3. **Foam plates and silencers are consumables** — stock 2–3 foam plates and a bag of silencers from day one; budget weekly-to-monthly foam swaps on abrasive corrugate.
4. **Blow-off retained in the design** — it's not just cycle time; the reverse pulse cleans check valves and foam.
5. **Wide hysteresis, few starts** — whether compressor or pump: big receiver, wide pressure/vacuum band, staggered or VFD starts. Motors die of starts, not of running.
6. **Monthly leak walk** (soapy water; receiver decay time as the whole-system number) — every leak-l/min is duty cycle and starts.

## 9.4 Key numbers to remember (the podcast cheat-sheet)

- 1 atm = 101.3 kPa = 1 kg of push per cm² — the absolute ceiling.
- Cardboard's working zone: **−20…−40 kPa**. Deeper = wasted air + crushed boxes.
- Our measured burn: **265 l/min of 6.5-bar air per gripper**, ~0.7:1 converted to suction by single-stage venturis.
- Compressed air costs **~10–14 W of wall power per l/min** from small piston compressors; ejectors return 0.65–0.8 l/min of suction per l/min of air → **~0.06–0.08 l/min suction per watt**.
- A 1.5 kW claw pump: **~0.7 l/min suction per watt at −95 kPa** — the 5–10× gap.
- A 375 W BLDC blower: thousands of l/min at −30 kPa — the mobile-robot answer.
- Check-valve foam heads + air-saving generation: **60–90% consumption cut** on decent boxes; zero on torn ones.
- Our 40 L tanks force **~120 motor starts/hour**; spec is 6–8. A 200 L receiver → ~10. The tank was the murder weapon; the klixon was the witness.
- Whole Shenzhen parts basket: **~€1,400–2,400** vs €8,000–15,000 European list.

## 9.5 Open items

- Verify the groepenkast for 3-phase 400 V incoming (4-pole main switch / L1-L2-L3) — a CEE socket makes the bigger Kippers Shamal (4 pk/540 l/min) and every industrial pump trivial.
- Re-run the tank drawdown with BOTH grippers (7.5→5.5 bar, ~9 s expected) to lock the dual-gripper consumption number.
- Leak-down test per box SKU (grip a representative box, valve off, watch decay) — this single measurement decides how much the air-saving/check-valve combo will actually save on our real freight.
- Get AIRBEST quotes for TXM130×400-A3-V and AM-25L-ES before the trip; confirm -V check-valve option and spare foam plate codes.

*End of field guide.*
