# Vacuum sizing you can feel: cups, leaks, restrictions, and the pump

*Podcast companion · 29 October 2026 · Based on Gripper knowledge / 02, “From robot acceleration to the right pump,” dated 28 October 2026.*

## Start with the carton, not the pump

Imagine the robot holding a carton. It is not enough for the pump to make an impressive vacuum reading somewhere near the motor. The attached cups need enough pressure difference, over enough useful contact area, to support the carton through the motion. They also need the right placement to keep it from tipping, peeling away, or sagging too far.

There are two sides to sizing this system. The mechanical side asks how much grip the motion demands. The pneumatic side asks how much grip the pump, plumbing, and leaks actually deliver. A successful design keeps the delivered grip above the required grip throughout the motion, with margin.

That distinction explains why buying a larger pump sometimes helps enormously and sometimes solves almost nothing.

## First, agree on what “more pressure” means

Room air presses on the carton. Removing air from inside a cup makes the pressure there lower, so the outside air presses the carton against the cup more strongly.

There is one useful formula to name once: **holding force equals pressure difference times effective area**. From here on, think in relationships rather than symbols.

Lower **absolute pressure inside the cup** means a deeper vacuum and more holding force. Higher absolute pressure means the vacuum is weakening. A gauge showing a more negative number is showing a deeper vacuum. “More pressure” on its own is therefore ambiguous; say either “deeper vacuum” or “higher absolute pressure.”

For an unchanged effective contact area, doubling the pressure difference doubles the ideal normal holding force. That does not mean doubling a pump's advertised flow doubles the force. Flow and pressure difference are different things.

The source's office cup illustrates the distinction. At a vacuum depth of about sixty kilopascals, its measured pull-off load was about four point two kilograms. The model predicts about two point eight kilograms at forty kilopascals. That second number assumes the force scales with vacuum; it is not another measurement. A straight pull-off result also does not directly describe resistance to sideways sliding or peeling.

## Acceleration spends grip

A stationary carton already needs support against gravity. Accelerating upward adds to that demand. For the source's fifteen-kilogram carton, standing still requires roughly one hundred and forty-seven newtons of vertical support. Accelerating upward at eight metres per second squared raises that to about two hundred and sixty-seven newtons.

So the carton did not get heavier, but the grip has to act as if it did. Lowering the upward acceleration gives holding margin back. It does not directly stop an air leak or improve the pump's pressure curve.

Direction matters as much as magnitude. Sideways acceleration loads the cups in shear and can tip the carton. The distance between the centre of mass and the supporting cups creates a lever arm. A grip on a different face can therefore change the required vacuum substantially even though the carton, pump, and acceleration magnitude stay the same.

This is why the source tests several directions and grip arrangements. A total-force calculation is a useful starting point, but it cannot tell the whole story of a carton that is rotating or peeling away at one edge.

## Losing one cup hurts twice

First, the lost cup no longer contributes contact area or support. The remaining cups must carry more of the load. If eight identical cups were sharing a simple straight pull equally, losing one would remove one eighth of the area. The remaining seven would need about fourteen percent more pressure difference to restore the original ideal total force. That is an illustration, not a prediction for our actual gripper: real cups do not necessarily share the load equally.

Second, an uncovered cup becomes an inlet for room air. Unless the branch is isolated, that air enters the shared vacuum system. If the existing pump cannot remove it at the previous operating pressure, the system settles at a higher absolute pressure. The still-attached cups can then become weaker too.

We have simultaneously increased the grip required from each survivor and reduced the grip it can deliver. An edge cup can be especially important because losing it also removes leverage against tipping. Several cups lost on one side can be worse than the same number lost symmetrically.

A larger pump can help with the incoming air. It cannot put the missing contact area back or move the remaining cups into better positions. The source even contains simulated grip arrangements that fail the holding criteria at every tested vacuum level. Those require a mechanical or motion change, not just more pumping capacity.

## The pump is continually clearing incoming air

Picture a room with air entering through several doorways and an extractor removing it. Here the “doorways” are uncovered cups, porous cardboard, imperfect cup rims, and leaks in fittings or seals. The extractor is the pump.

When the system has settled, the mass of air entering each second equals the mass being removed. If leakage increases, the old pressure generally cannot be maintained with the same pump and plumbing. If a better seal reduces leakage, that same pump can usually reach a deeper vacuum.

Pressure difference gives us holding force. Airflow capacity lets us establish and maintain that pressure difference despite incoming air. Large flow is valuable when there is a large leak; large flow is not itself a force on the carton.

The pump's headline flow also needs context. Its capacity changes with inlet pressure. At low absolute pressure the air is thinner, so a given volume contains less air mass. Comparing litres measured at room pressure with litres measured at the pump inlet can make the available capacity look misleadingly large. Compare flows on the same pressure basis, and use the pump curve near the pressure the system actually needs.

## Restriction holes protect the neighbours, at a price

Each cup connects to the chamber through a small hole. When that cup is uncovered, the hole limits how quickly room air can flood into the chamber. Making it smaller can protect the other cups from this open branch.

But the restriction cannot tell the difference between unwanted air from an uncovered cup and air that must be evacuated from an attached cup. Cardboard and cup rims leak too. That air first enters the attached cup, then must pass through the same small hole to reach the chamber and pump.

Make the hole too small and air cannot leave the attached cup readily enough. Its absolute pressure rises above the chamber pressure. The chamber gauge can look excellent while the cup itself has a disappointingly weak vacuum.

That is the tradeoff. A large hole connects a sealed cup well to the pump but admits too much air when uncovered. A small hole limits the uncovered-cup leak but can starve an attached cup of evacuation capacity. There is a useful middle, not a universal rule that smaller is better.

Hole **diameter** also has a stronger effect than it first sounds. With otherwise identical hole geometry and pressures, flow scales with hole area. Reducing diameter from two millimetres to one and a half leaves about fifty-six percent of the area. That suggests roughly forty-four percent less flow through that hole under those fixed conditions. It does **not** imply forty-four percent deeper vacuum: changing the hole changes the pressures throughout the network, so the whole system must settle again.

The source's particular model finds a broad useful region around one point two five to one point seven five millimetres, with one point five as a middle candidate. More uncovered cups tends to favour smaller restrictions. More leakage through the attached carton pushes the other way, because those cups need a better path for evacuation. These are study-specific candidates to verify, not ready-made purchase or drilling instructions.

## Why pulling harder eventually stops helping

A hole can reach a flow limit. Once air in its narrow passage reaches the speed of sound, lowering the downstream pressure further does not keep increasing the incoming mass flow, provided the upstream pressure and other conditions stay fixed. This is called choked flow.

For the source's room-fed open holes, that transition occurs at a downstream absolute pressure of roughly half atmospheric pressure. The important intuition is that the leak can reach a ceiling. It does not disappear. The pump still has to remove that incoming air continuously.

A different limit appears at an attached cup behind a very small restriction. Air keeps entering through the carton, but the restriction limits how much can leave. Eventually, improving the chamber vacuum gives little additional improvement inside the cup. A bigger pump may then mostly improve the gauge reading downstream of the restriction.

The study's one-millimetre restriction is an example: under its assumed leaks and pump family, the attached-cup pressure cannot be pushed below roughly five hundred and fifty-six millibar. That is a model-specific floor, not a universal property of one-millimetre holes. Better carton sealing or a different restriction changes it.

## The hose can hide the problem too

The cup, chamber, and pump inlet are not necessarily at the same pressure. Air needs a pressure difference to move through restrictions, outlets, hoses, and fittings. Along the normal evacuation path, absolute pressure falls toward the pump.

A long, narrow, kinked, or restrictive flow path can leave the pump inlet at a deep vacuum while the chamber remains at a weaker vacuum. Increasing pump capacity can increase flow and the associated plumbing losses. Some of the improvement can be spent getting air through the hose instead of improving the cups.

Measuring only at the pump therefore cannot distinguish a good grip from a strong pump behind a bottleneck. Comparing pump, chamber, and attached-cup pressures tells you where the vacuum is being lost. A large cup-to-chamber gap points toward the cup restriction and local leakage. A large chamber-to-pump gap points toward the evacuation path.

## Choose the intervention that matches the problem

If an uncovered cup collapses the shared vacuum, reduce how much air that open branch admits, isolate it where the design supports that, or provide more usable pumping capacity at the required pressure. Remember that the lost support still needs to be addressed.

If the chamber vacuum is good but the attached cup vacuum is weak, look at local leakage and the cup restriction. Simply making the restriction smaller could make this particular problem worse.

If both cup and chamber vacuum are weak, check the total leaks, actual pump performance, and pressure losses before deciding which component to replace. Sealing a background leak can improve every connected cup without changing the pump.

If the vacuum is adequate but the carton still tilts or sags, reconsider cup placement, grip face, compliance, acceleration, and the acceptance criterion. The source distinguishes “does not drop” from “held in place.” A carton that hangs on while moving too far is not necessarily usable for the planned motion.

Finally, distinguish settled performance from timing. The pneumatic sizing model is a steady-state calculation. It does not establish how quickly the cups reach usable vacuum after contact, or how they recover immediately after a cup opens. Small restrictions can slow evacuation; more internal volume means more air to remove. Those timings need separate measurement or a transient model before they can be folded into a cycle-time claim.

## What we still need to measure

The source's pump numbers depend on a calibration choice. The current Wordfik pump is represented by a Becker curve because its own curve was unavailable. The measured pressures can be explained either by a weaker pump or by printed holes that flow like larger openings. The study uses the larger-opening explanation, but pressure measurements alone did not settle that question.

That uncertainty matters when predicting what a different pump will do. Measure the openings, measure the pump's actual flow, and measure pressure inside an attached cup. The study also extrapolates from seventeen measured cups to a thirty-two-cup system and assumes cup force and stiffness scale with vacuum beyond the single measured vacuum level.

Use the study to understand which changes are promising and what to test. Treat its minimum pump sizes as calculated thresholds, not demonstrated operating margins.

The relationships to remember are these: acceleration and lost support increase the mechanical demand; leakage consumes pumping capacity; restrictions trade open-cup protection against attached-cup evacuation; and the pressure that matters for holding is the pressure **inside the attached cups**. A better design brings those four things into balance.

---

## Reading reference: what changes what?

These are tendencies with the other conditions held fixed. The coupled system can move to a new operating point; the rows are not independent percentage rules.

| Change | Direct effect | Consequence and limit |
|---|---|---|
| Greater upward acceleration | More support force required | Higher required cup vacuum, more effective area, or a different motion/grip is needed. Does not directly improve or worsen the pump curve. |
| Lose an attached cup | Less support and an open air path | Remaining cups face greater load and potentially weaker vacuum. Position of the lost cup matters. |
| More carton or rim leakage | More air enters an attached cup | Local cup pressure rises unless evacuation keeps up; the added air also burdens the shared system. |
| More background leakage | Air enters the chamber | Uses shared pump capacity without providing any useful support. |
| Smaller cup restriction | Less flow through the branch | Protects against open cups but can weaken attached-cup vacuum and slow evacuation. |
| Larger cup restriction | Easier cup-to-chamber evacuation | Helps locally leaky attached cups but increases open-cup inflow. |
| More pump flow at the required pressure | More air can be removed | Can sustain deeper vacuum against leaks, until restrictions, plumbing, ultimate pressure, or mechanics dominate. |
| Lower pump ultimate pressure | Deeper no-flow vacuum limit | Does not by itself establish capacity under leakage. |
| Less restrictive hose/outlet | Less pressure loss along the flow path | Delivers more of the pump's vacuum to the chamber under flow. |
| More useful sealed area at the same cup vacuum | More ideal normal holding force | Placement, shear, peeling, compliance, and added leakage still matter. |
| Less internal volume | Less air to evacuate initially | Can improve response time; alone it does not remove a continuous leak or change the steady-state balance. |

## Sources and scope

- [Primary study: Vacuum Sizing Pipeline](https://www.randd.dev/vacuum-sizing-pipeline.html), especially sections 2–3 and 5–8. Local editable source: `randd/vacuum-sizing-pipeline.md`.
- [Study report: VD40 gripper vacuum and pump requirements](https://www.randd.dev/assets/vacuum-sizing/VD40_gripper_vacuum_and_pump_requirements.pdf). The numerical examples and calibration limitations above come from this study, not new experiments.
- [Schmalz: vacuum suction cups](https://www.schmalz.com/en-ca/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/vacuum-suction-cups): pressure difference, effective area, and holding force.
- [Schmalz: flow restrictors](https://www.schmalz.com/en/products/automation-743270/vacuum-grippers-746238/vacuum-suction-cups-301609/accessories-vacuum-suction-cups-305861/flow-restrictors-sc-sw-305941): limiting leakage from uncovered cups.
- [Becker VT 4.40 datasheet](https://www.beckerpumps.com.au/wp-content/uploads/2024/01/ds_VT_4.40.pdf): reference pump characteristics. It is a stand-in for the study's Wordfik pump, not a measurement of that pump.

The eight-to-seven-cup example and the two-to-one-and-a-half-millimetre comparison are illustrative calculations. The discussion of response time is a qualitative engineering extension; the source's steady-state model does not calculate it.
