"""CulvertCrawl product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a clear-anodized hull with filleted edges, a teal lid
on its lip with stainless screws, a pressure-test plug and a lit status light; lugged rubber tracks
over toothed sprockets and idlers with slotted side plates; a clear acrylic dome over the fisheye
camera; a black LED bezel with eight lit emitters; the clear laser boom with its cable, diode
housing, clear exit window around the cone mirror and end cap; the painted ballast skid plate with
countersunk bolts; and a ribbed bend restrictor at the tether gland. The surface kit has a painted
reel frame with a wound tether, lightened flanges, crank, slip ring and payout counter, and a
rugged control case with latches, handle, emergency stop, connectors and a gamepad on the lid.
Context is a short, cut-open section of 600 mm corrugated steel culvert on a patch of ground,
the projected laser ring on its wall (illustrative) and a 1.75 m clay mannequin standing at the
reel. APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS and track_contact_height() in model.py, with
each part rebuilt at the same placements as crawler_parts() and surface_parts(). Axes as
model.py's crawler frame: forward = +X, lateral = Y, up = Z, track contact line at Z = 0,
crawler centered on X = 0, Y = 0. The culvert runs along +X from its mouth at X = MOUTH_X, with its invert track_contact_height(600) below the contact line.
The surface kit is turned 180 degrees about Z so it stands outside the mouth (toward -X) and is
lowered onto the ground patch. The reel keeps model.py's position relative to the kit; for a
compact hero the control case is moved from beside the reel to the front left (CASE_SHIFT), a
render layout only. See docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parents[1] / ".kit"))

from build123d import (Axis, Box, Cone, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Torus,
                       Vector, extrude, fillet)
from model import PARAMS, track_contact_height

TITLE = "CulvertCrawl: tethered pipe inspection crawler with laser ring profiling"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); the crawler drives into "
             "a cut-open 600 mm culvert at right with the laser ring lit on the wall ahead, the tether runs "
             "back to the reel and control case at the mouth, with a 1.75 m person for scale"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view of the crawler from the front right and above (about 28 deg elevation): lid and "
             "screws, hull, electronics stack, worm gear motors, tracks and side plates, ballast skid plate, "
             "camera, dome, LED ring, laser boom and head, tether gland and bend restrictor"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 16, "az": -32,
     "note": "Detail of the crawler alone from the front right, slightly above (about 16 deg elevation): "
             "fisheye camera behind the clear dome, the lit LED ring, and the clear laser boom with the "
             "diode head and cone mirror window 300 mm ahead of the lens"},
]

P = PARAMS

# ---------------- colours (restrained product palette; kit accent) ----------------
C_ACCENT = "#0F766E"
C_HULL = "#B9C0C7"        # clear-anodized aluminium
C_DARK_AL = "#2B3036"     # black-anodized aluminium
C_RUBBER = "#1F2328"
C_SPROCKET = "#474D55"
C_STEEL_PAINT = "#3F454D"
C_SS = "#C9CED4"          # stainless fasteners
C_BLACK = "#1A1D21"
C_DOME = "#E4EFF5"
C_LED = "#FFF3D6"
C_PCB = "#166534"
C_PCB_DARK = "#1A1D21"
C_CHIP = "#111827"
C_MIRROR = "#E5E7EB"
C_CASE = "#33383E"
C_CASE_LID = "#3B4148"
C_RED = "#C81E1E"
C_YELLOW = "#E3B505"
C_CLAY = "#9CA3AF"
C_PIPE = "#AEB4BA"
C_GROUND = "#CFCBC3"
C_LASER = "#22C55E"
C_CELL = "#1E3A8A"

# ---------------- scene layout (render only; no dimension changes) ----------------
PIPE_ID = 600.0                          # design case culvert (docs/04-calcs)
PIPE_SHELL = 4.0                         # corrugated steel sheet, appearance only
CORR_PITCH = 68.0                        # annular corrugation pitch, appearance only
MOUTH_X = -150.0                         # culvert mouth; the crawler's rear is still outside
PIPE_END_X = 650.0                       # far end of the cut section (laser ring plane at 420 is inside)
TZ = track_contact_height(PIPE_ID)       # 12.3 mm: invert below the contact line
INVERT_Z = -TZ
PIPE_AXIS_Z = INVERT_Z + PIPE_ID / 2
GROUND_Z = INVERT_Z - PIPE_SHELL         # pipe and surface kit stand on this
REEL_X = MOUTH_X - 450.0                 # reel hub center (frame legs at +/-150 mm)
SURF_X0 = -REEL_X - 180.0                # surface_parts() x0 so that, turned 180 deg, the reel lands at REEL_X
PERSON_H = 1750.0
CASE_SHIFT = (96.0, -688.0)              # control case moved from model.py's spot beside the reel to the front left
PERSON_AT = (-706.0, -452.0)             # stands at the reel, between it and the control case
PERSON_TURN = 70.0                       # deg about Z from facing -Y, turned toward the culvert mouth
GROUND_TURN = 50.0                       # ground patch aligned with the hero view (az -40)
GROUND_UV = (-1400.0, 720.0, -700.0, 740.0)   # patch extent across (u) and into (d) the hero view


# ---------------- helpers ----------------
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _xcyl(r, length, x0, y=0.0, z=0.0):
    return Pos(x0 + length / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, length)


def _ycyl(r, length, x=0.0, y=0.0, z=0.0):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, length)


def _tube(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _surface(shape):
    """model.py surface-kit frame (x0 = SURF_X0) to the scene: turned 180 deg about Z, on the ground."""
    return Pos(0, 0, GROUND_Z) * Rot(0, 0, 180) * shape


def _hex_head(x, y, z, af=7.0, h=2.8, axis="z"):
    """Socket-head screw: round head with a hex socket; axis 'z' faces +Z, 'x+' faces +X, 'x-' faces -X."""
    head = Cylinder(af / 2, h)
    head = _fillet_try(head, head.faces().sort_by(Axis.Z)[-1].edges(), [0.6, 0.3])
    head -= Pos(0, 0, h / 2 - 0.6) * extrude(RegularPolygon(af * 0.22, 6), amount=1.2)
    if axis == "x+":
        head = Rot(0, 90, 0) * head
    elif axis == "x-":
        head = Rot(0, -90, 0) * head
    return Pos(x, y, z) * head


# ---------------- crawler ----------------
def _hull(p):
    """Body, lid and details of item 1, same envelope as model.py."""
    L, W, H, t, z0 = p["hull_l"], p["hull_w"], p["hull_h"], p["wall"], p["hull_z0"]
    lt, lip, cz = p["lid_t"], p["lid_lip"], p["cam_z"]
    body = Pos(0, 0, z0 + H / 2) * Box(L, W, H)
    body = _fillet_try(body, body.edges().filter_by(Axis.Z), [8.0, 5.0, 3.0])
    body = _fillet_try(body, body.faces().sort_by(Axis.Z)[0].edges(), [4.0, 2.5, 1.5])
    inner = Pos(0, 0, z0 + t + H / 2) * Box(L - 2 * t, W - 2 * t, H)
    inner = _fillet_try(inner, inner.edges().filter_by(Axis.Z), [4.0, 2.0])
    body -= inner
    # dome bore through the front wall so the camera shows through the dome
    body -= _xcyl(p["dome_r"] - 1.0, 3 * t, L / 2 - 2 * t, 0, cz)
    # side grooves (machined flutes) along both flanks: a restrained texture
    for sy in (-1, 1):
        for dz in (-10.0, 0.0, 10.0):
            body -= Pos(-10, sy * W / 2, z0 + H * 0.45 + dz) * Box(150, 1.6, 2.0)
    lid = Pos(0, 0, z0 + H + lt / 2) * Box(L + 2 * lip, W + 2 * lip, lt)
    lid = _fillet_try(lid, lid.edges().filter_by(Axis.Z), [9.0, 6.0, 3.0])
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.Z)[-1].edges(), [2.0, 1.2, 0.6])
    # shallow recessed name panel on the lid
    lid -= Pos(10, 0, z0 + H + lt - 0.4) * Box(120, 44, 1.0)
    screws = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (L / 2 - 8), sy * (W / 2 - 6)
            screws.append(_hex_head(x, y, z0 + H + lt + 1.5, af=7.0, h=3.0))
    screws = _union(screws)
    # name plate (raised, light) with an accent bar
    plate = Pos(10, 0, z0 + H + lt - 0.4 + 0.5) * Box(116, 40, 1.0)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Z), [3.0, 1.5])
    bar = Pos(-40, 0, z0 + H + lt + 0.4) * Box(8, 34, 0.6)
    # pressure-test port plug (hex) and status light on the rear of the lid
    plug = Pos(-L / 2 + 26, 0, z0 + H + lt + 2.0) * extrude(RegularPolygon(6.0, 6), amount=4.0, both=True)
    plug = Pos(0, 0, 0) * plug + Pos(-L / 2 + 26, 0, z0 + H + lt + 4.5) * Cylinder(3.5, 1.0)
    status_bezel = Pos(-L / 2 + 44, 0, z0 + H + lt + 0.6) * (Cylinder(4.5, 1.2) - Cylinder(2.6, 2.0))
    status = Pos(-L / 2 + 44, 0, z0 + H + lt + 0.9) * Sphere(2.6) & Pos(-L / 2 + 44, 0, z0 + H + lt + 3) * Box(8, 8, 4.2)
    # dome flange (bolted clamp ring) with six screws, same envelope as model.py
    flange = _xcyl(p["dome_r"] + 6, 5, L / 2, 0, cz) - _xcyl(p["dome_r"] - 1.0, 7, L / 2 - 1, 0, cz)
    flange = _fillet_try(flange, flange.faces().sort_by(Axis.X)[-1].edges(), [1.2, 0.6])
    # tether gland: hex body and dome nut, same position and size as model.py (r 8, 12 long)
    gx0 = -L / 2 - 12
    gland = Pos(gx0 + 4, 0, cz) * Rot(0, 90, 0) * extrude(RegularPolygon(9.0, 6), amount=4.0, both=True)
    gland += _xcyl(7.2, 8, gx0 - 0.5, 0, cz)
    gland = gland & _xcyl(9.5, 12.5, gx0 - 0.5, 0, cz)
    return body, lid, screws, plate, bar, plug, status_bezel, status, flange, gland


def _track_side(p, y):
    """One track module (item 2): lugged belt, sprocket (rear), idler (front), inner side plate."""
    tr, tx, tw = p["track_r"], p["track_x"], p["track_w"]
    lug_h, belt_t = 3.0, 5.0
    ro = tr - lug_h                           # belt outer surface
    ri = ro - belt_t                          # belt inner surface
    outer = Pos(0, y, tr) * Box(2 * tx, tw, 2 * ro) + _ycyl(ro, tw, -tx, y, tr) + _ycyl(ro, tw, tx, y, tr)
    inner = Pos(0, y, tr) * Box(2 * tx, tw + 2, 2 * ri) + _ycyl(ri, tw + 2, -tx, y, tr) + _ycyl(ri, tw + 2, tx, y, tr)
    belt = outer - inner
    lugs = []
    n_straight = 12
    for i in range(n_straight):
        x = -tx + (i + 0.5) * (2 * tx / n_straight)
        for z in (tr + ro + lug_h / 2, tr - ro - lug_h / 2):
            lugs.append(Pos(x, y, z) * Box(6.0, tw - 4, lug_h))
    for cx, a0 in ((tx, -90.0), (-tx, 90.0)):
        for k in range(1, 6):
            a = a0 + k * 30.0
            lug = Pos(0, 0, ro + lug_h / 2) * Box(6.0, tw - 4, lug_h)
            lugs.append(Pos(cx, y, tr) * Rot(0, a, 0) * lug)
    belt = belt + _union(lugs)
    # sprocket (rear, driven) and idler (front): wheels inside the belt with lightening holes
    wheels = []
    for cx, teeth in ((-tx, True), (tx, False)):
        w = _ycyl(ri, tw - 10, cx, y, tr)
        w -= _ycyl(ri - 4, tw - 16, cx, y, tr) - _ycyl(9, tw, cx, y, tr)   # dished web
        for k in range(5):
            a = math.radians(72 * k + 18)
            w -= _ycyl(4.5, tw, cx + 16 * math.cos(a), y, tr + 16 * math.sin(a))
        w += _ycyl(8, tw - 6, cx, y, tr)                                    # hub
        if teeth:
            for k in range(10):
                a = 36.0 * k
                w += Pos(cx, y, tr) * Rot(0, a, 0) * Pos(0, 0, ri - 1.5) * Box(4.0, tw - 12, 3.0)
        wheels.append(w & _ycyl(ri + 0.01, tw, cx, y, tr))
    wheels = _union(wheels)
    # outer hub caps with a bolt
    side_out = 1 if y > 0 else -1
    caps = []
    for cx in (-tx, tx):
        cap = _ycyl(10, 3, cx, y + side_out * (tw / 2 - 5 + 1.5), tr)
        caps.append(cap)
        caps.append(_ycyl(3.5, 2, cx, y + side_out * (tw / 2 - 5 + 4), tr))
    caps = _union(caps)
    # inner side plate as model.py (2 tx x 3 x 30) with slots and rounded ends
    side_in = -side_out
    py = y + side_in * (tw / 2 + 1.5)
    plate = Pos(0, py, tr) * Box(2 * tx, 3, 30)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Y), [8.0, 5.0])
    for x in (-50.0, 0.0, 50.0):
        plate -= Pos(x, py, tr) * Box(30, 5, 12)
    plate = _fillet_try(plate, [], [1.0])
    return belt, wheels, caps, plate


def _motors(p):
    """Item 3 as model.py, split into can, gearbox and shaft for colour."""
    tr, tx, tw = p["track_r"], p["track_x"], p["track_w"]
    gx, gy, gz = p["gearbox"]
    cans, gears, shafts = [], [], []
    for s in (1, -1):
        y = s * 20.0
        can = _xcyl(p["motor_r"], p["motor_len"], -tx + gx / 2 + 2, y, 52)
        can = _fillet_try(can, can.edges(), [2.0, 1.0])
        can += _xcyl(p["motor_r"] - 3, 4, -tx + gx / 2 + 2 + p["motor_len"], y, 52)   # end bell
        cans.append(can)
        gear = Pos(-tx, y, 52) * Box(gx, gy, gz)
        gear = _fillet_try(gear, gear.edges().filter_by(Axis.Y), [4.0, 2.0])
        gears.append(gear)
        shaft_len = p["track_y"] - abs(y) - tw / 2 + 12
        shafts.append(_ycyl(4, shaft_len, -tx, y + s * (gy / 2 + shaft_len / 2 - 4), tr))
    return _union(cans), _union(gears), _union(shafts)


def _electronics(p):
    """Item 4 inside the same three envelopes as model.py: carrier board, Pi 4 layer, converter block."""
    z0, t = p["hull_z0"], p["wall"]
    zb = z0 + t + 16 - 4                     # bottom of the 90 x 62 x 8 envelope
    pcb1 = Pos(30, 0, zb + 0.8) * Box(90, 62, 1.6)
    parts1 = (Pos(55, 15, zb + 1.6 + 2.5) * Box(14, 10, 5) + Pos(55, -15, zb + 1.6 + 2.5) * Box(14, 10, 5)   # driver ICs and sinks
              + Pos(10, 0, zb + 1.6 + 3) * Box(18, 40, 6) + Pos(30, 22, zb + 1.6 + 1) * Box(30, 6, 2))
    zp = z0 + t + 32 - 7                     # bottom of the 70 x 50 x 14 envelope
    pi = Pos(30, 0, zp + 0.8) * Box(70, 50, 1.6)
    pi_parts = (Pos(4, 12, zp + 1.6 + 6) * Box(16, 18, 12) + Pos(4, -10, zp + 1.6 + 6) * Box(16, 18, 12)   # USB and Ethernet
                + Pos(38, 0, zp + 1.6 + 1) * Box(14, 14, 2) + Pos(52, 16, zp + 1.6 + 4) * Box(20, 6, 8))       # SoC, header
    heatsink = Pos(38, 0, zp + 1.6 + 2) * Box(14, 14, 0.1)
    for k in range(5):
        heatsink += Pos(38 - 6 + 3 * k, 0, zp + 1.6 + 2 + 3) * Box(1.2, 14, 6)
    conv = Pos(-30, 0, z0 + t + 12) * Box(40, 30, 16)
    conv = _fillet_try(conv, conv.edges().filter_by(Axis.Z), [2.0, 1.0])
    for k in range(6):
        conv -= Pos(-30 - 12.5 + 5 * k, 0, z0 + t + 20) * Box(2.0, 24, 2.0)
    return pcb1 + pi, parts1 + pi_parts, heatsink, conv


def _front(p):
    """Items 5 and 6: camera module and lens, clear dome shell, LED bezel and emitters."""
    L, cz, dr = p["hull_l"], p["cam_z"], p["dome_r"]
    module = Pos(L / 2 - 22, 0, cz) * Box(20, 28, 28)
    module = _fillet_try(module, module.edges().filter_by(Axis.X), [2.0, 1.0])
    barrel = _xcyl(9.0, 16, L / 2 - 12, 0, cz) + _xcyl(11.0, 4, L / 2 - 12, 0, cz)
    barrel = _fillet_try(barrel, barrel.faces().sort_by(Axis.X)[-1].edges(), [1.0, 0.5])
    glass = _xcyl(6.5, 1.0, L / 2 + 4, 0, cz)
    dome = Pos(L / 2, 0, cz) * Rot(0, 90, 0) * (Sphere(dr, arc_size1=0, align=None) - Sphere(dr - 3, arc_size1=0, align=None))
    lo, li, lt = p["led_r_out"], p["led_r_in"], p["led_t"]
    x_led = L / 2 + 5
    bezel = _xcyl(lo, lt, x_led, 0, cz) - _xcyl(li, lt + 2, x_led - 1, 0, cz)
    bezel = _fillet_try(bezel, bezel.faces().sort_by(Axis.X)[-1].edges(), [1.5, 0.8])
    leds, lenses = [], []
    rm = (lo + li) / 2
    for k in range(8):
        a = math.radians(45 * k + 22.5)
        y, z = rm * math.cos(a), cz + rm * math.sin(a)
        bezel -= _xcyl(3.2, 2.0, x_led + lt - 1.0, y, z)
        leds.append(Pos(x_led + lt - 1.0, y, z) * Sphere(2.9) & _xcyl(4, 4, x_led + lt - 1.0, y, z))
    return module, barrel, glass, dome, bezel, _union(leds)


def _laser(p):
    """Item 7 with the model.py interfaces: clear boom from the dome apex, diode head, cone mirror."""
    L, cz = p["hull_l"], p["cam_z"]
    ring_x = L / 2 + p["ring_d"]
    x0 = L / 2 + p["dome_r"]
    hx0 = ring_x - p["head_l"]
    blen = hx0 - x0
    boom = _xcyl(p["boom_r"], blen, x0, 0, cz) - _xcyl(p["boom_r"] - 1.8, blen + 2, x0 - 1, 0, cz)
    cable = _xcyl(1.4, blen + 4, x0 - 1, 0, cz - 3.0)
    collar = _xcyl(p["boom_r"] + 2.5, 8, x0 - 2, 0, cz)          # clamp collar at the dome apex
    collar = _fillet_try(collar, collar.edges(), [1.0, 0.5])
    hr = p["head_r"]
    housing = _xcyl(hr, 14, hx0, 0, cz)
    housing = _fillet_try(housing, housing.faces().sort_by(Axis.X)[0].edges(), [2.0, 1.0])
    for k in range(4):
        housing -= _xcyl(hr + 1, 1.2, hx0 + 3 + 2.4 * k, 0, cz) - _xcyl(hr - 0.6, 3, hx0 + 2 + 2.4 * k, 0, cz)
    window = _xcyl(hr, 18, hx0 + 14, 0, cz) - _xcyl(hr - 1.5, 20, hx0 + 13, 0, cz)
    mirror = Pos(ring_x + 6, 0, cz) * Rot(0, -90, 0) * Cone(hr - 1.6, 1, 12)
    cap = _xcyl(hr, 3, hx0 + 32, 0, cz)
    cap = _fillet_try(cap, cap.faces().sort_by(Axis.X)[-1].edges(), [1.2, 0.6])
    return boom, cable, collar, housing, window, mirror, cap


def _ballast(p):
    bl, bw, bt = p["ballast"]
    z0 = p["ballast_z0"]
    plate = Pos(0, 0, z0 + bt / 2) * Box(bl, bw, bt)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Z), [6.0, 3.0])
    plate = _fillet_try(plate, plate.faces().sort_by(Axis.Z)[0].edges(), [2.0, 1.0])
    lip = Pos(bl / 2 + 6, 0, z0 + bt / 2 + 8) * Rot(0, -35, 0) * Box(20, bw, bt * 0.6)
    lip = _fillet_try(lip, lip.edges().filter_by(Axis.Y), [2.0, 1.0])
    plate = plate + lip
    # countersunk bolt heads flush in the underside, and two grooves across the skid face
    for sx in (-1, 1):
        for sy in (-1, 1):
            plate -= Pos(sx * (bl / 2 - 30), sy * (bw / 2 - 12), z0 + 0.5) * Cylinder(4.5, 1.2)
    for x in (-60.0, 60.0):
        plate -= Pos(x, 0, z0) * Box(3.0, bw + 2, 2.0)
    return plate


def _restrictor(p):
    """Item 9a: bend restrictor with ribs and the tether stub, same envelope as model.py."""
    L, cz = p["hull_l"], p["cam_z"]
    rx = -L / 2 - 12
    rl, rr, tod = p["relief_l"], p["relief_r"], p["tether_od"]
    boot = _xcyl(rr - 1.5, rl, rx - rl, 0, cz)
    for k in range(5):
        boot += _xcyl(rr, 3.0, rx - rl + 2 + 6 * k, 0, cz)
    boot += Pos(rx - rl - 8, 0, cz) * Rot(0, 90, 0) * Cone(tod / 2 + 1, rr, 16)
    stub = _xcyl(tod / 2, 20, rx - rl - 36, 0, cz)
    return boot, stub


# ---------------- surface kit ----------------
def _reel(p):
    """Item 10 at model.py sizes, in the model.py surface frame (x0 = SURF_X0)."""
    R, Wr, Zh = p["reel_r"], p["reel_w"], p["reel_hub_z"]
    rx = SURF_X0 + 180.0
    flanges = _ycyl(R, 6, rx, Wr / 2, Zh) + _ycyl(R, 6, rx, -Wr / 2, Zh)
    flanges = _fillet_try(flanges, flanges.edges(), [1.5, 0.8])
    for sy in (1, -1):
        for k in range(6):
            a = math.radians(60 * k)
            flanges -= _ycyl(18, 10, rx + 72 * math.cos(a), sy * Wr / 2, Zh + 72 * math.sin(a))
    drum = _ycyl(115, Wr - 6, rx, 0, Zh)
    wound = _ycyl(145, Wr - 6, rx, 0, Zh)
    for k in range(14):
        y = -Wr / 2 + 3 + 3.5 + 7.2 * k
        wound -= _ycyl(147, 0.9, rx, y, Zh) - _ycyl(143.5, 2, rx, y, Zh)
    frame = []
    for dy in (Wr / 2 + 12, -Wr / 2 - 12):
        for dx in (-150, 150):
            frame.append(_tube((rx + dx, dy, 0), (rx, dy, Zh), 10))
        frame.append(_ycyl(20, 8, rx, dy, Zh))                            # bearing boss
    frame.append(_tube((rx - 150, Wr / 2 + 12, 0), (rx - 150, -Wr / 2 - 12, 0), 10))
    frame.append(_tube((rx + 150, Wr / 2 + 12, 0), (rx + 150, -Wr / 2 - 12, 0), 10))
    # counter bracket from the leg to the payout counter (model.py leaves the counter unsupported)
    frame.append(_tube((rx - 118, -Wr / 2 - 12, 48), (rx - 190, -10, 128), 6))
    frame.append(_tube((rx - 118, Wr / 2 + 12, 48), (rx - 190, 10, 128), 6))
    frame = _union(frame)
    feet = _union([Pos(rx + dx, dy, 3) * Box(34, 34, 6) for dx in (-150, 150) for dy in (Wr / 2 + 12, -Wr / 2 - 12)])
    axle = _ycyl(12, Wr + 60, rx, 0, Zh)
    crank = _tube((rx, -Wr / 2 - 30, Zh), (rx + 90, -Wr / 2 - 30, Zh + 60), 7)
    knob = _ycyl(9, 50, rx + 90, -Wr / 2 - 55, Zh + 60)
    knob = _fillet_try(knob, knob.edges(), [3.0, 1.5])
    slip = _ycyl(22, 40, rx, Wr / 2 + 50, Zh)
    slip = _fillet_try(slip, slip.edges(), [2.0, 1.0])
    slip_cable = _tube((rx, Wr / 2 + 70, Zh), (rx, Wr / 2 + 90, Zh - 30), 3.0) + \
        _tube((rx, Wr / 2 + 90, Zh - 30), (rx + 60, Wr / 2 + 110, 40), 3.0)
    counter = Pos(rx - 190, 0, 150) * Box(60, 44, 50)
    counter = _fillet_try(counter, counter.edges(), [4.0, 2.0])
    wheel = _ycyl(25, 12, rx - 190, 0, 150 - 25 - 4) & Pos(rx - 190, 0, 100) * Box(60, 20, 40)
    readout = Pos(rx - 190, -22.3, 158) * Box(34, 1.0, 16)
    return flanges, drum, wound, frame, feet, axle, crank, knob, slip, slip_cable, counter, wheel, readout


def _case(p):
    """Item 11 and 12 at model.py sizes, in the model.py surface frame (x0 = SURF_X0)."""
    rx = SURF_X0 + 180.0
    bl, bw, bh = p["box"]
    bx = rx + 260
    cx = bx + bl / 2
    body = Pos(cx, 0, bh / 2) * Box(bl, bw, bh)
    body = _fillet_try(body, body.edges().filter_by(Axis.Z), [14.0, 8.0, 4.0])
    body = _fillet_try(body, body.faces().sort_by(Axis.Z)[0].edges(), [6.0, 3.0])
    body -= Pos(cx, 0, bh / 2 + 6) * Box(bl - 12, bw - 12, bh)
    body -= Pos(cx, -bw / 2, bh - 8) * Box(bl + 2, 1.6, 1.4)                 # parting groove front
    body -= Pos(cx, bw / 2, bh - 8) * Box(bl + 2, 1.6, 1.4)                  # parting groove back
    for k in range(4):                                                       # stacking ribs on the sides
        body -= Pos(cx - 120 + 80 * k, -bw / 2, bh / 2 - 20) * Box(6, 2.4, 80)
    lid = Pos(cx, 0, bh + 4) * Box(bl, bw, 8)
    lid = _fillet_try(lid, lid.edges().filter_by(Axis.Z), [14.0, 8.0, 4.0])
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 1.5])
    latches, hinges = [], []
    for dx in (-120, 120):
        latches.append(Pos(cx + dx, -bw / 2 - 3, bh - 10) * Box(44, 6, 30))
    latches = _fillet_try(_union(latches), [], [1.0])
    handle = _tube((cx - 70, 0, bh + 8), (cx - 60, 0, bh + 30), 5) + _tube((cx + 70, 0, bh + 8), (cx + 60, 0, bh + 30), 5) \
        + _tube((cx - 60, 0, bh + 30), (cx + 60, 0, bh + 30), 7)
    # internal battery and boost converter, as model.py
    battery = Pos(bx + 130, 0, 6 + 85) * Box(180, 175, 170)
    boost = Pos(bx + 300, 60, 36) * Box(110, 80, 60)
    # emergency stop (as model.py), fuse holders, tether and Ethernet connectors on the lid
    estop_base = Pos(bx + 330, -100, bh + 16) * Cylinder(22, 16)
    estop_base = _fillet_try(estop_base, estop_base.faces().sort_by(Axis.Z)[-1].edges(), [2.0, 1.0])
    estop = Pos(bx + 330, -100, bh + 30) * Cylinder(28, 12)
    estop = _fillet_try(estop, estop.faces().sort_by(Axis.Z)[-1].edges(), [5.0, 3.0, 1.5])
    connectors = _union([Pos(bx + 330, 40 + 45 * k, bh + 14) * Cylinder(12, 12) for k in range(2)]
                        + [Pos(bx + 270, 110, bh + 12) * Box(22, 30, 8)])
    fuses = _union([Pos(bx + 270, 40 + 30 * k, bh + 13) * Cylinder(8, 10) for k in range(2)])
    lamp = Pos(bx + 270, -30, bh + 10) * Sphere(6) & Pos(bx + 270, -30, bh + 14) * Box(14, 14, 8)
    # gamepad in the model.py envelope (150 x 95 x 28 on the lid)
    gx, gy, gz = bx + 150, -40, bh + 22
    pad = Pos(gx, gy, gz - 4) * Box(110, 60, 20)
    for sx in (-1, 1):
        pad += Pos(gx + sx * 50, gy - 12, gz - 4) * Cylinder(24, 20)
    pad = pad & Pos(gx, gy, gz) * Box(150, 95, 28)
    pad = _fillet_try(pad, pad.faces().sort_by(Axis.Z)[-1].edges(), [4.0, 2.0, 1.0])
    sticks = _union([Pos(gx + sx * 26, gy + 8, gz + 9) * Cylinder(7, 6) for sx in (-1, 1)])
    buttons = _union([Pos(gx + 44 + dx, gy + 14 + dy, gz + 7) * Cylinder(4, 2) for dx, dy in ((0, 8), (0, -8), (8, 0), (-8, 0))])
    return body, lid, latches, handle, battery, boost, estop_base, estop, connectors, fuses, lamp, pad, sticks, buttons


# ---------------- context ----------------
def _keep_open(shape):
    """Cut away the upper part of the culvert nearest the viewer (-Y) so the crawler shows; keep the invert."""
    keep = Pos(0, 2500, 0) * Box(10000, 5000, 10000) + Pos(0, 0, PIPE_AXIS_Z - 130 - 2500) * Box(10000, 10000, 5000)
    return shape & keep


def _culvert():
    ro = PIPE_ID / 2 + PIPE_SHELL
    length = PIPE_END_X - MOUTH_X
    shell = _xcyl(ro, length, MOUTH_X, 0, PIPE_AXIS_Z) - _xcyl(PIPE_ID / 2, length + 2, MOUTH_X - 1, 0, PIPE_AXIS_Z)
    rings = []
    x = MOUTH_X + 24.0
    while x < PIPE_END_X - 20:
        rings.append(Pos(x, 0, PIPE_AXIS_Z) * Rot(0, 90, 0) * Torus(PIPE_ID / 2 + 3.0, 6.0))
        x += CORR_PITCH
    pipe = shell + _union(rings)
    pipe = pipe - _xcyl(PIPE_ID / 2 + 20, 30, MOUTH_X - 30, 0, PIPE_AXIS_Z) \
        - _xcyl(PIPE_ID / 2 + 20, 30, PIPE_END_X, 0, PIPE_AXIS_Z)
    return _keep_open(pipe)


def _laser_line(p):
    ring_x = p["hull_l"] / 2 + p["ring_d"]
    ring = Pos(ring_x, 0, PIPE_AXIS_Z) * Rot(0, 90, 0) * Torus(PIPE_ID / 2 - 1.5, 1.6)
    return _keep_open(ring)


def _ground():
    u0, u1, d0, d1 = GROUND_UV
    a = math.radians(GROUND_TURN)
    uc, dc = (u0 + u1) / 2, (d0 + d1) / 2
    x = uc * math.cos(a) + dc * math.sin(a)
    y = uc * math.sin(a) - dc * math.cos(a)
    g = Box(u1 - u0, d1 - d0, 40)
    g = _fillet_try(g, g.edges().filter_by(Axis.Z), [80.0, 40.0])
    return Pos(x, y, GROUND_Z - 20) * Rot(0, 0, GROUND_TURN) * g


def _tether_route(p):
    """Item 9 from the crawler's tether stub along the invert, out of the mouth, over the counter to the drum."""
    L, cz = p["hull_l"], p["cam_z"]
    stub_end = -L / 2 - 12 - p["relief_l"] - 36
    rx = REEL_X
    pts = [(stub_end + 0.5, 0, cz), (stub_end - 60, 0, GROUND_Z + 22), (stub_end - 120, 0, GROUND_Z + 4),
           (rx + 300, 0, GROUND_Z + 4), (rx + 190 + 32, 0, GROUND_Z + 128), (rx + 158, 0, GROUND_Z + 128),
           (rx + 20, 0, GROUND_Z + p["reel_hub_z"] - 150)]
    segs = [_tube(a, b, p["tether_od"] / 2) for a, b in zip(pts[:-1], pts[1:])]
    segs += [Pos(*q) * Sphere(p["tether_od"] / 2) for q in pts[1:-1]]
    return _union(segs)


def _person():
    from context_parts import mannequin
    fig = mannequin(PERSON_H, "stand")
    return Pos(PERSON_AT[0], PERSON_AT[1], GROUND_Z) * Rot(0, 0, PERSON_TURN) * fig


# ---------------- assembly ----------------
def product_parts(p=PARAMS):
    out = []

    def case(shape):
        return Pos(CASE_SHIFT[0], CASE_SHIFT[1], 0) * _surface(shape)

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # crawler (items 1 to 9a)
    body, lid, screws, plate, bar, plug, sbezel, status, flange, gland = _hull(p)
    add("Hull body (clear anodized)", body, C_HULL, "metal", 1, "shell", (0, 0, 0))
    add("Hull lid (teal anodized)", lid, C_ACCENT, "metal", 1, "shell", (0, 0, 230))
    add("Lid screws (4)", screws, C_SS, "metal", 13, "shell", (0, 0, 280))
    add("Lid name plate", plate, "#E8EAED", "plastic", 1, "shell", (0, 0, 235))
    add("Name plate accent bar", bar, C_ACCENT, "painted", 1, "shell", (0, 0, 236))
    add("Pressure-test port plug", plug, C_SS, "metal", 1, "shell", (0, 0, 260))
    add("Status light bezel", sbezel, C_BLACK, "plastic", 1, "shell", (0, 0, 250))
    add("Status light (lit)", status, "#34D399", "emissive", 1, "shell", (0, 0, 250))
    add("Dome clamp flange", flange, C_DARK_AL, "metal", 1, "shell", (60, 0, 0))
    add("Tether gland", gland, C_BLACK, "plastic", 1, "shell", (-50, 0, 0))

    tr_parts = {}
    for side, y in (("left", p["track_y"]), ("right", -p["track_y"])):
        belt, wheels, caps, splate = _track_side(p, y)
        s = 1 if y > 0 else -1
        add(f"Track belt, {side}", belt, C_RUBBER, "rubber", 2, "shell", (0, s * 130, -20))
        add(f"Sprocket and idler, {side}", wheels, C_SPROCKET, "metal", 2, "shell", (0, s * 105, -20))
        add(f"Hub caps, {side}", caps, C_SS, "metal", 2, "shell", (0, s * 150, -20))
        add(f"Track side plate, {side}", splate, C_DARK_AL, "metal", 2, "shell", (0, s * 75, -20))

    cans, gears, shafts = _motors(p)
    add("Worm gear motor cans (2)", cans, "#9AA1A9", "metal", 3, "internal", (-30, 0, 120))
    add("Worm gearboxes (2)", gears, C_BLACK, "plastic", 3, "internal", (-30, 0, 120))
    add("Motor output shafts (2)", shafts, C_SS, "metal", 3, "internal", (-30, 0, 120))

    boards, comps, sink, conv = _electronics(p)
    add("Electronics boards", boards, C_PCB, "plastic", 4, "internal", (30, 0, 145))
    add("Electronics components", comps, C_CHIP, "plastic", 4, "internal", (30, 0, 145))
    add("Pi 4 heatsink", sink, C_SS, "metal", 4, "internal", (30, 0, 145))
    add("48 to 12 V converter", conv, "#2F3A48", "metal", 4, "internal", (0, 0, 135))

    module, barrel, glass, dome, bezel, leds = _front(p)
    add("Camera module", module, C_BLACK, "plastic", 5, "internal", (70, 0, 60))
    add("Fisheye lens barrel", barrel, "#23272C", "metal", 5, "internal", (80, 0, 60))
    add("Fisheye front element", glass, "#0B1220", "screen", 5, "internal", (80, 0, 60))
    add("Acrylic dome port", dome, C_DOME, "clear", 5, "shell", (120, 0, 0))
    add("LED ring bezel", bezel, C_BLACK, "plastic", 6, "shell", (95, 0, 0))
    add("LED emitters (8, lit)", leds, C_LED, "emissive", 6, "shell", (95, 0, 0))

    boom, cable, collar, housing, window, mirror, cap = _laser(p)
    add("Clear laser boom", boom, "#DCEEF5", "clear", 7, "shell", (160, 0, 0))
    add("Boom cable", cable, C_BLACK, "rubber", 7, "internal", (160, 0, 0))
    add("Boom collar", collar, C_DARK_AL, "metal", 7, "shell", (145, 0, 0))
    add("Laser diode housing", housing, C_DARK_AL, "metal", 7, "shell", (190, 0, 0))
    add("Laser exit window", window, "#DCEEF5", "clear", 7, "shell", (205, 0, 0))
    add("Cone mirror", mirror, C_MIRROR, "metal", 7, "internal", (205, 0, 0))
    add("Laser head end cap", cap, C_DARK_AL, "metal", 7, "shell", (225, 0, 0))

    add("Ballast skid plate", _ballast(p), C_STEEL_PAINT, "painted", 8, "shell", (0, 0, -150))

    boot, stub = _restrictor(p)
    add("Tether bend restrictor", boot, C_BLACK, "rubber", 9, "shell", (-95, 0, 0))
    add("Tether stub", stub, C_RUBBER, "rubber", 9, "shell", (-115, 0, 0))

    # surface kit (items 9 to 12): shown in the hero only
    add("Tether, routed to the reel", _tether_route(p), "#15181C", "rubber", 9, "accessory", (0, 0, 0))
    (flanges, drum, wound, frame, feet, axle, crank, knob, slip, slip_cable,
     counter, wheel, readout) = _reel(p)
    add("Reel flanges", _surface(flanges), "#3B4148", "painted", 10, "accessory", (0, 0, 0))
    add("Reel drum", _surface(drum), "#3B4148", "painted", 10, "accessory", (0, 0, 0))
    add("Wound tether", _surface(wound), "#15181C", "rubber", 9, "accessory", (0, 0, 0))
    add("Reel A-frame", _surface(frame), C_ACCENT, "painted", 10, "accessory", (0, 0, 0))
    add("Reel feet", _surface(feet), C_RUBBER, "rubber", 10, "accessory", (0, 0, 0))
    add("Reel axle", _surface(axle), C_SS, "metal", 10, "accessory", (0, 0, 0))
    add("Reel crank", _surface(crank), C_SS, "metal", 10, "accessory", (0, 0, 0))
    add("Crank knob", _surface(knob), C_BLACK, "plastic", 10, "accessory", (0, 0, 0))
    add("Slip ring", _surface(slip), "#9AA1A9", "metal", 10, "accessory", (0, 0, 0))
    add("Slip ring lead", _surface(slip_cable), "#15181C", "rubber", 10, "accessory", (0, 0, 0))
    add("Payout counter", _surface(counter), C_BLACK, "plastic", 10, "accessory", (0, 0, 0))
    add("Payout wheel", _surface(wheel), "#9AA1A9", "metal", 10, "accessory", (0, 0, 0))
    add("Payout readout (lit)", _surface(readout), "#5EEAD4", "emissive", 10, "accessory", (0, 0, 0))

    (cbody, clid, latches, handle, battery, boost, ebase, estop, conns, fuses, lamp,
     pad, sticks, buttons) = _case(p)
    add("Control case body", case(cbody), C_CASE, "plastic", 11, "accessory", (0, 0, 0))
    add("Control case lid", case(clid), C_CASE_LID, "plastic", 11, "accessory", (0, 0, 0))
    add("Case latches", case(latches), C_ACCENT, "plastic", 11, "accessory", (0, 0, 0))
    add("Case handle", case(handle), C_BLACK, "rubber", 11, "accessory", (0, 0, 0))
    add("LiFePO4 battery", case(battery), C_CELL, "painted", 11, "accessory", (0, 0, 0))
    add("48 V boost converter", case(boost), "#2F3A48", "metal", 11, "accessory", (0, 0, 0))
    add("Emergency stop base", case(ebase), C_YELLOW, "plastic", 11, "accessory", (0, 0, 0))
    add("Emergency stop", case(estop), C_RED, "plastic", 11, "accessory", (0, 0, 0))
    add("Tether and Ethernet connectors", case(conns), C_SS, "metal", 11, "accessory", (0, 0, 0))
    add("Fuse holders", case(fuses), C_BLACK, "plastic", 11, "accessory", (0, 0, 0))
    add("Tether power light (lit)", case(lamp), "#34D399", "emissive", 11, "accessory", (0, 0, 0))
    add("Operator gamepad", case(pad), "#23272C", "plastic", 12, "accessory", (0, 0, 0))
    add("Gamepad sticks", case(sticks), "#4B5563", "rubber", 12, "accessory", (0, 0, 0))
    add("Gamepad buttons", case(buttons), C_ACCENT, "plastic", 12, "accessory", (0, 0, 0))

    # context
    add("Culvert, 600 mm corrugated steel, cut open", _culvert(), C_PIPE, "metal", None, "context", (0, 0, 0))
    add("Laser ring on the pipe wall (illustrative)", _laser_line(p), C_LASER, "emissive", None, "context", (0, 0, 0))
    add("Ground at the culvert mouth", _ground(), C_GROUND, "painted", None, "context", (0, 0, 0))
    add("Person, 1.75 m mannequin (scale)", _person(), C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for q in product_parts():
        s = q["shape"]
        print(f"{q['name']:44s} {q['group']:9s} {q['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
