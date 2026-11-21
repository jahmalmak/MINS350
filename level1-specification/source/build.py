from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

APP = "CampusConnect"

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement('w:shd'); s.set(qn('w:val'), 'clear'); s.set(qn('w:color'), 'auto'); s.set(qn('w:fill'), hexcolor)
    tcPr.append(s)


def setw(t, widths):
    t.autofit = False
    grid = t._tbl.tblGrid
    for i, gc in enumerate(grid.findall(qn('w:gridCol'))):
        gc.set(qn('w:w'), str(int(widths[i]*1440)))
    for row in t.rows:
        for i, w in enumerate(widths): row.cells[i].width = Inches(w)

from docx.enum.section import WD_SECTION
def landscape_pic(doc, path, caption):
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    sec.orientation = WD_ORIENT.LANDSCAPE
    if sec.page_width < sec.page_height: sec.page_width, sec.page_height = sec.page_height, sec.page_width
    sec.left_margin = sec.right_margin = Inches(0.5); sec.top_margin = sec.bottom_margin = Inches(0.5)
    p = doc.add_paragraph(); r = p.add_run(caption); r.bold = True
    from PIL import Image
    w, h = Image.open(path).size
    width = min(10.0, 7.0 * w / h)
    doc.add_picture(path, width=Inches(width))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    sec2.orientation = WD_ORIENT.PORTRAIT
    if sec2.page_width > sec2.page_height: sec2.page_width, sec2.page_height = sec2.page_height, sec2.page_width
    sec2.left_margin = sec2.right_margin = Inches(0.9); sec2.top_margin = sec2.bottom_margin = Inches(0.8)

def base(doc):
    st = doc.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
    for s in doc.sections:
        s.left_margin = s.right_margin = Inches(0.9); s.top_margin = s.bottom_margin = Inches(0.8)

def table(doc, headers, rows, widths=None, header_fill="2B5797"):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = 'Table Grid'
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = ""; r = c.paragraphs[0].add_run(h); r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); r.font.size = Pt(10); shade(c, header_fill)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""; p = cells[i].paragraphs[0]
            run = p.add_run(str(v)); run.font.size = Pt(10)
    if widths: setw(t, widths)
    return t

def bullets(doc, items, style='List Bullet'):
    for it in items:
        p = doc.add_paragraph(style=style)
        if isinstance(it, tuple):
            p.add_run(it[0]).bold = True; p.add_run(it[1])
        else:
            p.add_run(it)

# ---------------- USER STORIES ----------------
# (id, generated text, status, reason)
STORIES = [
 (1, "As a student, I want to sign up with my school email so that the app knows which school I go to.", "ACCEPTED", "Selected → edited as Story S1 (Feature 1.1)."),
 (2, "As a user, I want the app to be easy to use so that I enjoy using it.", "REJECTED", "Vague — no specific action and not testable; usability belongs in non-functional requirements."),
 (3, "As a student, I want to see events near me so that I can go to them.", "ACCEPTED", "Selected → edited as Story S3 (Feature 2.2); added a user-chosen radius to make it specific."),
 (4, "As a student, I want to chat with other people going to an event so that I can make friends before I get there.", "REJECTED", "Out of scope — in-app messaging was removed after the critique (privacy and moderation burden)."),
 (5, "As a student, I want to pick my interests when I first open the app so that I see events I like.", "ACCEPTED", "Selected → edited as Story S2 (Features 1.2 + 2.1)."),
 (6, "As a student, I want to buy tickets inside the app so that I don't have to go to another website.", "REJECTED", "Out of scope for v1 — payments add legal/financial complexity; event page links to external ticketing instead."),
 (7, "As a student, I want to search for events so that I can find events.", "REJECTED", "Circular/redundant — the \"so that\" restates the action; covered by Story S4 (search + filters)."),
 (8, "As a student, I want to filter events by type, date, and price so that I can find what I'm looking for faster.", "ACCEPTED", "Selected → edited as Story S4 (Features 2.3 + 2.4)."),
 (9, "As a student, I want to follow my friends and see which events they are going to so that we can go together.", "REJECTED", "Deferred to Phase 2 — social graph raises privacy concerns and is not essential to the client's core goal."),
 (10, "As an admin, I want the system to be secure so that user data is protected.", "REJECTED", "Vague non-functional requirement — no specific user action; captured as a constraint instead."),
 (11, "As a student, I want to open an event and see all the important details so that I can decide if I want to go.", "ACCEPTED", "Selected → edited as Story S5 (Feature 2.5); listed the exact required details."),
 (12, "As a student, I want an AI chatbot to recommend events to me so that I get suggestions.", "REJECTED", "Over-engineered — the personalized feed (Feature 2.1) already meets this need; weak \"so that\"."),
 (13, "As a local business, I want to pay to promote my event at the top of the feed so that more students see it.", "REJECTED", "Conflicts with client goal of a trustworthy, relevant feed; monetization not in v1."),
 (14, "As a student, I want to RSVP to an event and put it on my calendar so that I don't forget about it.", "ACCEPTED", "Selected → edited as Story S6 (Features 3.2 + 3.3)."),
 (15, "As a student, I want to see events on a map so that I know where they are.", "REJECTED", "Redundant — merged into Story S3 (nearby events shown as map + list)."),
 (16, "As a student, I want to bookmark events so that I can look at them later.", "REJECTED", "Redundant — overlaps Story S6 (save/RSVP); save is part of Feature 3.1 with the same outcome."),
 (17, "As a club officer, I want to post an event with all the needed information so that students know what's going on.", "ACCEPTED", "Selected → edited as Story S7 (Feature 4.1); specified required fields."),
 (18, "As a student, I want the app to have dark mode so that it looks cool.", "REJECTED", "Cosmetic — belongs to Garrett's Surface layer, not Scope; no functional value."),
 (19, "As a professor, I want to give students extra credit for going to events so that more students participate.", "REJECTED", "Irrelevant user role — professors are not a defined user constituency for v1."),
 (20, "As a student, I want to get a reminder before an event so that I don't miss it.", "ACCEPTED", "Selected → edited as Story S8 (Features 5.1 + 5.2); added change/cancellation alerts."),
 (21, "As a student, I want to rate and review events after I go so that other students know if it was good.", "REJECTED", "Low priority for v1 — adds moderation load; deferred to a later release."),
 (22, "As an organizer, I want the app to automatically pull my events from Instagram so that I don't have to type them again.", "REJECTED", "Technically infeasible for v1 — social platform APIs restrict scraping; replaced by the structured event form (Feature 4.1)."),
 (23, "As a student, I want to be notified about every new event so that I know everything that's happening.", "REJECTED", "Contradicts client requirement to avoid too many alerts; replaced by weekly digest + notification preferences (5.3, 5.4)."),
 (24, "As a student, I want to report an event that is fake or wrong so that other students aren't misled.", "ACCEPTED", "Selected → edited as Story S9 (Features 6.1 + 6.2)."),
 (25, "As a student, I want to edit my profile so that it is up to date.", "REJECTED", "Too generic — trivial CRUD action with a weak outcome; implied by Feature 1.2."),
 (26, "As a student, I want to use the app on my smartwatch so that I can check events on my wrist.", "REJECTED", "Irrelevant platform for v1 — usage contexts are mobile phone and desktop web."),
 (27, "As a club, I want to be verified so that students trust my events.", "ACCEPTED", "Selected → edited as Story S10 (Features 4.3 + 6.3); clarified the user role."),
 (28, "As a user, I want the app to load fast so that I don't have to wait.", "REJECTED", "Vague non-functional requirement — no measurable target or specific action; moved to performance constraints."),
 (29, "As a parent, I want to see what events my child is going to so that I know they are safe.", "REJECTED", "Irrelevant constituency and a privacy violation — students are adults; parents are not users."),
]

SELECTED = [
 ("S1", 1, "As a new student, I want to sign up using my school (.edu) email address so that the app verifies which campus I attend and shows events relevant to my school.", "1.1 Sign up / log in with school email", "Email must be verified before the feed loads; non-.edu emails are rejected for student accounts."),
 ("S2", 5, "As a new student, I want to choose my school, major, year, and at least three interest categories during onboarding so that my \"For You\" feed shows events that match what I care about.", "1.2 Profile + 2.1 Personalized feed", "Interests can be changed later; feed ranks by interest match, distance, and date."),
 ("S3", 3, "As a student without a car, I want to see events within a distance I choose (1, 5, 10, or 25 miles) on a map and in a list so that I only see events I can realistically get to.", "1.3 Location settings + 2.2 Nearby events", "If location permission is denied, the app uses the campus or ZIP code entered at onboarding."),
 ("S4", 8, "As a busy student, I want to search by keyword and filter events by category, date, distance, cost, and host type so that I can find a specific kind of event in under a minute.", "2.3 Keyword search + 2.4 Filters", "If no results, the app suggests widening the radius or clearing filters."),
 ("S5", 11, "As a student, I want to open an event and see its title, date/time, location with map, host and verification status, cost, description, and RSVP count so that I can decide whether to attend before committing.", "2.5 Event detail page", "These fields mirror the required fields in Story S7."),
 ("S6", 14, "As a student, I want to RSVP \"Going\" or \"Interested\" and add the event to my Google, Apple, or Outlook calendar so that I don't forget about it.", "3.2 RSVP + 3.3 Add to calendar (also 3.1 Save)", "Stored in the RSVP table; status drives reminders (S8) and the organizer's RSVP count (4.4)."),
 ("S7", 17, "As a verified club officer, I want to create an event by filling out a form with required fields (title, date/time, location, category, cost, description, host) so that students get complete, accurate information in one place.", "4.1 Create event form (+ 4.2 Edit/cancel)", "Publish is blocked until all required fields are valid; past events auto-archive (6.4)."),
 ("S8", 20, "As a student who RSVP'd to an event, I want to receive a reminder 24 hours and 1 hour before it starts, and an alert if it is changed or canceled, so that I don't miss it or show up to a canceled event.", "5.1 Reminders + 5.2 Change/cancel alerts", "Respects the notification preferences and quiet hours set in 5.4."),
 ("S9", 24, "As a student, I want to report an event as fake, inappropriate, inaccurate, canceled, or outdated so that a moderator can review it and the feed stays trustworthy.", "6.1 Report event + 6.2 Review reports", "Confirmed reports remove/correct the event and notify RSVP'd students."),
 ("S10", 27, "As a student organization or community organizer, I want to request verification by selecting my organization type (club, school department, business, or community organization) and submitting proof so that my events display a verified badge students can trust.", "4.3 Organizer verification + 6.3 Approve organizers", "Only verified organizers can publish events in v1."),
]

# ---------- Complete User Story List ----------
d = Document(); base(d)
for s in d.sections:
    s.orientation = WD_ORIENT.LANDSCAPE; s.page_width, s.page_height = s.page_height, s.page_width
h = d.add_heading("Complete User Story List", 0)
d.add_paragraph(f"Project: {APP} — Student Event Discovery App   |   Role: Analyst   |   Level 1 Specification support document")
p = d.add_paragraph()
p.add_run("Method: ").bold = True
p.add_run("29 user stories were generated with ChatGPT using the Analyzing-video method (prompt below), then reviewed against the client "
          "interview, the critique, and the updated feature chart. ")
p.add_run("Result: 10 accepted, 19 rejected").bold = True
p.add_run(" (requirement: reject 18–22; select 7–11).")
p = d.add_paragraph(); p.add_run("Prompt used: ").bold = True
p.add_run("\"Act as a business analyst. Generate 29 user stories for a mobile app that helps college students discover nearby events "
          "(campus, club, school, business, and community events), save and RSVP to them, and lets verified organizers post events. "
          "Use the format: As a <type of user>, I want to <action> so that <result>. Include a variety of user types.\"").italic = True
p = d.add_paragraph(); p.add_run("Rejection codes: ").bold = True
p.add_run("Vague · Redundant · Out of scope · Irrelevant role/platform · Deferred (Phase 2) · Conflicts with client goal · Infeasible · Cosmetic")

t = d.add_table(rows=1, cols=4); t.style = 'Table Grid'
for i, hname in enumerate(["#", "Generated User Story (unedited)", "Decision", "Reason / Note"]):
    c = t.rows[0].cells[i]; c.text = ""; r = c.paragraphs[0].add_run(hname); r.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255); shade(c, "2B5797")
for sid, text, status, reason in STORIES:
    cells = t.add_row().cells
    vals = [str(sid), text, status, reason]
    for i, v in enumerate(vals):
        cells[i].text = ""; r = cells[i].paragraphs[0].add_run(v); r.font.size = Pt(10)
        if i == 2:
            r.bold = True
            r.font.color.rgb = RGBColor(0x1E, 0x7B, 0x34) if status == "ACCEPTED" else RGBColor(0xB0, 0x24, 0x18)
    shade(cells[2], "E3F4E6" if status == "ACCEPTED" else "FBE5E3")
setw(t, [0.4, 4.4, 1.0, 3.4])

acc = sum(1 for s in STORIES if s[2] == "ACCEPTED"); rej = len(STORIES) - acc
d.add_paragraph()
d.add_paragraph(f"Totals: {len(STORIES)} stories — {acc} accepted, {rej} rejected.").runs[0].bold = True
d.save("Complete_User_Story_List.docx")
assert len(STORIES) == 29 and 18 <= rej <= 22 and 7 <= acc <= 11

# ---------- Level 1 Specification ----------
d = Document(); base(d)
d.add_heading("Level 1 Specification", 0)
d.add_paragraph(f"{APP} — Student Event Discovery App").runs[0].bold = True
d.add_paragraph("Prepared by: [Analyst name]     Client: [Client name]     Team: [Team name]     Date: [date]\n"
                "Covers Garrett's Elements of User Experience — bottom two layers: Strategy and Scope.")

d.add_heading("1. Strategy", 1)
d.add_heading("1.1 Project Summary (updated)", 2)
d.add_paragraph(
 f"{APP} is a mobile-first app (with a companion web version) that helps college students discover events and opportunities "
 "happening on and around their campus in one trusted place. Today, event information is scattered across Instagram, group chats, "
 "flyers, email newsletters, and individual school websites, so students miss events they would have enjoyed and organizers "
 "struggle to reach them.")
d.add_paragraph(
 "Students sign up with their school email, choose their interests, and set how far they are willing to travel. The app then shows a "
 "personalized feed and a nearby map/list of events, with search and filters for category, date, distance, cost, and host type. "
 "From an event page, students can save, RSVP, add the event to their calendar, share it, and get directions, and they receive "
 "reminders and change/cancellation alerts without being flooded by notifications.")
d.add_paragraph(
 "Events are posted by verified organizers — student clubs, school departments, local businesses, and community organizations — "
 "through a structured form with required fields. A report-and-moderate process plus automatic archiving of past events keeps "
 "listings accurate and trustworthy.")
p = d.add_paragraph(); p.add_run("What changed since the Baseline Plan (from the interview and critique):").bold = True
bullets(d, [
 "Added organizer verification by type (club, school department, business, community organization) — the client wants students to trust what they see.",
 "Defined \"nearby\" as a user-selected radius from GPS, with campus/ZIP fallback when location is off.",
 "Added structured required fields for event creation and a report/moderation flow for fake, inappropriate, canceled, or outdated events.",
 "Replaced \"notify on every new event\" with targeted reminders, change alerts, a weekly digest, and quiet hours.",
 "Events from other colleges and the community are included but labeled and filterable (on-campus vs. off-campus, host type).",
 "Removed for v1: in-app chat, ticket payments, social/friends feed, automatic social-media scraping, and paid promotion.",
 "First-version priorities: discovery (feed, nearby, search/filter), event detail, save/RSVP/calendar, organizer posting, reminders, and reporting.",
])

d.add_heading("1.2 User Constituencies", 2)
table(d, ["User role", "Characteristics / demographics", "Goals", "Needs from the system"], [
 ("Primary — Undergraduate students (residential & commuter)",
  "Ages 18–24; university and community-college students; smartphone-native; many are new to the area or commute and have limited transportation; varying budgets (many prefer free events).",
  "Meet people, find fun/social events, join clubs, discover free food and activities, build résumés.",
  "Fast, relevant feed; distance and cost filters; one-tap save/RSVP; reminders; confidence that events are real."),
 ("Graduate & non-traditional students",
  "Ages 24–45+; part-time, working, or parenting; limited free time; often on campus only in evenings.",
  "Find career, networking, academic, and family-friendly events that fit a tight schedule.",
  "Date/time filters (evenings/weekends), calendar sync, clear location and cost details, low notification noise."),
 ("Student organizers (club officers)",
  "Ages 18–24; volunteer leaders who rotate yearly; post several events per semester, mostly from phones or laptops.",
  "Increase attendance, reach students beyond their followers, plan food/space.",
  "Quick event form, verified badge, edit/cancel with automatic attendee alerts, RSVP counts."),
 ("Institutional organizers (school departments, student life, career center)",
  "Staff ages 25–60; desktop-based at work; post many events; accountable to the institution.",
  "Promote official programs and boost engagement/retention.",
  "Desktop-friendly posting, verified institutional status, accurate listings."),
 ("Community organizers & local businesses",
  "Nonprofits, venues, employers, cafés near campus; varied tech comfort.",
  "Reach students with volunteer, job, cultural, and local events.",
  "Verification process, clear labeling as off-campus/community, simple posting."),
 ("Administrators / moderators",
  "App team or designated campus staff; small group; desktop at work.",
  "Keep the platform safe, accurate, and trustworthy.",
  "Moderation queue for reports, verification approval tools, ability to remove/correct events and notify users."),
], widths=[1.4, 2.0, 1.6, 1.9])

d.add_heading("1.3 Usage Contexts", 2)
p = d.add_paragraph(); p.add_run("Platforms").bold = True
bullets(d, [
 ("Mobile (primary): ", "iOS and Android smartphones (native app or responsive web). Students browse, save, RSVP, and receive notifications here."),
 ("Desktop/laptop web (secondary): ", "Used mainly by organizers and admins to create events, manage verification, and moderate; also by students on campus lab computers."),
 ("Calendar & maps integration: ", "Google Calendar, Apple Calendar, Outlook (.ics); Google/Apple Maps for directions."),
])
p = d.add_paragraph(); p.add_run("Environments").bold = True
bullets(d, [
 ("On campus, between classes: ", "short 1–3 minute sessions, often walking, one-handed use, outdoor glare."),
 ("Dorm / home in the evening and weekends: ", "longer browsing sessions to plan the week."),
 ("Commuting (bus, train, passenger): ", "spotty connectivity; quick checks of saved events and directions."),
 ("Work / office (organizers & staff): ", "desktop posting and moderation during business hours."),
 ("At or on the way to the event: ", "checking time, location, and directions; possible cancellation alerts."),
])
p = d.add_paragraph(); p.add_run("Operating assumptions").bold = True
bullets(d, [
 "Internet is usually available (campus Wi-Fi or cellular) but can be intermittent; saved/RSVP'd events should be viewable offline (cached).",
 "Location services may be denied — the app falls back to the campus or ZIP code set during onboarding.",
 "Shared devices (library and lab computers) are used for the web version — sessions must time out and support easy log-out.",
 "Students may have older phones and limited data plans — pages and images should be lightweight.",
 "Users are sensitive to notification overload — notifications are opt-in by type with quiet hours.",
 "Accessibility: must be usable with screen readers and larger text sizes (target WCAG 2.1 AA).",
 "Student accounts require a school (.edu) email; organizers must be verified before publishing.",
])

d.add_heading("2. Scope", 1)
d.add_heading("2.1 Feature Chart (Updated)", 2)
d.add_paragraph("Hierarchical feature chart revised after the client interview and critique. The system is broken into six major "
                "feature areas (1.0–6.0), each decomposed into the specific features the Builder must implement. Feature numbers are used "
                "to trace user stories, the flow chart, and the data model back to Scope. "
                "[Submit the photo/scan of your hand-drawn version of this chart alongside or in place of this image.]")
landscape_pic(d, "Updated_Feature_Chart.png", "Figure 1 — Updated Feature Chart")
d.add_paragraph("Feature descriptions:").runs[0].bold = True
table(d, ["#", "Feature", "Description", "Primary user"], [
 ("1.1", "Sign up / log in", "Account creation with a verified school (.edu) email; log in / log out.", "Student, Organizer"),
 ("1.2", "Profile & interests", "School, major, class year, and interest categories used to personalize the feed.", "Student"),
 ("1.3", "Location & radius", "Home location from GPS or campus/ZIP fallback; preferred search radius.", "Student"),
 ("1.4", "User roles", "Student, Organizer, or Admin — controls what each user can do.", "All"),
 ("2.1", "Personalized feed", "Home feed ranked by interest match, distance, and date.", "Student"),
 ("2.2", "Nearby events", "Map and list of events within the chosen radius.", "Student"),
 ("2.3", "Keyword search", "Search event titles, descriptions, and hosts.", "Student"),
 ("2.4", "Filters", "Category, date, distance, cost (free/paid), host type, on/off campus.", "Student"),
 ("2.5", "Event detail page", "All event information, host verification status, RSVP count, and actions.", "Student"),
 ("3.1", "Save event", "Bookmark an event to view later (offline-available).", "Student"),
 ("3.2", "RSVP", "Mark Going or Interested.", "Student"),
 ("3.3", "Add to calendar", "Export to Google, Apple, or Outlook calendar (.ics).", "Student"),
 ("3.4", "Share event", "Share an event link by text or social apps.", "Student"),
 ("3.5", "Directions", "Open the event location in the phone's maps app.", "Student"),
 ("4.1", "Create event", "Structured form with required fields; validation before publishing.", "Organizer"),
 ("4.2", "Edit / cancel event", "Update or cancel an event; triggers alerts to RSVP'd students.", "Organizer"),
 ("4.3", "Organizer verification", "Organizer registers an organization, selects its type, and submits proof.", "Organizer"),
 ("4.4", "RSVP list & counts", "See how many students saved, are interested, or are going.", "Organizer"),
 ("5.1", "Event reminders", "Push/email reminders 24 h and 1 h before RSVP'd events.", "Student"),
 ("5.2", "Change / cancel alerts", "Notify RSVP'd students when an event changes or is canceled.", "Student"),
 ("5.3", "Weekly digest", "One weekly summary of new events matching interests.", "Student"),
 ("5.4", "Notification settings", "Turn notification types on/off; set quiet hours.", "Student"),
 ("6.1", "Report event", "Flag an event as fake, inappropriate, inaccurate, canceled, or outdated.", "Student"),
 ("6.2", "Review reports", "Admin reviews reports and removes/corrects events or dismisses the report.", "Admin"),
 ("6.3", "Approve organizers", "Admin approves or denies organization verification; verified badge shown.", "Admin"),
 ("6.4", "Auto-archive past events", "Events are archived automatically after their end time.", "System"),
], widths=[0.45, 1.5, 3.7, 1.25])
d.add_paragraph()
d.add_paragraph("Changes from the original feature chart:").runs[0].bold = True
table(d, ["Change", "Features", "Reason"], [
 ("Added", "1.2 Profile & interests, 1.3 Location & radius, 2.4 Filters, 3.2 RSVP, 3.3 Add to calendar", "Interview: client described personalized, nearby, filterable discovery and calendar use."),
 ("Added", "4.3 Organizer verification, 6.1–6.3 reporting & approval, 6.4 Auto-archive", "Interview: client wants only trustworthy, current events from known hosts."),
 ("Added / changed", "5.2 Change alerts, 5.3 Weekly digest, 5.4 Notification settings (replaced \"notify on every new event\")", "Interview: useful notifications without too many alerts."),
 ("Removed (v1)", "In-app chat, ticket payments, friends/social feed, social-media auto-import, paid promotion", "Critique: out of scope, privacy/moderation risk, or technically infeasible for v1."),
], widths=[1.1, 3.0, 2.8])

d.add_heading("2.2 User Stories (Selected & Edited)", 2)
d.add_paragraph("10 stories were selected from the 29-story Complete User Story List (submitted separately) and edited so each contains "
                "all three components — As a <type of user>, I want to <specific action> so that <result> — and traces to a feature above.")
table(d, ["ID", "Edited user story", "Linked feature(s)", "Notes for Builder", "Source #"],
      [(s[0], s[2], s[3], s[4], f"#{s[1]}") for s in SELECTED], widths=[0.45, 3.2, 1.45, 1.45, 0.55])


d.add_heading("2.3 Data Model (High-Level Schema)", 2)
d.add_paragraph("The data model was streamlined to six core entities. Items that were previously listed as separate entities but only "
                "describe another record (category, location, role, interests, verification, notification preferences, bookmarks, "
                "reminders) are now attributes. The Builder can create the database directly from the schema below "
                "(full SQL provided in schema.sql and in the appendix).")
landscape_pic(d, "Data_Model_ERD.png", "Figure 2 — High-Level Data Model (ERD)")
d.add_paragraph("Entities and key attributes:").runs[0].bold = True
table(d, ["Entity", "Purpose", "Key attributes (PK / FK in bold in SQL)", "Features"], [
 ("SCHOOL", "Campuses the app supports; maps a .edu email domain to a campus location.", "school_id (PK), name, email_domain, city, state, latitude, longitude", "1.1, 1.3, 2.4"),
 ("USER", "Everyone who logs in. Role decides permissions.", "user_id (PK), school_id (FK), email, password_hash, email_verified, first/last name, role, major, class_year, interests, home_lat/lng, radius_miles, notify_reminders, notify_digest, quiet_start/end", "1.1–1.4, 2.1, 5.4"),
 ("ORGANIZATION", "Club, school department, business, or community group that hosts events.", "org_id (PK), owner_user_id (FK), school_id (FK, optional), name, description, contact_email, org_type, verification_status, proof_url, verified_at", "4.3, 6.3"),
 ("EVENT", "An event listing.", "event_id (PK), org_id (FK), school_id (FK, optional), title, description, image_url, category, start/end_time, venue_name, address, latitude, longitude, is_on_campus, cost, ticket_url, status", "2.x, 4.1, 4.2, 6.4"),
 ("RSVP", "Links a user to an event they saved, are interested in, or are going to.", "rsvp_id (PK), user_id (FK), event_id (FK), status, reminder_sent, created_at — one row per user per event", "3.1, 3.2, 4.4, 5.1, 5.2"),
 ("REPORT", "A student's flag on an event, reviewed by an admin.", "report_id (PK), event_id (FK), reporter_id (FK), reason, details, status, resolved_by (FK), created_at", "6.1, 6.2"),
], widths=[1.05, 1.7, 3.0, 1.15])
d.add_paragraph()
d.add_paragraph("Relationships:").runs[0].bold = True
bullets(d, [
 "A School has many Users; each User belongs to one School.",
 "A User (organizer) manages one or more Organizations; each Organization has one owner.",
 "An Organization hosts many Events; each Event belongs to one Organization.",
 "Users and Events are many-to-many through RSVP (status = saved, interested, or going).",
 "Users and Events are many-to-many through Report; an admin User resolves each Report.",
 "An Event may be located at a School (on campus) or have no School (off campus / community).",
])
d.add_paragraph("Consolidation — former entities now stored as attributes:").runs[0].bold = True
table(d, ["Former entity", "Now stored as", "Why"], [
 ("Category / Event Type", "EVENT.category (fixed list)", "A single label describing an event; no data of its own."),
 ("Interest", "USER.interests (list of categories)", "Same values as category; only describes a user."),
 ("Location / Venue", "EVENT.venue_name, address, latitude, longitude, is_on_campus", "Each event has one location; no need to manage venues separately in v1."),
 ("Role / Student / Organizer / Admin", "USER.role", "Same person record with different permissions."),
 ("Organizer Type (Club, Business, etc.)", "ORGANIZATION.org_type", "One organization table with a type column."),
 ("Verification", "ORGANIZATION.verification_status, proof_url, verified_at", "One verification per organization."),
 ("Notification Preferences", "USER.notify_reminders, notify_digest, quiet_start, quiet_end", "A few settings per user."),
 ("Bookmark / Saved Event", "RSVP.status = 'saved'", "Same user–event link as an RSVP."),
 ("Reminder / Notification", "RSVP.reminder_sent (sent by a scheduled job)", "Generated from RSVPs and event times; no need to store each message in v1."),
 ("Calendar Entry", "Not stored — generated as an .ics file", "Created on demand from EVENT data."),
], widths=[1.7, 2.6, 2.6])

d.add_heading("2.4 System Flow Chart", 2)
d.add_paragraph("Detailed flow of the main paths: onboarding, discovery, engagement, notifications, organizer posting, verification, and moderation. "
                "Bracketed codes (e.g., [F2.4]) refer to the feature chart. A full-resolution PNG/PDF is provided separately.")
landscape_pic(d, "Detailed_Flow_Chart.png", "Figure 3 — Detailed System Flow Chart")

d.add_heading("Appendix — Interview questions used to inform this specification", 2)
qs = ["Walk through a student's journey from opening the app to finding an event.", "Profile information and how it is used.",
      "How the app learns a student's interests.", "How \"nearby\" is determined.", "Search and filter needs.",
      "Required information when posting an event.", "Who can create events; distinguishing students, clubs, schools, businesses, community orgs.",
      "Handling inaccurate, inappropriate, fake, canceled, or outdated events.", "Getting scattered social-media/website event info into the app.",
      "What happens when a student is interested (save, join, calendar).", "Notifications and reminders without overload.",
      "Highest-priority event types for v1.", "Handling events from other schools and outside organizations.",
      "Information shown on an event page.", "Essential features for the first version."]
for i, q in enumerate(qs, 1):
    d.add_paragraph(f"Q{i}. {q}", style='List Number' if False else None)

d.add_heading("Appendix — Database schema (SQL)", 2)
for line in open("schema.sql").read().splitlines():
    p = d.add_paragraph(); p.paragraph_format.space_after = Pt(0)
    r = p.add_run(line if line else " "); r.font.name = "Courier New"; r.font.size = Pt(8)
d.save("Level_1_Specification.docx")
print("built", acc, rej)
