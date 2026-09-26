"""CulvertCrawl concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. The culvert axis runs along X with the mouth at X = MOUTH and the pipe
extending toward -X; the crawler sits at X = 0. The pipe invert (inside bottom) is at Z = 0. The crawler drives
toward -X (deeper into the pipe); the tether reel and surface box stand outside the mouth
at +X. Crawler parts are first modeled in a local frame (forward = +X, track bottom at Z = 0)
and then placed in the pipe with place().
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Torus, Cone, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all

# ---------------- key dimensions (mm) ----------------
PIPE_R = 300.0          # 600 mm (24 in) ID culvert used for the hero scene
PIPE_WALL = 8.0
PIPE_L = 2000.0
TRACK_Y, TRACK_W, CAM_Z = 65.0, 40.0, 62.0   # checked against cad/src/model.py PARAMS below
CX = 0.0                # crawler center (world); kept at X = 0 so the kit cutaway plane passes through it
MOUTH = 700.0           # culvert mouth (world X)
TZ = PIPE_R - math.sqrt(PIPE_R ** 2 - (TRACK_Y + TRACK_W / 2) ** 2)  # outer track edges touch the invert


def place(shape):
    """Local crawler frame (forward +X) to world: turn to face -X, set at CX on the invert."""
    return Pos(CX, 0, TZ) * Rot(0, 0, 180) * shape


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def xcyl(r, length, x0, y=0.0, z=0.0):
    """Cylinder along +X starting at x0."""
    return Pos(x0 + length / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, length)


def ycyl(r, length, x=0.0, y=0.0, z=0.0):
    """Cylinder along Y centered at (x, y, z)."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, length)


def keep_far_half(shape):
    """Remove the upper half of a context shape nearest the viewer (-Y) so the pipe interior shows,
    keeping the invert under the crawler."""
    return shape & (Pos(0, 2500, 0) * Box(10000, 5000, 10000) + Pos(0, 0, -4900) * Box(10000, 10000, 10000))


# ---------------- crawler and surface kit from the parametric model (cad/src/model.py) ----------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import PARAMS as MP, crawler_parts, surface_parts  # noqa: E402

assert (TRACK_Y, TRACK_W, CAM_Z) == (MP["track_y"], MP["track_w"], MP["cam_z"]), "sync with model.py"
CP = crawler_parts()
REEL_X = MOUTH + 460.0                     # model places the reel 180 mm after x0
SP = surface_parts(x0=REEL_X - 180.0)
REEL_Z = MP["reel_hub_z"]
COUNTER_X = REEL_X - 190.0

# 9 Tether: strain relief on the crawler, then routed along the invert, out of the mouth to the counter and reel
rear = (CX + MP["hull_l"] / 2 + 12 + MP["relief_l"] + 36, 0, TZ + CAM_Z)
tether_pts = [rear, (CX + MP["hull_l"] / 2 + 140, 0, 8), (MOUTH - 40, 0, 6), (MOUTH + 40, 0, 14),
              (COUNTER_X, 0, 150), (REEL_X - 10, 0, REEL_Z + 118)]
tether = place(CP[9][1])
for a, b in zip(tether_pts[:-1], tether_pts[1:]):
    tether = tether + tube3(a, b, 3.5)

parts = [
    Part(CP[1][0], place(CP[1][1]), "#A8B0B8", 1, (0, 0, 260)),
    Part(CP[2][0], place(CP[2][1]), "#1F2937", 2, (0, 0, -110)),
    Part(CP[3][0], place(CP[3][1]), "#0F766E", 3, (0, 0, 520)),
    Part(CP[4][0], place(CP[4][1]), "#16A34A", 4, (0, 0, 700)),
    Part(CP[5][0], place(CP[5][1]), "#2563EB", 5, (-60, 120, 330)),
    Part(CP[6][0], place(CP[6][1]), "#D4A017", 6, (-200, 420, 220)),
    Part(CP[7][0], place(CP[7][1]), "#C2410C", 7, (-80, 300, -20)),
    Part(CP[8][0], place(CP[8][1]), "#6B7280", 8, (0, 0, -230)),
    Part("Tether, 60 m hybrid, with strain relief", tether, "#111827", 9, (-850, -950, -300)),
    Part(SP[10][0], SP[10][1], "#7C3AED", 10, (-1250, -1300, -350)),
    Part(SP[11][0], SP[11][1], "#0E7490", 11, (-1100, -650, -350)),
    Part(SP[12][0], SP[12][1], "#374151", 12, (-950, -650, -250)),
]

# Context for the hero only: a sectioned 600 mm culvert and the projected laser ring (light, illustrative)
pipe = Pos(MOUTH - PIPE_L / 2, 0, PIPE_R) * Rot(0, 90, 0) * (Cylinder(PIPE_R + PIPE_WALL, PIPE_L) - Cylinder(PIPE_R, PIPE_L + 2))
ring_x = CX - (MP["hull_l"] / 2 + MP["ring_d"])
light = Pos(ring_x, 0, PIPE_R) * Rot(0, 90, 0) * Torus(PIPE_R - 3, 3)
context = [Part("Culvert, 600 mm ID, sectioned", keep_far_half(pipe), "#C8CDD3"),
           Part("Laser ring on pipe wall", keep_far_half(light), "#22C55E")]

if __name__ == "__main__":
    render_all(
        parts, project="CulvertCrawl", title="Tethered culvert crawler concept", dwg_no="CVC-DWG-010", date="2026-09-25",
        key_figures=["Fits 300 to 900 mm (12 to 36 in) pipe; 610 x 170 x 106 mm crawler",
                     "5.8 kg; 3.05 kg net submerged; 0.15 m/s survey speed",
                     "Laser ring 300 mm ahead; 0.24 / 0.62 / 0.97 % of D (300/600/900)",
                     "60 m tether, 48 V DC; reach 56 m dry, 52 m wet uphill",
                     "28 W crawler loads; 6.4 h per charge (CVC-CAL-001 v0.2)",
                     "Parts $906 against the $910 budget (indicative)"],
        cut_exclude=("Tether, 60 m hybrid, with strain relief", "Tether reel, slip ring, payout counter",
                     "Surface control box (LiFePO4, 48 V boost)", "Operator gamepad"),
        context=context,
        flow={"title": "power flow while driving and profiling, W (estimates)", "unit": "W",
              "stages": [("LiFePO4 battery out", 36.0), ("48 V boost out", 32.2),
                         ("At crawler, 60 m", 30.8), ("Crawler loads", 28.0)],
              "losses": [(0, "Boost and surface box", 3.8), (1, "Tether (4.4 %)", 1.4),
                         (2, "Buck converters (9 %)", 2.8)]},
    )
