"""CulvertCrawl prototype build plan pictures (CVC-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|layouts|wiring ...]
With no argument it draws everything; "sheets 101 104" draws only those sheets, "steps 3" only that
step, "joints 5" only that joint. Every picture is drawn from cad/src/model.py (build_components and
build_surface), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png           crawler, every component pulled apart, in build order
    docs/05-build-plan/overview-surface.png   tether reel and surface box, the same way
    cad/drawings/CVC-DWG-101 to 119           making sketches for the made components
    docs/05-build-plan/joint-NN.png           close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png            one picture per assembly step
    docs/05-build-plan/hull-holes.png         hole positions on the hull walls (matplotlib)
    docs/05-build-plan/wiring.png             block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import gc
import math
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, build_surface, derived, bx  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
D = derived(P)
C = build_components(P)
S = build_surface(P)
L, W = P["hull_l"], P["hull_w"]
XF = L / 2
ZC = P["cam_z"]
RX = 180.0                      # reel axle x in the surface frame
ZH = P["reel_hub_z"]
BX0 = RX + 260                  # surface box near end

COL = {"body": "#A8B0B8", "lid": "#0F766E", "ballast": "#57534E", "plate": "#1D4ED8", "belt": "#1F2937", "wheel": "#4B5563",
       "gearbox": "#B45309", "can": "#D97706", "shaft": "#111827", "seal": "#7C3AED", "tray": "#94A3B8", "pi": "#16A34A",
       "deck": "#15803D", "mount": "#F59E0B", "camera": "#2563EB", "dome": "#BAE6FD", "bezel": "#374151", "led": "#FDE047",
       "fbracket": "#9333EA", "fin": "#7DD3FC", "boom": "#38BDF8", "housing": "#6B7280", "diode": "#DC2626",
       "window": "#E0F2FE", "mirror": "#E5E7EB", "cap": "#4B5563", "pen": "#111827", "relief": "#1F2937", "eye": "#9CA3AF",
       "bolt": "#111827", "plug": "#111827",
       "frame": "#0E7490", "spacer": "#64748B", "drum": "#E5E7EB", "flange": "#F97316", "hub": "#6B7280", "axle": "#9CA3AF",
       "bearing": "#374151", "crank": "#B91C1C", "brake": "#111827", "slip": "#7C3AED", "anchor": "#2563EB",
       "bar": "#1D4ED8", "counter": "#16A34A", "case": "#D6D3D1", "caselid": "#E7E5E4", "board": "#D4A373",
       "post": "#6B7280", "panel": "#9CA3AF", "battery": "#C2410C", "strap": "#111827", "boost": "#15803D",
       "monitor": "#0F766E", "estop": "#DC2626", "fuse": "#F59E0B", "conn": "#1F2937", "pad": "#374151"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def c(*ks):
    return fuse([C[k].shape for k in ks])


def s_(*ks):
    return fuse([S[k].shape for k in ks])


def win(shape, x0, x1, y0, y1, z0, z1):
    """The part of shape inside a box (a close-up window or a section)."""
    try:
        r = shape & bx(x0, x1, y0, y1, z0, z1)
        return r if r is not None and r.volume > 1e-3 else None
    except Exception:
        return None


def wparts(items, box):
    out = []
    for name, shape, col in items:
        w = win(shape, *box)
        if w is not None:
            out.append(part(name, w, col))
    return out


def side(shape, sgn):
    """The solids of shape on one side of the centre line (sgn +1 right, -1 left)."""
    return fuse([x for x in shape.solids() if x.center().Y * sgn > 0])


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


# ----------------------------------------------------------------- named components, in build order
def crawler():
    return {
        "body": part("Hull body", c("body"), COL["body"]),
        "lid": part("Hull lid, screws and test plug", c("lid", "lid_screws", "plug"), COL["lid"]),
        "ballast": part("Ballast skid plate", c("ballast"), COL["ballast"]),
        "seals": part("Shaft lip seals (2)", c("seals"), COL["seal"]),
        "motors": part("Worm gear motors (2)", c("gearboxes", "cans", "shafts"), COL["gearbox"]),
        "plates": part("Side plates (2) and screws", c("plate_r", "plate_l", "plate_screws"), COL["plate"]),
        "tracks": part("Belts, sprockets, idlers", c("belts", "wheels", "idler_axles"), COL["belt"]),
        "tray": part("Electronics tray", c("tray"), COL["tray"]),
        "pi": part("Pi 4 and deck", c("pi", "deck"), COL["pi"]),
        "camera": part("Camera mount and camera", c("cam_mount", "camera"), COL["camera"]),
        "dome": part("Dome port", c("dome"), COL["dome"]),
        "bezel": part("Front bezel, LEDs, screws", c("bezel", "leds", "bezel_screws"), COL["bezel"]),
        "fbracket": part("Fin bracket", c("fin_bracket", "fin_screws"), COL["fbracket"]),
        "fin": part("Boom fin", c("fin"), COL["fin"]),
        "boom": part("Boom and laser head", c("boom", "housing", "diode", "window", "mirror", "cap"), COL["boom"]),
        "rear": part("Penetrator, strain relief, eye bolt", c("penetrator", "relief", "eyebolt"), COL["pen"]),
    }


def surface():
    return {
        "frames": part("Side frames (2)", s_("frame_r", "frame_l"), COL["frame"]),
        "spacers": part("Spacer tubes and tie rods", s_("spacers", "frame_rods"), COL["spacer"]),
        "bar": part("Payout counter bar", s_("counter_bar"), COL["bar"]),
        "bearings": part("Flanged bearings (2)", s_("bearings", "bearing_bolts"), COL["bearing"]),
        "drum": part("Drum", s_("drum"), COL["drum"]),
        "flanges": part("Flanges (2) and drum tie rods", s_("flanges", "drum_rods"), COL["flange"]),
        "hubs": part("Shaft hubs (2)", s_("hubs"), COL["hub"]),
        "axle": part("Hollow axle", s_("axle"), COL["axle"]),
        "crank": part("Crank", s_("crank"), COL["crank"]),
        "brake": part("Brake knob", s_("brake"), COL["brake"]),
        "slip": part("Slip ring", s_("slipring"), COL["slip"]),
        "anchor": part("Slip ring anchor", s_("anchor"), COL["anchor"]),
        "counter": part("Payout counter", s_("counter"), COL["counter"]),
        "board": part("Chassis base board", s_("baseboard"), COL["board"]),
        "battery": part("Battery and strap", s_("battery", "strap"), COL["battery"]),
        "boost": part("Boost converter, monitor", s_("boost", "monitor"), COL["boost"]),
        "posts": part("Chassis posts (4)", s_("posts"), COL["post"]),
        "panel": part("Panel, stop, fuses, connectors", s_("panel", "estop", "fuses", "connectors"), COL["panel"]),
        "case": part("Rugged case and lid", s_("case", "case_lid"), COL["case"]),
        "gamepad": part("Gamepad", s_("gamepad"), COL["pad"]),
    }


# ----------------------------------------------------------------- overviews
def overview():
    M = crawler()
    off = {"body": (0, 0, 0), "lid": (0, 0, 160), "ballast": (0, 0, -150), "seals": (-60, -150, 90), "motors": (-280, 0, 150),
           "plates": (0, -250, 60), "tracks": (0, -470, -170), "tray": (30, 0, 300), "pi": (30, 0, 420), "camera": (170, 0, 190),
           "dome": (190, 0, 0), "bezel": (260, 0, 0), "fbracket": (220, 0, -190), "fin": (300, 0, -230), "boom": (330, 0, 150),
           "rear": (-250, 0, -60)}
    order = ["body", "lid", "ballast", "seals", "motors", "plates", "tracks", "tray", "pi", "camera", "dome", "bezel",
             "fbracket", "fin", "boom", "rear"]
    parts = []
    for k in order:
        p = M[k]
        parts.append(mv(p, off[k]))
    r1 = bv.overview(parts, OUT / "overview.png", "CulvertCrawl crawler: every component, pulled apart",
                     subtitle="Numbered in build order (the surface kit is in the next picture). Seen from the front right and above",
                     elev=24, azim=-62, size=(13, 8.5), dpi=150, key=True)
    M = surface()
    off = {"frames": (0, 0, 0), "spacers": (0, 0, -70), "bar": (-140, 0, -40), "bearings": (0, 0, 140), "drum": (-380, 0, 360),
           "flanges": (0, 0, 360), "hubs": (0, 0, 560), "axle": (0, 0, 680), "crank": (0, -230, 560), "brake": (0, -230, -40),
           "slip": (0, 230, 680), "anchor": (0, 170, -20), "counter": (-260, 0, 0),
           "board": (0, 0, 0), "battery": (0, 0, 120), "boost": (0, 0, 120), "posts": (0, 0, 230), "panel": (0, 0, 420),
           "case": (0, 0, -300), "gamepad": (420, 0, -260)}
    order = ["frames", "spacers", "bar", "bearings", "drum", "flanges", "hubs", "axle", "crank", "brake", "slip", "anchor",
             "counter", "board", "battery", "boost", "posts", "panel", "case", "gamepad"]
    parts = [mv(M[k], off[k]) for k in order]
    r2 = bv.overview(parts, OUT / "overview-surface.png", "CulvertCrawl surface kit: every component, pulled apart",
                     subtitle="Tether reel (1 to 13) and surface control box (14 to 20), numbered in build order. Seen from the front right and above",
                     elev=24, azim=-60, size=(12, 8), dpi=150, key=True)
    return [r1, r2]


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = crawler()
    U = surface()
    base = dict(project="CulvertCrawl", date=DATE)
    out = []

    def sheet(no, *a, **k):
        if only and str(no) not in only:
            return
        out.append(bv.component_sheet(*a, dwg_no=f"CVC-DWG-{no}", **k, **base))
        gc.collect()

    sheet(101, Part("Hull body", c("body"), COL["body"]), [M["ballast"], M["plates"], M["lid"], M["bezel"]],
          title="CulvertCrawl hull body: making sketch", material="6061-T6 aluminium block 240 x 88 x 80 mm",
          inset_view=(28, -58),
          notes=["Machine from a 240 x 88 x 80 mm block of 6061; finish 240 x 88 x 74 mm.",
                 "Pocket from the top: 4 mm floor, side and rear walls; 10 mm front wall.",
                 "Leave a rim 12 mm wide and 10 mm deep inside the top all round,",
                 "  drive pads 6 mm thick on the side walls at the rear (gearbox faces),",
                 "  idler bosses 16 mm across, 8 mm proud, and four floor pads 10 mm",
                 "  across and 8 mm tall for the tray. Hole positions: hull-holes picture.",
                 "Rim top: O-ring groove 2.4 wide x 1.3 deep, 8.3 mm in from the outside;",
                 "  ten M4 tapped holes 8 deep, 5 mm in from the outside edge.",
                 "Side walls: 8.2 mm shaft bore and 16 mm seal counterbore 6 deep from",
                 "  outside; two 4.5 mm gearbox screw holes; M6 idler hole 10 deep.",
                 "Front wall: 50 mm camera bore; O-ring groove 56 to 61 mm across,",
                 "  1.3 deep; four M4 bezel holes 7 deep; 5 mm lead hole; M3 camera holes.",
                 "Rear wall: 10.2 mm penetrator hole on the centre line, 55 mm up from the bottom.",
                 "Check: leak test at 20 kPa with the lid, plug and blanks fitted."])

    sheet(102, Part("Hull lid", c("lid"), COL["lid"]), [M["body"], M["bezel"]],
          title="CulvertCrawl hull lid: making sketch", material="6061-T6 aluminium plate 6 mm",
          notes=["Cut 240 x 88 mm from 6 mm plate; square, deburr, break the edges.",
                 "Ten 4.5 mm holes, 5 mm in from the long edges, at 8, 64, 120,",
                 "  176 and 232 mm from the rear end (the same positions as the rim).",
                 "Drill the lid and the hull rim together if you can (clamp, spot",
                 "  through, then tap the rim M4).",
                 "Pressure-test port: 8.5 mm hole tapped M10 x 1, 30 mm from the rear",
                 "  end, on the centre line.",
                 "Underside flat to 0.1 mm over the O-ring land; no scratches across it.",
                 "Fit: sits flush on the rim, O-ring in the rim groove, ten M4 x 12",
                 "  pan-head screws tightened evenly in a cross pattern.",
                 "Check: the lid lies flat on the rim with no rock before the O-ring",
                 "  is fitted."])

    bal = c("ballast")
    sheet(103, Part("Ballast skid plate", bal, COL["ballast"]), [M["body"], M["plates"], M["fbracket"], M["rear"]],
          title="CulvertCrawl ballast skid plate: making sketch", material="Mild steel flat bar 90 x 15 mm, finished 88 x 14 mm",
          inset_view=(-20, -58),
          notes=["Saw 255 mm off 90 x 15 mm flat; mill or file to 255 x 88 x 14 mm.",
                 "Square nose; break every edge about 1 mm.",
                 "Each side: three M4 tapped holes 10 deep, 7 mm up from the bottom",
                 "  face, at 80, 140 and 200 mm from the rear end.",
                 "Nose: two M4 tapped holes 8 deep, 4.5 mm up from the bottom face,",
                 "  6 and 16 mm to the crawler's left of the centre line.",
                 "Rear: one M8 hole, drilled 6.8 and tapped through, on the centre line,",
                 "  9 mm from the rear end (the eye bolt).",
                 "Paint or zinc plate after drilling; keep the top face flat.",
                 "Fit: the hull floor sits on the top face; the hull's front overhangs",
                 "  the nose by 5 mm and the plate sticks out 20 mm behind the hull.",
                 "Check: about 2.45 kg."])

    pr = C["plate_l"].shape
    sheet(104, Part("Side plate", pr, COL["plate"]), [M["body"], M["ballast"], M["motors"]],
          title="CulvertCrawl track side plate (make 2, a left and a right): making sketch",
          material="5052 or 6061 aluminium sheet 3 mm", inset_view=(15, -70),
          notes=["Cut two 230 x 53 mm from 3 mm sheet; round the corners 3 mm.",
                 "Measured from the rear end and up from the bottom edge:",
                 "  shaft hole 10 mm at 18 along, 26 up (retains the lip seal);",
                 "  gearbox screws 4.5 mm at 10 and 38 along, 43 up;",
                 "  idler hole 6.4 mm at 218 along, 26 up;",
                 "  ballast screws 4.5 mm at 58, 118 and 178 along, 6 up.",
                 "Countersink all five screw holes on the outer face (90 degrees) so",
                 "  the heads sit flush: the belt runs 2 mm away.",
                 "The left plate is the mirror of the right: drill them as a pair, then",
                 "  countersink each on its own outer face.",
                 "Fit: inner face flat on the hull side and the ballast side, top edge",
                 "  34 mm below the hull top, rear end 2 mm in from the hull's rear face.",
                 "Check: lay it on the hull side; every hole lines up with its partner."])

    sheet(105, Part("Electronics tray", c("tray"), COL["tray"]), [M["body"], M["pi"]],
          title="CulvertCrawl electronics tray: making sketch", material="5052 aluminium sheet 2 mm",
          inset_view=(35, -58),
          notes=["Cut 104 x 62 mm from 2 mm sheet; deburr.",
                 "Four 3.4 mm holes for the floor pads: 8 and 96 mm from the rear",
                 "  edge, 24 mm each side of the centre line.",
                 "Four 2.7 mm holes for the Pi spacers, on the Pi 4's 58 x 49 mm",
                 "  pattern: 9.5 and 67.5 mm from the rear edge, 24.5 mm each side.",
                 "Also cut the deck: 68 x 56 mm, 2 mm sheet or a printed plate, with the",
                 "  same Pi pattern 3.5 mm in from its rear and side edges.",
                 "Fit: four M3 x 6 screws into the floor pads; the Pi sits on 4 mm",
                 "  spacers; the deck on 20 mm M2.5 standoffs above the Pi.",
                 "A thermal pad between the Pi's heat sink and the deck or tray gives",
                 "  the heat path to the hull.",
                 "Check: the tray drops in past the rim (64 mm opening) without force."])

    sheet(106, Part("Camera mount", c("cam_mount"), COL["mount"]), [M["body"], M["camera"], M["dome"]],
          title="CulvertCrawl camera mount: making sketch", material="PETG or ASA, printed, 100 % infill",
          inset_view=(20, -30),
          notes=["Print flat, 56 wide x 48 tall x 4 mm.",
                 "Centre hole 16 mm for the lens barrel.",
                 "Four 3.4 mm holes on a 40 x 40 mm square, centred on the lens hole,",
                 "  for M3 screws into the front wall.",
                 "Four M2 holes on a 20 x 20 mm square for the camera board standoffs",
                 "  (move them to suit the board you buy).",
                 "Fit: flat on the inside of the front wall, lens hole on the camera",
                 "  axis 62 mm above the track contact line.",
                 "The lens's optical centre must sit on the dome centre (the hull's",
                 "  front face): set it with the lens thread, then lock it.",
                 "Check: the lens barrel passes the bore without touching it."])

    sheet(107, Part("Front bezel", c("bezel"), COL["bezel"]), [M["body"], M["dome"], M["camera"]],
          title="CulvertCrawl front bezel: making sketch", material="6061-T6 aluminium bar 90 mm diameter",
          inset_view=(15, -35),
          notes=["Turn a ring 88 mm outside, 62 mm bore, 10 mm thick.",
                 "Back face: recess 73 mm across, 5 mm deep, for the dome flange.",
                 "Front face: eight pockets 10.5 mm across, 3 deep, on a 75 mm",
                 "  circle, starting 22.5 degrees from the top, every 45 degrees.",
                 "  None sits at the bottom, where the fin passes.",
                 "Four 4.5 mm holes on an 80 mm circle at 45, 135, 225, 315 degrees.",
                 "From each pocket drill 2 mm through to a 2 x 2 mm wire groove on the",
                 "  back face, and run it out at the crawler's lower right, by the lead hole.",
                 "Fit: back face flat on the front wall, recess over the dome flange;",
                 "  four M4 x 16 screws. LEDs bonded in the pockets, wired in series,",
                 "  then the pockets and groove potted with clear epoxy.",
                 "Check: the dome flange is gripped evenly; the dome does not turn."])

    fb = C["fin_bracket"].shape
    sheet(108, Part("Fin bracket", fb, COL["fbracket"]), [M["ballast"], M["fin"], M["bezel"]],
          title="CulvertCrawl fin bracket: making sketch", material="Aluminium equal angle 30 x 30 x 3 mm",
          view_shape=b.Pos(0, 0, 0) * fb, inset_view=(10, -40),
          notes=["Cut 9 mm off 30 x 30 x 3 mm angle (the angle's length is the",
                 "  bracket's height); deburr.",
                 "Back leg (on the ballast nose): two 4.5 mm holes, 4.5 mm up,",
                 "  9 and 19 mm from the corner.",
                 "Forward leg (carries the fin): two 3.2 mm holes, 4.5 mm up,",
                 "  20 and 26 mm forward of the back face.",
                 "Fit: back leg flat on the ballast nose, corner on the centre line,",
                 "  back leg to the crawler's left; two M4 x 10 screws into the nose.",
                 "The forward leg stands just right of the centre line; the fin",
                 "  bolts to its left face. The bracket top is 1 mm below the bezel.",
                 "Check: the forward leg is square to the ballast nose."])

    fin = C["fin"].shape
    sheet(109, Part("Boom fin", fin, COL["fin"]), [M["fbracket"], M["boom"], M["dome"], M["bezel"]],
          title="CulvertCrawl boom fin: making sketch", material="Clear cast acrylic sheet 8 mm",
          inset_view=(15, -60),
          notes=["Laser cut or saw and file from 8 mm clear cast acrylic.",
                 "Outline, measured from the bezel front face (x) and up from the",
                 "  track contact line (z): (1, 8), (15, 8), (132, 53), (29, 53), (1, 25).",
                 "The top edge from 29 to 132 lies under the boom; the sloping back",
                 "  edge keeps 4 mm from the dome.",
                 "Two 3.2 mm holes 4.5 mm up, 4 and 10 mm from the back edge.",
                 "Polish the top edge flat and square for bonding.",
                 "Fit: left face of the bracket's forward leg on the fin's right face,",
                 "  two M3 x 16 bolts with nyloc nuts.",
                 "The boom is solvent-welded along the top edge (see the boom sketch).",
                 "Check: the fin stands square to the hull top."])

    bm = C["boom"].shape
    sheet(110, Part("Boom tube", bm, COL["boom"]), [M["fin"], M["dome"], M["boom"]],
          title="CulvertCrawl boom tube: making sketch", material="Clear acrylic tube 18 mm outside, 12 mm inside",
          view_shape=b.Pos(-200, 0, -ZC) * bm, inset_view=(15, -60),
          notes=["Cut 233 mm of 18 x 12 mm clear acrylic tube; square both ends.",
                 "Root end: solvent-weld a 12 mm acrylic plug 3 mm deep.",
                 "Drill a 3 mm hole in the underside 8 mm from the root end for the",
                 "  laser's wires; seal it with clear silicone after threading them.",
                 "Fit: the root end sits 37 mm in front of the hull's front face,",
                 "  7 mm clear of the dome. Solvent-weld the tube along the fin's top",
                 "  edge, on the camera axis 62 mm up.",
                 "The front end goes 10 mm into the diode housing (bond with epoxy).",
                 "Keep the tube clean and unscratched: the camera looks through it."])

    head = c("housing", "window", "cap")
    sheet(111, Part("Laser head", head, COL["housing"]), [M["boom"], M["fin"]],
          title="CulvertCrawl laser head (housing, window, end cap): making sketch",
          material="6061 aluminium bar 26 mm; clear acrylic tube 26 x 22 mm", view_shape=b.Pos(-380, 0, -ZC) * head,
          inset_view=(15, -60),
          notes=["Diode housing: turn 26 mm bar to 30 mm long. Bore 18 mm, 10 deep,",
                 "  for the boom; bore 12 mm through for the diode module;",
                 "  counterbore 22 mm, 4 deep, at the front for the window spigot.",
                 "Window: 20 mm of 26 x 22 mm clear acrylic tube, plus a 4 mm spigot",
                 "  ring 22 x 18 mm solvent-welded inside each end.",
                 "End cap: turn 26 mm bar to a 3 mm disc with a 4 mm spigot 22 x 18;",
                 "  bond the cone mirror's stem to its centre, apex facing back.",
                 "The laser leaves the cone 300 mm in front of the dome centre:",
                 "  set this with the diode's focus and a card before bonding the cap.",
                 "Fit: boom bonded in the housing, diode clamped in its bore with a",
                 "  drop of silicone, window and cap bonded with clear epoxy.",
                 "Check: a sharp, even ring on a card held round the window."])

    fr = S["frame_r"].shape
    sheet(112, Part("Reel side frame", fr, COL["frame"]), [U["drum"], U["flanges"], U["bearings"], U["spacers"]],
          title="CulvertCrawl reel side frame (make 2): making sketch", material="6061 aluminium plate 6 mm",
          view_shape=b.Pos(-RX, 0, 0) * fr, inset_view=(20, -50),
          notes=["Cut two from 6 mm plate (jigsaw with a metal blade, or waterjet):",
                 "  base 320 mm, 30 mm upright at each end, sloping sides up to a",
                 "  top 80 mm wide, 262 mm above the base.",
                 "Window: triangle 190 mm wide at 45 mm up, apex 155 mm up.",
                 "Axle hole 21 mm, 230 mm up on the centre line.",
                 "Bearing bolt holes 8.4 mm, 27 mm above and below the axle hole.",
                 "Spacer rod holes 6.4 mm: 130 mm each side of centre, 18 up; and",
                 "  on the centre line 30 up.",
                 "Right frame only: 5.5 mm hole 175 mm up for the slip ring anchor.",
                 "Left frame only: M8 tapped hole 100 mm forward of and 100 mm below",
                 "  the axle, for the brake.",
                 "Also cut three spacer tubes 20 x 2 mm, 152 mm long; cut one of them",
                 "  into two 63.5 mm halves for the front foot (the counter bar sits",
                 "  between them). Check: both frames stand square on a flat bench."])

    sheet(113, Part("Reel drum", s_("drum"), COL["drum"]), [U["flanges"], U["frames"]],
          title="CulvertCrawl reel drum: making sketch", material="PVC pressure pipe 225 mm outside, 5.5 mm wall",
          view_shape=b.Pos(-RX, 0, -ZH) * S["drum"].shape, inset_view=(20, -50),
          notes=["Cut 104 mm of 225 mm PVC pipe; square both ends on a disc sander.",
                 "Tether entry: a 10 mm hole through the wall, mid-width; round its",
                 "  edges so the tether cannot chafe.",
                 "Fit: clamped between the two flanges by the four tie rods; it does",
                 "  not need glue.",
                 "Capacity: 60 m of 7 mm tether in about six layers, leaving 5 mm of",
                 "  flange above the top layer.",
                 "Check: both ends square to the pipe axis within 0.5 mm."])

    fl = S["flanges"].shape.solids()[0]
    sheet(114, Part("Reel flange", fl, COL["flange"]), [U["drum"], U["hubs"], U["frames"]],
          title="CulvertCrawl reel flange (make 2): making sketch", material="HDPE sheet 6 mm",
          view_shape=b.Pos(-RX, 0, -ZH) * fl, inset_view=(20, -50),
          notes=["Cut two 320 mm discs from 6 mm HDPE (router on a pivot, or jigsaw",
                 "  and sand). Mark the centre.",
                 "Centre hole 20.4 mm for the axle.",
                 "Four 6.4 mm tie rod holes on a 200 mm circle, at 45, 135, 225 and",
                 "  315 degrees.",
                 "Four 5.5 mm hub holes on a 38 mm circle, at the same angles (check",
                 "  against the hub you buy).",
                 "Fit: one each side of the drum, tie rods through both, nuts and",
                 "  washers outside; the shaft hub bolts to the outer face.",
                 "Check: the flanges run true within 2 mm when the reel turns."])

    sheet(115, Part("Crank", s_("crank"), COL["crank"]), [U["axle"], U["bearings"], U["frames"]],
          title="CulvertCrawl reel crank: making sketch", material="Aluminium bar 28 mm and flat bar 12 x 6 mm; 18 mm handle",
          view_shape=b.Pos(-RX, 0, -ZH) * S["crank"].shape, inset_view=(15, -30),
          notes=["Hub: 14 mm of 28 mm round bar, bored 20 mm, with an M6 set screw.",
                 "Arm: 12 x 6 mm flat bar 83 mm long, screwed or welded to the hub,",
                 "  its far end 95 mm from the axle centre.",
                 "Handle: 18 mm round bar or a bought crank handle, 50 mm long, on an",
                 "  M8 shoulder bolt through the arm 90 mm from the axle, free to turn.",
                 "Fit: hub on the left end of the axle, against the bearing; set screw",
                 "  onto a flat filed on the axle.",
                 "Check: the handle turns freely on its bolt."])

    sheet(116, Part("Slip ring anchor", s_("anchor"), COL["anchor"]), [U["slip"], U["frames"], U["bearings"]],
          title="CulvertCrawl slip ring anchor bracket: making sketch", material="Aluminium flat bar 20 x 3 mm",
          view_shape=b.Pos(-RX, 0, -ZH) * S["anchor"].shape, inset_view=(15, 30),
          notes=["Bend 20 x 3 mm flat bar into a Z: a 30 mm foot, a 45 mm run",
                 "  outward and a 58 mm upright (sizes from the drawing).",
                 "Foot: one 5.5 mm hole 17 mm above its bottom end.",
                 "Upright: file a slot at its top to take the slip ring's anti-rotation",
                 "  tab (or tie the stator lead to it).",
                 "Fit: foot flat on the outside of the right frame, one M5 bolt; the",
                 "  upright touches the underside of the slip ring body.",
                 "It stops the stator turning; it must not clamp it tight.",
                 "Check: the reel turns a full turn and the stator stays still."])

    sheet(117, Part("Payout counter bar", s_("counter_bar"), COL["bar"]), [U["counter"], U["spacers"], U["frames"]],
          title="CulvertCrawl payout counter bar: making sketch", material="Aluminium flat bar 25 x 6 mm",
          view_shape=b.Pos(-RX, 0, 0) * S["counter_bar"].shape, inset_view=(20, -70),
          notes=["Cut 132 mm of 25 x 6 mm flat bar; deburr.",
                 "6.4 mm hole 10 mm from the bottom end, on the centre line (the front",
                 "  foot tie rod goes through it).",
                 "Two 5.5 mm holes for the counter, 97 and 122 mm from the bottom end.",
                 "Fit: stands upright between the two halves of the front spacer tube;",
                 "  the tie rod clamps it. The counter bolts to its front face.",
                 "Check: the bar stands square to the base of the frames."])

    sheet(118, Part("Chassis base board", s_("baseboard"), COL["board"]), [U["battery"], U["posts"], U["boost"]],
          title="CulvertCrawl surface box chassis base board: making sketch", material="Exterior plywood 6 mm (or HDPE)",
          view_shape=b.Pos(-BX0, 0, 0) * S["baseboard"].shape, inset_view=(35, -60),
          notes=["Cut 394 x 314 mm from 6 mm exterior plywood; seal with varnish.",
                 "Check the inside of your case first: the board must drop in with",
                 "  about 2 mm all round. Trim corners to clear the case's mouldings.",
                 "Four posts: 20 mm square aluminium tube, 106 mm long, centred",
                 "  22 mm in from each side; screw up from below into a plug in each.",
                 "Battery bay: 181 x 167 mm, 22 mm from the near end, centred.",
                 "Two strap slots 25 x 3 mm either side of the bay, 80 to 105 mm",
                 "  along it.",
                 "Mark the boost converter and current monitor positions from the",
                 "  wiring picture; fix them with M4 screws and nuts.",
                 "Check: the chassis lifts out by the posts with nothing attached to",
                 "  the case."])

    sheet(119, Part("Chassis panel", s_("panel"), COL["panel"]), [U["posts"], U["board"], U["battery"], U["boost"]],
          title="CulvertCrawl surface box panel: making sketch", material="5052 aluminium sheet 2 mm",
          view_shape=b.Pos(-BX0, 0, -118) * S["panel"].shape, inset_view=(40, -60),
          notes=["Cut 394 x 314 mm from 2 mm sheet; round the corners 5 mm.",
                 "Holes, from the panel's end nearest the reel, and from the centre line",
                 "  (stop side marked A, connector side marked B):",
                 "  emergency stop 22 mm at 322 along, 100 A; fuse holders 16 mm",
                 "  at 242 and 192 along, 100 A; tether connector 24 mm at 322, 40 B;",
                 "  Ethernet 24 mm at 322, 100 B; charge port 16 mm at 242, 100 B;",
                 "  power switch 12 mm at 172, 100 B.",
                 "Four 4.5 mm holes 22 mm in from each corner for the posts.",
                 "Label every part on the panel; the stop gets a yellow ring label.",
                 "Fit: on the four posts with M4 screws; the lid closes over the",
                 "  stop with 19 mm to spare.",
                 "Check: the lid closes and latches with every part fitted."])
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []

    def jn(n, items, box, title, sub, **kw):
        if only and str(n) not in only:
            return
        ps = wparts(items, box)
        out.append(bv.joint(ps, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))
        gc.collect()

    zt = P["hull_z0"] + P["hull_h"]
    g0, g1, gd = P["oring_groove"]
    oring = bx(-XF + g0 + 0.2, XF - g0 - 0.2, -W / 2 + g0 + 0.2, W / 2 - g0 - 0.2, zt - gd, zt) - \
        bx(-XF + g1 - 0.2, XF - g1 + 0.2, -W / 2 + g1 - 0.2, W / 2 - g1 + 0.2, zt - gd - 1, zt + 1)
    # 1 lid on the rim: cut across the hull at a lid screw
    jn(1, [("Hull wall and rim", c("body"), COL["body"]), ("Lid", c("lid"), COL["lid"]),
           ("O-ring in the rim groove", oring, COL["seal"]),
           ("M4 lid screw, outside the O-ring", c("lid_screws"), COL["bolt"])],
       (50, 56, 10, 46, zt - 22, zt + 10), "lid on the hull rim (cut across at a screw)",
       "The O-ring sits in the groove in the rim top, inside the screw line; the lid is flush with the hull sides",
       elev=8, azim=-2, size=(8, 6))
    # 2 drive: cut horizontally through the shaft axis
    zs = P["track_r"]
    jn(2, [("Hull side wall and drive pad", c("body"), COL["body"]), ("Gearbox (output face on the pad)", c("gearboxes"), COL["gearbox"]),
           ("Output shaft, 8 mm", c("shafts"), COL["shaft"]), ("Lip seal in its counterbore", c("seals"), COL["seal"]),
           ("Side plate (holds the seal in)", c("plate_r"), COL["plate"]), ("Sprocket", c("wheels"), COL["wheel"]),
           ("Belt", c("belts"), COL["belt"]), ("Gearbox screws, countersunk", c("plate_screws"), COL["bolt"])],
       (-130, -70, 10, 90, 0, zs), "drive shaft through the side wall (cut level with the shaft)",
       "Left side, seen from above. Gearbox face on the pad; seal in the wall, held by the side plate; sprocket on the shaft",
       elev=75, azim=-90, size=(8, 6))
    # 3 side plate to hull and ballast: cut across at the middle ballast screw
    jn(3, [("Hull side wall", c("body"), COL["body"]), ("Ballast plate", c("ballast"), COL["ballast"]),
           ("Side plate", c("plate_r"), COL["plate"]), ("M4 countersunk screw into the ballast", c("plate_screws"), COL["bolt"]),
           ("Belt", c("belts"), COL["belt"])],
       (-3, 3, 20, 90, 0, 70), "side plate on the hull and the ballast plate (cut across at a screw)",
       "Seen from the front. The plate lies flat on both; its screws tie the hull to the ballast plate",
       elev=5, azim=-1, size=(8, 6))
    # 4 idler axle into the hull boss: cut horizontally at the axle
    jn(4, [("Hull side wall and idler boss", c("body"), COL["body"]), ("Side plate", c("plate_r"), COL["plate"]),
           ("Idler", c("wheels"), COL["wheel"]), ("M6 shoulder bolt (the idler axle)", c("idler_axles"), COL["bolt"]),
           ("Belt", c("belts"), COL["belt"])],
       (75, 125, 20, 90, 0, zs), "idler axle into the hull boss (cut level with the axle)",
       "Left side, seen from above. The bolt head sits in the idler hub; its thread stops 2 mm short of the inside",
       elev=75, azim=-90, size=(8, 6))
    # 5 front end: vertical cut through the axis
    jn(5, [("Front wall", c("body"), COL["body"]), ("Dome port and flange", c("dome"), COL["dome"]),
           ("Front bezel", c("bezel"), COL["bezel"]), ("LED in its pocket", c("leds"), COL["led"]),
           ("Camera mount", c("cam_mount"), COL["mount"]), ("Camera and lens", c("camera"), COL["camera"]),
           ("Lid", c("lid"), COL["lid"])],
       (85, 155, 0, 50, 10, 108), "front end: dome, bezel and camera (cut on the centre line)",
       "Seen from the left. The bezel clamps the dome flange on an O-ring; the lens centre sits at the dome centre",
       elev=8, azim=-75, size=(8, 6.5))
    # 6 fin bracket and fin root
    bxn = P["ballast_x"][1]
    jn(6, [("Ballast plate nose", c("ballast"), COL["ballast"]), ("Fin bracket", c("fin_bracket"), COL["fbracket"]),
           ("Boom fin", c("fin"), COL["fin"]), ("Screws: M4 into the nose, M3 through the fin", c("fin_screws"), COL["bolt"])],
       (bxn - 12, bxn + 40, -30, 30, 0, 32), "fin bracket on the ballast nose, fin bolted to it",
       "Seen from the front left and above (bezel left out). The bracket top stays 1 mm below the bezel",
       elev=22, azim=-45, size=(8, 6))
    # 7 fin under the boom
    jn(7, [("Boom fin", c("fin"), COL["fin"]), ("Boom tube, solvent-welded on the fin", c("boom"), COL["boom"]),
           ("Dome port", c("dome"), COL["dome"]), ("Front bezel", c("bezel"), COL["bezel"])],
       (118, 280, -30, 30, 0, 95), "fin under the boom",
       "Seen from the left. The fin's top edge carries the boom on the camera axis; its back edge clears the dome by 4 mm",
       elev=6, azim=-90, size=(9, 5.5))
    # 8 laser head, cut on the centre line
    rx_ = D["ring_x"]
    jn(8, [("Boom tube", c("boom"), COL["boom"]), ("Diode housing", c("housing"), COL["housing"]),
           ("Laser diode module", c("diode"), COL["diode"]), ("Window tube", c("window"), COL["window"]),
           ("Cone mirror", c("mirror"), COL["mirror"]), ("End cap", c("cap"), COL["cap"])],
       (rx_ - 50, rx_ + 15, 0, 20, ZC - 20, ZC + 20), "laser head (cut on the centre line)",
       "Seen from the left. The beam runs forward to the cone and leaves through the window as a disc, 300 mm ahead of the dome centre",
       elev=10, azim=-80, size=(8, 5.5))
    # 9 rear: penetrator, strain relief, eye bolt
    jn(9, [("Hull rear wall", c("body"), COL["body"]), ("Ballast plate", c("ballast"), COL["ballast"]),
           ("Tether penetrator", c("penetrator"), COL["pen"]), ("Strain relief and tether", c("relief"), COL["relief"]),
           ("Eye bolt (strength member tied here)", c("eyebolt"), COL["eye"]), ("Gearbox", c("gearboxes"), COL["gearbox"])],
       (-200, -95, 0, 60, 0, 100), "rear: tether penetrator, strain relief and eye bolt (cut on the centre line)",
       "Seen from the left and behind. The aramid strength member is tied to the eye; the penetrator only seals",
       elev=12, azim=-120, size=(8, 6))
    # 10 tray and electronics on the floor pads
    jn(10, [("Hull floor and pads", c("body"), COL["body"]), ("Electronics tray", c("tray"), COL["tray"]),
            ("Pi 4 on spacers", c("pi"), COL["pi"]), ("Deck on standoffs", c("deck"), COL["deck"]),
            ("Motor can", c("cans"), COL["can"])],
       (-20, 105, 0, 40, 20, 90), "electronics tray and stack (cut on the centre line)",
       "Seen from the left. Tray on four floor pads; Pi on 4 mm spacers; deck on 20 mm standoffs",
       elev=10, azim=-75, size=(8, 6))
    # 11 reel bearing and hub, horizontal cut through the axle
    jn(11, [("Side frame", s_("frame_r"), COL["frame"]), ("Flanged bearing", s_("bearings"), COL["bearing"]),
            ("Hollow axle", s_("axle"), COL["axle"]), ("Shaft hub", s_("hubs"), COL["hub"]),
            ("Flange", s_("flanges"), COL["flange"]), ("Drum", s_("drum"), COL["drum"]),
            ("Slip ring", s_("slipring"), COL["slip"])],
       (RX - 45, RX + 45, 30, 150, ZH - 40, ZH), "reel bearing, hub and slip ring, right side (cut level with the axle)",
       "Seen from above. Hub bolted to the flange; axle turns in the bearing; slip ring rotor on the axle end",
       elev=80, azim=-90, size=(8, 6))
    # 12 drum between flanges with a tie rod
    jn(12, [("Drum", s_("drum"), COL["drum"]), ("Flanges", s_("flanges"), COL["flange"]),
            ("Tie rod, M6, nuts outside", s_("drum_rods"), COL["bolt"]), ("Hubs", s_("hubs"), COL["hub"]),
            ("Axle", s_("axle"), COL["axle"])],
       (RX - 160, RX, -70, 70, ZH - 5, ZH + 160), "drum clamped between the flanges (cut through the axle)",
       "Seen from the front. Four tie rods squeeze the drum between the flanges",
       elev=10, azim=-95, size=(8, 6))
    # 13 brake on the left frame
    jn(13, [("Left side frame", s_("frame_l"), COL["frame"]), ("Brake knob, screw and pad", s_("brake"), COL["brake"]),
            ("Flange", s_("flanges"), COL["flange"])],
       (RX - 140, RX - 60, -105, -40, ZH - 140, ZH - 60), "brake on the left frame",
       "Seen from the left and in front. Turn the knob in to press the pad on the flange; 0.5 mm clear when off",
       elev=15, azim=-140, size=(7, 5.5))
    # 14 payout counter bar on the front spacer
    jn(14, [("Front spacer halves", s_("spacers"), COL["spacer"]), ("Tie rod", s_("frame_rods"), COL["bolt"]),
            ("Payout counter bar", s_("counter_bar"), COL["bar"]), ("Payout counter", s_("counter"), COL["counter"]),
            ("Side frames", s_("frame_r", "frame_l"), COL["frame"])],
       (RX - 200, RX - 110, -90, 90, 0, 145), "payout counter on its bar",
       "Seen from the front left. The bar is clamped between the two halves of the front spacer by the tie rod",
       elev=20, azim=-140, size=(8, 6))
    # 15 surface box chassis corner, cut
    jn(15, [("Case floor", win(s_("case"), BX0, BX0 + 410, -165, 165, 0, 6), COL["case"]), ("Base board", s_("baseboard"), COL["board"]),
            ("Post", s_("posts"), COL["post"]), ("Panel", s_("panel"), COL["panel"]),
            ("Battery and strap", s_("battery", "strap"), COL["battery"]), ("Fuse holders", s_("fuses"), COL["fuse"]),
            ("Emergency stop", s_("estop"), COL["estop"])],
       (BX0 + 6, BX0 + 404, -159, -60, 0, 160), "surface box chassis (case walls left out, cut 60 mm left of the centre line)",
       "Seen from the near side. Base board on the case floor, posts up to the panel; nothing is screwed to the case",
       elev=14, azim=-70, size=(9, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = crawler()
    U = surface()
    out = []

    def st(n, done, new, title, sub, **kw):
        if only and str(n) not in only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))
        gc.collect()

    hull = M["body"]
    st(1, [M["ballast"]], [mv(hull, (0, 0, 120))], "hull onto the ballast plate",
       "Hull floor flat on the plate, hull front 5 mm ahead of its nose; clamp until the side plates are on",
       elev=22, azim=-55)
    st(2, [hull, M["ballast"]], [mv(part("Lip seal, right", side(c("seals"), -1), COL["seal"]), (0, -70, 0)),
                                 mv(part("Lip seal, left", side(c("seals"), 1), COL["seal"]), (0, 70, 0))],
       "shaft lip seals into the side walls",
       "Grease the lips; press each seal into its counterbore from outside, lips facing out, flush with the wall",
       elev=20, azim=-30)
    gbs = C["gearboxes"].shape.solids()
    st(3, [hull, M["ballast"], M["seals"]], [mv(M["motors"], (0, 0, 120))], "worm gear motors into the hull",
       "Lower each motor near the centre line, then slide it out until its output face sits on the pad and the shaft passes the seal",
       elev=40, azim=-60, label_done=False)
    done = [hull, M["ballast"], M["seals"], M["motors"]]
    st(4, done, [mv(part("Right side plate and screws", c("plate_l") + side(c("plate_screws"), -1), COL["plate"]), (0, -90, 0)),
                 mv(part("Left side plate and screws", c("plate_r") + side(c("plate_screws"), 1), COL["plate"]), (0, 90, 0))],
       "side plates on",
       "Two M4 countersunk screws through each plate into its gearbox (small O-rings under the plate), three into the ballast side",
       elev=18, azim=-60, label_done=False)
    done += [M["plates"]]
    st(5, done, [mv(part("Right track: belt, sprocket, idler and axle bolt", side(c("belts", "wheels", "idler_axles"), -1), COL["belt"]), (0, -110, 0)),
                 mv(part("Left track", side(c("belts", "wheels", "idler_axles"), 1), COL["belt"]), (0, 110, 0))],
       "sprockets, idlers and belts",
       "Sprocket on each shaft (set screw on the flat); idler on its M6 shoulder bolt into the hull boss with the belt round both",
       elev=18, azim=-60, label_done=False)
    done += [M["tracks"]]
    st(6, done, [mv(M["tray"], (0, 0, 120))], "electronics tray onto the floor pads",
       "Four M3 x 6 screws into the pads",
       elev=45, azim=-60, label_done=False)
    st(7, done + [M["tray"]], [mv(part("Pi 4 on spacers", c("pi"), COL["pi"]), (0, 0, 100)),
                               mv(part("Deck with driver and converters", c("deck"), COL["deck"]), (0, 0, 200))],
       "Pi 4 and deck",
       "Pi on four 4 mm spacers; deck on 20 mm M2.5 standoffs; then wire as the wiring picture shows",
       elev=45, azim=-60, label_done=False)
    done += [M["tray"], M["pi"]]
    st(8, done, [mv(part("Camera mount and camera", c("cam_mount", "camera"), COL["camera"]), (-90, 0, 0))],
       "camera mount and camera onto the front wall",
       "Four M3 screws into the front wall from inside; lens through the bore, its centre at the hull's front face",
       elev=45, azim=-30, label_done=False)
    done += [M["camera"]]
    st(9, done, [mv(M["dome"], (80, 0, 0))], "dome port onto the front wall",
       "O-ring greased in the front wall groove; dome flange centred over it",
       elev=15, azim=-35, label_done=False)
    done += [M["dome"]]
    st(10, done, [mv(M["bezel"], (80, 0, 0))], "front bezel over the dome",
       "LED leads through the potted lead hole first; four M4 x 16 screws, tightened evenly until the flange is gripped",
       elev=15, azim=-35, label_done=False)
    done += [M["bezel"]]
    st(11, done, [mv(M["fbracket"], (60, 0, 0))], "fin bracket onto the ballast nose",
       "Two M4 x 10 screws into the nose; forward leg just right of the centre line",
       elev=20, azim=-40, label_done=False)
    done += [M["fbracket"]]
    st(12, done, [mv(part("Fin with the boom and laser head bonded on", c("fin", "boom", "housing", "diode", "window", "mirror", "cap"),
                          COL["fin"]), (0, 80, 0))],
       "fin, boom and laser head",
       "Two M3 x 16 bolts through the fin and the bracket, nyloc nuts; laser leads down the fin's back edge",
       elev=20, azim=-50, label_done=False)
    done += [M["fin"], M["boom"]]
    st(13, done, [mv(M["rear"], (-120, 0, 0))], "tether penetrator, strain relief and eye bolt",
       "Penetrator nut inside; eye bolt into the ballast plate; tie the aramid to the eye with slack in the cable",
       elev=20, azim=-130, label_done=False)
    done += [M["rear"]]
    st(14, done, [mv(M["lid"], (0, 0, 120))], "lid on",
       "Desiccant in, O-ring clean and greased in the rim groove; ten M4 screws in a cross pattern; then the leak test",
       elev=25, azim=-55, label_done=False)
    # surface kit
    st(15, [], [mv(part("Side frames (2)", s_("frame_r", "frame_l"), COL["frame"]), (0, 0, 0)),
                mv(part("Spacer tubes, tie rods and counter bar", s_("spacers", "frame_rods", "counter_bar"), COL["spacer"]), (0, 0, -80))],
       "reel frame", "Three spacer tubes between the frames on M6 tie rods; the counter bar between the two halves of the front spacer",
       elev=22, azim=-55)
    fr = [U["frames"], U["spacers"], U["bar"]]
    st(16, fr, [mv(U["bearings"], (0, 0, 80))], "bearings onto the frames",
       "One flanged bearing on the outside of each frame, two M8 bolts each, set screws loose for now",
       elev=22, azim=-55, label_done=False)
    fr += [U["bearings"]]
    st(17, [U["drum"]], [mv(part("Flange, left", side(s_("flanges"), -1), COL["flange"]), (0, -110, 0)),
                         mv(part("Flange, right", side(s_("flanges"), 1), COL["flange"]), (0, 110, 0)),
                         mv(part("Shaft hubs and tie rods", s_("hubs", "drum_rods"), COL["hub"]), (0, 0, 220))],
       "drum, flanges and hubs", "Drum between the flanges on four M6 tie rods; one shaft hub bolted to each flange's outer face",
       elev=20, azim=-55)
    st(18, fr, [mv(part("Drum assembly", s_("drum", "flanges", "drum_rods", "hubs"), COL["flange"]), (0, 0, 250)),
                mv(U["axle"], (0, -260, 0))],
       "drum into the frame, axle through",
       "Hold the drum between the frames; slide the axle in through one bearing, both hubs and the other bearing; tighten the set screws",
       elev=22, azim=-55, label_done=False)
    fr += [U["drum"], U["flanges"], U["hubs"], U["axle"]]
    st(19, fr, [mv(U["crank"], (0, -120, 0)), mv(U["brake"], (0, -80, 0)), mv(U["slip"], (0, 120, 0)), mv(U["anchor"], (0, 80, 0))],
       "crank, brake, slip ring and anchor",
       "Crank on the left axle end; brake knob into the left frame; slip ring rotor on the right axle end; anchor catches its stator",
       elev=22, azim=-35, label_done=False)
    fr += [U["crank"], U["brake"], U["slip"], U["anchor"]]
    st(20, fr, [mv(U["counter"], (-120, 0, 0))], "payout counter onto its bar",
       "Two M5 bolts; the tether runs between the wheel and the pinch roller",
       elev=22, azim=-55, label_done=False)
    st(21, [U["board"]], [mv(U["battery"], (0, 0, 120)), mv(U["boost"], (0, 0, 120)), mv(U["posts"], (0, 0, 200))],
       "battery, converter and posts onto the base board",
       "Battery on its side in its bay, strapped down; converter and monitor on M4 screws; four posts screwed up from below",
       elev=30, azim=-55, label_done=False)
    st(22, [U["board"], U["battery"], U["boost"], U["posts"]], [mv(U["panel"], (0, 0, 150))],
       "panel onto the posts",
       "Stop, fuse holders, connectors and switch fitted and wired to the panel first; four M4 screws into the posts",
       elev=30, azim=-55, label_done=False)
    st(23, [part("Rugged case, lid open (not shown)", s_("case"), COL["case"])], [mv(part("Chassis (base board, posts, panel and parts)", s_("baseboard", "posts", "panel", "battery", "strap",
                                                                                 "boost", "monitor", "estop", "fuses", "connectors"), COL["panel"]),
                             (0, 0, 250))],
       "chassis into the case", "Drop it in; nothing is screwed to the case. Close the lid and check it latches",
       elev=30, azim=-55, label_done=True)
    return out


# ----------------------------------------------------------------- hull hole layout
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    z0, H = P["hull_z0"], P["hull_h"]
    fig = plt.figure(figsize=(12, 9), dpi=150)
    fig.text(0.03, 0.975, "Hull body: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.945, "Sizes in mm, taken from the model. Heights are up from the hull's bottom face (the hull bottom is 22 mm above the track contact line).",
             fontsize=8.5, color=MUT, va="top")

    def holes(ax, items):
        for (u, v, d, lab, side) in items:
            ax.add_patch(Circle((u, v), d / 2, fc="white", ec=INK, lw=1))
            ax.plot([u - d / 2 - 2, u + d / 2 + 2], [v, v], color=MUT, lw=0.4)
            ax.plot([u, u], [v - d / 2 - 2, v + d / 2 + 2], color=MUT, lw=0.4)
            if lab:
                dx = {"r": d / 2 + 3, "l": -d / 2 - 3, "u": 0, "d": 0}[side]
                dy = {"r": 0, "l": 0, "u": d / 2 + 3, "d": -d / 2 - 3}[side]
                ax.text(u + dx, v + dy, lab, fontsize=7, color=AC, ha={"r": "left", "l": "right", "u": "center", "d": "center"}[side],
                        va={"r": "center", "l": "center", "u": "bottom", "d": "top"}[side])

    # right side wall, seen from the right (rear at the left)
    ax = fig.add_axes([0.03, 0.50, 0.62, 0.40]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), L, H, fc="#F3F4F6", ec=INK, lw=1.2))
    ax.text(L / 2, H + 6, "Right side wall, seen from the right (rear end at the left). The left wall is the mirror image.",
            ha="center", fontsize=8.5, color=INK)
    zs = P["track_r"] - z0
    holes(ax, [(L / 2 - 100, zs, 16, "shaft 8.2 through, seal 16 x 6 deep (20 along, 13 up)", "r"),
               (L / 2 - 108, 52 - z0, 4.5, "gearbox 4.5\n(12 along, 30 up)", "l"),
               (L / 2 - 80, 52 - z0, 4.5, "gearbox 4.5\n(40 along, 30 up)", "r"),
               (L / 2 + 100, zs, 6, "idler M6, 10 deep\n(220 along, 13 up)", "u")])
    ax.text(L / 2 - 91, H - 8, "drive pad inside: 6 to 50 along, full height to 46 up", fontsize=7, color=MUT, ha="center")
    ax.text(L / 2 + 100, H - 8, "idler boss inside, 16 across", fontsize=7, color=MUT, ha="center")
    ax.set_xlim(-30, L + 30); ax.set_ylim(-20, H + 14)
    # front wall, seen from the front
    ax = fig.add_axes([0.66, 0.50, 0.32, 0.40]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-W / 2, 0), W, H, fc="#F3F4F6", ec=INK, lw=1.2))
    ax.text(0, H + 6, "Front wall, seen from the front", ha="center", fontsize=8.5, color=INK)
    zc = ZC - z0
    ax.add_patch(Circle((0, zc), 25, fc="white", ec=INK, lw=1))
    ax.add_patch(Circle((0, zc), 30.4, fc="none", ec=MUT, lw=0.6, ls="--"))
    ax.text(0, zc, "bore 50\n(40 up)", ha="center", va="center", fontsize=7, color=AC)
    ax.text(0, -7, "O-ring groove 56 to 61 across, 1.3 deep (dashed)", ha="center", fontsize=6.5, color=MUT)
    k = 40 / math.sqrt(2)
    holes(ax, [(sy * k, zc + sz * k, 4, None, "r") for sy in (1, -1) for sz in (1, -1)])
    ax.text(W / 2 + 3, zc + k, "M4 x 7 deep on an\n80 circle, at 45 deg", fontsize=6.5, color=AC, va="center")
    holes(ax, [(-36, 29 - z0, 5, None, "r")])
    ax.text(-W / 2 - 4, 29 - z0, "lead 5 (crawler's right:\n36 left of centre\nseen from the front,\n7 up)", fontsize=6.5,
            color=AC, va="center", ha="right")
    ax.text(0, -14, "Inside face: four M3 holes 6 deep on a 40 x 40 square round the bore", ha="center", fontsize=6.5, color=MUT)
    ax.set_xlim(-W / 2 - 50, W / 2 + 40); ax.set_ylim(-20, H + 14)
    # rim, seen from above
    ax = fig.add_axes([0.03, 0.08, 0.62, 0.36]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, -W / 2), L, W, fc="#F3F4F6", ec=INK, lw=1.2))
    rw = P["rim"][0]
    ax.add_patch(Rectangle((rw, -W / 2 + rw), L - 2 * rw, W - 2 * rw, fc="white", ec=INK, lw=0.8))
    g0, g1, _ = P["oring_groove"]
    gm = (g0 + g1) / 2
    ax.add_patch(Rectangle((gm, -W / 2 + gm), L - 2 * gm, W - 2 * gm, fc="none", ec="#7C3AED", lw=1.0, ls="--"))
    for x in P["lid_screw_x"]:
        for s in (1, -1):
            ax.add_patch(Circle((x + L / 2, s * (W / 2 - P["lid_screw_in"])), 2, fc="white", ec=INK, lw=0.9))
    for x in P["lid_screw_x"]:
        ax.text(x + L / 2, W / 2 + 4, f"{x + L / 2:g}", ha="center", fontsize=7, color=AC)
    ax.text(L / 2, W / 2 + 13, "Rim top, seen from above: ten M4 holes 8 deep, 5 in from each long edge, at these distances from the rear end",
            ha="center", fontsize=8.5, color=INK)
    ax.text(L / 2, 0, "pocket (open), 216 x 64 at the rim", ha="center", va="center", fontsize=7.5, color=MUT)
    ax.text(L / 2, -W / 2 - 8, "Purple dashed: O-ring groove, 2.4 wide, 1.3 deep, 8.3 to 10.7 in from the outside", ha="center", fontsize=7.5, color="#7C3AED")
    ax.set_xlim(-10, L + 10); ax.set_ylim(-W / 2 - 14, W / 2 + 18)
    # rear wall
    ax = fig.add_axes([0.66, 0.08, 0.32, 0.36]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-W / 2, 0), W, H, fc="#F3F4F6", ec=INK, lw=1.2))
    ax.text(0, H + 6, "Rear wall, seen from behind", ha="center", fontsize=8.5, color=INK)
    holes(ax, [(0, P["tether_z"] - z0, 10.2, "penetrator 10.2\n(centre line, 55 up)", "d")])
    ax.set_xlim(-W / 2 - 12, W / 2 + 12); ax.set_ylim(-14, H + 14)
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/culvertcrawl", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "hull-holes.png", facecolor="white"); plt.close(fig)
    return OUT / "hull-holes.png"


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(13, 7.6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 130); ax.set_ylim(0, 76); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 74, "CulvertCrawl prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 70.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper; ferrules on every screw terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(128, 1.5, "github.com/BoujeeEnjinia1701/culvertcrawl", fontsize=7, color="#0F766E", ha="right", family="monospace")
    for (x, y, w, h, t) in ((1.5, 9, 47, 57, "Surface control box"), (51, 9, 19, 57, "Tether reel"), (73, 9, 55.5, 57, "Crawler hull (sealed)")):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
        ax.text(x + 1, y + h - 0.6, t, fontsize=8.5, color=MUT, va="top", fontweight="bold")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.2, title, ha="center", va="top", fontsize=8.2, fontweight="bold", color=INK)
        if sub:
            ax.text(x + w / 2, y + h - 3.9, sub, ha="center", va="top", fontsize=6.8, color=MUT, linespacing=1.25)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=6.6, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, BLK = "#B91C1C", "#1D4ED8", "#6B7280", "#111827"
    # surface box
    blk(3, 50, 13, 10, "LiFePO4 battery", "12.8 V 20 Ah\nwith BMS", "#C2410C")
    blk(19, 52, 9, 7, "10 A fuse", "", "#F59E0B")
    blk(31, 52, 14, 7, "Power switch", "", BLK)
    blk(31, 40, 14, 8, "Emergency stop", "latching, NC", "#DC2626")
    blk(18, 38, 11, 10, "Boost", "12 to 48 V\n100 W", "#15803D")
    blk(3, 25, 15, 10, "Current monitor", "1.5 A cutoff\nrelay", "#0F766E")
    blk(22, 26, 9, 7, "2 A fuse", "", "#F59E0B")
    blk(34, 24, 12, 10, "Tether\nconnector", "4 power pins,\n4 data pins", BLK)
    blk(34, 12, 12, 8, "Ethernet", "bulkhead", BLK)
    blk(3, 12, 13, 8, "Charge port", "to the BMS", BLK)
    # reel
    blk(53, 36, 15, 12, "Slip ring", "6 circuits:\n2 power, 2 pairs", "#7C3AED")
    blk(53, 18, 15, 10, "Payout counter", "encoder and\nUSB reader", "#16A34A")
    # crawler
    blk(75, 50, 14, 10, "Penetrator", "tether in,\nrear wall", BLK)
    blk(92, 50, 15, 10, "48 to 12 V buck", "36 to 75 V in", "#15803D")
    blk(110, 50, 15, 10, "Motor driver", "dual, current\nlimited", "#B45309")
    blk(110, 37, 15, 9, "Motors (2)", "12 V worm gear,\nHall encoders", "#B45309")
    blk(92, 37, 15, 9, "12 to 5 V buck", "", "#15803D")
    blk(75, 23, 15, 14, "Raspberry Pi 4", "Ethernet, camera,\nIMU, leak sensor", "#16A34A")
    blk(93, 25, 14, 9, "LED driver", "PWM, frame\nsynchronized", "#D97706")
    blk(110, 24, 15, 9, "Laser switch", "MOSFET, Class 2\ndiode", "#DC2626")
    blk(93, 12, 14, 8, "LEDs (8)", "in the bezel", "#D97706")
    blk(110, 12, 15, 8, "Laser diode", "in the head", "#DC2626")
    # power path
    wire([(16, 55.5), (19, 55.5)], RED); wire([(28, 55.5), (31, 55.5)], RED)
    lab(17.5, 58, "1.5 mm²", RED, "center")
    wire([(45, 55.5), (47, 55.5), (47, 44), (45, 44)], RED)
    wire([(31, 44), (29, 44)], RED); lab(30, 46.2, "1.5 mm²", RED, "center")
    wire([(23.5, 38), (23.5, 36), (10.5, 36), (10.5, 35)], RED); lab(16.5, 37.4, "48 V, 0.75 mm²", RED, "center")
    wire([(18, 30), (22, 30)], RED); wire([(31, 30), (34, 30)], RED)
    wire([(40, 34), (40, 38), (51, 38), (51, 40), (53, 40)], RED); lab(48, 36.6, "0.75 mm²", RED, "center")
    wire([(9.5, 20), (9.5, 50)], GRY, 1.2); lab(10.2, 22.5, "charge lead", GRY)
    # data path
    wire([(40, 20), (40, 22.5), (49.5, 22.5), (49.5, 42), (53, 42)], BLU); lab(42, 24.2, "Ethernet pairs", BLU)
    wire([(68, 42), (71.5, 42), (71.5, 55), (75, 55)], BLK, 2.6); lab(71.8, 47, "tether, 60 m", BLK)
    wire([(89, 56), (92, 56)], RED); lab(90.5, 58.5, "0.5 mm²", RED, "center")
    wire([(107, 56), (110, 56)], RED); lab(108.5, 58.5, "0.75 mm²", RED, "center")
    wire([(117.5, 50), (117.5, 46)], RED); lab(118.2, 48, "0.5 mm²", RED)
    wire([(99.5, 50), (99.5, 46)], RED)
    wire([(92, 41.5), (88, 41.5), (88, 37)], RED); lab(88.6, 39.3, "5 V, 1.0 mm²", RED)
    wire([(82, 50), (82, 37)], BLU); lab(82.6, 44, "Ethernet", BLU)
    wire([(90, 30), (93, 30)], GRY, 1.2); wire([(107, 31), (110, 31)], GRY, 1.2)
    wire([(100, 25), (100, 20)], RED); lab(100.6, 22.5, "0.5 mm²", RED)
    wire([(117.5, 24), (117.5, 20)], RED); lab(118.2, 22, "0.25 mm²", RED)
    wire([(99.5, 37), (99.5, 34)], RED)
    wire([(90, 26), (91, 26), (91, 46), (110, 46)], GRY, 1.2); lab(104, 47.5, "PWM, enable", GRY, "center")
    wire([(68, 23), (70, 23), (70, 6), (32, 6)], BLU, 1.4); lab(50, 6, "USB to the operator's laptop", BLU, "center")
    wire([(34, 16), (30, 16), (30, 6)], BLU, 1.4); lab(25, 9, "laptop Ethernet", BLU, "center")
    ax.text(74, 6.6, "LED and laser leads leave the hull through the potted lead hole in the front wall.",
            fontsize=7.0, color=MUT)
    ax.text(74, 3.8, "Red: power. Blue: data. Grey: control and charging. 48 V DC is extra-low voltage.",
            fontsize=7.0, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    if not args:
        args = list(fns)
    what, only = args[0], [a for a in args[1:] if a.isdigit()] or None
    if what in fns and len(args) > 1 and only:
        r = fns[what](only)
        print(what, "->", r)
    else:
        for w in args:
            r = fns[w]()
            print(w, "->", r)
