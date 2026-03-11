---
title: "Defect Classification Guide"
audience:
  primary: "technical"
language: "en"
content_type: "guide"
last_updated: "2026-01-08"
version: "1.0"
localization_status: "original"
---

# Defect Classification and Acceptance Criteria Guide

**Document Type:** Quality Management Reference
**Last Updated:** January 8, 2026
**Scope:** Standard defect classification for battery current collector foil

---

## Overview

This guide provides standardized defect classification, severity levels, and acceptance criteria applicable to battery current collector foil manufacturing. It serves as a practical reference for quality inspection, non-conformance reporting, and continuous improvement initiatives.

---

## 1. DEFECT CLASSIFICATION FRAMEWORK

### 1.1 Defect Categories

Battery current collector foil defects are classified into four main categories:

#### 1) STRUCTURAL DEFECTS
Defects affecting coating integrity or physical adhesion:
- **Delamination/Peeling:** Coating separation from substrate
- **Cracking:** Linear fractures in coating or foil
- **Blistering:** Raised areas indicating air/moisture trapped under coating
- **Wrinkles/Waves:** Large-scale distortions in foil surface

#### 2) DIMENSIONAL DEFECTS
Variations outside specification:
- **Thickness Variation:** Over/under specification limits
- **Width Deviation:** Edge not meeting specification
- **Length Variation:** Coil length outside specification
- **Edge Quality:** Rough, damaged, or misaligned edges

#### 3) SURFACE DEFECTS
Localized surface imperfections:
- **Scratches:** Linear marks; classified by length and depth
- **Pits/Indentations:** Point defects; classified by diameter and depth
- **Contamination:** Foreign particles (dust, metal, organic)
- **Oxidation/Corrosion Spots:** Surface discoloration or corrosion initiation
- **Gouges/Tears:** Partial through-thickness damage
- **Surface Roughness:** Deviation from smoothness specification

#### 4) MATERIAL PROPERTY DEFECTS
Characteristics outside specification:
- **Conductivity/Resistivity:** Electrical property out of range
- **Tensile Strength/Elongation:** Mechanical property non-compliance
- **Hardness Variation:** Consistency issue in material properties
- **Adhesion Strength:** Below specification adhesion values

---

### 1.2 Defect Severity Classification

All defects are classified into four severity levels:

#### CRITICAL DEFECTS
**Definition:** Hazardous to equipment operator; causes product failure; renders product unsafe or non-functional

**Examples:**
- Large delamination exposing conductor (>25mm²)
- Coating completely absent over significant area (>50mm²)
- Conductivity <50% of specification (major safety risk)
- Adhesion failure in adhesion test (Class 4-5 per ISO 2409)
- Contamination with conductive particles that could cause short circuit
- Structural failure visible (complete tearing, cracking)

**Acceptance:** **ZERO TOLERANCE** - AQL 0 (no defects acceptable in sample)
**Action:** Immediate containment; full batch review; root cause analysis; customer notification likely

**Confidence:** 95% | **Source:** IATF 16949, Automotive standards

---

#### MAJOR DEFECTS
**Definition:** Significant deviation from specification; likely to cause product failure or reduced performance

**Examples:**
- Localized delamination (5-25mm²)
- Thickness variation >2× tolerance (e.g., >4μm when tolerance is ±2μm)
- Scratch >10mm length or >5μm depth
- Conductivity 50-75% of specification
- Adhesion marginal (Class 2-3 per ISO 2409)
- Pit >2mm diameter or >10μm depth
- Contamination with potential bridging risk
- Multiple minor defects in same area

**Acceptance:** **VERY RESTRICTED** - AQL 0.65-1.0 (0-1 defects in sample depending on sample size)
**Action:** Batch hold pending review; 100% inspection of batch; customer notification for critical batches

**Confidence:** 95% | **Source:** Quality management standards

---

#### MINOR DEFECTS
**Definition:** Slight deviation from specification; may affect appearance or marginal performance; unlikely to cause failure

**Examples:**
- Scratch 5-10mm length, <5μm depth
- Small pit <2mm diameter, <10μm depth
- Slight thickness variation within 1.5× tolerance
- Conductivity 75-95% of specification
- Adhesion marginal but acceptable (Class 1 per ISO 2409)
- Light surface contamination (particles 0.1-0.5mm)
- Minor oxidation discoloration
- Small wrinkles not affecting function

**Acceptance:** **ACCEPTED WITH LIMITS** - AQL 2.5-4.0 (2-4 defects acceptable depending on sample size)
**Action:** Document and track; assess if single batch or systematic issue; continue monitoring

**Confidence:** 90% | **Source:** Quality management standards

---

#### COSMETIC DEFECTS
**Definition:** Appearance only; no functional or safety impact

**Examples:**
- Surface dust or light contamination (<0.1mm particles)
- Very light scratches (<5mm length, <2μm depth)
- Very slight discoloration
- Minor surface roughness variation
- Light fingerprints or handling marks

**Acceptance:** **GENERALLY ACCEPTED** - AQL 2.5-6.5 depending on criticality
**Action:** Track but typically acceptable; no special action required

**Confidence:** 85% | **Source:** Industry quality standards

---

### 1.3 Severity Classification Matrix

| **Defect Type** | **Critical** | **Major** | **Minor** | **Cosmetic** |
|---|---|---|---|---|
| **Delamination** | >25mm² | 5-25mm² | <5mm² | Not applicable |
| **Scratch (length)** | >25mm | 10-25mm | 5-10mm | <5mm |
| **Scratch (depth)** | >10μm | 5-10μm | 2-5μm | <2μm |
| **Pit (diameter)** | >5mm | 2-5mm | 0.5-2mm | <0.5mm |
| **Pit (depth)** | >20μm | 10-20μm | 5-10μm | <5μm |
| **Thickness Var.** | >2× tolerance | 1.5-2× tolerance | 1-1.5× tolerance | <1× tolerance |
| **Conductivity %** | <50% spec | 50-75% spec | 75-95% spec | ≥95% spec |
| **Adhesion (ISO2409)** | Class 4-5 | Class 2-3 | Class 1 | Class 0 |
| **Contamination** | >1 conductive particle | Bridging risk; >5 particles | Light; <5 particles 0.1-0.5mm | <0.1mm particles |

---

## 2. SPECIFIC DEFECT TYPES AND MEASUREMENTS

### 2.1 STRUCTURAL DEFECTS

#### Delamination / Peeling

**Definition:** Separation of coating from substrate; loss of adhesion

**Measurement Method:**
1. Identify delaminated area using cross-hatch test (ISO 2409) or visual inspection
2. Measure length and width of delaminated region
3. Calculate area: Length × Width (mm²)
4. Determine if separation is complete (coating removed) or partial (raised/bubbled)

**Classification:**

| **Severity** | **Area Size** | **Condition** | **Action** |
|---|---|---|---|
| **Critical** | >25mm² | Complete separation; coating removed | Reject batch; investigate root cause |
| **Major** | 5-25mm² | Partial or complete separation | Hold batch; 100% inspection |
| **Minor** | <5mm² | Small raised area; coating mostly attached | Document; continue monitoring |
| **Cosmetic** | <1mm² | Barely visible separation | Accept if isolated |

**Root Cause Investigation:**
- Surface cleanliness before coating?
- Coating adhesion properties (composition, temperature)?
- Substrate surface treatment adequate?
- Moisture exposure during processing or storage?
- Composite layer adhesion (for multi-layer foil)?

**Prevention/Correction:**
- Improve surface cleaning before coating
- Verify coating material composition and cure
- Enhance substrate preparation (plasma treatment, roughening)
- Control humidity during production and storage
- Adjust coating application pressure/temperature

**Confidence:** 95% | **Source:** Quality standards, coating technology

---

#### Cracking

**Definition:** Linear fractures in coating or substrate foil

**Measurement Method:**
1. Identify crack location and orientation
2. Measure crack length (mm)
3. Assess crack depth (visual or cross-section analysis)
4. Determine if crack penetrates through coating to substrate

**Classification:**

| **Severity** | **Crack Length** | **Condition** | **Action** |
|---|---|---|---|
| **Critical** | >25mm | Through-thickness crack; exposes conductor | Reject; investigate equipment/material |
| **Major** | 10-25mm | Extended crack; may propagate | Hold batch; root cause analysis |
| **Minor** | 5-10mm | Moderate crack; localized | Document; assess if pattern |
| **Cosmetic** | <5mm | Hairline crack; stable | Accept if isolated |

**Root Cause Investigation:**
- Coating brittleness (composition, cure temperature)?
- Thermal stress during processing?
- Substrate quality (work hardening)?
- Coating thickness too high?

**Prevention/Correction:**
- Adjust coating composition for flexibility
- Control temperature ramp rates during processing
- Verify substrate material properties
- Optimize coating thickness specification

---

#### Blistering

**Definition:** Raised bumps indicating air or moisture trapped under coating

**Measurement Method:**
1. Identify blister location and count
2. Measure blister diameter at base (mm)
3. Assess blister height (visual or measurement)
4. Check if blister is rupturing/leaking

**Classification:**

| **Severity** | **Diameter** | **Condition** | **Action** |
|---|---|---|---|
| **Critical** | >5mm | Large blisters; coating rupturing; exposing conductor | Reject batch |
| **Major** | 2-5mm | Moderate blisters; risk of rupture | Hold batch; inspect |
| **Minor** | 0.5-2mm | Small blisters; stable | Document; monitor |
| **Cosmetic** | <0.5mm | Tiny blisters; not noticeable | Accept if rare |

**Root Cause Investigation:**
- Moisture absorption during coating process?
- Air entrapment during coating application?
- Insufficient substrate surface drying?
- Outgassing from substrate material?

**Prevention/Correction:**
- Reduce humidity in production environment
- Verify substrate drying procedures
- Adjust coating application speed/pressure
- Consider pre-bake of substrate before coating

---

#### Wrinkles / Waves

**Definition:** Large-scale distortions in foil surface; wavelike pattern or pronounced creases

**Measurement Method:**
1. Identify wrinkle location and orientation (machine direction or cross-web)
2. Measure wrinkle wavelength (mm) - distance between crests
3. Measure amplitude (μm) - height of wave
4. Estimate affected area (% of surface)

**Classification:**

| **Severity** | **Amplitude** | **Affected Area** | **Action** |
|---|---|---|---|
| **Critical** | >100μm | >50% of surface | Reject; major process issue |
| **Major** | 50-100μm | 10-50% of surface | Hold; investigate process |
| **Minor** | 20-50μm | <10% of surface | Document; assess trend |
| **Cosmetic** | <20μm | <5% of surface | Accept if stable |

**Root Cause Investigation:**
- Foil tension control during rolling?
- Roller surface condition (dirt, wear)?
- Material composition (temper, hardness)?
- Temperature control in rolling zone?

**Prevention/Correction:**
- Improve foil tension control during manufacturing
- Verify roller condition; clean/replace as needed
- Optimize material properties for less wrinkling
- Monitor and control process temperature

---

### 2.2 DIMENSIONAL DEFECTS

#### Thickness Variation

**Definition:** Measurements outside specification range

**Measurement Method:**
1. Record multiple thickness measurements across foil (minimum 10 points per meter)
2. Calculate mean, minimum, maximum, standard deviation
3. Compare to specification (e.g., 15 μm ±2 μm = 13-17 μm range)
4. Calculate thickness distribution

**Classification:**

| **Severity** | **Deviation from Spec** | **Example (15±2 μm)** | **Action** |
|---|---|---|---|
| **Critical** | >150% of tolerance | <11 μm or >19 μm (>>4μm deviation) | Reject; reject likely entire batch |
| **Major** | 100-150% of tolerance | 11-12 μm or 18-19 μm | Hold; 100% thickness mapping |
| **Minor** | 50-100% of tolerance | 12-13 μm or 17-18 μm | Document; trend analysis |
| **Cosmetic** | 0-50% of tolerance | 13.5-14.5 μm or 15.5-16.5 μm | Accept |

**Statistical Control:**
- **Cpk ≥1.67:** Process highly capable (target for critical characteristics)
- **Cpk 1.33-1.67:** Process capable; acceptable
- **Cpk <1.33:** Process requires improvement; implement corrective action

**Root Cause Investigation:**
- Rolling pressure/temperature inconsistency?
- Rolling equipment wear?
- Raw material thickness variation?
- Thermal effects on substrate?

**Prevention/Correction:**
- Implement real-time thickness monitoring
- Perform equipment maintenance (pressure balance, temperature control)
- Qualify incoming raw material thickness
- Implement SPC with control charts

**Confidence:** 95% | **Source:** IATF 16949, Manufacturing standards

---

#### Width Deviation

**Definition:** Foil width outside specification

**Measurement Method:**
1. Measure foil width at multiple locations (start, middle, end; left, center, right)
2. Compare to specification (e.g., 50 mm ±0.5 mm)
3. Identify edge straightness

**Classification:**

| **Severity** | **Deviation from Spec** | **Example (50±0.5 mm)** | **Action** |
|---|---|---|---|
| **Critical** | >150% of tolerance | <49 mm or >51 mm | Reject entire batch |
| **Major** | 100-150% of tolerance | 49-49.25 mm or 50.75-51 mm | Hold; investigate |
| **Minor** | 50-100% of tolerance | 49.25-49.5 mm or 50.5-50.75 mm | Document; assess |
| **Cosmetic** | <50% of tolerance | 49.5-49.75 mm or 50.25-50.5 mm | Accept |

**Root Cause Investigation:**
- Slitting blade misalignment?
- Blade wear or damage?
- Edge guide calibration?
- Coil winding tension?

**Prevention/Correction:**
- Regular slitting blade maintenance and replacement
- Verify edge guide alignment
- Implement width monitoring system
- Adjust coil winding tension

---

### 2.3 SURFACE DEFECTS

#### Scratches

**Definition:** Linear marks or grooves on surface

**Measurement Method:**
1. Identify scratch location and orientation
2. Measure scratch length (mm) - use graduated ruler or image analysis
3. Estimate depth (μm) - visual comparison to tolerance or optical measurement
4. Assess if isolated or part of pattern

**Classification:**

| **Severity** | **Length (mm)** | **Depth (μm)** | **Quantity** | **Action** |
|---|---|---|---|---|
| **Critical** | >25 | >10 | Any | Reject; major quality issue |
| **Major** | 10-25 | 5-10 | >2 in same area | Hold; investigate |
| **Minor** | 5-10 | 2-5 | 1-2 | Document; trend analysis |
| **Cosmetic** | <5 | <2 | >2 isolated | Accept |

**Root Cause Investigation:**
- Rough edges on handling equipment?
- Wire or metal particles in coating process?
- Scratching during storage/transport?
- Abrasive contact during winding?

**Prevention/Correction:**
- Improve handling equipment (smooth edges)
- Filter coating materials; prevent contamination
- Use protective packaging during storage
- Optimize winding parameters to prevent edge rubbing

**Confidence:** 90% | **Source:** Quality standards

---

#### Pits and Indentations

**Definition:** Point defects or shallow depressions in surface

**Measurement Method:**
1. Identify pit location; count pits
2. Measure pit diameter at surface (mm)
3. Estimate pit depth (μm)
4. Assess if isolated or clustered

**Classification:**

| **Severity** | **Diameter (mm)** | **Depth (μm)** | **Density** | **Action** |
|---|---|---|---|---|
| **Critical** | >5 | >20 | Any | Reject; hazardous |
| **Major** | 2-5 | 10-20 | >3 per cm² | Hold; assess |
| **Minor** | 0.5-2 | 5-10 | 1-3 per cm² | Document; monitor |
| **Cosmetic** | <0.5 | <5 | <1 per cm² | Accept |

**Root Cause Investigation:**
- Impact damage during handling?
- Substrate inclusions or impurities?
- Environmental corrosion (moisture)?
- Equipment contact marks?

**Prevention/Correction:**
- Improve protective packaging
- Control storage environment (humidity, temperature)
- Verify substrate material quality
- Review equipment surfaces (non-damaging contact)

---

#### Contamination

**Definition:** Foreign particles or material on foil surface

**Measurement Method:**
1. Visual inspection under standard lighting (≥300 lux)
2. Identify contaminant type (dust, metal, organic)
3. Measure particle size (mm)
4. Count particles; assess if isolated or pattern
5. Special attention to electrically conductive particles

**Classification:**

| **Severity** | **Particle Type** | **Size** | **Quantity** | **Action** |
|---|---|---|---|---|
| **Critical** | Conductive (metal, solder) | Any | Any | Reject; short circuit risk |
| **Major** | Ionic (salt) or non-conductive | >0.5 mm | >5 per cm² | Hold; clean and retest |
| **Minor** | Dust, organic | 0.1-0.5 mm | 1-5 per cm² | Document; attempt cleaning |
| **Cosmetic** | Dust | <0.1 mm | <1 per cm² | Accept |

**Root Cause Investigation:**
- Unfiltered production air?
- Storage environment (dust, moisture)?
- Coating/sealant particles?
- Handling with contaminated tools?

**Prevention/Correction:**
- Install air filtration in production area
- Use cleanroom practices for critical batches
- Implement controlled storage area
- Use clean handling procedures and tools
- Consider additional cleaning/inspection step

**Confidence:** 90% | **Source:** Quality standards

---

#### Oxidation / Corrosion Spots

**Definition:** Surface discoloration or corrosion initiation; visible oxidation

**Measurement Method:**
1. Identify discolored area; measure extent
2. Assess if surface oxidation or through-thickness corrosion
3. Estimate coverage area (mm² or % of surface)
4. Determine if corrosion is active or stable

**Classification:**

| **Severity** | **Area** | **Type** | **Progression** | **Action** |
|---|---|---|---|---|
| **Critical** | >100mm² | Red rust (active corrosion) | Spreading | Reject; material compromised |
| **Major** | 10-100mm² | White/blue oxidation or red rust | Active | Hold; investigate storage |
| **Minor** | <10mm² | Light white oxidation | Stable | Document; assess trend |
| **Cosmetic** | <1mm² | Slight surface tarnish | None | Accept if isolated |

**Root Cause Investigation:**
- Storage environment (humidity >60%)?
- Protective coating inadequate?
- Aluminum vs. copper reactivity?
- Handling without gloves (salt from skin)?

**Prevention/Correction:**
- Control storage humidity (target <50% RH)
- Use desiccant packs in sealed packaging
- Apply protective coating/lacquer for long storage
- Implement proper handling procedures
- Consider vacuum or inert atmosphere packaging for extended storage

---

### 2.4 MATERIAL PROPERTY DEFECTS

#### Conductivity / Resistivity

**Definition:** Electrical conductivity outside specification

**Measurement Method:**
1. Measure conductivity using 4-point probe method
2. Record in %IACS (at 20°C standard) or S/m
3. Conduct minimum 5 measurements per batch
4. Calculate average; compare to specification

**Classification:**

| **Severity** | **Conductivity Range** | **Example (58% IACS spec)** | **Action** |
|---|---|---|---|
| **Critical** | <50% of spec | <29% IACS | Reject; material non-compliant |
| **Major** | 50-75% of spec | 29-43.5% IACS | Hold; investigate supplier |
| **Minor** | 75-95% of spec | 43.5-55% IACS | Document; alert supplier |
| **Acceptable** | ≥95% of spec | ≥55% IACS | Accept |

**Root Cause Investigation:**
- Wrong material alloy/grade?
- Insufficient heat treatment (annealing)?
- Material work hardening (cold worked too much)?
- Supplier/manufacturing change?
- Contamination in material?

**Prevention/Correction:**
- Implement incoming material inspection/testing
- Supplier audit and capability verification
- Material cert review; require COC (Certificate of Conformance)
- Adjust heat treatment parameters if in-house processing
- Consider material composition analysis if suspect

**Confidence:** 85% | **Source:** Material standards, electrical properties

---

#### Tensile Strength / Elongation

**Definition:** Mechanical properties outside specification per ASTM E345

**Measurement Method:**
1. Prepare samples (minimum 5 per batch)
2. Conduct tensile test per ASTM E345 procedure
3. Record maximum load, elongation, yield point
4. Calculate tensile strength (load/area)
5. Calculate elongation (% extension at break)

**Classification for Aluminum Foil** (typical spec: TS 45-70 MPa; Elong ≥3%):

| **Severity** | **Tensile Strength** | **Elongation** | **Action** |
|---|---|---|---|
| **Critical** | <30 MPa or >90 MPa | <1% | Reject; material unsuitable |
| **Major** | 30-40 or 75-90 MPa | 1-2% | Hold; verify spec compliance |
| **Minor** | 40-45 or 65-75 MPa | 2-3% | Document; assess trend |
| **Acceptable** | 45-70 MPa | ≥3% | Accept |

**Root Cause Investigation:**
- Temper incorrect (alloy not annealed/hardened properly)?
- Work hardening variation?
- Heat treatment inadequate?
- Wrong material grade supplied?
- Processing temperature affect?

**Prevention/Correction:**
- Verify material temper specification; match to supplier data
- Review heat treatment procedures if in-house
- Incoming material testing
- Temperature control during processing
- Supplier verification and audits

**Confidence:** 95% | **Source:** ASTM E345, Material specifications

---

#### Adhesion Strength

**Definition:** Coating adhesion below specification per ISO 2409, ISO 4624, or ASTM D3330

**Measurement Method:**

**ISO 2409 Cross-Cut Test:**
1. Cut lattice pattern through coating
2. Apply adhesive tape
3. Remove tape rapidly
4. Count flaked squares; rate Class 0-5

**ISO 4624 Pull-Off Test:**
1. Glue dolly to coated surface
2. Mount in pull-off tester
3. Apply perpendicular tensile load
4. Record force at failure (N or MPa)

**ASTM D3330 Peel Test:**
1. Apply tape to foil surface
2. Mount in peel tester (90° or 180°)
3. Peel tape at controlled rate
4. Record peel force (N or N/cm)

**Classification:**

| **Test Method** | **Critical** | **Major** | **Minor** | **Acceptable** |
|---|---|---|---|---|
| **ISO 2409** | Class 4-5 | Class 2-3 | Class 1 | Class 0-1 |
| **ISO 4624** | <0.5 MPa | 0.5-1.0 MPa | 1.0-1.5 MPa | ≥1.5 MPa |
| **ASTM D3330 (180°)** | <3 N/cm | 3-5 N/cm | 5-7 N/cm | ≥7-10 N/cm |

**Root Cause Investigation:**
- Surface cleanliness/contamination?
- Coating process parameters (temperature, pressure)?
- Substrate surface treatment adequate?
- Coating material composition/quality?
- Moisture/humidity exposure?
- Composite layer material compatibility?

**Prevention/Correction:**
- Improve surface cleaning (chemical or plasma treatment)
- Optimize coating application temperature
- Enhance substrate surface preparation (roughness/activation)
- Verify coating material batch quality
- Control humidity during production and storage
- For composite foil: review layer adhesion; consider material engineering solution
- Implement 100% adhesion testing until resolved

**Confidence:** 95% | **Source:** ISO 2409, ISO 4624, ASTM D3330

---

## 3. ACCEPTANCE SAMPLING AND AQL

### 3.1 AQL Selection

**AQL (Acceptable Quality Limit)** defines the maximum percentage of defects acceptable in a batch.

**Standard AQL Levels:**

| **AQL** | **Application** | **Max Defects (typical sample n=125)** | **Risk Level** |
|---|---|---|---|
| **0.65** | Safety-critical (automotive) | 0-1 | Very stringent |
| **1.0** | Critical characteristics | 1-2 | Stringent |
| **1.5** | Major characteristics | 2-3 | Moderate-high |
| **2.5** | Minor characteristics | 4-5 | Moderate |
| **4.0** | Non-critical items | 5-7 | Less stringent |
| **6.5** | Cosmetic items | 8-10 | Permissive |

**Selection for Battery Current Collector Foil:**
- **Critical Characteristics** (adhesion, thickness): **AQL 1.0**
- **Major Characteristics** (conductivity, surface): **AQL 1.5-2.5**
- **Minor/Cosmetic** (light scratches, dust): **AQL 4.0+**

**Standard Reference:** ANSI/ASQ Z1.4 (Statistical Sampling Procedures)

**Confidence:** 95% | **Source:** Quality sampling standards

---

### 3.2 Acceptance Numbers

**Acceptance Decision Table** (ANSI/ASQ Z1.4):

| **Sample Size** | **AQL 0.65** | **AQL 1.0** | **AQL 1.5** | **AQL 2.5** |
|---|---|---|---|---|
| **n=32** | Ac=0, Re=1 | Ac=0, Re=1 | Ac=0, Re=1 | Ac=0, Re=1 |
| **n=50** | Ac=0, Re=1 | Ac=0, Re=1 | Ac=0, Re=1 | Ac=1, Re=2 |
| **n=80** | Ac=0, Re=1 | Ac=0, Re=1 | Ac=1, Re=2 | Ac=1, Re=2 |
| **n=125** | Ac=0, Re=1 | Ac=1, Re=2 | Ac=1, Re=2 | Ac=2, Re=3 |
| **n=200** | Ac=0, Re=1 | Ac=1, Re=2 | Ac=2, Re=3 | Ac=3, Re=4 |

**Legend:**
- **Ac (Acceptance Number):** Maximum defects allowed to accept lot
- **Re (Rejection Number):** Minimum defects to reject lot
- **n (Sample Size):** Number of items to inspect from lot

**Example:** AQL 1.0, Sample Size 125, if defects found ≤1 → Accept lot; if ≥2 → Reject lot

---

## 4. DOCUMENTATION AND CORRECTIVE ACTION

### 4.1 Non-Conformance Report (NCR)

**Required Information:**

| **Section** | **Details** |
|---|---|
| **Identification** | NCR #, date, part #, lot #, batch quantity |
| **Defect Description** | Type (critical/major/minor/cosmetic), location, extent |
| **Quantification** | Measurements, area affected, sample size |
| **Discovery** | Where found (incoming, in-process, final), inspection method |
| **Specification** | Nominal, LSL, USL, tolerance |
| **Immediate Action** | Hold/quarantine, containment steps, customer impact assessment |
| **Root Cause Analysis** | Investigation findings, why it occurred |
| **Corrective Action** | Process change, equipment fix, procedure update |
| **Verification** | Confirmation testing, follow-up monitoring period |
| **Closure** | Effectiveness verified; process control restored |

**Retention:** Maintain 2-3 years; link to lot/batch for traceability

**Confidence:** 95% | **Source:** ISO 9001:2015, IATF 16949

---

### 4.2 Trend Analysis

**Monitor Over Time:**
- Defect frequency by type (track monthly)
- Pareto analysis (80/20 rule - identify vital few)
- Cpk trend (improving or declining process capability)
- Supplier performance (incoming material defects)
- Seasonal patterns (humidity, temperature effects)

**Action Triggers:**
- Increasing trend in any defect type → Investigate immediately
- Cpk declining below 1.33 → Process adjustment required
- Same root cause appearing 3+ times → Implement preventive action

---

## 5. QUICK REFERENCE: DEFECT DECISION FLOWCHART

```
Defect Identified
        ↓
Is defect safety-critical or causes immediate failure?
    ├─ YES → CRITICAL DEFECT
    │        Reject lot; investigate root cause
    │        Notify customer if already shipped
    │        Implement corrective action
    │
    └─ NO → Continue investigation
            ↓
Does defect significantly impact performance/function?
    ├─ YES → MAJOR DEFECT
    │        Hold batch; 100% inspection
    │        Root cause analysis
    │        Determine disposition (rework/scrap/use)
    │
    └─ NO → Continue investigation
            ↓
Does defect slightly affect appearance or marginal function?
    ├─ YES → MINOR DEFECT
    │        Document findings
    │        Monitor for pattern
    │        Continue production if isolated
    │
    └─ NO → COSMETIC DEFECT
            Document (if tracking)
            Accept; no action required
```

---

## 6. SPECIFIC ACCEPTANCE CRITERIA BY APPLICATION

### 6.1 For Anode Current Collector (Copper Foil)

| **Parameter** | **Specification** | **Acceptance Limit** | **Test Method** |
|---|---|---|---|
| Thickness | 10-15 μm | ±1 μm (Cpk ≥1.33) | ASTM B568/B499 |
| Conductivity | ≥97% IACS | Min 95% IACS | 4-Point Probe |
| Tensile Strength | 200-300 MPa | Within range | ASTM E345 |
| Elongation | ≥2-5% | Min 2% | ASTM E345 |
| Adhesion (ISO2409) | Class 0-1 | Accept | ISO 2409 |
| Adhesion (ISO4624) | ≥1.5 MPa | Min 1.0 MPa | ISO 4624 |
| Surface Defects | Per AQL 1.0 | Max 1 defect per sample | Visual/AOI |
| Corrosion (96h B117) | No red rust | Min 95% coating intact | ASTM B117 |

---

### 6.2 For Cathode Current Collector (Aluminum Foil)

| **Parameter** | **Specification** | **Acceptance Limit** | **Test Method** |
|---|---|---|---|
| Thickness | 15-20 μm | ±2 μm (Cpk ≥1.33) | ASTM B568/B499 |
| Conductivity | ≥58% IACS | Min 55% IACS | 4-Point Probe |
| Tensile Strength | 45-70 MPa | Within range | ASTM E345 |
| Elongation | ≥3% | Min 3% | ASTM E345 |
| Adhesion (ISO2409) | Class 0-1 | Accept | ISO 2409 |
| Adhesion (ISO4624) | ≥1.5 MPa | Min 1.0 MPa | ISO 4624 |
| Surface Defects | Per AQL 1.0 | Max 1 defect per sample | Visual/AOI |
| Corrosion (96h B117) | Light white film | Min 90% coating intact | ASTM B117 |

---

### 6.3 For Composite Current Collector (Multi-Layer)

| **Parameter** | **Specification** | **Acceptance Limit** | **Test Method** |
|---|---|---|---|
| Total Thickness | 12-18 μm | ±1.5 μm (Cpk ≥1.67) | ASTM B568/B499 |
| Layer Adhesion | Class 0 (ISO2409) | Zero defects | ISO 2409 |
| Interface Adhesion | ≥5-10 N/cm (180°) | Min 5 N/cm | ASTM D3330 |
| Pull-Off Strength | ≥1.5 MPa | Min 1.5 MPa critical | ISO 4624 |
| Delamination | None | Zero defects | Visual/cross-cut test |
| Conductivity (blended) | Per spec | Weighted average | 4-Point Probe |
| Surface Defects | Per AQL 0.65 | Zero critical; max 1 major | Visual/AOI |
| Environmental (IEC60068) | Per customer spec | Pass all tests | Temperature, vibration |

**Confidence:** 95% | **Source:** Battery component standards, customer requirements

---

## APPENDIX: References

- ISO 2409:2020 - Paints and Varnishes – Cross-cut Test
- ISO 4624:2023 - Paints and Varnishes – Pull-off Test for Adhesion
- ASTM D3330-04(2018) - Peel Adhesion of Pressure-Sensitive Tape
- ASTM E345-16 - Tension Testing of Metallic Foil
- ASTM B117-19 - Operating Salt Spray (Fog) Apparatus
- ASTM B568 - X-Ray Measurement of Coating Thicknesses
- ASTM B499-09R21E01 - Magnetic Method for Coating Thickness
- IATF 16949:2016 - Automotive Quality Management System
- ANSI/ASQ Z1.4 - Sampling Procedures and Tables for Inspection by Attributes
- ISO 9001:2015 - Quality Management Systems
- IEC 62660 - Electric Vehicle Battery Standards

---

**Document Version:** 1.0
**Last Updated:** January 8, 2026
**Prepared by:** Claude Code Research Agent
**Classification:** Quality Management Reference
