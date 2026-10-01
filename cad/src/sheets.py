"""CulvertCrawl general arrangement drawing CVC-DWG-001 (Rev P3, constructable design CVC-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/CVC-DWG-001.svg, .pdf and .png from the parametric model (cad/src/model.py).
The concept blueprint in media/ uses CVC-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import warnings  # noqa: E402
warnings.filterwarnings("ignore")
from build123d import Compound, Cylinder, Pos, Rot  # noqa: E402
from drawing import Sheet, project_views, M, TB_Y  # noqa: E402
from model import PARAMS as P, crawler_parts, track_contact_height  # noqa: E402

parts = crawler_parts()
crawler = Compound(children=[s for _, s in parts.values()])
work = ROOT / "cad/drawings/_views"
views = project_views(crawler, work)


def fit_view(d, name):
    """End view (from the front) of the crawler sitting in a pipe of inside diameter d."""
    R = d / 2
    tz = track_contact_height(d)
    ring = Pos(P["hull_l"] / 2 + P["ring_d"] + 40, 0, R) * Rot(0, 90, 0) * (Cylinder(R + 6, 2) - Cylinder(R, 4))
    shape = Compound(children=[Pos(0, 0, tz) * s for _, s in parts.values()] + [ring])
    return project_views(shape, work / name)["right"]


fit300, fit900 = fit_view(300, "p300"), fit_view(900, "p900")

s = Sheet(project="CulvertCrawl", title="General arrangement, crawler", dwg_no="CVC-DWG-001",
          rev="P3", author="Amish Chadha", date="2026-09-30", concept=True,
          material="Hull 6061 Al; ballast steel; side plates Al; boom, fin, window acrylic. See bom/bom.csv. PRELIMINARY",
          revisions=[("P1", "Preliminary GA from parametric model (CVC-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Ring plane 300; ballast 230 x 80 x 14 (CVC-DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Design for construction (CVC-DDR-003)", "2026-09-30", "AC")])
s.add_ortho(views, ["front", "top", "right"])
k = s.scale
# fit checks: end views in 300 mm and 900 mm pipe at 1:10, side by side
s.add_svg(fit300, 272, 28, 40, 96, scale=0.1, label="Fit, 300 mm", sublabel="Scale 1:10")
s.add_svg(fit900, 318, 28, 96, 96, scale=0.1, label="Fit, 900 mm", sublabel="Scale 1:10")
s.add_notes("Key dimensions and figures (mm unless noted)", [
    f"Width over tracks {2 * (P['track_y'] + P['track_w'] / 2):.0f}; height over lid screws 106",
    f"Length {P['hull_l'] + P['ring_d'] + 12 + 13 + P['relief_l'] + 16:.0f}, rear strain relief to laser end cap (track length 270)",
    f"Track centers {2 * P['track_y']:.0f} apart; belts {P['track_w']:.0f} wide; sprockets R{P['track_r']:.0f} at {2 * P['track_x']:.0f}",
    f"Hull {P['hull_l']:.0f} x {P['hull_w']:.0f} x {P['hull_h']:.0f}, {P['wall']:.0f} wall, {P['front_wall']:.0f} front wall",
    f"Flush lid {P['lid_t']:.0f}, ten M4 screws, O-ring in a {P['rim'][0]:.0f} mm inner rim",
    f"Camera axis {P['cam_z']:.0f} above track contact line; dome R{P['dome_r']:.0f}; bezel R{P['bezel'][1]:.0f}",
    f"Laser ring plane {P['ring_d']:.0f} ahead of the dome center; boom on a clear fin",
    f"Ballast {P['ballast'][0]:.0f} x {P['ballast'][1]:.0f} x {P['ballast'][2]:.0f} steel, {P['ballast_z0']:.0f} above contact line",
    f"Side plates 3 thick tie hull to ballast; tether penetrator {P['tether_z']:.0f} up",
    "Mass 6.6 kg; 3.8 kg net when submerged (CVC-CAL-001 v0.4)",
    "Clearance to wall 50 or more in 300 to 900 mm pipe",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=272, y=142, width=144)
s.save(ROOT / "cad/drawings/CVC-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print(f"ortho scale {k:g}; wrote cad/drawings/CVC-DWG-001.svg, .pdf, .png")
