"""CulvertCrawl parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    culvertcrawl-crawler.step / .stl       crawler assembly (items 1 to 9a)
    culvertcrawl-surface-kit.step / .stl   tether reel and surface control box (items 10 to 12)

Massing-plus level of detail: correct interfaces and main dimensions, not fabrication detail.
PRELIMINARY, NOT FOR FABRICATION.

Crawler frame (local): forward = +X, lateral = Y, up = Z; the track contact line is Z = 0 and the
crawler is centered on X = 0, Y = 0. The camera optical center is the dome center at X = hull_l / 2;
the laser ring plane is ring_d ahead of it. Numbers are checked in docs/04-calcs (CVC-CAL-001).
"""
from __future__ import annotations

import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below. docs/04-calcs/sizing.py imports them.
PARAMS = {
    # hull (item 1): 6061 aluminium, open-top body plus bolted lid with O-ring
    "hull_l": 240.0, "hull_w": 88.0, "hull_h": 74.0, "wall": 4.0, "lid_t": 6.0, "lid_lip": 3.0,
    "hull_z0": 22.0,            # hull bottom above the track contact line
    # tracks (item 2)
    "track_y": 65.0,            # track centerline offset from the crawler axis
    "track_w": 40.0,            # belt width
    "track_r": 35.0,            # sprocket and idler radius over the belt
    "track_x": 100.0,           # sprocket and idler centers at +/- track_x
    # motors (item 3): 5840-class worm gear motors inside the hull, rear
    "motor_r": 16.0, "motor_len": 60.0, "gearbox": (46.0, 32.0, 40.0),
    # camera, dome and LED ring (items 5, 6)
    "cam_z": 62.0,              # optical axis height above the track contact line
    "dome_r": 30.0,
    "led_r_out": 44.0, "led_r_in": 32.0, "led_t": 8.0,
    # laser ring projector (item 7)
    "ring_d": 300.0,            # ring plane ahead of the camera optical center (dome center); 200 at CAL-001 v0.1, 300 by DDR-002
    "boom_r": 9.0, "head_r": 13.0, "head_l": 26.0,
    # ballast skid plate (item 8): steel
    "ballast": (230.0, 80.0, 14.0), "ballast_z0": 8.0,   # 210 x 80 x 12 at z0 10 before DDR-002 (+0.46 kg)
    # tether (item 9)
    "tether_od": 7.0, "relief_l": 30.0, "relief_r": 11.0,
    # surface kit (items 10, 11)
    "reel_r": 160.0, "reel_w": 110.0, "reel_hub_z": 230.0,
    "box": (410.0, 330.0, 175.0),
}

P = PARAMS


def _xcyl(r, length, x0, y=0.0, z=0.0):
    from build123d import Cylinder, Pos, Rot
    return Pos(x0 + length / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, length)


def _ycyl(r, length, x=0.0, y=0.0, z=0.0):
    from build123d import Cylinder, Pos, Rot
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, length)


def _tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def crawler_parts(p=P) -> dict:
    """Crawler parts in the local frame, keyed by BOM line. Returns {bom: (name, shape)}."""
    from build123d import Box, Cylinder, Sphere, Cone, Pos, Rot
    L, W, H, t, z0 = p["hull_l"], p["hull_w"], p["hull_h"], p["wall"], p["hull_z0"]
    # 1 Hull: open-top body, lid with lip over the O-ring face, dome bore in front, tether gland at rear
    body = Pos(0, 0, z0 + H / 2) * Box(L, W, H) - Pos(0, 0, z0 + t + H / 2) * Box(L - 2 * t, W - 2 * t, H)
    lid = Pos(0, 0, z0 + H + p["lid_t"] / 2) * Box(L + 2 * p["lid_lip"], W + 2 * p["lid_lip"], p["lid_t"])
    for sx in (-1, 1):
        for sy in (-1, 1):  # lid screw heads (M4 class), massing only
            lid = lid + Pos(sx * (L / 2 - 8), sy * (W / 2 - 6), z0 + H + p["lid_t"] + 1.5) * Cylinder(3.5, 3)
    dome_flange = _xcyl(p["dome_r"] + 6, 5, L / 2, 0, p["cam_z"])
    gland = _xcyl(8, 12, -L / 2 - 12, 0, p["cam_z"])
    hull = body + lid + dome_flange + gland

    # 2 Tracks: belt around a rear drive sprocket and a front idler, each side, with an inner side plate
    tr, tx, tw = p["track_r"], p["track_x"], p["track_w"]
    tracks = None
    for y in (p["track_y"], -p["track_y"]):
        belt = (Pos(0, y, tr) * Box(2 * tx, tw, 2 * tr)
                + _ycyl(tr, tw, -tx, y, tr) + _ycyl(tr, tw, tx, y, tr))
        belt = belt - _ycyl(tr - 8, tw + 2, -tx, y, tr) - _ycyl(tr - 8, tw + 2, tx, y, tr)
        hub = _ycyl(tr - 8, tw - 10, -tx, y, tr) + _ycyl(tr - 8, tw - 10, tx, y, tr)
        side = -1 if y > 0 else 1
        plate = Pos(0, y + side * (tw / 2 + 1.5), tr) * Box(2 * tx, 3, 30)
        tracks = (belt + hub + plate) if tracks is None else tracks + belt + hub + plate

    # 3 Worm gear motors (pair): can along X, gearbox at the rear, output shaft through the hull wall
    gx, gy, gz = p["gearbox"]
    motors = None
    for s in (1, -1):
        y = s * 20.0
        can = _xcyl(p["motor_r"], p["motor_len"], -tx + gx / 2 + 2, y, 52)
        gear = Pos(-tx, y, 52) * Box(gx, gy, gz)
        shaft_len = p["track_y"] - abs(y) - tw / 2 + 12
        shaft = _ycyl(4, shaft_len, -tx, y + s * (gy / 2 + shaft_len / 2 - 4), tr)
        m = can + gear + shaft
        motors = m if motors is None else motors + m

    # 4 Electronics stack: compute board, driver and converter layer, 48 to 12 V module, IMU, leak sensor
    electronics = (Pos(30, 0, z0 + t + 16) * Box(90, 62, 8)
                   + Pos(30, 0, z0 + t + 32) * Box(70, 50, 14)
                   + Pos(-30, 0, z0 + t + 12) * Box(40, 30, 16))

    # 5 Camera module and dome port (optical center at the dome center)
    camera = Pos(L / 2 - 22, 0, p["cam_z"]) * Box(20, 28, 28) \
        + (Pos(L / 2, 0, p["cam_z"]) * Sphere(p["dome_r"])
           & Pos(L / 2 + 50, 0, p["cam_z"]) * Box(100, 100, 100))

    # 6 LED ring light around the dome
    led = Pos(L / 2 + 5 + p["led_t"] / 2, 0, p["cam_z"]) * Rot(0, 90, 0) * (
        Cylinder(p["led_r_out"], p["led_t"]) - Cylinder(p["led_r_in"], p["led_t"] + 2))

    # 7 Laser ring projector: clear boom from the LED bezel, diode housing and 90 degree cone mirror
    ring_x = L / 2 + p["ring_d"]
    x0 = L / 2 + p["dome_r"]
    boom = _xcyl(p["boom_r"], ring_x - p["head_l"] - x0, x0, 0, p["cam_z"])
    head = _xcyl(p["head_r"], p["head_l"], ring_x - p["head_l"], 0, p["cam_z"])
    mirror = Pos(ring_x + 6, 0, p["cam_z"]) * Rot(0, -90, 0) * Cone(p["head_r"], 1, 12)
    laser = boom + head + mirror

    # 8 Ballast skid plate with a turned-up front edge
    bl, bw, bt = p["ballast"]
    ballast = Pos(0, 0, p["ballast_z0"] + bt / 2) * Box(bl, bw, bt)
    lip = Pos(bl / 2 + 6, 0, p["ballast_z0"] + bt / 2 + 8) * Rot(0, -35, 0) * Box(20, bw, bt * 0.6)
    ballast = ballast + lip

    # 9a Tether strain relief and bend restrictor at the rear gland
    rx = -L / 2 - 12
    relief = _xcyl(p["relief_r"], p["relief_l"], rx - p["relief_l"], 0, p["cam_z"]) \
        + Pos(rx - p["relief_l"] - 8, 0, p["cam_z"]) * Rot(0, 90, 0) * Cone(p["tether_od"] / 2 + 1, p["relief_r"], 16) \
        + _xcyl(p["tether_od"] / 2, 20, rx - p["relief_l"] - 36, 0, p["cam_z"])

    return {1: ("Sealed hull and lid", hull), 2: ("Track modules (pair)", tracks),
            3: ("Worm gear motors (2)", motors), 4: ("Electronics stack (Pi 4, driver, DC-DC)", electronics),
            5: ("Fisheye camera and dome port", camera), 6: ("LED ring light", led),
            7: ("Laser ring projector on boom", laser), 8: ("Ballast skid plate", ballast),
            9: ("Tether strain relief (tether stub)", relief)}


def surface_parts(p=P, x0=0.0) -> dict:
    """Tether reel with slip ring and payout counter, surface control box, gamepad (massing).
    Placed along +X from x0, standing on Z = 0."""
    from build123d import Box, Cylinder, Pos
    R, Wr, Zh = p["reel_r"], p["reel_w"], p["reel_hub_z"]
    rx = x0 + 180.0
    reel = _ycyl(R, 6, rx, Wr / 2, Zh) + _ycyl(R, 6, rx, -Wr / 2, Zh) + _ycyl(115, Wr - 6, rx, 0, Zh)
    for dy in (Wr / 2 + 12, -Wr / 2 - 12):
        for dx in (-150, 150):
            reel = reel + _tube((rx + dx, dy, 0), (rx, dy, Zh), 10)
    reel = reel + _tube((rx - 150, Wr / 2 + 12, 0), (rx - 150, -Wr / 2 - 12, 0), 10) \
        + _tube((rx + 150, Wr / 2 + 12, 0), (rx + 150, -Wr / 2 - 12, 0), 10)
    reel = reel + _ycyl(12, Wr + 60, rx, 0, Zh)                                   # axle
    reel = reel + _tube((rx, -Wr / 2 - 30, Zh), (rx + 90, -Wr / 2 - 30, Zh + 60), 7) \
        + _ycyl(9, 50, rx + 90, -Wr / 2 - 55, Zh + 60)                             # crank
    reel = reel + _ycyl(22, 40, rx, Wr / 2 + 50, Zh)                              # slip ring
    reel = reel + Pos(rx - 190, 0, 150) * Box(60, 44, 50)                          # payout counter
    bl, bw, bh = p["box"]
    bx = rx + 260
    case = Pos(bx + bl / 2, 0, bh / 2) * Box(bl, bw, bh) - Pos(bx + bl / 2, 0, bh / 2 + 6) * Box(bl - 12, bw - 12, bh)
    case = case + Pos(bx + bl / 2, 0, bh + 4) * Box(bl, bw, 8)
    case = case + Pos(bx + 130, 0, 6 + 85) * Box(180, 175, 170) + Pos(bx + 300, 60, 36) * Box(110, 80, 60)
    case = case + Pos(bx + 330, -100, bh + 16) * Cylinder(22, 16) + Pos(bx + 330, -100, bh + 30) * Cylinder(28, 12)
    pad = Pos(bx + 150, -40, bh + 22) * Box(150, 95, 28)
    return {10: ("Tether reel, slip ring, payout counter", reel),
            11: ("Surface control box (LiFePO4, 48 V boost)", case),
            12: ("Operator gamepad", pad)}


def track_contact_height(pipe_id, p=P):
    """Height of the track contact line above the pipe invert when the outer track edges bear on the wall."""
    R = pipe_id / 2
    e = p["track_y"] + p["track_w"] / 2
    return R - math.sqrt(R * R - e * e)


def assemble(parts: dict):
    from build123d import Compound
    return Compound(children=[s for _, s in parts.values()])


def main():
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[2]
    (root / "cad/step").mkdir(parents=True, exist_ok=True)
    (root / "cad/stl").mkdir(parents=True, exist_ok=True)
    crawler = assemble(crawler_parts())
    surface = assemble(surface_parts())
    for name, shape in (("crawler", crawler), ("surface-kit", surface)):
        export_step(shape, str(root / f"cad/step/culvertcrawl-{name}.step"))
        export_stl(shape, str(root / f"cad/stl/culvertcrawl-{name}.stl"))
    bb = crawler.bounding_box()
    print(f"crawler bounding box {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm "
          f"(x {bb.min.X:.0f} to {bb.max.X:.0f})")
    for d in (300, 600, 900):
        print(f"track contact line above invert in {d} mm pipe: {track_contact_height(d):.1f} mm")
    print("wrote cad/step/culvertcrawl-crawler.step, culvertcrawl-surface-kit.step and matching STL files")


if __name__ == "__main__":
    main()
