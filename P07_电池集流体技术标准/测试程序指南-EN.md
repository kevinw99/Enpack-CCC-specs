---
title: "Testing Procedures Guide"
audience:
  primary: "technical"
language: "en"
content_type: "guide"
last_updated: "2026-01-08"
version: "1.0"
localization_status: "original"
---

# Battery Current Collector Foil Testing Procedures Guide

**Document Type:** Technical Reference
**Last Updated:** January 8, 2026
**Scope:** Standard testing methods for current collector foil quality assurance

---

## Overview

This guide provides practical testing procedure summaries for battery current collector foil manufacturing, cross-referenced to international standards. It serves as a quick reference for implementing quality checks at various production stages.

---

## 1. THICKNESS MEASUREMENT PROCEDURES

### 1.1 Automated Thickness Mapping

**Standard:** ASTM B568 (X-Ray) or ASTM B499 (Magnetic)

**Equipment Required:**
- Automated thickness measurement system (X-ray or magnetic)
- Calibration reference standards
- Data logging system

**Procedure Summary:**

| **Step** | **Action** | **Standard Requirement** |
|---|---|---|
| 1 | Calibrate equipment using reference standards | Prior to each shift |
| 2 | Place foil sample on measurement stage | Full width sampling |
| 3 | Scan across foil width at 10-20mm intervals | Complete coverage |
| 4 | Record thickness values at minimum 10 points per meter | Data logging |
| 5 | Calculate statistics (mean, min, max, std dev) | Cpk calculation |
| 6 | Compare to specification (e.g., 15 μm ±2 μm) | Acceptance/rejection |
| 7 | Document results with lot/batch number | Traceability |

**Acceptance Criteria:**
- All measurements within specification range
- Mean thickness within nominal ±1 μm
- Standard deviation <0.5 μm (typically)
- Cpk ≥1.33 (target 1.67 for critical)

**Frequency:** Continuous during production; every 30 minutes minimum for manual sampling

**Confidence:** 95% | **Source:** ASTM B568, B499, IATF 16949

---

## 2. ELECTRICAL CONDUCTIVITY TESTING

### 2.1 Four-Point Probe Measurement

**Standard:** ISO 2853 (reference), ASTM standardized procedure

**Equipment Required:**
- Four-point probe measurement system
- Reference standards (certified conductivity values)
- Temperature-controlled environment (20°C standard)
- Data recording system

**Procedure Summary:**

| **Step** | **Action** | **Standard Requirement** |
|---|---|---|
| 1 | Allow sample to reach 20°C ambient temperature | Temperature stabilization |
| 2 | Calibrate probe with reference standard of known conductivity | System validation |
| 3 | Place sample on measurement platform | Clean, flat surface |
| 4 | Apply four-point probe to foil surface (minimum 5 positions) | Representative sampling |
| 5 | Record conductivity reading in %IACS or S/m | Unit specification |
| 6 | Calculate average value from multiple measurements | Data aggregation |
| 7 | Compare to material specification (e.g., ≥58% IACS for Al) | Acceptance decision |

**Acceptance Criteria:**
- Aluminum foil: ≥58% IACS (typical for high-purity material)
- Copper foil: ≥97% IACS
- Minimum of 5 measurements per sample batch
- All individual measurements within specification
- Average ≥specification minimum

**Test Conditions:**
- Temperature: 20°C ± 2°C (standardized reference)
- Environment: Laboratory conditions (no moisture condensation)
- Frequency: Every 4-8 hours of production; minimum once per shift

**Confidence:** 85% | **Source:** Material specifications, four-point probe standards

---

## 3. MECHANICAL PROPERTY TESTING

### 3.1 Tensile Testing of Foil

**Standard:** ASTM E345 - Tension Testing of Metallic Foil

**Equipment Required:**
- Universal tensile testing machine
- Tension test grips suitable for thin foil (minimum 0.006" / 0.15mm thickness)
- Extensometer or displacement measurement
- Test specimens per ASTM E345 requirements
- Load cell (calibrated, traceable to NIST)

**Sample Preparation:**
- Sample size: Typically 10-25mm width × 50-100mm length
- Minimum 5 specimens per test batch (typically 3-5 per direction)
- Cut samples using appropriate method (no burring)
- Machine direction (MD) and transverse direction (TD) samples recommended

**Procedure Summary:**

| **Step** | **Action** | **Standard Requirement** |
|---|---|---|
| 1 | Measure sample thickness and width precisely (±0.001") | Accurate area calculation |
| 2 | Mount sample in tension grips (secure but not crushed) | Proper alignment |
| 3 | Zero load cell and extensometer | System calibration |
| 4 | Apply tensile load at constant rate (strain rate per ASTM E345) | Standard strain rate |
| 5 | Record load and extension continuously to failure | Complete data capture |
| 6 | Calculate stress (load/original area) and strain (extension/length) | Standard calculation |
| 7 | Determine tensile strength (maximum stress), elongation, yield strength | Key properties |
| 8 | Compare results to specification limits | Acceptance decision |

**Test Parameters per ASTM E345:**
- **Load Rate:** 1-3 mm/min crosshead speed (or equivalent strain rate)
- **Temperature:** Room temperature (23°C ±5°C)
- **Sample Size:** Minimum 3 specimens per batch
- **Data Recording:** Continuous throughout test

**Acceptance Criteria (Typical for Aluminum Foil):**
- **Tensile Strength:** 45-70 MPa (varies by temper/alloy)
- **Elongation:** ≥3% (minimum, often 5-15% depending on specification)
- **Yield Strength:** 20-50 MPa (varies by temper)

**Acceptance Criteria (Typical for Copper Foil):**
- **Tensile Strength:** 200-300 MPa (half-hard or hard temper)
- **Elongation:** ≥2-5% (varies by temper)
- **Yield Strength:** 150-250 MPa

**Frequency:** Per production batch or daily minimum; continuous for critical material

**Confidence:** 95% | **Source:** ASTM E345-16

---

## 4. ADHESION TESTING PROCEDURES

### 4.1 Cross-Cut Adhesion Test (ISO 2409 / ASTM D3359)

**Standard:** ISO 2409:2020 or ASTM D3359-17

**Equipment Required:**
- Cross-cut tool (cutting tool with parallel blades, 1-2mm spacing)
- Pressure-sensitive tape (standard adhesive tape per specification)
- 90-degree angle peel tool
- Timer (for tape application time)

**Procedure Summary:**

| **Step** | **Action** | **Standard Requirement** |
|---|---|---|
| 1 | Select test area on coated sample (away from edges, undamaged) | Representative location |
| 2 | Mark grid pattern (typically 11 parallel cuts each direction, 1mm spacing) | Consistent pattern |
| 3 | Make parallel cuts through coating to substrate using cutting tool | Complete penetration |
| 4 | Brush away any loose coating particles with soft brush | Clean test area |
| 5 | Apply pressure-sensitive tape over grid (firm pressure, 2-3 passes) | 100% contact |
| 6 | Allow tape to set for 1-2 minutes (per standard) | Adhesive set time |
| 7 | Grasp tape corner at 90-degree angle | Standard peel angle |
| 8 | Rapidly remove tape in continuous motion (1-2 seconds removal) | Quick peel |
| 9 | Examine grid pattern and count flaked squares | Classification |
| 10 | Rate result on Class 0-5 scale (see below) | Standard classification |

**Rating Scale:**

| **Class** | **Appearance** | **Acceptance** |
|---|---|---|
| 0 | No flaking or detachment; perfect adhesion | **ACCEPT** |
| 1 | Small flakes at cut intersections; ≤5% of grid area affected | **ACCEPT** |
| 2 | Flaking along cuts; 5-15% of grid area affected | **MARGINAL** |
| 3 | Flaking in patches; 15-35% of grid area affected | **REJECT** |
| 4 | Flaking in patches; >35% of grid area affected | **REJECT** |
| 5 | Complete peeling; entire coating removed | **REJECT** |

**Acceptance Criteria:**
- Battery components: Class 0-1 (most stringent)
- Typical industrial: Class 1-2 acceptable

**Test Conditions:**
- Temperature: 23°C ±5°C
- Humidity: 45-75% RH
- Sample preparation: No surface cleaning; test as-produced

**Frequency:** Every production batch or 100% of composite foil production

**Confidence:** 95% | **Source:** ISO 2409:2020, ASTM D3359-17

---

### 4.2 Pull-Off Adhesion Test (ISO 4624)

**Standard:** ISO 4624:2023 - Paints and Varnishes Pull-Off Test for Adhesion

**Equipment Required:**
- Pull-off adhesion tester (hydraulic or mechanical)
- Adhesive (typically epoxy resin per standard)
- Dollies (cylindrical, 12mm or 16mm diameter, per method)
- Surface preparation materials
- Load cell (traceable to NIST)

**Procedure Summary:**

| **Step** | **Action** | **Standard Requirement** |
|---|---|---|
| 1 | Prepare surface (clean, no loose coating, dry) | Surface requirements |
| 2 | Bond dolly to coated surface using specified adhesive | Dolly adhesion |
| 3 | Allow adhesive to cure per specification (typically 24 hours) | Cure time |
| 4 | Mount dolly in pull-off tester (perpendicular to surface) | Proper alignment |
| 5 | Apply tensile load perpendicular to coated surface | 90-degree pull |
| 6 | Increase load at constant rate until failure occurs | Standard rate |
| 7 | Record maximum load at failure | Peak measurement |
| 8 | Calculate pull-off strength (force/dolly area) | Adhesion strength |
| 9 | Determine failure mode (coating, adhesive, substrate) | Failure analysis |
| 10 | Report adhesion strength in MPa or N/cm² | Standard units |

**Acceptance Criteria:**
- **Standard Coatings:** ≥1.5 MPa (typical)
- **Battery Current Collector Composite Foil:** ≥5-10 N/cm² (≥0.5-1.0 MPa) minimum
- **Critical Applications:** ≥1.5-2.0 MPa
- **Failure Mode:** Cohesive (within coating) preferred; adhesive failure indicates quality issue

**Methods per ISO 4624:**
- **Method A:** Two-dolly method (suitable for rigid and deformable substrates)
- **Method B:** Single dolly method (rigid substrates only)
- **Method C:** Dolly-to-dolly method (one as painted substrate)

**Frequency:** Per batch for composite foils; critical inspection parameter

**Confidence:** 95% | **Source:** ISO 4624:2023

---

### 4.3 90-Degree Peel Adhesion Test (ASTM D3330)

**Standard:** ASTM D3330/D3330M - Peel Adhesion of Pressure-Sensitive Tape

**Equipment Required:**
- Peel test machine (tensile tester capable of controlled pull rate)
- Pressure-sensitive tape (standard adhesive tape)
- Metal foil substrate (prepared sample)
- Angle block or guide (for proper 90-degree geometry)
- Load cell (calibrated)

**Procedure Summary:**

| **Step** | **Action** | **Standard Requirement** |
|---|---|---|
| 1 | Prepare sample strip (typically 25mm width minimum) | Adequate size |
| 2 | Clean substrate surface (remove contamination, dry) | Surface preparation |
| 3 | Apply tape to substrate over approximately 50mm length | Tape application |
| 4 | Roll tape down firmly (typically with 2kg roller) | Consistent contact |
| 5 | Allow dwell time (typically 1-10 minutes per method) | Adhesive set |
| 6 | Mount sample in peel test machine (90-degree or 180-degree) | Proper geometry |
| 7 | Set pull rate per standard (typically 300mm/minute) | Standard rate |
| 8 | Measure peel force as tape is removed | Continuous measurement |
| 9 | Calculate average peel strength (force/width) | Result calculation |
| 10 | Report peel strength in N/cm or similar units | Standard units |

**Test Methods (ASTM D3330):**
- **90-Degree Peel:** Tape pulled perpendicular to substrate
- **180-Degree Peel:** Tape folded back; pulled parallel to substrate
  - 180-degree peel typically gives higher values
  - Most common for composite foil adhesion assessment

**Acceptance Criteria (Composite Foil - Electrode to Current Collector):**
- **Minimum 180° Peel Strength:** 5-10 N/cm
- **Typical Specification:** ≥5 N/cm (varies by customer)
- **Critical Applications:** ≥7-10 N/cm

**Frequency:** Batch sampling or 100% for critical composite foil batches

**Confidence:** 90% | **Source:** ASTM D3330-04(2018)

---

## 5. CORROSION RESISTANCE TESTING

### 5.1 Salt Spray (Fog) Test

**Standard:** ASTM B117 - Salt Spray (Fog) Apparatus

**Equipment Required:**
- Salt spray chamber (ASTM B117 compliant)
- Test solution (5% NaCl + 95% water by weight)
- pH meter (for solution verification)
- Specimen holders (non-reactive material)
- Temperature control system
- Spray nozzles (calibrated)

**Procedure Summary:**

| **Step** | **Action** | **Standard Requirement** |
|---|---|---|
| 1 | Prepare test solution (5% NaCl in distilled water) | Solution preparation |
| 2 | Verify pH (typically 6.5-7.2) | pH specification |
| 3 | Prepare test specimens (cut to specified size, identify) | Sample preparation |
| 4 | Place specimens on holders (horizontal or angled) | Orientation |
| 5 | Install specimens in salt spray chamber | Chamber loading |
| 6 | Set chamber temperature to 35±2°C (95±3°F) | Temperature control |
| 7 | Start continuous salt fog spray | Exposure initiation |
| 8 | Maintain spray rate (1.0-2.0 mL/80cm²/hr) | Spray intensity |
| 9 | Periodically observe specimens (24-96 hours typical) | Visual monitoring |
| 10 | Remove specimens at specified duration (e.g., 96 hours) | Test completion |
| 11 | Rinse and dry specimens carefully (avoid rubbing) | Post-test prep |
| 12 | Evaluate extent of corrosion (visual or mass loss) | Result assessment |
| 13 | Document corrosion pattern and severity | Reporting |

**Test Conditions:**
- **Solution Composition:** 5% NaCl + 95% distilled water (by weight)
- **Temperature:** 35±2°C (95±3°F)
- **Humidity:** Fog saturated (nearly 100% RH)
- **Spray Rate:** 1.0-2.0 mL/80cm²/hr (0.05-0.1 inch/hour)
- **pH:** 6.5-7.2 (measured at start of test)

**Test Duration:**
- **Standard:** 24, 48, 72, or 96 hours (customer-specified)
- **Typical for Current Collectors:** 96 hours (4 days)
- **Extended Testing:** 500+ hours for high-corrosion-resistance applications

**Acceptance Criteria:**
- **No Red Rust:** Coating material should show no visible red corrosion
- **Maximum White Corrosion:** <5-10% of surface (customer-specific)
- **Cathodic Protection:** Copper foil should show white corrosion, not red
- **Mass Loss:** Typically <10% of original mass (varies by specification)

**Evaluation Methods:**
- **Visual Assessment:** Photograph specimen; compare to reference standards
- **Mass Loss:** Weigh specimen before/after test
- **Coating Adhesion:** Check if coating is still well-adhered after corrosion

**Frequency:** Periodic validation (per production run or quarterly); certification testing

**Confidence:** 95% | **Source:** ASTM B117-19

---

## 6. SURFACE INSPECTION AND DEFECT DETECTION

### 6.1 Automated Optical Inspection (AOI)

**Standard:** IATF 16949 Process Control, Customer Specifications

**System Components:**
- Automated optical inspection camera system
- Lighting system (high-intensity, consistent spectrum)
- Image processing software
- Defect classification algorithm
- Documentation system

**Procedure Summary:**

| **Step** | **Action** | **Standard Requirement** |
|---|---|---|
| 1 | Calibrate AOI system (lighting, focus, resolution) | System validation |
| 2 | Load foil sample into inspection stage | Position optimization |
| 3 | Capture high-resolution images across full surface | Complete coverage |
| 4 | Apply defect detection algorithms | Automated analysis |
| 5 | Identify and classify defects automatically | Classification |
| 6 | Measure defect dimensions (size, depth, area) | Quantification |
| 7 | Compare against acceptance criteria | Acceptance decision |
| 8 | Flag non-conforming areas or entire samples | Quality action |
| 9 | Generate defect report with images and measurements | Documentation |

**Defect Categories Detected:**
- **Thickness Variations:** Mapping of surface thickness via optical or other methods
- **Surface Scratches:** Linear defects; measured by length and depth
- **Pits and Indentations:** Point defects; measured by diameter and depth
- **Contamination:** Foreign particles; identified by color, size, material
- **Delamination:** Coating separation; detected by surface appearance change
- **Wrinkles/Waviness:** Large-scale surface variations; detected by topography

**Acceptance Criteria Typical Examples:**
- **Scratches:** Length <10mm, depth <5μm; maximum 2 per sample
- **Pits:** Diameter <2mm, depth <10μm; maximum 3 per sample
- **Contamination:** Maximum 1 particle >0.5mm per cm²
- **Delamination:** None acceptable in critical areas; maximum 1% area in non-critical

**Frequency:** Continuous during production (every piece scanned)

**Confidence:** 85% | **Source:** IATF 16949, Industry best practices

---

### 6.2 Visual Inspection (Sampling)

**Standard:** AQL Sampling (ANSI/ASQ Z1.4 or equivalent)

**Inspection Protocol:**

| **Step** | **Action** | **Standard Requirement** |
|---|---|---|
| 1 | Determine lot size and AQL level | Risk assessment |
| 2 | Calculate sample size per AQL table (ANSI/ASQ Z1.4) | Statistical sampling |
| 3 | Randomly select samples from lot | Unbiased selection |
| 4 | Conduct visual inspection under standard lighting | Controlled conditions |
| 5 | Classify defects by type and severity | Categorization |
| 6 | Count critical, major, and minor defects | Defect counting |
| 7 | Compare to acceptance number per AQL table | Acceptance decision |
| 8 | Accept or reject lot based on results | Quality gate |
| 9 | Document inspection results and defects found | Traceability |

**AQL Levels (Examples):**
- **AQL 0.65:** Critical defects only; very stringent (automotive safety)
- **AQL 1.0:** Major + critical defects; stringent (battery components)
- **AQL 2.5:** Major + minor defects; moderate (standard industrial)
- **AQL 4.0:** Minor defects acceptable; less stringent (cosmetic)

**Defect Severity Classification:**
- **Critical:** Hazardous; causes failure; unacceptable
- **Major:** Significant deviation; likely to cause failure
- **Minor:** Small deviation; affects appearance; may not affect function
- **Cosmetic:** Appearance only; no functional impact

**Inspection Conditions:**
- **Lighting:** Minimum 300 lux (equivalent to bright indoor lighting)
- **Distance:** 30-45cm from eye to sample
- **Background:** Neutral color (gray or white)
- **Inspectors:** Trained and certified in defect recognition

**Frequency:** Per batch or per shift; minimum daily

**Confidence:** 85% | **Source:** ANSI/ASQ Z1.4, Quality standards

---

## 7. PROCESS CAPABILITY ANALYSIS

### 7.1 Cpk Calculation Procedure

**Standard:** IATF 16949 SPC, Statistical Methods

**Data Collection:**
1. Select critical characteristic (e.g., thickness)
2. Collect minimum 30-100 individual measurements
3. Record measurements in order (time-sequenced)
4. Ensure normal distribution (use normality test if needed)
5. Verify process is in statistical control (control chart)

**Calculation Steps:**

```
Step 1: Calculate Mean (μ)
μ = Σ(All measurements) / Number of measurements

Step 2: Calculate Standard Deviation (σ)
σ = √[Σ(measurement - μ)² / (n-1)]

Step 3: Identify Specification Limits
USL = Upper Specification Limit (e.g., 17 μm)
LSL = Lower Specification Limit (e.g., 13 μm)

Step 4: Calculate Cpk
Cpk = min[(USL - μ)/(3σ), (μ - LSL)/(3σ)]

Step 5: Interpret Result
Cpk ≥ 1.67: Process highly capable (target for critical characteristics)
Cpk ≥ 1.33: Process capable (acceptable baseline)
Cpk < 1.33: Process needs improvement
```

**Example Calculation:**
- Specification: 15 μm ±2 μm (LSL=13, USL=17, Nominal=15)
- Mean measured: 14.8 μm
- Standard deviation: 0.4 μm
- Cpk = min[(17-14.8)/(3×0.4), (14.8-13)/(3×0.4)]
- Cpk = min[1.83, 1.5] = **1.5** (Capable)

**Reporting:**
- Include Cpk value, date, sample size, characteristic
- Document control limits (LSL, USL, nominal)
- Include control chart visualization
- Schedule process improvement if Cpk <1.33

**Frequency:** Monthly minimum; after process changes; annually for full validation

**Confidence:** 95% | **Source:** IATF 16949 SPC Tools

---

## 8. SAMPLING AND DOCUMENTATION

### 8.1 Sample Selection Strategy

**Sampling Plan Components:**

| **Component** | **Details** | **Purpose** |
|---|---|---|
| **Lot Definition** | Production batch quantity, time period | Traceability |
| **Sample Size** | Minimum n=5 for properties; per AQL for visual | Statistical validity |
| **Selection Method** | Random selection from different locations/time | Unbiased sampling |
| **Stratification** | Samples from start, middle, end of run | Coverage |
| **Frequency** | Per batch, per shift, continuous monitoring | Consistency check |

**Sample Location Strategy (Foil):**
- Samples from beginning, middle, and end of production run
- Full-width representation (center, left, right edge)
- Avoid visibly damaged or clearly non-representative areas
- Document exact location of each sample for traceability

**Sample Size Recommendations:**

| **Test Type** | **Min Sample Size** | **Rationale** |
|---|---|---|
| Thickness (automated) | Continuous scan | Full coverage |
| Conductivity | 5 per batch | Statistical validity |
| Tensile testing | 5 per batch (3 MD, 2 TD minimum) | Directional verification |
| Adhesion (cross-cut) | 5 per batch | Multiple locations |
| Adhesion (pull-off) | 3-5 per batch | Quantitative verification |
| Salt spray | 1-2 per certification | Long-term testing |
| Visual inspection | Per AQL sampling plan | Statistical acceptance |

**Confidence:** 90% | **Source:** IATF 16949, Statistical standards

---

### 8.2 Documentation Requirements

**Documentation System for Each Test:**

| **Field** | **Information to Record** |
|---|---|
| **Identification** | Test name, standard, date, time |
| **Sample Info** | Lot number, batch number, production date, material type |
| **Specification** | Nominal value, LSL, USL, tolerance |
| **Results** | Measured value(s), mean, standard deviation, Cpk |
| **Acceptance** | Accept/Reject, OK/Not OK decision |
| **Inspector** | Name, ID, signature/authentication |
| **Equipment** | Equipment ID, calibration status, due date |
| **Notes** | Any anomalies, conditions, observations |
| **Disposition** | Approved for use, hold, rework, scrap |

**Recommended Record Retention:**
- Keep test records for minimum 2-3 years (automotive standard)
- Organize by lot number, production date, and test type
- Implement electronic database for searchability and traceability
- Back up digital records weekly; maintain archive copies

**Confidence:** 95% | **Source:** ISO 9001:2015, IATF 16949:2016

---

## 9. QUICK REFERENCE: TEST DECISION MATRIX

| **Characteristic** | **Test Method** | **Standard** | **Frequency** | **Acceptance** | **Confidence** |
|---|---|---|---|---|---|
| **Thickness** | Automated measurement | ASTM B568/B499 | Continuous | Within ±tolerance, Cpk≥1.33 | 95% |
| **Conductivity** | 4-Point Probe | ISO 2853 ref. | Every 4-8 hrs | ≥58% IACS (Al), ≥97% (Cu) | 85% |
| **Tensile Strength** | ASTM E345 | ASTM E345 | Per batch | Within specification range | 95% |
| **Elongation** | ASTM E345 | ASTM E345 | Per batch | ≥3-5% minimum | 90% |
| **Cross-Cut Adhesion** | ISO 2409 test | ISO 2409/D3359 | Every batch | Class 0-1 | 95% |
| **Pull-Off Adhesion** | ISO 4624 test | ISO 4624 | Per batch | ≥5-10 N/cm² minimum | 95% |
| **180° Peel Adhesion** | ASTM D3330 | ASTM D3330 | Per batch | ≥5-10 N/cm minimum | 90% |
| **Corrosion Resist.** | Salt spray ASTM B117 | ASTM B117 | Certification | <5-10% white corrosion | 95% |
| **Surface Defects** | AOI + visual | IATF 16949 | Continuous/sampling | Per AQL acceptance | 85% |
| **Process Capability** | SPC/Cpk analysis | IATF 16949 | Monthly minimum | Cpk≥1.33 (target 1.67) | 95% |

---

## 10. TROUBLESHOOTING COMMON TEST FAILURES

### 10.1 Thickness Variation Issues

**Problem:** Thickness measurements outside specification

**Investigation Steps:**
1. Verify measurement equipment calibration (is it correct?)
2. Check sample collection locations (different areas of coil?)
3. Review raw material incoming thickness (supplier issue?)
4. Examine coating application equipment (even distribution?)
5. Verify substrate temperature during processing (affects dimensions)

**Root Cause Examples:**
- Defective measurement equipment → Recalibrate/repair
- Rolling equipment wear → Maintenance/adjustment
- Raw material non-conformance → Supplier quality issue
- Temperature fluctuations → Temperature control system failure
- Uneven pressure application → Equipment setup error

**Action:** Implement control chart; perform SPC Cpk study; address root cause per CAPA procedure

---

### 10.2 Low Adhesion Values

**Problem:** Cross-cut or pull-off adhesion test fails

**Investigation Steps:**
1. Check surface preparation (cleanliness, oxide layer?)
2. Verify coating process parameters (temperature, thickness, speed)
3. Examine coating material batch (expired, moisture absorbed?)
4. Review substrate composition (material specification correct?)
5. Assess storage conditions (humidity, temperature exposure)

**Root Cause Examples:**
- Contaminated substrate surface → Improve cleaning process
- Coating application temperature too low → Heat control adjustment
- Substrate oxidation layer → Surface treatment specification
- Wrong coating material used → Material verification system
- Composite layer adhesion issue → Material engineering solution

**Action:** 100% adhesion testing until resolved; investigate specific production batch

---

### 10.3 Conductivity Out of Specification

**Problem:** Electrical conductivity measurements low

**Investigation Steps:**
1. Verify conductivity measurement equipment calibration
2. Check material composition/purity (correct alloy/grade?)
3. Review material heat treatment (annealing, hardening?)
4. Examine storage conditions (oxidation, contamination?)
5. Verify sample preparation (clean, no oxide layer damage?)

**Root Cause Examples:**
- Defective measurement equipment → Recalibrate
- Wrong material received from supplier → Material verification
- Insufficient heat treatment → Process parameter review
- Surface oxidation layer thicker than expected → Cleaning procedure
- Material composition off-specification → Supplier quality issue

**Action:** Supplier coordination; material batch review; potential rework or scrap decision

---

### 10.4 Corrosion During Salt Spray Test

**Problem:** Excessive corrosion during ASTM B117 testing

**Investigation Steps:**
1. Verify coating thickness (adequate coverage?)
2. Review coating composition (correct specification?)
3. Check substrate surface preparation (clean, passivated?)
4. Examine test parameters (temperature, humidity, spray rate correct?)
5. Assess coating adhesion (delamination during test?)

**Root Cause Examples:**
- Inadequate coating thickness → Increase application thickness
- Coating defects (pinholes, cracks) → Process improvement
- Substrate oxidation → Surface treatment enhancement
- Test equipment out of specification → Equipment maintenance
- Wrong coating material → Material verification failure

**Action:** Review coating process; increase thickness; improve surface treatment; retest

---

## APPENDIX: Equipment Calibration Checklist

| **Equipment** | **Calibration Standard** | **Frequency** | **Certificate Required** |
|---|---|---|---|
| Thickness measurement (X-ray) | ASTM B568 reference standards | Annually | Yes |
| Thickness measurement (magnetic) | ASTM B499 reference standards | Annually | Yes |
| Conductivity probe | Certified standards (known %IACS) | Annually | Yes |
| Tensile testing machine | ASTM E4 / Load cell standard | Annually | Yes |
| Load cell | NIST traceable standard | Annually | Yes |
| Temperature chamber (salt spray) | Calibrated thermometer | Quarterly | Yes |
| Humidity chamber | Humidity reference | Quarterly | Yes |
| Micrometer/caliper | Gauge blocks (NIST traceable) | Annually | Yes |
| Scale (weight) | Calibrated weights (NIST) | Annually | Yes |
| pH meter | pH standard solutions | Monthly | Yes |

---

## References

- ASTM E345-16: Standard Test Methods for Tension Testing of Metallic Foil
- ASTM B117-19: Standard Practice for Operating Salt Spray (Fog) Apparatus
- ASTM B499-09R21E01: Standard Test Method for Measurement of Coating Thicknesses by Magnetic Method
- ASTM B568: Standard Test Method for Measurement of Coating Thicknesses by X-ray Spectrometry
- ASTM D3359-17: Standard Test Methods for Rating Adhesion by Tape Test
- ASTM D3330-04(2018): Standard Test Method for Peel Adhesion of Pressure-Sensitive Tape
- ISO 2409:2020: Paints and Varnishes – Cross-cut Test
- ISO 4624:2023: Paints and Varnishes – Pull-off Test for Adhesion
- IATF 16949:2016: Automotive Quality Management System
- ANSI/ASQ Z1.4: Sampling Procedures and Tables for Inspection by Attributes

---

**Document Version:** 1.0
**Last Updated:** January 8, 2026
**Prepared by:** Claude Code Research Agent
