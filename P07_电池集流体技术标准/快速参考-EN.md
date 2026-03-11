---
title: "Technical Standards Quick Reference"
audience:
  primary: "technical"
language: "en"
content_type: "reference"
last_updated: "2026-01-08"
version: "1.0"
localization_status: "original"
---

# Technical Standards Quick Reference Guide

**Purpose:** Fast lookup reference for common standards, test methods, and acceptance criteria
**Last Updated:** January 8, 2026

---

## SECTION 1: KEY STANDARDS AT A GLANCE

### Quality Management Systems
| **Standard** | **Focus** | **Key Requirement** | **Application** |
|---|---|---|---|
| **ISO 9001:2015** | General QMS | Document procedures; continuous improvement | All manufacturers |
| **IATF 16949:2016** | Automotive QMS | SPC, APQP, PPAP, FMEA, MSA integration | Automotive suppliers |
| **ISO/TS 16949:2009** | Legacy automotive QMS | Replaced by IATF 16949:2016 | Older certifications |

### Battery and Electrical Standards
| **Standard** | **Focus** | **Key Testing** | **Application** |
|---|---|---|---|
| **IEC 61960-3** | Lithium battery cells (prismatic/cylindrical) | Capacity, cycle life, voltage range | Portable battery applications |
| **IEC 61960-4** | Lithium battery cells (coin) | Capacity, voltage, safety | Coin cell batteries |
| **IEC 62660-1** | EV battery performance | Electrical performance, discharge capacity | Electric vehicle batteries |
| **IEC 62660-2** | EV battery reliability & abuse | Thermal, vibration, shock, electrical abuse | Automotive traction batteries |
| **IEC 62660-3** | EV battery safety | Safety performance, thermal runaway test | EV battery safety validation |
| **IEC 60068** | Environmental testing | Temperature cycling, vibration, shock | Electronic component reliability |

### Automotive Supplier Standards
| **Standard** | **Scope** | **Grades/Levels** | **Key Requirement** |
|---|---|---|---|
| **AEC-Q100** | Discrete semiconductors | Grades 0-3 (temperature ranges) | Reliability testing; thermal cycling |
| **AEC-Q200** | Passive components | 5 grade categories | Thermal cycling, mechanical shock |

### Testing Standards (ASTM/ISO)
| **Standard** | **Test Type** | **Material** | **Key Parameter** |
|---|---|---|---|
| **ASTM E345** | Tensile testing | Metallic foil | Strength, elongation, yield |
| **ASTM B568** | Thickness (X-ray) | Coated metals | Quantitative thickness |
| **ASTM B499** | Thickness (magnetic) | Non-magnetic coatings on magnetic base | Quantitative thickness |
| **ISO 2409** | Cross-cut adhesion | Coatings | Class 0-5 rating |
| **ISO 4624** | Pull-off adhesion | Coatings | Tensile strength (MPa) |
| **ASTM D3330** | Peel adhesion | Pressure-sensitive tape | Peel force (N/cm) |
| **ASTM B117** | Salt spray (corrosion) | Metals/coatings | Corrosion resistance |
| **ISO 286** | Tolerances | All products | Dimensional tolerance grades |

---

## SECTION 2: CURRENT COLLECTOR FOIL SPECIFICATIONS

### Anode Current Collector (Copper Foil)
| **Property** | **Typical Specification** | **Test Method** | **Frequency** |
|---|---|---|---|
| **Thickness** | 10-15 μm, ±1 μm | ASTM B568/B499 | Continuous |
| **Conductivity** | ≥97% IACS @ 20°C | 4-Point Probe | Every 4-8 hrs |
| **Tensile Strength** | 200-300 MPa | ASTM E345 | Per batch |
| **Elongation** | ≥2-5% | ASTM E345 | Per batch |
| **Adhesion (ISO2409)** | Class 0-1 | ISO 2409 cross-cut | Every batch |
| **Adhesion (ISO4624)** | ≥1.5 MPa | ISO 4624 pull-off | Per batch |
| **Corrosion (B117/96h)** | No red rust; <5-10% white | ASTM B117 | Certification |
| **Surface Defects** | AQL 1.0 | Visual/AOI | Continuous |

### Cathode Current Collector (Aluminum Foil)
| **Property** | **Typical Specification** | **Test Method** | **Frequency** |
|---|---|---|---|
| **Thickness** | 15-20 μm, ±2 μm | ASTM B568/B499 | Continuous |
| **Conductivity** | ≥58% IACS @ 20°C | 4-Point Probe | Every 4-8 hrs |
| **Tensile Strength** | 45-70 MPa | ASTM E345 | Per batch |
| **Elongation** | ≥3% | ASTM E345 | Per batch |
| **Adhesion (ISO2409)** | Class 0-1 | ISO 2409 cross-cut | Every batch |
| **Adhesion (ISO4624)** | ≥1.5 MPa | ISO 4624 pull-off | Per batch |
| **Corrosion (B117/96h)** | Light white oxide; >90% intact | ASTM B117 | Certification |
| **Surface Defects** | AQL 1.0 | Visual/AOI | Continuous |

### Composite Current Collector (Multi-Layer)
| **Property** | **Typical Specification** | **Test Method** | **Frequency** |
|---|---|---|---|
| **Total Thickness** | 12-18 μm, ±1.5 μm | ASTM B568/B499 | Continuous |
| **Layer Adhesion** | Class 0 (no defects) | ISO 2409 cross-cut | Every batch |
| **Interface Adhesion** | ≥5-10 N/cm (180° peel) | ASTM D3330 | Every batch |
| **Pull-Off Strength** | ≥1.5 MPa | ISO 4624 | Per batch |
| **Delamination** | Zero (100% inspection) | Visual inspection | Every sheet |
| **Blended Conductivity** | Per specification | Weighted measurement | Per batch |
| **Environmental Testing** | Per IEC 60068 | Temperature, vibration | Periodic validation |

---

## SECTION 3: PROCESS CAPABILITY REQUIREMENTS (IATF 16949)

### Cpk Values and Interpretation
| **Cpk Value** | **Capability** | **Status** | **Action Required** |
|---|---|---|---|
| **Cpk ≥1.67** | Highly capable | Excellent | Maintain process; monitor trends |
| **Cpk 1.33-1.67** | Capable | Acceptable | Continue monitoring; target improvement |
| **Cpk 1.0-1.33** | Marginal | At risk | Implement improvement plan |
| **Cpk <1.0** | Incapable | Critical | Immediate intervention required |

### Cpk Calculation Quick Formula
```
Cpk = min[(USL - Mean)/(3σ), (Mean - LSL)/(3σ)]

Where:
- USL = Upper Specification Limit
- LSL = Lower Specification Limit
- Mean = Average of measurements
- σ = Standard deviation

Example: Thickness 15 μm ±2 μm (LSL=13, USL=17)
If Mean=14.8 μm, σ=0.4 μm:
Cpk = min[(17-14.8)/(3×0.4), (14.8-13)/(3×0.4)]
Cpk = min[1.83, 1.5] = 1.5 (Capable)
```

---

## SECTION 4: ADHESION TESTING QUICK REFERENCE

### ISO 2409 - Cross-Cut Test Results
| **Class** | **Appearance** | **Acceptance** |
|---|---|---|
| **0** | Perfect adhesion; no flaking | ✅ ACCEPT |
| **1** | Small flakes at intersections; <5% area | ✅ ACCEPT |
| **2** | Flaking along cuts; 5-15% area | ⚠️ MARGINAL |
| **3** | Flaking in patches; 15-35% area | ❌ REJECT |
| **4** | Flaking in patches; >35% area | ❌ REJECT |
| **5** | Complete peeling; all removed | ❌ REJECT |

### ISO 4624 - Pull-Off Test Results
| **Result** | **Strength (MPa)** | **Status** |
|---|---|---|
| **Excellent** | ≥2.0 MPa | ✅ ACCEPT |
| **Good** | 1.5-2.0 MPa | ✅ ACCEPT |
| **Marginal** | 1.0-1.5 MPa | ⚠️ AT LIMIT |
| **Poor** | 0.5-1.0 MPa | ❌ REJECT |
| **Failed** | <0.5 MPa | ❌ REJECT |

### ASTM D3330 - 180° Peel Test Results
| **Peel Strength** | **Status** | **Application** |
|---|---|---|
| **≥10 N/cm** | Excellent | ✅ High-reliability applications |
| **7-10 N/cm** | Good | ✅ Standard applications |
| **5-7 N/cm** | Acceptable | ✅ Composite foil minimum |
| **3-5 N/cm** | Marginal | ⚠️ Requires investigation |
| **<3 N/cm** | Failed | ❌ Rejected |

---

## SECTION 5: DEFECT SEVERITY CLASSIFICATION

### Quick Decision Guide
| **Defect Impact** | **Severity** | **AQL** | **Batch Action** | **Testing** |
|---|---|---|---|---|
| Safety hazard; causes failure | **CRITICAL** | 0 | Reject all | Investigation + CAPA |
| Significant impact on function | **MAJOR** | 0.65-1.0 | Hold; 100% inspect | Root cause analysis |
| Slight impact; marginal function | **MINOR** | 2.5-4.0 | Document; monitor | Continue sampling |
| Appearance only | **COSMETIC** | 4.0-6.5 | Accept | Track if systematic |

### Common Defects and Severity

| **Defect Type** | **Size/Extent** | **Severity** |
|---|---|---|
| **Delamination** | >25 mm² | Critical |
| | 5-25 mm² | Major |
| | <5 mm² | Minor |
| **Thickness Variation** | >2× tolerance | Critical |
| | 1.5-2× tolerance | Major |
| | <1.5× tolerance | Minor |
| **Scratch (length)** | >25 mm | Critical |
| | 10-25 mm | Major |
| | 5-10 mm | Minor |
| | <5 mm | Cosmetic |
| **Conductivity** | <50% spec | Critical |
| | 50-75% spec | Major |
| | 75-95% spec | Minor |
| **Adhesion (ISO2409)** | Class 4-5 | Critical |
| | Class 2-3 | Major |
| | Class 1 | Minor |
| | Class 0 | Acceptable |

---

## SECTION 6: AQL SAMPLING REFERENCE

### AQL Levels for Battery Components
| **AQL** | **Application** | **Risk** | **Typical Sample (n=125)** |
|---|---|---|---|
| **0.65** | Safety-critical | Very stringent | 0-1 defects accepted |
| **1.0** | Critical characteristics | Stringent | 1-2 defects accepted |
| **1.5** | Major characteristics | Moderate-high | 2-3 defects accepted |
| **2.5** | Minor characteristics | Moderate | 4-5 defects accepted |
| **4.0** | Non-critical | Less stringent | 5-7 defects accepted |

### Acceptance Decisions (ANSI/ASQ Z1.4)
**Sample Size n=125, AQL=1.0:**
- If defects found ≤1 → **Accept lot**
- If defects found ≥2 → **Reject lot**

**Sample Size n=125, AQL=2.5:**
- If defects found ≤2 → **Accept lot**
- If defects found ≥3 → **Reject lot**

---

## SECTION 7: TESTING DECISION MATRIX

| **Characteristic** | **Method** | **Frequency** | **Accept Criteria** | **Confidence** |
|---|---|---|---|---|
| **Thickness** | Automated ASTM B568/B499 | Continuous | Within tolerance; Cpk≥1.33 | 95% |
| **Conductivity** | 4-Point Probe | Every 4-8 hrs | ≥58% IACS (Al), ≥97% (Cu) | 85% |
| **Tensile** | ASTM E345 | Per batch | Within specification range | 95% |
| **Adhesion** | ISO 2409/ISO 4624/ASTM D3330 | Every batch | Class 0-1 or ≥1.5 MPa | 95% |
| **Corrosion** | ASTM B117 salt spray | Certification | No red rust; <10% white corrosion | 95% |
| **Defects** | Visual/AOI | Continuous | Per AQL acceptance number | 85% |
| **SPC** | Control charts; Cpk analysis | Monthly | Cpk≥1.33 (target 1.67) | 95% |

---

## SECTION 8: EQUIPMENT CALIBRATION CHECKLIST

| **Equipment** | **Standard** | **Frequency** | **Certificate** |
|---|---|---|---|
| **Thickness gauge (X-ray)** | ASTM B568 | Annually | Yes |
| **Thickness gauge (magnetic)** | ASTM B499 | Annually | Yes |
| **Conductivity probe** | Certified standards | Annually | Yes |
| **Tensile machine** | ASTM E4 | Annually | Yes |
| **Load cell** | NIST traceable | Annually | Yes |
| **Micrometer** | Gauge blocks | Annually | Yes |
| **Scale (weight)** | Calibrated weights | Annually | Yes |
| **Temperature/humidity** | Reference standards | Quarterly | Yes |
| **pH meter** | pH standards | Monthly | Yes |

---

## SECTION 9: COMMON FAILURES AND QUICK ACTIONS

| **Problem** | **Root Cause** | **Quick Check** | **Action** |
|---|---|---|---|
| **Thickness variation** | Equipment wear / temperature | Check calibration; measure at 3 points | Maintenance or adjust process |
| **Low conductivity** | Wrong material / heat treatment | Review supplier cert; check specs | Material verification; supplier audit |
| **Adhesion failure** | Contamination / process parameter | Check surface cleanliness | Clean surface; verify coating temp |
| **Delamination** | Moisture / poor coating | Check humidity; review coating process | Control environment; adjust application |
| **Corrosion during test** | Inadequate coating | Measure coating thickness | Increase thickness; improve quality |
| **High defect rate** | Equipment or process issue | Review SPC data; check equipment | Root cause analysis; CAPA |

---

## SECTION 10: STANDARDS IMPLEMENTATION PRIORITY

### Phase 1 - CRITICAL (Month 1-3)
- [ ] ISO 9001:2015 basic documentation
- [ ] IATF 16949:2016 gap assessment
- [ ] Thickness and conductivity testing capability
- [ ] Adhesion testing setup (ISO 2409 cross-cut)

### Phase 2 - HIGH (Month 4-6)
- [ ] Advanced tensile testing (ASTM E345)
- [ ] Pull-off adhesion testing (ISO 4624)
- [ ] Corrosion testing (ASTM B117)
- [ ] SPC implementation with Cpk calculation

### Phase 3 - MEDIUM (Month 7-12)
- [ ] Full IATF 16949:2016 compliance
- [ ] AEC-Q standard requirements
- [ ] Lean Six Sigma program launch
- [ ] Process capability validation (Cpk≥1.33)

### Phase 4 - ONGOING
- [ ] Standards audit and update
- [ ] Continuous improvement initiatives
- [ ] Supplier quality management
- [ ] Advanced analytics and optimization

---

## SECTION 11: KEY TELEPHONE REFERENCE

### If You Need to...

**Check a standard number:**
→ See Section 1: Key Standards at a Glance

**Find acceptance criteria:**
→ See Section 2: Current Collector Foil Specifications
→ See Section 4: Adhesion Testing Quick Reference

**Understand test procedure:**
→ See Section 7: Testing Decision Matrix
→ Reference: 测试程序指南-EN.md

**Classify a defect:**
→ See Section 5: Defect Severity Classification
→ Reference: 缺陷分类指南-EN.md

**Calculate process capability:**
→ See Section 3: Process Capability Requirements
→ Reference: 技术标准综合-EN.md (Section 5.1)

**Decide on sampling:**
→ See Section 6: AQL Sampling Reference
→ Reference: 缺陷分类指南-EN.md (Section 3)

**Fix a failing test:**
→ See Section 9: Common Failures and Quick Actions
→ Reference: 测试程序指南-EN.md (Section 10)

---

## SECTION 12: DOCUMENT CROSS-REFERENCES

| **Need** | **Primary Document** | **Section** |
|---|---|---|
| **Detailed standard info** | 技术标准综合-EN.md | All sections |
| **Test procedures** | 测试程序指南-EN.md | Sections 1-7 |
| **Defect definitions** | 缺陷分类指南-EN.md | Sections 1-3 |
| **Implementation plan** | status.md | "Implementation Recommendations" |
| **Quick lookup** | 快速参考-EN.md | This document |

---

## IMPORTANT NOTES

### For Critical Characteristics
- Thickness, adhesion, and conductivity require highest control (Cpk≥1.67)
- 100% testing or aggressive sampling (AQL 0.65-1.0) recommended
- Real-time monitoring preferred; document all results

### For Composite Foil
- Interface adhesion between layers is critical
- 180° peel test (ASTM D3330) is best quantitative measure
- Minimum ≥5 N/cm; critical applications ≥7-10 N/cm

### Automotive Applications
- IATF 16949:2016 mandatory for tier 1-2 suppliers
- AEC-Q standards apply for battery-specific components
- Customer-specific requirements often exceed standards
- Document all testing; maintain 2-3 year records

### For New Products
- Conduct FMEA before production
- Perform capability studies (Cpk analysis) on all critical characteristics
- Complete PPAP (Production Part Approval Process)
- Customer sign-off required before full production

---

**Version:** 1.0 | **Last Updated:** January 8, 2026 | **Confidence:** 85%+

*For detailed information, refer to the comprehensive documents in this standards package.*
