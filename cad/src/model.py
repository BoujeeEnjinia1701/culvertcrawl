"""CulvertCrawl parametric model (build123d), TRL 3, constructable design (CVC-DDR-003).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    culvertcrawl-crawler.step / .stl       crawler assembly (BOM lines 1 to 9, 14 and 15)
    culvertcrawl-surface-kit.step / .stl   tether reel, payout counter, surface control box, gamepad
                                           (BOM lines 10 to 12)
and prints the constructability checks (python cad/src/model.py --check prints them only).

Crawler frame (local): forward = +X, lateral = Y (+Y is the crawler's left side), up = Z;
the track contact line is Z = 0 and the hull is centred on X = 0, Y = 0. The camera optical centre
is the dome centre at X = hull_l / 2; the laser ring plane is ring_d ahead of it.

Revised 2026-09-30 under Amish's instruction to make the design physically buildable
(CVC-DDR-003, "Design for construction"). Every component is now a shape that can be machined,
cut, drilled, printed or bought, and every joint has a fixing:
    hull machined from a solid block, with a 12 mm rim inside the top for the lid O-ring and ten
    M4 lid screws, a 10 mm front wall bored for the camera, drive pads and idler bosses inside the
    side walls, and floor pads for the electronics tray;
    track belts narrowed to 36 mm (same outer edge) so a 3 mm side plate fits between hull and belt;
    each side plate is held by the two gearbox screws, the idler axle and three screws into the
    ballast plate, so the plates also tie the hull to the ballast;
    worm gear motors inside the hull with their output faces on the drive pads, shaft lip seals
    in the side walls, and the converter moved off the motors onto a deck above the Pi;
    front bezel ring clamping the dome flange on an O-ring, carrying eight potted LEDs;
    laser boom carried on a clear acrylic fin bolted to a bracket on the ballast plate front;
    laser head with a clear window and end cap that hold the cone mirror;
    ballast plate 250 x 88 x 14 mm with a bevelled nose and an eye bolt for the tether's strength
    member; tether penetrator raised clear of the gearboxes;
    tether reel with two aluminium side frames, bearings, a hollow axle, a drum clamped between
    flanges, a brake, a slip ring anchor and a payout counter bracket; surface box with a drop-in
    chassis (base board, posts, panel), so the bought case is not drilled.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (CVC-CAL-001), the drawing CVC-DWG-001 (cad/src/sheets.py), the concept
media (cad/src/concept_media.py) and the build plan pictures (cad/src/build_plan_media.py).
PRELIMINARY, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below. docs/04-calcs/sizing.py imports them.
PARAMS = {
    # hull (item 1): 6061 aluminium block, pocketed; bolted flush lid on an O-ring in the rim
    "hull_l": 240.0, "hull_w": 88.0, "hull_h": 74.0, "wall": 4.0, "lid_t": 6.0,
    "lid_lip": 0.0,             # the concept lid overhung 3 mm; it is now flush (CVC-DDR-003)
    "front_wall": 10.0,         # front wall, bored for the camera and tapped for the bezel
    "rim": (12.0, 10.0),        # inner rim at the top of the walls: width from the outside, depth
    "lid_screw_x": (-112.0, -56.0, 0.0, 56.0, 112.0), "lid_screw_in": 5.0,
    "oring_groove": (8.3, 10.7, 1.3),   # lid O-ring groove in the rim top: from the outer edge, depth
    "hull_z0": 22.0,            # hull bottom above the track contact line
    # tracks (item 2): 36 mm belts with the same outer edge as the concept's 40 mm belts
    "track_y": 67.0,            # belt centreline offset from the crawler axis (65 in the concept)
    "track_w": 36.0,            # belt width (40 in the concept)
    "track_r": 35.0,            # sprocket and idler radius over the belt
    "belt_t": 8.0,              # belt thickness (wheel radius under the belt 27)
    "track_x": 100.0,           # sprocket (rear) and idler (front) centres at -/+ track_x
    "side_plate": (-118.0, 112.0, 9.0, 62.0, 3.0),   # x0, x1, z0, z1, thickness (item 15)
    # motors (item 3): 5840-class worm gear motors; output shaft at the sprocket centre
    "motor_r": 16.0, "motor_len": 60.0, "gearbox": (46.0, 32.0, 40.0),
    "gearbox_x": (-114.0, -68.0), "gearbox_z": (27.0, 67.0), "motor_y": 18.0,
    "drive_pad_t": 6.0,         # pads inside the side walls under each gearbox face
    "shaft_r": 4.0, "seal": (16.0, 6.0),     # lip seal OD and counterbore depth
    "gb_screws": ((-108.0, 52.0), (-80.0, 52.0)),  # gearbox screws (x, z), M4 countersunk
    "ballast_screws_x": (-60.0, 0.0, 60.0), "ballast_screw_z": 15.0,
    # electronics (item 4) on a tray (item 15) on four floor pads
    "tray": (-4.0, 100.0, 31.0, 34.0, 2.0),   # x0, x1, half width, z0, thickness
    "tray_pads": ((4.0, 24.0), (92.0, 24.0)),
    # camera, dome and LED ring (items 5, 6) and the front bezel (item 14)
    "cam_z": 62.0,              # optical axis height above the track contact line
    "dome_r": 30.0, "dome_t": 3.0, "dome_flange": (36.0, 5.0), "dome_bore": 25.0,
    "bezel": (31.0, 44.0, 10.0),              # inner radius, outer radius, thickness
    "led_r_out": 44.0, "led_r_in": 32.0, "led_t": 8.0,   # LED ring envelope (kept for the renders)
    "led_pitch_r": 37.5, "led_board_d": 10.0,
    # laser ring projector (item 7)
    "ring_d": 300.0,            # ring plane ahead of the dome centre (CVC-DDR-002)
    "boom_r": 9.0, "boom_root": 157.0,   # boom root, x in the crawler frame
    "head_r": 13.0, "head_l": 26.0,
    "fin_t": 8.0,
    # ballast skid plate (item 8): steel; now 88 wide and extended to the rear for the eye bolt
    "ballast": (255.0, 88.0, 14.0), "ballast_x": (-140.0, 115.0), "ballast_z0": 8.0,
    # tether (item 9)
    "tether_od": 7.0, "tether_z": 77.0, "relief_l": 30.0, "relief_r": 11.0,
    # surface kit (items 10, 11)
    "reel_r": 160.0, "reel_w": 110.0, "reel_hub_z": 230.0, "drum_r": 112.5,
    "frame_y": 76.0, "frame_t": 6.0,
    "box": (410.0, 330.0, 175.0), "box_base_h": 140.0,
}

P = PARAMS


@dataclass
class Comp:
    name: str
    shape: object
    bom: int | None
    kind: str          # made, bought, fixing
    group: int | None  # exploded view / BOM callout this part belongs to


# ------------------------------------------------------------------ helpers
def _b():
    import build123d as b
    return b


def bx(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def xcyl(r, x0, x1, y=0.0, z=0.0):
    b = _b()
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, x1 - x0)


def ycyl(r, y0, y1, x=0.0, z=0.0):
    b = _b()
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, y1 - y0)


def zcyl(r, z0, z1, x=0.0, y=0.0):
    b = _b()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def xring(r0, r1, x0, x1, y=0.0, z=0.0):
    return xcyl(r1, x0, x1, y, z) - xcyl(r0, x0 - 1, x1 + 1, y, z)


def tube(a, c, r):
    b = _b()
    a = b.Vector(*a); c = b.Vector(*c); d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def xz_plate(pts, y0, t):
    """Flat plate with outline pts (x, z) lying from y0 to y0 + t."""
    b = _b()
    f = b.Plane.XZ * b.Polygon(*pts, align=None)
    return b.Pos(0, y0 + t, 0) * b.extrude(f, t)


def fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def derived(p=PARAMS):
    L, W, H, z0 = p["hull_l"], p["hull_w"], p["hull_h"], p["hull_z0"]
    return {
        "hull_top": z0 + H, "lid_top": z0 + H + p["lid_t"], "front": L / 2, "rear": -L / 2,
        "side": W / 2, "inner_side": W / 2 - p["wall"], "inner_front": L / 2 - p["front_wall"],
        "inner_rear": -L / 2 + p["wall"], "floor_top": z0 + p["wall"],
        "rim_z": z0 + H - p["rim"][1],
        "belt_in": p["track_y"] - p["track_w"] / 2, "belt_out": p["track_y"] + p["track_w"] / 2,
        "ring_x": L / 2 + p["ring_d"],
        "bezel_front": L / 2 + p["bezel"][2],
        "plate_out": W / 2 + p["side_plate"][4],
    }


# ------------------------------------------------------------------ crawler
def build_components(p=PARAMS):
    """Every crawler component as a Comp, keyed by a short name."""
    b = _b()
    D = derived(p)
    L, W, H, t, z0 = p["hull_l"], p["hull_w"], p["hull_h"], p["wall"], p["hull_z0"]
    zc = p["cam_z"]
    xf, xr = L / 2, -L / 2
    yi = D["inner_side"]
    ft = D["floor_top"]
    rz = D["rim_z"]
    C = {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    # ---- 1 hull body: block, pocket, rim, pads and bosses, holes
    body = bx(xr, xf, -W / 2, W / 2, z0, z0 + H)
    body -= bx(D["inner_rear"], D["inner_front"], -yi, yi, ft, z0 + H + 1)
    rw = p["rim"][0]
    rim = bx(xr, xf, -W / 2, W / 2, rz, z0 + H) - bx(xr + rw, xf - rw, -W / 2 + rw, W / 2 - rw, rz - 1, z0 + H + 1)
    body += rim
    gx0, gx1 = p["gearbox_x"]
    gz0, gz1 = p["gearbox_z"]
    pad = p["drive_pad_t"]
    for s in (1, -1):
        # drive pad under the gearbox face, idler boss, floor pads
        body += bx(gx0, gx1 - 2, s * yi - (pad if s > 0 else 0), s * yi + (0 if s > 0 else pad), ft - 0.01, gz1 + 1)
        body += ycyl(8.0, s * yi - (8 if s > 0 else 0), s * yi + (0 if s > 0 else 8), p["track_x"], p["track_r"])
    for x, y in p["tray_pads"]:
        for s in (1, -1):
            body += zcyl(5.0, ft - 0.01, p["tray"][3], x, s * y)
    # holes: shaft bore and seal counterbore, gearbox screws, idler tapped hole, ballast nothing
    sx_, sz_ = -p["track_x"], p["track_r"]
    body -= ycyl(p["shaft_r"] + 0.1, -60, 60, sx_, sz_)
    for s in (1, -1):
        so, sd = p["seal"]
        body -= ycyl(so / 2, s * (W / 2 - sd) if s > 0 else -W / 2 - 1, W / 2 + 1 if s > 0 else -W / 2 + sd, sx_, sz_)
        for gx, gz in p["gb_screws"]:
            body -= ycyl(2.25, (yi - pad - 0.5) if s > 0 else -W / 2 - 1, W / 2 + 1 if s > 0 else -(yi - pad - 0.5), gx, gz)
        body -= ycyl(3.0, (W / 2 - 10) if s > 0 else -W / 2 - 1, W / 2 + 1 if s > 0 else -(W / 2 - 10), p["track_x"], p["track_r"])
    # front wall: camera bore, dome O-ring groove, bezel screw holes, potted lead hole, camera mount holes
    body -= xcyl(p["dome_bore"], D["inner_front"] - 1, xf + 1, 0, zc)
    body -= xring(28.0, 30.4, xf - 1.3, xf + 1, 0, zc)
    k = 40.0 / math.sqrt(2)
    for sy in (1, -1):
        for sz in (1, -1):
            body -= xcyl(2.0, xf - 7, xf + 1, sy * k, zc + sz * k)
            body -= xcyl(1.5, D["inner_front"] - 1, D["inner_front"] + 6, sy * 20, zc + sz * 20)
    body -= xcyl(2.5, D["inner_front"] - 1, xf + 1, -36.0, 29.0)
    # rear wall: tether penetrator; rim top: O-ring groove and lid screw holes
    body -= xcyl(5.1, xr - 1, D["inner_rear"] + 1, 0, p["tether_z"])
    g0, g1, gd = p["oring_groove"]
    groove = bx(xr + g0, xf - g0, -W / 2 + g0, W / 2 - g0, z0 + H - gd, z0 + H + 1) - \
        bx(xr + g1, xf - g1, -W / 2 + g1, W / 2 - g1, z0 + H - gd - 1, z0 + H + 2)
    body -= groove
    for x in p["lid_screw_x"]:
        for s in (1, -1):
            body -= zcyl(2.0, z0 + H - 8, z0 + H + 1, x, s * (W / 2 - p["lid_screw_in"]))
    add("body", "Hull body", body, 1, "made", 1)

    # ---- 1 lid, screws, pressure-test plug, tether penetrator
    lid = bx(xr, xf, -W / 2, W / 2, z0 + H, z0 + H + p["lid_t"])
    heads = []
    for x in p["lid_screw_x"]:
        for s in (1, -1):
            y = s * (W / 2 - p["lid_screw_in"])
            lid -= zcyl(2.25, z0 + H - 1, z0 + H + p["lid_t"] + 1, x, y)
            heads.append(zcyl(3.5, z0 + H + p["lid_t"], z0 + H + p["lid_t"] + 2.8, x, y) + zcyl(2.0, z0 + H - 7, z0 + H + p["lid_t"], x, y))
    lid -= zcyl(4.25, z0 + H - 1, z0 + H + p["lid_t"] + 1, -90, 0)
    add("lid", "Hull lid", lid, 1, "made", 1)
    add("lid_screws", "Lid screws, M4 (10)", fuse(heads), 13, "fixing", 1)
    plug = zcyl(4.25, z0 + H + 0.5, z0 + H + p["lid_t"], -90, 0) + zcyl(6.0, z0 + H + p["lid_t"], z0 + H + p["lid_t"] + 2.5, -90, 0)
    add("plug", "Pressure-test plug", plug, 1, "bought", 1)
    tz = p["tether_z"]
    pen = xcyl(5.0, xr - 12, D["inner_rear"] + 8, 0, tz) + xcyl(9.5, xr - 3, xr, 0, tz) + xcyl(8.0, xr - 12, xr - 3, 0, tz) \
        + xcyl(8.0, D["inner_rear"], D["inner_rear"] + 6, 0, tz)
    add("penetrator", "Tether penetrator (M10, IP68)", pen, 1, "bought", 1)

    # ---- 8 ballast plate: steel, bevelled nose, tapped sides, eye bolt hole at the rear
    bl, bw, bt = p["ballast"]
    bx0, bx1 = p["ballast_x"]
    bz0 = p["ballast_z0"]
    bal = bx(bx0, bx1, -bw / 2, bw / 2, bz0, bz0 + bt)
    for x in p["ballast_screws_x"]:
        for s in (1, -1):
            bal -= ycyl(2.0, (bw / 2 - 10) if s > 0 else -bw / 2 - 1, bw / 2 + 1 if s > 0 else -(bw / 2 - 10), x, p["ballast_screw_z"])
    ex = bx0 + 9
    bal -= zcyl(4.0, bz0 - 1, bz0 + bt + 1, ex, 0)                      # eye bolt, tapped M8 through
    for y in (6.0, 16.0):
        bal -= xcyl(2.0, bx1 - 8, bx1 + 1, y, bz0 + 4.5)                # fin bracket screws, tapped M4
    add("ballast", "Ballast skid plate", bal, 8, "made", 8)
    eye = zcyl(4.0, bz0, bz0 + bt + 2, ex, 0) + zcyl(9.0, bz0 + bt, bz0 + bt + 4, ex, 0)
    eye += b.Pos(ex, 0, bz0 + bt + 16) * b.Rot(0, 90, 0) * b.Torus(9.0, 3.2)
    add("eyebolt", "Eye bolt for the tether's strength member, M8", eye, 13, "bought", 9)

    # ---- 15 side plates (pair): 3 mm aluminium, flat on the hull sides and ballast sides
    sx0, sx1, sz0, sz1, st = p["side_plate"]
    plates, pfix = [], []
    for s in (1, -1):
        y0 = W / 2 if s > 0 else -W / 2 - st
        pl = bx(sx0, sx1, y0, y0 + st, sz0, sz1)
        yo_ = y0 + st if s > 0 else y0                  # outer face of the plate
        cb = (yo_ - 2, yo_ + 1) if s > 0 else (yo_ - 1, yo_ + 2)
        pl -= ycyl(5.0, y0 - 1, y0 + st + 1, sx_, sz_)
        pts = list(p["gb_screws"]) + [(x, p["ballast_screw_z"]) for x in p["ballast_screws_x"]]
        for gx, gz in pts:
            pl -= ycyl(2.25, y0 - 1, y0 + st + 1, gx, gz)
            pl -= ycyl(3.6, cb[0], cb[1], gx, gz)       # countersink, drawn as a 2 mm counterbore
            inner = (yi - pad - 8) if (gx, gz) in p["gb_screws"] else (bw / 2 - 8)
            sh = ycyl(2.0, inner, yo_ - 2, gx, gz) if s > 0 else ycyl(2.0, yo_ + 2, -inner, gx, gz)
            hd = ycyl(3.6, yo_ - 2, yo_, gx, gz) if s > 0 else ycyl(3.6, yo_, yo_ + 2, gx, gz)
            pfix.append(sh + hd)
        pl -= ycyl(3.2, y0 - 1, y0 + st + 1, p["track_x"], p["track_r"])
        plates.append(pl)
    add("plate_r", "Side plate, left", plates[0], 15, "made", 2)
    add("plate_l", "Side plate, right", plates[1], 15, "made", 2)
    add("plate_screws", "Side plate screws, M4 countersunk (10)", fuse(pfix), 13, "fixing", 2)

    # ---- 2 tracks: belts (loops), sprocket on the motor shaft, idler on its axle bolt
    tr, tx, tw, btk = p["track_r"], p["track_x"], p["track_w"], p["belt_t"]
    belts, wheels, axles = [], [], []
    for s in (1, -1):
        y0, y1 = D["belt_in"], D["belt_out"]
        if s < 0:
            y0, y1 = -y1, -y0
        outer = bx(-tx, tx, y0, y1, 0, 2 * tr) + ycyl(tr, y0, y1, -tx, tr) + ycyl(tr, y0, y1, tx, tr)
        inner = bx(-tx, tx, y0 - 1, y1 + 1, btk, 2 * tr - btk) + ycyl(tr - btk, y0 - 1, y1 + 1, -tx, tr) + ycyl(tr - btk, y0 - 1, y1 + 1, tx, tr)
        belts.append(outer - inner)
        for x in (-tx, tx):
            w = ycyl(tr - btk, y0 + 1, y1 - 1, x, tr)
            if x < 0:
                w -= ycyl(p["shaft_r"], y0, y1, x, tr)
            else:
                w -= ycyl(3.0, y0, y1, x, tr)
                w -= ycyl(5.5, (y1 - 5) if s > 0 else y0 - 1, y1 + 1 if s > 0 else y0 + 5, x, tr)
            wheels.append(w)
        # idler axle: M6 shoulder bolt, head recessed in the idler hub, threaded into the hull boss
        a0, a1 = (W / 2 - 10, y1 - 5) if s > 0 else (y0 + 5, -(W / 2 - 10))
        ax = ycyl(3.0, a0, a1, tx, tr) + (ycyl(5.0, y1 - 5, y1 - 1, tx, tr) if s > 0 else ycyl(5.0, y0 + 1, y0 + 5, tx, tr))
        axles.append(ax)
    add("belts", "Track belts (2)", fuse(belts), 2, "bought", 2)
    add("wheels", "Sprockets and idlers (4)", fuse(wheels), 2, "bought", 2)
    add("idler_axles", "Idler axle bolts, M6 shoulder (2)", fuse(axles), 2, "fixing", 2)

    # ---- 3 worm gear motors: gearbox on the drive pad, can forward, shaft through the seal
    gb, cans, shafts = [], [], []
    for s in (1, -1):
        yo = s * (yi - pad)                     # output face of the gearbox
        y0, y1 = (yo - p["gearbox"][1], yo) if s > 0 else (yo, yo + p["gearbox"][1])
        g = bx(gx0, gx1, y0, y1, gz0, gz1)
        for gx, gz in p["gb_screws"]:
            g -= ycyl(2.0, (yo - 8) if s > 0 else yo - 1, yo + 1 if s > 0 else yo + 8, gx, gz)
        gb.append(g)
        cans.append(xcyl(p["motor_r"], gx1, gx1 + p["motor_len"], s * p["motor_y"], 52.0))
        sh_end = D["belt_out"] - 13
        shafts.append(ycyl(p["shaft_r"], yo, sh_end, sx_, sz_) if s > 0 else ycyl(p["shaft_r"], -sh_end, yo, sx_, sz_))
    seals = []
    for s in (1, -1):
        so, sd = p["seal"]
        a, c = (W / 2 - 5, W / 2) if s > 0 else (-W / 2, -W / 2 + 5)
        seals.append(ycyl(so / 2, a, c, sx_, sz_) - ycyl(p["shaft_r"], a - 1, c + 1, sx_, sz_))
    add("gearboxes", "Worm gearboxes (2)", fuse(gb), 3, "bought", 3)
    add("cans", "Motor cans (2)", fuse(cans), 3, "bought", 3)
    add("shafts", "Output shafts, 8 mm (2)", fuse(shafts), 3, "bought", 3)
    add("seals", "Shaft lip seals, 8 x 16 x 5 (2)", fuse(seals), 3, "bought", 3)

    # ---- 15 electronics tray on the floor pads; 4 Pi, deck and modules
    tx0, tx1, thw, tz0, tth = p["tray"]
    tray = bx(tx0, tx1, -thw, thw, tz0, tz0 + tth)
    for x, y in p["tray_pads"]:
        for s in (1, -1):
            tray -= zcyl(1.7, tz0 - 1, tz0 + tth + 1, x, s * y)
    holes = [(5.5, 24.5), (63.5, 24.5)]
    for x, y in holes:
        for s in (1, -1):
            tray -= zcyl(1.35, tz0 - 1, tz0 + tth + 1, x, s * y)
    add("tray", "Electronics tray", tray, 15, "made", 4)
    ez = tz0 + tth
    pi = bx(2, 87, -28, 28, ez + 4, ez + 5.6)
    spacers = fuse([zcyl(2.5, ez, ez + 4, x, s * y) for x, y in holes for s in (1, -1)])
    pi_parts = bx(18, 58, -18, 18, ez + 5.6, ez + 18) + bx(67, 87, -26, 26, ez + 5.6, ez + 22)
    standoffs = fuse([zcyl(2.5, ez + 5.6, ez + 26, x, s * y) for x, y in holes for s in (1, -1)])
    deck = bx(2, 70, -28, 28, ez + 26, ez + 28)
    for x, y in holes:
        for s in (1, -1):
            deck -= zcyl(1.35, ez + 25, ez + 29, x, s * y)
    mods = bx(6, 46, -15, 15, ez + 28, ez + 44) + bx(50, 68, -20, 20, ez + 28, ez + 38)
    add("pi", "Raspberry Pi 4", pi + pi_parts + spacers, 4, "bought", 4)
    add("deck", "Deck with motor driver, converters and IMU", deck + mods + standoffs, 4, "bought", 4)

    # ---- 5 camera mount (printed), camera board, lens; dome
    fi = D["inner_front"]
    mount = bx(fi - 4, fi, -28, 28, zc - 24, zc + 24) - xcyl(8.0, fi - 5, fi + 1, 0, zc)
    for sy in (1, -1):
        for sz in (1, -1):
            mount -= xcyl(1.7, fi - 5, fi + 1, sy * 20, zc + sz * 20)
    cam_board = bx(fi - 18, fi - 6, -14, 14, zc - 14, zc + 14)
    cam_post = fuse([xcyl(2.0, fi - 6, fi - 4, sy * 10, zc + sz * 10) for sy in (1, -1) for sz in (1, -1)])
    lens = xcyl(7.0, fi - 6, xf - 2, 0, zc)
    add("cam_mount", "Camera mount", mount, 15, "made", 5)
    add("camera", "Camera board and fisheye lens", cam_board + cam_post + lens, 5, "bought", 5)
    dr, dt = p["dome_r"], p["dome_t"]
    sph = (b.Pos(xf, 0, zc) * b.Sphere(dr) - b.Pos(xf, 0, zc) * b.Sphere(dr - dt)) & bx(xf, xf + dr + 1, -dr - 1, dr + 1, zc - dr - 1, zc + dr + 1)
    fr, ft_ = p["dome_flange"]
    dome = sph + xring(dr - dt, fr, xf, xf + ft_, 0, zc)
    add("dome", "Acrylic dome port", dome, 5, "bought", 5)

    # ---- 14 front bezel: clamps the dome flange, holds eight LEDs
    br0, br1, bth = p["bezel"]
    bez = xring(br0, br1, xf, xf + bth, 0, zc) - xcyl(fr + 0.5, xf - 1, xf + ft_, 0, zc)
    led_pts = []
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        y, z = p["led_pitch_r"] * math.sin(a), zc + p["led_pitch_r"] * math.cos(a)
        led_pts.append((y, z))
        bez -= xcyl(p["led_board_d"] / 2 + 0.25, xf + bth - 3, xf + bth + 1, y, z)
    bscrews = []
    for sy in (1, -1):
        for sz in (1, -1):
            bez -= xcyl(2.25, xf - 1, xf + bth + 1, sy * k, zc + sz * k)
            bscrews.append(xcyl(2.0, xf - 6, xf + bth, sy * k, zc + sz * k) + xcyl(3.5, xf + bth, xf + bth + 2.8, sy * k, zc + sz * k))
    add("bezel", "Front bezel", bez, 14, "made", 6)
    add("bezel_screws", "Bezel screws, M4 (4)", fuse(bscrews), 13, "fixing", 6)
    leds = fuse([xcyl(p["led_board_d"] / 2, xf + bth - 3, xf + bth - 1.4, y, z) + xcyl(2.5, xf + bth - 1.4, xf + bth - 0.2, y, z) for y, z in led_pts])
    add("leds", "LEDs on 10 mm boards (8), potted", leds, 6, "bought", 6)

    # ---- 7 laser projector: fin bracket, fin, boom, diode housing, window, mirror, end cap
    rx_ = D["ring_x"]
    fb = bx(bx1, bx1 + 3, -3, 27, bz0, bz0 + 9) + bx(bx1, bx1 + 30, -3, 0, bz0, bz0 + 9)
    for y in (6.0, 16.0):
        fb -= xcyl(2.25, bx1 - 1, bx1 + 4, y, bz0 + 4.5)
    for x in (bx1 + 20, bx1 + 26):
        fb -= ycyl(1.5, -4, 1, x, bz0 + 4.5)
    add("fin_bracket", "Fin bracket", fb, 15, "made", 7)
    fbs = fuse([xcyl(2.0, bx1 - 8, bx1 + 3, y, bz0 + 4.5) + xcyl(3.5, bx1 + 3, bx1 + 5.5, y, bz0 + 4.5) for y in (6.0, 16.0)]
               + [ycyl(1.5, -3, p["fin_t"], x, bz0 + 4.5) + ycyl(2.8, p["fin_t"], p["fin_t"] + 2.4, x, bz0 + 4.5) + ycyl(3.2, -5.4, -3, x, bz0 + 4.5)
                  for x in (bx1 + 20, bx1 + 26)])
    add("fin_screws", "Fin bracket screws, M4 (2) and M3 (2)", fbs, 13, "fixing", 7)
    br_ = p["boom_r"]
    root = p["boom_root"]
    zb = zc - br_
    fin_pts = [(xf + bth + 1, bz0), (bx1 + 30, bz0), (root + 105, zb), (root + 2, zb), (xf + bth + 1, 25.0)]
    fin = b.Pos(0, p["fin_t"], 0) * xz_plate(fin_pts, -p["fin_t"], p["fin_t"])
    for x in (bx1 + 20, bx1 + 26):
        fin -= ycyl(1.5, -1, p["fin_t"] + 1, x, bz0 + 4.5)
    add("fin", "Boom fin (clear acrylic)", fin, 7, "made", 7)
    hx0 = rx_ - 40                                  # diode housing from 40 mm behind the ring plane
    boom = xcyl(br_, root, hx0 + 10, 0, zc) - xcyl(br_ - 3, root + 3, hx0 + 11, 0, zc)
    add("boom", "Boom tube (clear acrylic)", boom, 7, "made", 7)
    hr = p["head_r"]
    housing = xcyl(hr, hx0, rx_ - 10, 0, zc) - xcyl(br_, hx0 - 1, hx0 + 10, 0, zc) - xcyl(6.0, hx0 + 10, rx_ - 9, 0, zc)
    housing -= xcyl(11.0, rx_ - 14, rx_ - 9, 0, zc)
    add("housing", "Diode housing", housing, 7, "made", 7)
    diode = xcyl(6.0, hx0 + 12, rx_ - 15, 0, zc)
    add("diode", "Laser diode module, Class 2", diode, 7, "bought", 7)
    window = xcyl(hr, rx_ - 10, rx_ + 10, 0, zc) - xcyl(hr - 2, rx_ - 11, rx_ + 11, 0, zc)
    window += xring(hr - 4, hr - 2, rx_ - 14, rx_ - 10, 0, zc)        # spigot into the housing
    add("window", "Window tube (clear acrylic)", window, 7, "made", 7)
    mirror = b.Pos(rx_ + 1, 0, zc) * b.Rot(0, -90, 0) * b.Cone(10.0, 0.5, 10.0) + xcyl(6.0, rx_ + 6, rx_ + 10, 0, zc)
    add("mirror", "Cone mirror, 90 degrees", mirror, 7, "bought", 7)
    cap = xcyl(hr, rx_ + 10, rx_ + 13, 0, zc) + xring(hr - 4, hr - 2, rx_ + 6, rx_ + 10, 0, zc)
    add("cap", "End cap", cap, 7, "made", 7)

    # ---- 9 tether strain relief and stub, from the penetrator rearward
    rxe = xr - 12
    relief = xcyl(p["relief_r"], rxe - p["relief_l"], rxe, 0, tz) \
        + b.Pos(rxe - p["relief_l"] - 8, 0, tz) * b.Rot(0, 90, 0) * b.Cone(p["tether_od"] / 2 + 1, p["relief_r"], 16) \
        + xcyl(p["tether_od"] / 2, rxe - p["relief_l"] - 36, rxe - p["relief_l"] - 16, 0, tz)
    add("relief", "Tether strain relief (tether stub)", relief, 9, "bought", 9)
    return C


def crawler_parts(p=PARAMS) -> dict:
    """Crawler parts grouped by exploded-view callout: {n: (name, shape)}."""
    C = build_components(p)
    names = {1: "Sealed hull and lid", 2: "Track modules and side plates", 3: "Worm gear motors (2)",
             4: "Electronics tray, Pi 4 and deck", 5: "Fisheye camera, mount and dome port", 6: "Front bezel with LED ring",
             7: "Laser ring projector on fin and boom", 8: "Ballast skid plate", 9: "Tether strain relief and eye bolt"}
    out = {}
    for c in C.values():
        g = c.group
        out[g] = c.shape if g not in out else out[g] + c.shape
    return {g: (names[g], out[g]) for g in sorted(out)}


# ------------------------------------------------------------------ surface kit
def build_surface(p=PARAMS, x0=0.0):
    """Tether reel, payout counter, surface control box and gamepad, standing on Z = 0, along +X from x0."""
    b = _b()
    C = {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    R, Wr, Zh, dr = p["reel_r"], p["reel_w"], p["reel_hub_z"], p["drum_r"]
    rx = x0 + 180.0
    fy, ft = p["frame_y"], p["frame_t"]
    # side frames: 6 mm aluminium plates in the X-Z plane, with a lightening window
    outline = [(rx - 160, 0), (rx + 160, 0), (rx + 160, 30), (rx + 40, Zh + 32), (rx - 40, Zh + 32), (rx - 160, 30)]
    frames = []
    for s in (1, -1):
        y0 = fy if s > 0 else -fy - ft
        f = xz_plate(outline, y0, ft)
        f -= xz_plate([(rx - 95, 45), (rx + 95, 45), (rx, Zh - 75)], y0 - 1, ft + 2)
        f -= ycyl(10.5, y0 - 1, y0 + ft + 1, rx, Zh)
        for x, z in ((rx - 130, 18), (rx + 130, 18), (rx, 30)):
            f -= ycyl(3.2, y0 - 1, y0 + ft + 1, x, z)
        for dz in (-27, 27):
            f -= ycyl(4.2, y0 - 1, y0 + ft + 1, rx, Zh + dz)
        if s > 0:
            f -= ycyl(2.75, y0 - 1, y0 + ft + 1, rx, Zh - 55)          # slip ring anchor bolt
        else:
            f -= ycyl(4.0, y0 - 1, y0 + ft + 1, rx - 100, Zh - 100)    # brake screw, tapped M8
        frames.append(f)
    add("frame_r", "Reel side frame, right", frames[0], 10, "made", 10)
    add("frame_l", "Reel side frame, left", frames[1], 10, "made", 10)
    # spacer tubes on M6 tie rods: rear foot, front foot (split for the counter bar), bottom centre
    sp = [ycyl(10, -fy, fy, rx + 130, 18) - ycyl(3.2, -fy - 1, fy + 1, rx + 130, 18),
          ycyl(10, -fy, fy, rx, 30) - ycyl(3.2, -fy - 1, fy + 1, rx, 30),
          ycyl(10, -fy, -12.5, rx - 130, 18) - ycyl(3.2, -fy - 1, 0, rx - 130, 18),
          ycyl(10, 12.5, fy, rx - 130, 18) - ycyl(3.2, 0, fy + 1, rx - 130, 18)]
    add("spacers", "Frame spacer tubes (4)", fuse(sp), 10, "made", 10)
    rods = fuse([ycyl(3.0, -fy - ft - 6, fy + ft + 6, x, z) for x, z in ((rx + 130, 18), (rx, 30), (rx - 130, 18))])
    add("frame_rods", "Frame tie rods, M6, with nuts (3)", rods, 13, "fixing", 10)
    # drum (PVC pipe) clamped between two flanges by four tie rods; flange hubs on the axle
    drum = ycyl(dr, -Wr / 2 + 3, Wr / 2 - 3, rx, Zh) - ycyl(dr - 5.5, -Wr / 2, Wr / 2, rx, Zh)
    drum -= b.Pos(rx, 0, Zh - dr + 2) * b.Box(10, 10, 12)                    # tether entry hole
    add("drum", "Reel drum", drum, 10, "made", 10)
    fl = []
    for s in (1, -1):
        a, c = (Wr / 2 - 3, Wr / 2 + 3) if s > 0 else (-Wr / 2 - 3, -Wr / 2 + 3)
        f = ycyl(R, a, c, rx, Zh) - ycyl(10.2, a - 1, c + 1, rx, Zh)
        for i in range(4):
            ang = math.radians(45 + 90 * i)
            f -= ycyl(3.2, a - 1, c + 1, rx + 100 * math.cos(ang), Zh + 100 * math.sin(ang))
            f -= ycyl(2.75, a - 1, c + 1, rx + 19 * math.cos(ang), Zh + 19 * math.sin(ang))
        fl.append(f)
    add("flanges", "Reel flanges (2)", fuse(fl), 10, "made", 10)
    trods = fuse([ycyl(3.0, -Wr / 2 - 8, Wr / 2 + 8, rx + 100 * math.cos(math.radians(45 + 90 * i)), Zh + 100 * math.sin(math.radians(45 + 90 * i)))
                  for i in range(4)])
    add("drum_rods", "Drum tie rods, M6, with nuts (4)", trods, 13, "fixing", 10)
    hubs = fuse([(ycyl(25, Wr / 2 + 3, Wr / 2 + 8, rx, Zh) + ycyl(15, Wr / 2 + 8, Wr / 2 + 18, rx, Zh) - ycyl(10.0, 0, 100, rx, Zh)),
                 (ycyl(25, -Wr / 2 - 8, -Wr / 2 - 3, rx, Zh) + ycyl(15, -Wr / 2 - 18, -Wr / 2 - 8, rx, Zh) - ycyl(10.0, -100, 0, rx, Zh))])
    add("hubs", "Flange shaft hubs, 20 mm (2)", hubs, 10, "bought", 10)
    axle = ycyl(10, -fy - ft - 26, fy + ft + 18, rx, Zh) - ycyl(7, -fy - ft - 30, fy + ft + 20, rx, Zh)
    add("axle", "Hollow axle, 20 mm tube", axle, 10, "bought", 10)
    brg = []
    for s in (1, -1):
        a, c = (fy + ft, fy + ft + 12) if s > 0 else (-fy - ft - 12, -fy - ft)
        h = ycyl(24, a, c, rx, Zh) + bx(rx - 10, rx + 10, a, c, Zh - 36, Zh + 36) - ycyl(10.0, a - 1, c + 1, rx, Zh)
        for dz in (-27, 27):
            h -= ycyl(4.2, a - 1, c + 1, rx, Zh + dz)
        brg.append(h)
    add("bearings", "Flanged bearings, 20 mm bore (2)", fuse(brg), 10, "bought", 10)
    bb = fuse([ycyl(4.0, (-fy - ft - 18) if s < 0 else fy - 2, (-fy + 2) if s < 0 else fy + ft + 18, rx, Zh + dz) for s in (1, -1) for dz in (-27, 27)])
    add("bearing_bolts", "Bearing bolts, M8 (4)", bb, 13, "fixing", 10)
    # crank (left), brake (left, lower front of the flange), slip ring and its anchor (right)
    yc = -fy - ft - 12
    crank = ycyl(14, yc - 14, yc, rx, Zh) - ycyl(10.0, yc - 15, yc + 1, rx, Zh)
    crank += bx(rx - 6, rx + 6, yc - 12, yc - 6, Zh + 12, Zh + 95)
    crank += ycyl(9, yc - 62, yc - 12, rx, Zh + 90)
    add("crank", "Crank", crank, 10, "made", 10)
    bxk, bzk = rx - 100, Zh - 100
    brake = ycyl(4.0, -fy - ft - 4, -Wr / 2 - 6.5, bxk, bzk) + ycyl(8, -Wr / 2 - 6.5, -Wr / 2 - 3.5, bxk, bzk) \
        + ycyl(14, -fy - ft - 16, -fy - ft - 4, bxk, bzk)
    add("brake", "Brake knob and pad", brake, 10, "bought", 10)
    slip = ycyl(22, fy + ft + 18, fy + ft + 21, rx, Zh) + ycyl(11, fy + ft + 21, fy + ft + 61, rx, Zh)
    add("slipring", "Slip ring (Ethernet rated)", slip, 10, "bought", 10)
    ys = fy + ft
    anchor = bx(rx - 10, rx + 10, ys, ys + 45, Zh - 72, Zh - 69) + bx(rx - 10, rx + 10, ys + 42, ys + 45, Zh - 69, Zh - 11) \
        + bx(rx - 10, rx + 10, ys, ys + 3, Zh - 72, Zh - 42)
    anchor -= ycyl(2.75, ys - 1, ys + 4, rx, Zh - 55)
    add("anchor", "Slip ring anchor bracket", anchor, 10, "made", 10)
    # payout counter on a vertical bar through the front foot spacer
    bar = bx(rx - 133, rx - 127, -12.5, 12.5, 8, 140) - ycyl(3.2, -14, 14, rx - 130, 18)
    for z in (105, 130):
        bar -= xcyl(2.75, rx - 134, rx - 126, 0, z)
    add("counter_bar", "Payout counter bar", bar, 10, "made", 10)
    counter = bx(rx - 193, rx - 133, -22, 22, 95, 140)
    add("counter", "Payout counter (wheel, encoder, USB reader)", counter, 10, "bought", 10)
    # surface box: bought case, drop-in chassis
    bl, bw_, bh = p["box"]
    hb = p["box_base_h"]
    bx0 = rx + 260
    base = bx(bx0, bx0 + bl, -bw_ / 2, bw_ / 2, 0, hb) - bx(bx0 + 6, bx0 + bl - 6, -bw_ / 2 + 6, bw_ / 2 - 6, 6, hb + 1)
    lid = bx(bx0, bx0 + bl, -bw_ / 2, bw_ / 2, hb, bh) - bx(bx0 + 6, bx0 + bl - 6, -bw_ / 2 + 6, bw_ / 2 - 6, hb - 1, bh - 6)
    add("case", "Rugged case", base, 11, "bought", 11)
    add("case_lid", "Rugged case lid", lid, 11, "bought", 11)
    bp = bx(bx0 + 8, bx0 + bl - 8, -bw_ / 2 + 8, bw_ / 2 - 8, 6, 12)
    add("baseboard", "Chassis base board", bp, 11, "made", 11)
    posts = fuse([bx(x - 10, x + 10, y - 10, y + 10, 12, 118) for x in (bx0 + 30, bx0 + bl - 30) for y in (-bw_ / 2 + 30, bw_ / 2 - 30)])
    add("posts", "Chassis posts (4)", posts, 11, "made", 11)
    panel = bx(bx0 + 8, bx0 + bl - 8, -bw_ / 2 + 8, bw_ / 2 - 8, 118, 120)
    for x, y, r in ((bx0 + 330, -100, 11.0), (bx0 + 250, -100, 8.0), (bx0 + 200, -100, 8.0), (bx0 + 330, 40, 12.0), (bx0 + 330, 100, 12.0),
                    (bx0 + 250, 100, 8.0), (bx0 + 180, 100, 6.0)):
        panel -= zcyl(r, 116, 121, x, y)
    for x in (bx0 + 30, bx0 + bl - 30):
        for y in (-bw_ / 2 + 30, bw_ / 2 - 30):
            panel -= zcyl(2.25, 116, 121, x, y)                          # M4 screws into the posts
    add("panel", "Chassis panel", panel, 11, "made", 11)
    batt = bx(bx0 + 30, bx0 + 211, -83, 84, 12, 89)
    add("battery", "LiFePO4 battery, 12.8 V 20 Ah", batt, 11, "bought", 11)
    strap = bx(bx0 + 110, bx0 + 135, -84, 85, 89, 91) + bx(bx0 + 110, bx0 + 135, -86, -84, 12, 91) + bx(bx0 + 110, bx0 + 135, 85, 87, 12, 91)
    add("strap", "Battery strap", strap, 11, "bought", 11)
    boost = bx(bx0 + 250, bx0 + 360, 40, 120, 12, 72)
    monitor = bx(bx0 + 250, bx0 + 310, -130, -80, 12, 32)
    add("boost", "48 V boost converter", boost, 11, "bought", 11)
    add("monitor", "Current monitor and cutoff relay", monitor, 11, "bought", 11)
    pz = 120.0
    estop = zcyl(11, 106, pz, bx0 + 330, -100) + zcyl(20, pz, pz + 12, bx0 + 330, -100) + zcyl(17, pz + 12, pz + 30, bx0 + 330, -100)
    fuses = zcyl(8, 104, pz, bx0 + 250, -100) + zcyl(8, 104, pz, bx0 + 200, -100) + zcyl(10, pz, pz + 16, bx0 + 250, -100) + zcyl(10, pz, pz + 16, bx0 + 200, -100)
    conns = fuse([zcyl(r, 104, pz, x, y) + zcyl(r + 3, pz, pz + h, x, y) for x, y, r, h in
                  ((bx0 + 330, 40, 12.0, 14), (bx0 + 330, 100, 12.0, 14), (bx0 + 250, 100, 8.0, 12), (bx0 + 180, 100, 6.0, 10))])
    add("estop", "Emergency stop", estop, 11, "bought", 11)
    add("fuses", "Fuse holders, 10 A and 2 A", fuses, 11, "bought", 11)
    add("connectors", "Tether, Ethernet and charge connectors, switch", conns, 11, "bought", 11)
    pad = bx(bx0 + 75, bx0 + 225, -88, 7, bh, bh + 28)
    add("gamepad", "Operator gamepad", pad, 12, "bought", 12)
    return C


def surface_parts(p=PARAMS, x0=0.0) -> dict:
    """Surface kit grouped by callout: {10: reel, 11: box, 12: gamepad}."""
    C = build_surface(p, x0)
    names = {10: "Tether reel, slip ring, payout counter", 11: "Surface control box (LiFePO4, 48 V boost)", 12: "Operator gamepad"}
    out = {}
    for c in C.values():
        g = c.group
        out[g] = c.shape if g not in out else out[g] + c.shape
    return {g: (names[g], out[g]) for g in sorted(out)}


def track_contact_height(pipe_id, p=P):
    """Height of the track contact line above the pipe invert when the outer track edges bear on the wall."""
    R = pipe_id / 2
    e = p["track_y"] + p["track_w"] / 2
    return R - math.sqrt(R * R - e * e)


def assemble(parts: dict):
    from build123d import Compound
    return Compound(children=[s for _, s in parts.values()])


# ------------------------------------------------------------------ material masses from the model
DENSITY = {"Hull body": 2.70, "Hull lid": 2.70, "Ballast skid plate": 7.85, "Side plate, left": 2.70, "Side plate, right": 2.70,
           "Electronics tray": 2.70, "Front bezel": 2.70, "Fin bracket": 2.70, "Diode housing": 2.70, "End cap": 2.70,
           "Boom fin (clear acrylic)": 1.19, "Boom tube (clear acrylic)": 1.19, "Window tube (clear acrylic)": 1.19,
           "Camera mount": 1.07}


def made_masses(p=PARAMS):
    """Mass in kg of each made crawler part, from its model volume."""
    C = build_components(p)
    return {c.name: c.shape.volume / 1e6 * DENSITY[c.name] for c in C.values() if c.name in DENSITY}


SURFACE_DENSITY = {   # kg/L of model volume (tubes as a share of the solid drawn)
    "frame_r": 2.70, "frame_l": 2.70, "spacers": 2.70 * 0.3, "drum": 1.40, "flanges": 0.95, "hubs": 7.8, "axle": 2.70,
    "crank": 2.70, "anchor": 2.70, "counter_bar": 2.70, "frame_rods": 7.9, "drum_rods": 7.9, "bearing_bolts": 7.9,
    "baseboard": 0.60, "posts": 2.70 * 0.3, "panel": 2.70}
SURFACE_BOUGHT = {"bearings": 0.30, "brake": 0.05, "slipring": 0.15, "counter": 0.25,
                  "case": 3.0, "battery": 2.5, "strap": 0.05, "boost": 0.4, "monitor": 0.1, "estop": 0.1, "fuses": 0.05,
                  "connectors": 0.15, "case_lid": 0.0, "gamepad": 0.2}


def surface_masses(p=PARAMS):
    """kg by surface item: {'reel': ..., 'box': ..., 'gamepad': ...}, made parts from model volumes."""
    S = build_surface(p)
    out = {"reel": 0.0, "box": 0.0, "gamepad": 0.0}
    for k, c in S.items():
        m = c.shape.volume / 1e6 * SURFACE_DENSITY[k] if k in SURFACE_DENSITY else SURFACE_BOUGHT[k]
        out[{10: "reel", 11: "box", 12: "gamepad"}[c.group]] += m
    return out


# ------------------------------------------------------------------ constructability checks
def _vol(a, c):
    try:
        s = a & c
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch or stay apart. Returns (description, overlap mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    S = build_surface(p)
    rows = []

    def chk(desc, a, c, expect):
        v = _vol(a, c)
        g = a.distance_to(c)
        ok = v < 1e-2 and (g < 0.05 if expect == "touch" else g >= expect - 1e-6)
        rows.append((desc, v, g, expect, ok))

    c = lambda k: C[k].shape  # noqa: E731
    s = lambda k: S[k].shape  # noqa: E731
    chk("Lid on the hull rim", c("lid"), c("body"), "touch")
    chk("Lid screws in the rim", c("lid_screws"), c("body"), "touch")
    chk("Pressure-test plug in the lid", c("plug"), c("lid"), "touch")
    chk("Tether penetrator in the rear wall", c("penetrator"), c("body"), "touch")
    chk("Hull on the ballast plate", c("body"), c("ballast"), "touch")
    for k in ("plate_r", "plate_l"):
        chk(f"{C[k].name} on the hull side", c(k), c("body"), "touch")
        chk(f"{C[k].name} on the ballast side", c(k), c("ballast"), "touch")
        chk(f"{C[k].name} clear of the belt", c(k), c("belts"), 1.5)
        chk(f"{C[k].name} clear of the wheels", c(k), c("wheels"), 2.0)
    chk("Side plate screws in the plates", c("plate_screws"), c("plate_r") + c("plate_l"), "touch")
    chk("Side plate screws clear of the belts", c("plate_screws"), c("belts") + c("wheels"), 1.5)
    chk("Gearboxes on the drive pads", c("gearboxes"), c("body"), "touch")
    chk("Gearboxes clear of each other", C["gearboxes"].shape.solids()[0], C["gearboxes"].shape.solids()[1], 3.0)
    chk("Motor cans clear of the hull", c("cans"), c("body"), 1.0)
    chk("Motor cans clear of the tray", c("cans"), c("tray"), 3.0)
    chk("Gearboxes clear of the penetrator", c("gearboxes"), c("penetrator"), 1.0)
    chk("Shafts through the seals", c("shafts"), c("seals"), "touch")
    chk("Shafts clear of the hull bore", c("shafts"), c("body"), 0.05)
    chk("Seals in the side wall counterbores", c("seals"), c("body"), "touch")
    chk("Shafts in the sprockets", c("shafts"), c("wheels"), "touch")
    chk("Idler axles into the hull bosses", c("idler_axles"), c("body"), "touch")
    chk("Idler axles in the idlers", c("idler_axles"), c("wheels"), "touch")
    chk("Belts on the wheels", c("belts"), c("wheels"), "touch")
    chk("Belts clear of the hull", c("belts"), c("body") + c("lid"), 3.0)
    chk("Tray on the floor pads", c("tray"), c("body"), "touch")
    chk("Pi on the tray", c("pi"), c("tray"), "touch")
    chk("Deck on the Pi standoffs", c("deck"), c("pi"), "touch")
    chk("Deck clear of the lid", c("deck"), c("lid"), 5.0)
    chk("Deck clear of the hull rim", c("deck"), c("body"), 2.0)
    chk("Pi and deck clear of the camera", c("pi") + c("deck"), c("camera"), 0.5)
    chk("Camera mount on the front wall", c("cam_mount"), c("body"), "touch")
    chk("Camera on its mount", c("camera"), c("cam_mount"), "touch")
    chk("Lens clear of the dome", c("camera"), c("dome"), 1.0)
    chk("Lens clear of the front wall bore", c("camera"), c("body"), 1.0)
    chk("Dome flange on the front wall", c("dome"), c("body"), "touch")
    chk("Bezel on the front wall", c("bezel"), c("body"), "touch")
    chk("Bezel on the dome flange", c("bezel"), c("dome"), "touch")
    chk("Bezel screws in the front wall", c("bezel_screws"), c("body"), "touch")
    chk("LEDs in the bezel pockets", c("leds"), c("bezel"), "touch")
    chk("Bezel clear of the lid", c("bezel"), c("lid"), 0.0)
    chk("Bezel clear of the ballast plate", c("bezel"), c("ballast"), 2.0)
    chk("Bezel clear of the belts", c("bezel"), c("belts"), 2.0)
    chk("Fin bracket on the ballast front", c("fin_bracket"), c("ballast"), "touch")
    chk("Fin bracket clear of the bezel", c("fin_bracket"), c("bezel"), 0.5)
    chk("Fin on the bracket", c("fin"), c("fin_bracket"), "touch")
    chk("Fin clear of the bezel", c("fin"), c("bezel"), 0.5)
    chk("Fin clear of the dome", c("fin"), c("dome"), 3.0)
    chk("Fin under the boom", c("fin"), c("boom"), "touch")
    chk("Boom clear of the dome", c("boom"), c("dome"), 3.0)
    chk("Boom in the diode housing", c("boom"), c("housing"), "touch")
    chk("Diode in the housing", c("diode"), c("housing"), "touch")
    chk("Window on the housing", c("window"), c("housing"), "touch")
    chk("End cap on the window", c("cap"), c("window"), "touch")
    chk("Mirror on the end cap", c("mirror"), c("cap"), "touch")
    chk("Mirror clear of the window", c("mirror"), c("window"), 0.5)
    chk("Eye bolt in the ballast plate", c("eyebolt"), c("ballast"), "touch")
    chk("Eye bolt clear of the hull", c("eyebolt"), c("body"), 2.0)
    chk("Eye bolt clear of the tether relief", c("eyebolt"), c("relief"), 5.0)
    chk("Strain relief on the penetrator", c("relief"), c("penetrator"), "touch")
    # surface kit
    chk("Spacers between the side frames", s("spacers"), s("frame_r") + s("frame_l"), "touch")
    chk("Bearings on the side frames", s("bearings"), s("frame_r") + s("frame_l"), "touch")
    chk("Axle in the bearings", s("axle"), s("bearings"), "touch")
    chk("Axle in the hubs", s("axle"), s("hubs"), "touch")
    chk("Hubs on the flanges", s("hubs"), s("flanges"), "touch")
    chk("Drum between the flanges", s("drum"), s("flanges"), "touch")
    chk("Flanges clear of the side frames", s("flanges"), s("frame_r") + s("frame_l"), 10.0)
    chk("Hubs clear of the side frames", s("hubs"), s("frame_r") + s("frame_l"), 0.5)
    chk("Flanges clear of the spacers", s("flanges"), s("spacers"), 10.0)
    chk("Drum clear of the drum rods", s("drum"), s("drum_rods"), 1.0)
    chk("Crank on the axle", s("crank"), s("axle"), "touch")
    chk("Crank clear of the bearing", s("crank"), s("bearings"), 0.0)
    chk("Brake through the left frame", s("brake"), s("frame_l"), "touch")
    chk("Brake pad clear of the flange when off", s("brake"), s("flanges"), 0.5)
    chk("Slip ring on the axle end", s("slipring"), s("axle"), "touch")
    chk("Slip ring anchor on the right frame", s("anchor"), s("frame_r"), "touch")
    chk("Slip ring anchor holds the slip ring body", s("anchor"), s("slipring"), "touch")
    chk("Counter bar on the front spacer", s("counter_bar"), s("spacers"), "touch")
    chk("Counter on its bar", s("counter"), s("counter_bar"), "touch")
    chk("Counter clear of the flanges", s("counter"), s("flanges"), 5.0)
    chk("Chassis base board on the case floor", s("baseboard"), s("case"), "touch")
    chk("Posts on the base board", s("posts"), s("baseboard"), "touch")
    chk("Panel on the posts", s("panel"), s("posts"), "touch")
    chk("Panel clear of the case walls", s("panel"), s("case"), 1.0)
    chk("Battery on the base board", s("battery"), s("baseboard"), "touch")
    chk("Battery clear of the panel", s("battery"), s("panel"), 10.0)
    chk("Battery clear of the posts", s("battery"), s("posts"), 2.0)
    chk("Boost converter clear of the battery and posts", s("boost"), s("battery") + s("posts"), 5.0)
    chk("Emergency stop clear of the closed lid", s("estop"), s("case_lid"), 3.0)
    chk("Panel parts clear of the closed lid", s("connectors") + s("fuses"), s("case_lid"), 3.0)
    chk("Panel parts clear of the battery", s("estop") + s("fuses") + s("connectors"), s("battery"), 5.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, g, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:56s} overlap {v:9.3f} mm3  gap {g:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def main():
    from build123d import Compound, export_step, export_stl
    root = Path(__file__).resolve().parents[2]
    (root / "cad/step").mkdir(parents=True, exist_ok=True)
    (root / "cad/stl").mkdir(parents=True, exist_ok=True)
    C = build_components()
    S = build_surface()
    crawler = Compound(children=[c.shape for c in C.values()])
    surface = Compound(children=[c.shape for c in S.values()])
    for name, shape in (("crawler", crawler), ("surface-kit", surface)):
        export_step(shape, str(root / f"cad/step/culvertcrawl-{name}.step"))
        export_stl(shape, str(root / f"cad/stl/culvertcrawl-{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
    bb = crawler.bounding_box()
    print(f"crawler bounding box {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm "
          f"(x {bb.min.X:.0f} to {bb.max.X:.0f})")
    for d in (300, 600, 900):
        print(f"track contact line above invert in {d} mm pipe: {track_contact_height(d):.1f} mm")
    for k, v in made_masses().items():
        print(f"mass of {k}: {v:.3f} kg")
    print("wrote cad/step/culvertcrawl-crawler.step, culvertcrawl-surface-kit.step and matching STL files")


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    main()
    print_checks()
