"""CulvertCrawl concept massing model and media (TRL 2).

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
TRACK_Y = 65.0          # track centerline offset from the crawler axis
TRACK_W = 40.0          # track belt width
TRACK_R = 35.0          # sprocket and idler radius over the belt
TRACK_X = 100.0         # sprocket and idler centers at +/- TRACK_X
HULL_L, HULL_W, HULL_H, HULL_T = 240.0, 88.0, 80.0, 4.0
HULL_Z0 = 22.0          # hull bottom above the track contact line
CAM_Z = 62.0            # camera and laser axis height above the track contact line
LENS_X = 150.0          # front of the dome port (local)
RING_D = 200.0          # laser ring plane distance ahead of the lens
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


# ---------------- crawler (local frame) ----------------
# 1 Sealed hull: aluminium box with O-ring lid, open shell so the cutaway shows the inside
hull = (Pos(0, 0, HULL_Z0 + HULL_H / 2) * Box(HULL_L, HULL_W, HULL_H)
        - Pos(0, 0, HULL_Z0 + HULL_H / 2) * Box(HULL_L - 2 * HULL_T, HULL_W - 2 * HULL_T, HULL_H - 2 * HULL_T))
lid_lip = Pos(0, 0, HULL_Z0 + HULL_H + 3) * Box(HULL_L + 6, HULL_W + 6, 6)
hull = hull + lid_lip


# 2 Track modules: belt around a rear drive sprocket and a front idler, each side
def track(y):
    belt = (Pos(0, y, TRACK_R) * Box(2 * TRACK_X, TRACK_W, 2 * TRACK_R)
            + ycyl(TRACK_R, TRACK_W, -TRACK_X, y, TRACK_R) + ycyl(TRACK_R, TRACK_W, TRACK_X, y, TRACK_R))
    return belt


tracks = track(TRACK_Y) + track(-TRACK_Y)
side_plates = (Pos(0, TRACK_Y - TRACK_W / 2 - 1.5, TRACK_R) * Box(2 * TRACK_X, 3, 30)
               + Pos(0, -TRACK_Y + TRACK_W / 2 + 1.5, TRACK_R) * Box(2 * TRACK_X, 3, 30))
tracks = tracks + side_plates


# 3 Worm gear motors (self-locking), lengthwise in the rear of the hull, driving the rear sprockets
def motor(y):
    can = xcyl(12.5, 55, -68, y, 50)
    gearbox = Pos(-90, y, 50) * Box(32, 30, 40)
    shaft = ycyl(4, 42, -TRACK_X, y + (21 if y > 0 else -21), TRACK_R)
    return can + gearbox + shaft


motors = motor(20) + motor(-20)

# 4 Electronics stack: Raspberry Pi 4, motor driver, 48 V to 12 V and 5 V converters, IMU, leak sensor
electronics = (Pos(30, 0, 44) * Box(90, 62, 8)            # compute board
               + Pos(30, 0, 58) * Box(70, 50, 14)         # driver and converter layer
               + Pos(-15, 0, 44) * Box(18, 40, 16))       # DC-DC module

# 5 Camera with fisheye lens behind an acrylic dome port
camera = (Pos(LENS_X - 30, 0, CAM_Z) * Box(20, 28, 28)
          + (Pos(HULL_L / 2, 0, CAM_Z) * Sphere(30) & Pos(HULL_L / 2 + 50, 0, CAM_Z) * Box(100, 100, 100)))

# 6 LED ring light around the dome
led_ring = Pos(HULL_L / 2 + 4, 0, CAM_Z) * Rot(0, 90, 0) * (Cylinder(44, 8) - Cylinder(32, 10))

# 7 Laser ring projector on a clear boom: laser diode and conical mirror at RING_D ahead of the lens
boom = xcyl(9, RING_D - 10, LENS_X - 5, 0, CAM_Z)
head = xcyl(13, 26, LENS_X + RING_D - 13, 0, CAM_Z) + Pos(LENS_X + RING_D, 0, CAM_Z) * Rot(0, -90, 0) * Cone(13, 3, 12)
laser = boom + head

# 8 Ballast skid plate under the hull (steel), also protects the hull bottom
ballast = Pos(0, 0, HULL_Z0 - 6) * Box(HULL_L - 30, 80, 12)

# 9a Tether strain relief and bend restrictor at the rear of the hull
relief = xcyl(11, 30, -HULL_L / 2 - 30, 0, CAM_Z) + Pos(-HULL_L / 2 - 38, 0, CAM_Z) * Rot(0, 90, 0) * Cone(5, 11, 16)

# ---------------- tether, reel and surface box (world) ----------------
REEL_X, REEL_Z, REEL_R, REEL_W = MOUTH + 460.0, 230.0, 160.0, 110.0
rear = (CX + HULL_L / 2 + 46, 0, TZ + CAM_Z)
tether_pts = [rear, (CX + HULL_L / 2 + 140, 0, 8), (MOUTH - 40, 0, 6), (MOUTH + 40, 0, 14), (MOUTH + 300, 0, 150),
              (REEL_X - 10, 0, REEL_Z + 118)]
tether = place(relief)
for a, b in zip(tether_pts[:-1], tether_pts[1:]):
    tether = tether + tube3(a, b, 3.5)

# 10 Reel: two flanges, drum with wound tether, A-frame, hand crank, slip ring and payout counter
flanges = ycyl(REEL_R, 6, REEL_X, REEL_W / 2, REEL_Z) + ycyl(REEL_R, 6, REEL_X, -REEL_W / 2, REEL_Z)
wound = ycyl(115, REEL_W - 6, REEL_X, 0, REEL_Z)
frame = None
for dy in (REEL_W / 2 + 12, -REEL_W / 2 - 12):
    for dx in (-150, 150):
        leg = tube3((REEL_X + dx, dy, 0), (REEL_X, dy, REEL_Z), 10)
        frame = leg if frame is None else frame + leg
frame = frame + tube3((REEL_X - 150, REEL_W / 2 + 12, 0), (REEL_X - 150, -REEL_W / 2 - 12, 0), 10) \
              + tube3((REEL_X + 150, REEL_W / 2 + 12, 0), (REEL_X + 150, -REEL_W / 2 - 12, 0), 10)
axle = ycyl(12, REEL_W + 60, REEL_X, 0, REEL_Z)
crank = tube3((REEL_X, -REEL_W / 2 - 30, REEL_Z), (REEL_X + 90, -REEL_W / 2 - 30, REEL_Z + 60), 7) \
        + ycyl(9, 50, REEL_X + 90, -REEL_W / 2 - 55, REEL_Z + 60)
slip_ring = ycyl(22, 40, REEL_X, REEL_W / 2 + 50, REEL_Z)
counter = Pos(MOUTH + 300, 0, 150) * Box(60, 44, 50) + tube3((MOUTH + 300, 0, 125), (REEL_X - 150, 0, 8), 7)
reel = flanges + wound + frame + axle + crank + slip_ring + counter

# 11 Surface control box: rugged case with LiFePO4 battery, 48 V boost converter, fuse, e-stop
BOX_X0, BOX_L, BOX_W, BOX_H = MOUTH + 700.0, 410.0, 330.0, 175.0
case = Pos(BOX_X0 + BOX_L / 2, 0, BOX_H / 2) * Box(BOX_L, BOX_W, BOX_H) \
    - Pos(BOX_X0 + BOX_L / 2, 0, BOX_H / 2 + 6) * Box(BOX_L - 12, BOX_W - 12, BOX_H)
case = case + Pos(BOX_X0 + BOX_L / 2, 0, BOX_H + 4) * Box(BOX_L, BOX_W, 8)          # lid
battery = Pos(BOX_X0 + 130, 0, 6 + 85) * Box(180, 175, 170)                            # 12.8 V 20 Ah LiFePO4
boost = Pos(BOX_X0 + 300, 60, 6 + 30) * Box(110, 80, 60)
estop = Pos(BOX_X0 + 330, -100, BOX_H + 8) * Cylinder(22, 16) + Pos(BOX_X0 + 330, -100, BOX_H + 22) * Cylinder(28, 12)
power_lead = tube3((BOX_X0, 60, 120), (REEL_X + 40, REEL_W / 2 + 70, REEL_Z), 4)
surface_box = case + battery + boost + estop + power_lead

# 12 Operator gamepad on the lid (laptop not in kit cost)
gamepad = Pos(BOX_X0 + 150, -40, BOX_H + 22) * Box(150, 95, 28)

parts = [
    Part("Sealed hull and lid", place(hull), "#A8B0B8", 1, (0, 0, 260)),
    Part("Track modules (pair)", place(tracks), "#1F2937", 2, (0, 0, -110)),
    Part("Worm gear motors (2)", place(motors), "#0F766E", 3, (0, 0, 520)),
    Part("Electronics stack (Pi 4, driver, DC-DC)", place(electronics), "#16A34A", 4, (0, 0, 700)),
    Part("Fisheye camera and dome port", place(camera), "#2563EB", 5, (-60, 120, 330)),
    Part("LED ring light", place(led_ring), "#D4A017", 6, (-200, 420, 220)),
    Part("Laser ring projector on boom", place(laser), "#C2410C", 7, (-80, 300, -20)),
    Part("Ballast skid plate", place(ballast), "#6B7280", 8, (0, 0, -230)),
    Part("Tether, 60 m hybrid, with strain relief", tether, "#111827", 9, (-850, -950, -300)),
    Part("Tether reel, slip ring, payout counter", reel, "#7C3AED", 10, (-1250, -1300, -350)),
    Part("Surface control box (LiFePO4, 48 V boost)", surface_box, "#0E7490", 11, (-1100, -650, -350)),
    Part("Operator gamepad", gamepad, "#374151", 12, (-950, -650, -250)),
]

# Context for the hero only: a sectioned 600 mm culvert and the projected laser ring (light, illustrative)
pipe = Pos(MOUTH - PIPE_L / 2, 0, PIPE_R) * Rot(0, 90, 0) * (Cylinder(PIPE_R + PIPE_WALL, PIPE_L) - Cylinder(PIPE_R, PIPE_L + 2))
ring_x = CX - (LENS_X + RING_D)
light = Pos(ring_x, 0, PIPE_R) * Rot(0, 90, 0) * Torus(PIPE_R - 3, 3)
context = [Part("Culvert, 600 mm ID, sectioned", keep_far_half(pipe), "#C8CDD3"),
           Part("Laser ring on pipe wall", keep_far_half(light), "#22C55E")]

if __name__ == "__main__":
    render_all(
        parts, project="CulvertCrawl", title="Tethered culvert crawler concept", dwg_no="CVC-DWG-010",
        key_figures=["Fits 300 to 900 mm (12 to 36 in) pipe; 490 x 170 x 125 mm crawler",
                     "About 5.5 kg with ballast; 0.15 m/s survey speed (estimate)",
                     "Laser ring 200 mm ahead of lens; about 1 % of diameter (estimate)",
                     "60 m tether, 48 V DC and 100 Mbit/s Ethernet; about 50 m reach (estimate)",
                     "About 28 W in the crawler; about 6 h per charge (estimate)",
                     "Parts about $900, over the $800 budget (indicative)"],
        cut_exclude=("Tether, 60 m hybrid, with strain relief", "Tether reel, slip ring, payout counter",
                     "Surface control box (LiFePO4, 48 V boost)", "Operator gamepad"),
        context=context,
        flow={"title": "power flow while driving and profiling, W (estimates)", "unit": "W",
              "stages": [("LiFePO4 battery out", 35.0), ("48 V boost out", 32.1),
                         ("At crawler, 60 m", 30.8), ("Crawler loads", 28.0)],
              "losses": [(0, "Boost converter (8 %)", 2.9), (1, "Tether copper (4 %)", 1.3),
                         (2, "Buck converters (9 %)", 2.8)]},
    )
