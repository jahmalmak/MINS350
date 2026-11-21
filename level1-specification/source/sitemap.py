import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# (label, children) ; kind prefix: "!" = action, ">" = link to shared screen, "*" = shared screen
TABS = [
 ("1. Discover (Home)", [
   ("Browse Events feed", [
     ("Category tabs: Social · Sports ·\nClubs · Volunteer · Career", []),
     ("Search Events", []),
     ("Filter Events panel\n(category, date, nearby)", []),
     ("*Event Details", [
        ("!Join / RSVP", []), ("!Save / Bookmark", []),
        ("!Add to Calendar", []), (">Host Organization", []),
     ]),
   ]),
   ("Find Clubs / Organizations", [
     ("Organization Profile", [(">Event Details", [])]),
   ]),
 ]),
 ("2. Saved Events", [
   ("Saved (Bookmarked) Events", [(">Event Details", []), ("!Remove from Saved", [])]),
   ("Joined / RSVP'd Events", [(">Event Details", []), ("!Add to Calendar", []), ("!Cancel RSVP", [])]),
 ]),
 ("3. Manage Events (+)", [
   ("Create Event form\n(title, category, date/time,\nlocation, description, host)", [
     ("Preview Event", [("!Post Event →\nconfirmation", [])]),
   ]),
   ("My Posted Events", [
     ("Edit Event", []), ("!Cancel / Delete Event", []), ("View Joined / RSVP List", []),
   ]),
 ]),
 ("4. Notifications", [
   ("Notification Center", [
     ("Upcoming Event Reminders", []), ("Saved Event Reminders", []),
     ("Nearby Event Alerts", []), (">Event Details", []),
   ]),
 ]),
 ("5. Profile", [
   ("My Profile", [
     ("Edit Profile", []), ("Select / Edit Interests", []),
     ("Notification Settings", []), ("Location Access", []), ("!Log Out", []),
   ]),
 ]),
]

COLW, BW, BH, STEP, IND = 3.55, 3.05, 0.62, 0.86, 0.32
fig, ax = plt.subplots(figsize=(22, 15))
ax.axis("off")

STY = {
 "tab":    dict(fc="#2B5797", ec="#1B3A66", tc="white", bold=True, ls="-"),
 "screen": dict(fc="#E8F1FB", ec="#2B5797", tc="black", bold=False, ls="-"),
 "shared": dict(fc="#D5E8D4", ec="#3B7D3B", tc="black", bold=True, ls="-"),
 "action": dict(fc="#FFF4CC", ec="#B8860B", tc="black", bold=False, ls="--"),
 "link":   dict(fc="white",   ec="#3B7D3B", tc="#3B7D3B", bold=False, ls=":"),
 "top":    dict(fc="#C9DCF3", ec="#2B5797", tc="black", bold=True, ls="-"),
}
def box(x, y, w, h, text, kind, fs=10.5):
    s = STY[kind]
    ax.add_patch(FancyBboxPatch((x, y - h/2), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                 fc=s["fc"], ec=s["ec"], lw=1.5, ls=s["ls"]))
    ax.text(x + w/2, y, text, ha="center", va="center", fontsize=fs, color=s["tc"],
            weight="bold" if s["bold"] else "normal", style="italic" if kind == "link" else "normal")

def parse(label):
    if label.startswith("!"): return label[1:], "action"
    if label.startswith(">"): return "→ " + label[1:], "link"
    if label.startswith("*"): return label[1:], "shared"
    return label, "screen"

def lines_h(label): return label.count("\n") + 1

def draw(children, px, py_bottom, level, y):
    """draw children below parent at x=px; returns new y"""
    spine = px + 0.16
    last_mid = None
    for label, sub in children:
        text, kind = parse(label)
        h = BH + 0.22 * (lines_h(text) - 1)
        y -= (STEP + 0.22 * (lines_h(text) - 1) / 2)
        cx = px + IND
        box(cx, y, BW - IND * level, h, text, kind, fs=10 if level > 1 else 10.5)
        ax.plot([spine, cx], [y, y], color="#555", lw=1.1)
        last_mid = y
        cy = y
        y -= 0.22 * (lines_h(text) - 1) / 2
        if sub:
            y = draw(sub, cx, cy - h/2, level + 1, y)
    if last_mid is not None:
        ax.plot([spine, spine], [py_bottom, last_mid], color="#555", lw=1.1)
    return y

total_w = COLW * len(TABS) - (COLW - BW)
mid = total_w / 2

# ---- Entry / onboarding row ----
ytop = 4.2
ax.text(mid, ytop + 1.55, "Student Event App — Site Map (Prototype v1)", ha="center", fontsize=20, weight="bold")
box(mid - 1.6, ytop + 0.65, 3.2, 0.7, "Launch / Welcome Screen", "top", 12)
row_y = ytop - 0.55
on = ["Log In", "Sign Up", "Create Profile", "Select Interests\n(Social, Sports, Clubs,\nVolunteer, Career)", "Allow Location\n(optional)"]
ow, og = 2.55, 0.55
start = mid - (len(on) * ow + (len(on) - 1) * og) / 2
xs = [start + i * (ow + og) for i in range(len(on))]
for i, (x, t) in enumerate(zip(xs, on)):
    box(x, row_y, ow, 0.62 + 0.22 * (lines_h(t) - 1), t, "screen", 10.5)
ax.annotate("", xy=(xs[0] + ow/2, row_y + 0.32), xytext=(mid - 0.8, ytop + 0.3), arrowprops=dict(arrowstyle="->", color="#333"))
ax.annotate("", xy=(xs[1] + ow/2, row_y + 0.32), xytext=(mid - 0.2, ytop + 0.3), arrowprops=dict(arrowstyle="->", color="#333"))
for i in range(1, len(on) - 1):
    ax.annotate("", xy=(xs[i+1], row_y), xytext=(xs[i] + ow, row_y), arrowprops=dict(arrowstyle="->", color="#333"))
ax.text(xs[0] + ow/2, row_y - 0.62, "returning user", ha="center", fontsize=9, style="italic", color="#555")
ax.text((xs[1] + xs[4] + ow) / 2, row_y - 0.72, "new user onboarding (first launch only)", ha="center", fontsize=9, style="italic", color="#555")

# ---- Main navigation bar ----
nav_y = 1.55
box(mid - 3.0, nav_y, 6.0, 0.72, "Main Navigation — Bottom Tab Bar (always visible)", "top", 12.5)
ax.annotate("", xy=(mid - 1.0, nav_y + 0.37), xytext=(xs[0] + ow/2, row_y - 0.85), arrowprops=dict(arrowstyle="->", color="#333"))
ax.annotate("", xy=(mid + 1.0, nav_y + 0.37), xytext=(xs[4] + ow/2, row_y - 0.85), arrowprops=dict(arrowstyle="->", color="#333"))
bus = nav_y - 0.65
ax.plot([mid, mid], [nav_y - 0.36, bus], color="#333", lw=1.6)
ax.plot([BW/2, COLW * (len(TABS) - 1) + BW/2], [bus, bus], color="#333", lw=1.6)

ymin = 0
tab_y = 0.3
for i, (tab, kids) in enumerate(TABS):
    x = i * COLW
    ax.plot([x + BW/2, x + BW/2], [bus, tab_y + 0.36], color="#333", lw=1.6)
    box(x, tab_y, BW, 0.72, tab, "tab", 12.5)
    y = draw(kids, x, tab_y - 0.36, 1, tab_y)
    ymin = min(ymin, y)

# ---- Legend + exclusions ----
ly = ymin - 1.0
items = [("screen", "Screen / page"), ("shared", "Shared screen (reached from several places)"),
         ("action", "Action on a screen (button / dialog)"), ("link", "→ Link to a shared screen")]
lx = 0
for kind, t in items:
    box(lx, ly, 0.75, 0.42, "", kind)
    ax.text(lx + 0.9, ly, t, va="center", fontsize=10.5)
    lx += 0.9 + len(t) * 0.105 + 0.6
ax.text(mid, ly - 0.75, "Not in prototype v1 (per specification): private messaging · ticket payments · crime reporting · social media feed · automatic event importing",
        ha="center", fontsize=11, style="italic", color="#8B1A1A")

ax.set_xlim(-0.3, total_w + 0.3)
ax.set_ylim(ly - 1.1, ytop + 2.0)
plt.savefig("Site_Map.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.savefig("Site_Map.pdf", bbox_inches="tight", facecolor="white")
print("ok")
