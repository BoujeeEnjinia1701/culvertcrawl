"""CulvertCrawl sizing calculations, CVC-CAL-001 v0.2.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
First-principles estimates for a paper design (TRL 3). Nothing here is measured.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, track_contact_height  # noqa: E402

G = 9.81
RHO_W = 1000.0
OUT = []


def out(key, value, unit="", fmt="{:.2f}"):
    s = fmt.format(value) if isinstance(value, (int, float)) else str(value)
    OUT.append((key, s, unit))
    print(f"  {key:<58s} {s:>10s} {unit}")
    return value


def head(t):
    print(f"\n{t}")


# ---------------------------------------------------------------- inputs
A = {
    "mu_track": 0.6,          # track to wet silt, dry or submerged (sensitivity below)
    "c_rr": 0.15,             # track motion resistance on silt, fraction of normal load
    "mu_tether": 0.5,         # tether jacket on pipe invert
    "reserve": 0.20,          # traction held in reserve (R2)
    "slope": 0.05,            # design case grade, rise over run
    "reach_target": 50.0,     # m (R2)
    "tether_len": 60.0,       # m
    "tether_g_per_m": 55.0,   # g/m in air (estimate)
    "tether_od": P["tether_od"],
    "cond_ohm_per_km": 26.0,  # 0.75 mm2 class 5 stranded copper, IEC 60228 maximum at 20 C
    "v_bus": 48.0,
    "eta_buck": 0.91, "eta_boost": 0.92,
    "loads_w": {"Drive motors": 12.0, "LEDs": 8.0, "Pi, camera, network": 6.5, "Laser, IMU, sensors": 1.5},
    "peak_w": 50.0,           # crawler loads at peak (both motors near rated torque, LEDs on)
    "surface_w": 1.0,         # surface box monitor, relay, e-stop circuit
    "batt_v": 12.8, "batt_ah": 20.0, "batt_dod": 0.90, "derate": 0.80,
    "water_depth": 150.0,     # mm, design case
    "flow": 0.50,             # m/s, design case mean flow
    "cd": 1.1,                # crawler drag coefficient, bluff box
    "speed": 0.15,            # m/s survey speed
    "sprocket_r": P["track_r"] / 1000,
    "motor_rpm": 80.0,
    "belt_eff": 0.85,
    "cam_fps": 50.0,          # IMX708 2304 x 1296 mode (up to 56 fps)
    "img_circle_px": 1296.0,  # 180 degree equidistant circular fisheye inscribed in the sensor height
    "fov_deg": 180.0,
}

# ---------------------------------------------------------------- 1 geometry and fit (R1)
head("1 Geometry and fit (R1)")
L, Wd, H = P["hull_l"], P["hull_w"], P["hull_h"]
width = 2 * (P["track_y"] + P["track_w"] / 2)
height = max(P["hull_z0"] + H + P["lid_t"] + 3.0, P["cam_z"] + P["led_r_out"])
front = L / 2 + P["ring_d"] + 12
rear = -L / 2 - 12 - P["relief_l"] - 16
out("crawler width over tracks", width, "mm", "{:.0f}")
out("crawler height over lid screws", height, "mm", "{:.0f}")
out("crawler length, rear strain relief to cone mirror", front - rear, "mm", "{:.0f}")
out("track length (sprocket to idler, over belt)", 2 * (P["track_x"] + P["track_r"]), "mm", "{:.0f}")
fit = {}
for d in (300, 600, 900):
    R = d / 2
    tz = track_contact_height(d)
    # clearance from the upper crawler corners (lid lip and track tops) to the pipe wall
    pts = [(Wd / 2 + P["lid_lip"], tz + height), (width / 2, tz + 2 * P["track_r"])]
    clr = min(R - math.hypot(y, z - R) for y, z in pts)
    cam_h = tz + P["cam_z"]
    fit[d] = (tz, cam_h, clr)
    out(f"{d} mm pipe: track contact line above invert", tz, "mm", "{:.1f}")
    out(f"{d} mm pipe: camera axis above invert", cam_h, "mm", "{:.1f}")
    out(f"{d} mm pipe: least radial clearance, crawler to wall", clr, "mm", "{:.0f}")
beta600 = math.asin((P["track_y"] + P["track_w"] / 2) / 300)
k_wedge = {d: 1 / math.cos(math.asin((P["track_y"] + P["track_w"] / 2) / (d / 2))) for d in (300, 600, 900)}
out("track edge contact angle in 600 mm pipe", math.degrees(beta600), "deg", "{:.1f}")
out("normal load factor (sum of normals / weight), 600 mm", k_wedge[600], "", "{:.3f}")
out("normal load factor, 300 mm", k_wedge[300], "", "{:.3f}")
out("normal load factor, 900 mm", k_wedge[900], "", "{:.3f}")

# ---------------------------------------------------------------- 2 mass and buoyancy
head("2 Mass and buoyancy (R7, R10)")
hull_v = (L * Wd * H - (L - 2 * P["wall"]) * (Wd - 2 * P["wall"]) * (H - P["wall"])
          + (L + 2 * P["lid_lip"]) * (Wd + 2 * P["lid_lip"]) * P["lid_t"]) / 1e6  # L of metal
bl, bw, bt = P["ballast"]
ballast_v = bl * bw * bt / 1e6 + 20 * bw * bt * 0.6 / 1e6
mass = {
    "Hull and lid (6061, 2.70 kg/L)": hull_v * 2.70,
    "Tracks, sprockets, side plates": 1.00,
    "Worm gear motors (2 x 0.35 kg)": 0.70,
    "Electronics stack": 0.20,
    "Camera, dome, LED ring": 0.15,
    "Laser projector and boom": 0.11,   # 300 mm ring plane (DDR-002); 0.10 kg at 200 mm
    "Ballast plate (steel, 7.85 kg/L)": ballast_v * 7.85,
    "Fasteners, glands, seals, strain relief": 0.40,
}
for k, v in mass.items():
    out(f"mass: {k}", v, "kg")
m = out("crawler mass", sum(mass.values()), "kg")
W = m * G
hull_env = (L * Wd * (H + P["lid_t"])) / 1e6
dome = (2 / 3) * math.pi * (P["dome_r"] / 10) ** 3 / 1000
boom_v = (math.pi * P["boom_r"] ** 2 * (P["ring_d"] - P["dome_r"]) + math.pi * P["head_r"] ** 2 * P["head_l"]) / 1e6
tracks_v = 1.00 / 1.8           # rubber and aluminium, mean density about 1.8 kg/L
motors_v = 0.0                  # inside the hull envelope
led_v = math.pi * (P["led_r_out"] ** 2 - P["led_r_in"] ** 2) * P["led_t"] / 1e6
misc_v = 0.05
vol = out("displaced volume, fully submerged", hull_env + dome + boom_v + tracks_v + ballast_v + led_v + misc_v, "L")
m_net = out("net submerged mass", m - vol * RHO_W / 1000, "kg")
out("fraction of dry normal load left when submerged", m_net / m, "", "{:.2f}")
submerged_depth = A["water_depth"] - fit[600][0]
out("design case: water depth above track contact line (600 mm)", submerged_depth, "mm", "{:.0f}")
out("design case: crawler fully submerged (1 = yes)", float(submerged_depth >= height), "", "{:.0f}")
tether_kg = A["tether_g_per_m"] * A["tether_len"] / 1000
kit = {"Crawler": m, "Tether, 60 m": tether_kg, "Reel, frame, slip ring, counter": 2.5,
       "Surface box (LiFePO4 2.5 kg, case 3.0 kg, electronics 0.8 kg)": 6.3, "Gamepad": 0.2}
for k, v in kit.items():
    out(f"kit mass: {k}", v, "kg", "{:.1f}")
out("whole kit mass", sum(kit.values()), "kg", "{:.1f}")
out("heaviest single item (reel with tether)", tether_kg + 2.5, "kg", "{:.1f}")

# ---------------------------------------------------------------- 3 traction and reach (R2, R8)
head("3 Traction and reach (R2, R8)")
w_t = A["tether_g_per_m"] / 1000 * G                                        # N/m in air
v_t = math.pi * (A["tether_od"] / 2000) ** 2                                # m3/m
w_t_sub = (A["tether_g_per_m"] / 1000 - v_t * RHO_W) * G                    # N/m submerged
out("tether weight in air", w_t, "N/m", "{:.3f}")
out("tether weight submerged", w_t_sub, "N/m", "{:.3f}")
th = math.atan(A["slope"])
area = width / 1000 * height / 1000


def reach(weight, tether_w, uphill, flow=None, mu=A["mu_track"], k=k_wedge[600], reserve=A["reserve"]):
    """Tether length the crawler can drag on a straight grade. Returns (reach m, terms)."""
    s = 1 if uphill else -1
    n = weight * math.cos(th) * k
    trac = (1 - reserve) * mu * n
    rr = A["c_rr"] * n
    grade = s * weight * math.sin(th)
    if flow is None:                                                 # dry pipe: air drag neglected
        drag = 0.0
    else:
        v_rel = A["speed"] + flow if uphill else A["speed"] - flow    # flow runs downhill
        drag = 0.5 * RHO_W * A["cd"] * area * v_rel * abs(v_rel)
    per_m = tether_w * (A["mu_tether"] * math.cos(th) + s * math.sin(th))
    spare = trac - rr - grade - drag
    return spare / per_m, dict(trac=trac, rr=rr, grade=grade, drag=drag, per_m=per_m)


cases = [("dry 600 mm, uphill (enter at outlet)", W, w_t, True, None),
         ("dry 600 mm, downhill (enter at inlet)", W, w_t, False, None),
         ("design case wet: submerged, 0.5 m/s flow, uphill", m_net * G, w_t_sub, True, A["flow"]),
         ("design case wet: submerged, 0.5 m/s flow, downhill", m_net * G, w_t_sub, False, A["flow"])]
R2 = {}
for name, wt, tw, up, fl in cases:
    r, t = reach(wt, tw, up, fl)
    R2[name] = r
    out(f"{name}: usable traction", t["trac"], "N", "{:.1f}")
    out(f"{name}: track resistance", t["rr"], "N", "{:.1f}")
    out(f"{name}: grade force (+ resists)", t["grade"], "N", "{:.2f}")
    out(f"{name}: water drag (+ resists)", t["drag"], "N", "{:.2f}")
    out(f"{name}: tether drag per meter", t["per_m"], "N/m", "{:.3f}")
    out(f"{name}: REACH at 20 % reserve", r, "m", "{:.0f}")
r0, _ = reach(W, w_t, True, reserve=0.0)
out("dry uphill reach with no traction reserve", r0, "m", "{:.0f}")
rmu, _ = reach(m_net * G, w_t_sub, True, A["flow"], mu=0.45)
out("wet uphill reach if submerged track friction is 0.45", rmu, "m", "{:.0f}")
# return trip in the wet case: crawler reverses upstream, tether is wound in by the reel (no tether drag)
_, t = reach(m_net * G, w_t_sub, True, A["flow"])
out("wet case, reversing upstream with reel winding: force margin", t["trac"] - t["rr"] - t["grade"] - t["drag"], "N", "{:.1f}")
# ballast needed for 50 m uphill in the wet case
extra = 0.0
while reach((m_net + extra * (1 - 1 / 7.85)) * G, w_t_sub, True, A["flow"])[0] < A["reach_target"] and extra < 10:
    extra += 0.05
out("extra steel ballast for 50 m wet uphill", extra, "kg", "{:.2f}")
hold_drag = 0.5 * RHO_W * A["cd"] * area * A["flow"] ** 2
out("stationary in 0.5 m/s flow: water drag", hold_drag, "N", "{:.1f}")
out("stationary submerged: static friction available", A["mu_track"] * m_net * G * math.cos(th) * k_wedge[600], "N", "{:.1f}")
# motor torque at the traction limit
n_dry = W * math.cos(th) * k_wedge[600]
f_track = A["mu_track"] * n_dry / 2
tq = out("sprocket torque per motor at the dry traction limit", f_track * A["sprocket_r"] / A["belt_eff"], "N m")
out("top speed at 80 rpm", A["motor_rpm"] / 60 * 2 * math.pi * A["sprocket_r"], "m/s")
out("hold on 5 % with power off: grade force", W * math.sin(th), "N", "{:.2f}")
out("hold on 5 %: static friction available", A["mu_track"] * n_dry, "N", "{:.1f}")
r_t = P["track_r"]
out("step climb, conservative rule (idler radius)", r_t, "mm", "{:.0f}")
for mu in (0.6, 0.4):
    out(f"step climb, friction bound r(1 + sin(atan mu)), mu = {mu}", r_t * (1 + math.sin(math.atan(mu))), "mm", "{:.0f}")

# ---------------------------------------------------------------- 4 recovery (R3)
head("4 Recovery pull (R3)")
pull = A["mu_track"] * n_dry + W * math.sin(th) + w_t * (A["mu_tether"] * math.cos(th) + math.sin(th)) * A["reach_target"]
out("pull, tracks locked, 50 m of tether, uphill of the crew", pull, "N", "{:.0f}")
out("tether break strength", 1000.0, "N", "{:.0f}")
out("safety factor on the locked-track pull", 1000.0 / pull, "", "{:.1f}")
out("stuck pull the 1 kN member can take at a factor of 5", 200.0, "N", "{:.0f}")

# ---------------------------------------------------------------- 5 power, tether and endurance (R9, R11)
head("5 Power, tether and endurance (R9, R11)")
loads = sum(A["loads_w"].values())
out("crawler loads while driving and profiling", loads, "W", "{:.1f}")
r_loop = A["cond_ohm_per_km"] / 1000 * 2 * A["tether_len"]
out("tether loop resistance (2 x 60 m)", r_loop, "ohm")


def tether(p_in):
    i = (A["v_bus"] - math.sqrt(A["v_bus"] ** 2 - 4 * r_loop * p_in)) / (2 * r_loop)
    return i, A["v_bus"] - i * r_loop, i * i * r_loop


p_c = loads / A["eta_buck"]
i, v_c, loss = tether(p_c)
out("crawler input power", p_c, "W", "{:.1f}")
out("tether current", i, "A", "{:.2f}")
out("voltage at the crawler", v_c, "V", "{:.1f}")
out("tether copper loss", loss, "W", "{:.2f}")
out("tether loss as share of boost output", loss / (p_c + loss) * 100, "%", "{:.1f}")
p_boost = p_c + loss
p_batt = p_boost / A["eta_boost"] + A["surface_w"]
out("boost output", p_boost, "W", "{:.1f}")
out("battery output incl. surface electronics", p_batt, "W", "{:.1f}")
ip, vp, lp = tether(A["peak_w"] / A["eta_buck"])
out("peak: tether current", ip, "A", "{:.2f}")
out("peak: voltage at the crawler", vp, "V", "{:.1f}")
out("peak: tether voltage drop", A["v_bus"] - vp, "V", "{:.1f}")
i_batt_peak = (A["peak_w"] / A["eta_buck"] + lp) / A["eta_boost"] / 12.0
out("peak battery current at 12.0 V (low charge)", i_batt_peak, "A", "{:.1f}")
i24, v24, l24 = (lambda pin: ((24 - math.sqrt(24 ** 2 - 4 * r_loop * pin)) / (2 * r_loop),))(p_c)[0], None, None
out("tether loss if run at 24 V instead", i24 ** 2 * r_loop, "W", "{:.2f}")
e_use = A["batt_v"] * A["batt_ah"] * A["batt_dod"]
out("usable battery energy", e_use, "Wh", "{:.0f}")
out("endurance, nominal", e_use / p_batt, "h", "{:.1f}")
out("endurance, derated 20 % for cold and ageing", e_use * A["derate"] / p_batt, "h", "{:.1f}")
out("battery energy (nominal)", A["batt_v"] * A["batt_ah"], "Wh", "{:.0f}")

# ---------------------------------------------------------------- 6 laser ring profiling (R5)
head("6 Laser ring profiling (R5)")
deg_px = A["fov_deg"] / A["img_circle_px"]
out("fisheye angular resolution (equidistant)", deg_px, "deg/px", "{:.3f}")
E = {"sigma_px": 0.3,        # random ring-center localization, 1 sigma
     "lens_px": 0.3,         # lens model residual at the image edge, 1 sigma, grows as (theta/90 deg)^2
     "tilt_deg": 0.1,        # ring plane tilt residual after calibration in a reference pipe, 1 sigma
     "dist_mm": 0.3,         # ring plane distance residual, 1 sigma
     "yaw_deg": 2.0}         # crawler yaw in the pipe, uniform +/-, not known to the software
rng = np.random.default_rng(7)


def ring_sim(d, water=0.0, ring_d=P["ring_d"], trials=2000, n=720):
    """Monte Carlo of one ring measurement in a round pipe. Returns 95th percentile errors (mm) of
    mean diameter, vertical diameter (deflection) and the worst single wall point."""
    R = d / 2
    cz = fit[d][1]                                     # camera height above invert
    phi = np.linspace(0, 2 * np.pi, n, endpoint=False)
    y = R * np.sin(phi); z = R - R * np.cos(phi)       # wall points, invert at phi = 0
    keep = z > water
    y, z = y[keep], z[keep]
    dz = z - cz
    rho = np.hypot(y, dz)
    psi = np.arctan2(dz, y)
    res = np.radians(deg_px)
    e_d, e_v, e_pt = [], [], []
    for _ in range(trials):
        tilt = np.radians(rng.normal(0, E["tilt_deg"]))
        tilt_y = np.radians(rng.normal(0, E["tilt_deg"]))
        dd = rng.normal(0, E["dist_mm"])
        yaw = np.radians(rng.uniform(-E["yaw_deg"], E["yaw_deg"]))
        lens = rng.normal(0, E["lens_px"]) * res
        # true light plane: x = ring_d + dz tan(tilt) + y tan(tilt_y + yaw); the wall section of a yawed
        # crawler is the pipe circle stretched by 1/cos(yaw) across the pipe
        ys = y / np.cos(yaw)
        x = ring_d + dd + dz * np.tan(tilt) + ys * np.tan(tilt_y)
        rho_t = np.hypot(ys, dz)
        theta = np.arctan2(rho_t, x)
        theta_m = theta + lens * (theta / (np.pi / 2)) ** 2 + rng.normal(0, E["sigma_px"] * res, theta.size)
        psi_m = np.arctan2(dz, ys) + rng.normal(0, E["sigma_px"] * res, theta.size) / np.maximum(theta, 0.05)
        rho_m = ring_d * np.tan(theta_m)                   # software assumes the nominal plane
        ym, zm = rho_m * np.cos(psi_m), rho_m * np.sin(psi_m) + cz
        # axis-aligned ellipse fit: a y^2 + b z^2 + c y + e z = 1
        zc = zm - cz                                       # fit about the camera axis (inside the pipe)
        M = np.column_stack([ym ** 2, zc ** 2, ym, zc])
        a, b, c, e = np.linalg.lstsq(M, np.ones_like(ym), rcond=None)[0]
        y0, z0 = -c / (2 * a), -e / (2 * b)
        k = 1 + a * y0 ** 2 + b * z0 ** 2
        ay, az = math.sqrt(k / a), math.sqrt(k / b)       # semi-axes
        e_d.append(abs((ay + az) - d))
        e_v.append(abs(2 * az - d))
        # single point radial error about the fitted center
        r_true = np.hypot(y - 0, z - R)
        r_meas = np.hypot(ym - y0, zc - z0)
        e_pt.append(np.max(np.abs(r_meas - r_true)))
    p95 = lambda v: float(np.percentile(v, 95))
    return p95(e_d), p95(e_v), p95(e_pt), float(np.degrees(np.arctan2(d - cz, ring_d)))


R5 = {}
for d in (300, 600, 900):
    for water in (0.0, A["water_depth"]):
        if water >= d / 2:
            continue
        ed, ev, ep, top = ring_sim(d, water)
        R5[(d, water)] = (ed, ev, ep)
        tag = f"{d} mm, water {water:.0f} mm"
        if water == 0:
            out(f"{d} mm: top of pipe angle off the camera axis", top, "deg", "{:.1f}")
        out(f"{tag}: mean diameter error (95th pct)", ed / d * 100, "% of D", "{:.2f}")
        out(f"{tag}: vertical diameter error (95th pct)", ev / d * 100, "% of D", "{:.2f}")
        out(f"{tag}: worst wall point error (95th pct)", ep, "mm", "{:.1f}")
ed, ev, ep, top = ring_sim(900, A["water_depth"], ring_d=200.0)
out("900 mm, water 150 mm, former 200 mm ring plane: vertical diameter error", ev / 900 * 100, "% of D", "{:.2f}")
profiles_s = A["cam_fps"] / 2
out("profiles per second (laser on alternate frames)", profiles_s, "1/s", "{:.0f}")
out("profile spacing at 0.15 m/s", A["speed"] / profiles_s * 1000, "mm", "{:.0f}")
out("profile spacing at top speed", 0.293 / profiles_s * 1000, "mm", "{:.0f}")
# ring signal in a dark pipe, top of a 900 mm pipe
p_laser = 1.0e-3; lw = 2.0e-3; refl = 0.2; fnum = 2.0; px = 2.8e-6; qe = 0.6; t_exp = 0.010
circ = math.pi * 0.9
e_wall = p_laser / circ / lw                                      # W/m2 on the wall inside the line
L_wall = refl * e_wall / math.pi
e_sensor = math.pi * L_wall / (4 * fnum ** 2)
photons = e_sensor * px ** 2 * t_exp / (6.626e-34 * 3e8 / 520e-9)
out("ring irradiance on the wall, 900 mm pipe", e_wall, "W/m2", "{:.3f}")
out("signal electrons per pixel on the ring (10 ms, f/2)", photons * qe, "e-", "{:.0f}")
out("shot-noise limited SNR", math.sqrt(photons * qe), "", "{:.0f}")
out("pupil share of emitted power at 100 mm from the cone (7 mm pupil)", 7 / (2 * math.pi * 100) * 1000, "uW", "{:.0f}")

# ---------------------------------------------------------------- 7 video, link, lighting (R4, R6)
head("7 Video, data link and lighting (R4, R6)")
out("video frame rate (LED frames of a 50 fps stream)", A["cam_fps"] / 2, "fps", "{:.0f}")
video = 8.0
laser_frames = A["img_circle_px"] ** 2 * 1.0 * profiles_s / 1e6        # 1 bit per pixel grey JPEG
out("video stream (1080p H.264)", video, "Mbit/s", "{:.0f}")
out("laser frames (1296 x 1296 grey JPEG, 1 bit/px)", laser_frames, "Mbit/s", "{:.0f}")
out("link use of about 94 Mbit/s usable on 100BASE-TX", (video + laser_frames + 0.2) / 94 * 100, "%", "{:.0f}")
flux = 800.0
intensity = flux / math.pi                                               # 120 degree cone, pi sr
out("LED luminous intensity (800 lm in a 120 deg cone)", intensity, "cd", "{:.0f}")
out("illuminance on the far wall of a 900 mm pipe (0.83 m)", intensity / 0.83 ** 2, "lx", "{:.0f}")
out("illuminance 2 m ahead down the pipe", intensity / 2.0 ** 2, "lx", "{:.0f}")
out("payout encoder resolution (50 mm wheel, 600 counts)", math.pi * 50 / 600, "mm", "{:.2f}")
out("R6 distance tolerance at 50 m (1 % or 0.2 m)", max(0.01 * 50, 0.2), "m", "{:.1f}")

# ---------------------------------------------------------------- 8 thermal, pressure
head("8 Hull thermal and pressure")
q_in = A["loads_w"]["Pi, camera, network"] + A["loads_w"]["Laser, IMU, sensors"] * 0.5 + p_c * (1 - A["eta_buck"]) + 1.0
area_h = 2 * (L * Wd + L * (H + P["lid_t"]) + Wd * (H + P["lid_t"])) / 1e6
out("heat inside the hull", q_in, "W", "{:.1f}")
out("hull outer area", area_h, "m2", "{:.3f}")
out("hull rise over air, h = 8 W/(m2 K)", q_in / (area_h * 8), "K", "{:.0f}")
out("hull rise over water, h = 300 W/(m2 K)", q_in / (area_h * 300), "K", "{:.1f}")
out("water pressure at 1 m (IP68 target)", RHO_W * G * 1.0 / 1000, "kPa", "{:.1f}")

# ---------------------------------------------------------------- 9 cost (R12)
head("9 Cost (R12)")
with open(ROOT / "bom/bom.csv") as f:
    rows = list(csv.DictReader(f))
total = 0.0
groups = {"crawler (items 1 to 8)": 0.0, "tether, reel and surface kit (items 9 to 12)": 0.0, "hardware and consumables (item 13)": 0.0}
for r in rows:
    line = float(r["qty"]) * float(r["unit_cost_usd"])
    total += line
    n = int(r["item"].split()[0])
    groups[list(groups)[0 if n <= 8 else 1 if n <= 12 else 2]] += line
for k, v in groups.items():
    out(f"cost: {k}", v, "USD", "{:.0f}")
out("BOM lines", len(rows), "", "{:.0f}")
out("BOM total", total, "USD", "{:.0f}")
import yaml  # noqa: E402
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
out("budget_usd", budget, "USD", "{:.0f}")
out("margin (budget minus total)", budget - total, "USD", "{:.0f}")

with open(Path(__file__).with_name("results.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["quantity", "value", "unit"])
    w.writerows(OUT)
print("\nwrote docs/04-calcs/results.csv")
