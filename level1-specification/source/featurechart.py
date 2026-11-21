import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

groups = [
 ("1.0 Accounts &\nProfile", ["1.1 Sign up / log in\nwith school email", "1.2 Profile &\ninterests", "1.3 Location &\nradius", "1.4 User roles"]),
 ("2.0 Event\nDiscovery", ["2.1 Personalized\nfeed", "2.2 Nearby events\n(map + list)", "2.3 Keyword\nsearch", "2.4 Filters", "2.5 Event detail\npage"]),
 ("3.0 Event\nEngagement", ["3.1 Save event", "3.2 RSVP", "3.3 Add to\ncalendar", "3.4 Share event", "3.5 Directions"]),
 ("4.0 Event Creation\n& Management", ["4.1 Create event", "4.2 Edit / cancel\nevent", "4.3 Organizer\nverification", "4.4 RSVP list &\ncounts"]),
 ("5.0 Notifications", ["5.1 Event\nreminders", "5.2 Change / cancel\nalerts", "5.3 Weekly\ndigest", "5.4 Notification\nsettings"]),
 ("6.0 Trust &\nModeration", ["6.1 Report event", "6.2 Review\nreports (admin)", "6.3 Approve\norganizers (admin)", "6.4 Auto-archive\npast events"]),
]
W, H = 2.6, 0.9   # box size
gap = 0.55
colx = [i*(W+gap) for i in range(len(groups))]
total = colx[-1] + W
fig, ax = plt.subplots(figsize=(19, 11))
ax.set_xlim(-0.3, total+0.3); ax.set_ylim(-8.2, 2.6); ax.axis("off")

def box(x, y, text, fc, ec, fs, bold=False, w=W, h=H, tc="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec, lw=1.6))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs, weight="bold" if bold else "normal", color=tc)

rw = 4.6
rx = total/2 - rw/2
box(rx, 1.4, "CampusConnect\nStudent Event Discovery App", "#2B5797", "#1B3A66", 14, True, w=rw, h=1.0, tc="white")
bus_y = 0.9
ax.plot([total/2, total/2], [1.4, bus_y], color="#333", lw=1.6)
ax.plot([colx[0]+W/2, colx[-1]+W/2], [bus_y, bus_y], color="#333", lw=1.6)
gy = -0.25
for (g, leaves), x in zip(groups, colx):
    ax.plot([x+W/2, x+W/2], [bus_y, gy+H], color="#333", lw=1.6)
    box(x, gy, g, "#C9DCF3", "#2B5797", 12, True)
    spine_x = x + 0.22
    ly = gy - 0.45
    last = None
    for leaf in leaves:
        ly -= (H + 0.35)
        lx = x + 0.45
        box(lx, ly, leaf, "#F7FAFE", "#2B5797", 10.5, w=W-0.45)
        ax.plot([spine_x, lx], [ly+H/2, ly+H/2], color="#555", lw=1.2)
        last = ly+H/2
    ax.plot([spine_x, spine_x], [gy, last], color="#555", lw=1.2)
ax.text(total/2, 2.55, "CampusConnect — Feature Chart (Updated after Interview & Critique)", ha="center", fontsize=17, weight="bold")
ax.text(total/2, -8.1, "Removed from v1 after critique: in-app chat · ticket payments · friends/social feed · social-media auto-import · paid promotion",
        ha="center", fontsize=10.5, style="italic", color="#8B1A1A")
plt.savefig("Updated_Feature_Chart.png", dpi=160, bbox_inches="tight", facecolor="white")
