# CulvertCrawl

**Area:** Situational Field Hardware · **Status:** Concept · **Prototype budget:** about $800 USD · **Difficulty:** 4 of 5

Tethered tracked crawler with a camera, lights and laser ring profiling that measures pipe deformation and blockage.

## Problem

Small culverts and drains are hard to inspect without confined-space entry.

## Concept

Tethered tracked crawler with a camera, lights and laser ring profiling that measures pipe deformation and blockage.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Tracked chassis
- Gear motors (2)
- Waterproof camera
- LED ring
- Line laser
- Tether reel
- Raspberry Pi

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
