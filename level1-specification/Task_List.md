# Task List with Acceptance Criteria — Student Event App (prototype v1)

How to use this list:
- Do tasks in order inside each milestone. A task is **done** only when every acceptance criterion (AC) passes.
- Feature IDs (F, SF) and story IDs (S) refer to `Product_Requirements_Document.md` and `Level_1_Specification`.
- Priority: **P1** = must have; **P2** = should have.
- Check a box `[x]` when the task is done.

---

## M1 — Foundation

### T1. Set up the project — P1
- [ ] Done
- **Refs:** Workspace Rules §2
- **AC:**
  1. The app starts on an iOS or Android phone (or simulator) and shows a placeholder Welcome screen.
  2. The repository has a README with the commands to install and run the app.
  3. Lint and type checks run with one command and pass.

### T2. Create the database — P1
- [ ] Done
- **Refs:** PRD §7, `schema.sql`
- **AC:**
  1. Running `schema.sql` on an empty PostgreSQL database creates all 6 tables with no errors.
  2. A seed script adds 1 school, 3 users (student, organizer, admin), 3 organizations and at least 15 upcoming events covering all 5 categories.
  3. Inserting an event whose `end_time` is before its `start_time` is rejected.
  4. Inserting a second `rsvp` row for the same user and event is rejected.

### T3. Sign up, log in and log out — P1
- [ ] Done
- **Refs:** SF1, S1
- **AC:**
  1. **Given** a new email and a password of at least 8 characters, **when** the user signs up, **then** an `app_user` row is created with a hashed (never plain-text) password.
  2. Signing up with an email that already exists shows "An account with this email already exists."
  3. Logging in with a wrong password shows an error and does not reveal whether the email exists.
  4. A logged-in user stays logged in after closing and reopening the app.
  5. Log Out (Profile tab) returns the user to the Welcome screen.

### T4. Create profile and select interests (onboarding) — P1
- [ ] Done
- **Refs:** F1.1, F1.3, S2
- **AC:**
  1. After sign-up, the user sees Create Profile → Select Interests → Allow Location, in that order.
  2. First name, last name and school are required; Continue stays disabled until they are filled in.
  3. The Interests screen shows all 5 categories (Social, Sports, Clubs, Volunteer, Career/Networking); at least one must be picked.
  4. Choosing "Not now" on Allow Location still finishes onboarding; the school location is used for "nearby".
  5. After onboarding, the user lands on the Home feed with the bottom tab bar visible.

### T5. Edit profile and interests — P1
- [ ] Done
- **Refs:** F1.2, F1.3
- **AC:**
  1. Profile → Edit Profile shows the current values, and saved changes appear right away.
  2. Changing interests changes the order of the Home feed the next time it loads.
  3. A user cannot view or edit another user's profile settings.

---

## M2 — Discover

### T6. Bottom tab navigation — P1
- [ ] Done
- **Refs:** PRD §4, Site Map
- **AC:**
  1. Five tabs are always visible after login: Discover, Saved, Manage Events (+), Notifications, Profile.
  2. Each tab keeps its scroll position when the user switches away and back.

### T7. Browse events feed — P1
- [ ] Done
- **Refs:** F2.1, S2
- **AC:**
  1. The feed shows only events with `status = 'active'` whose end time has not passed.
  2. Events in the user's interest categories appear before other events; within each group, events are sorted by start time.
  3. Each card shows title, date/time, venue, category and host name.
  4. Pull-to-refresh reloads the feed.
  5. If there are no events, the feed shows "No upcoming events yet" instead of a blank screen.

### T8. Filter events by category, date and distance — P1
- [ ] Done
- **Refs:** F2.2, S3, S4
- **AC:**
  1. Tapping a category tab shows only events in that category; tapping "All" clears it.
  2. The filter panel offers date (Today, This week, This month) and distance (1, 5, 10, 25 miles).
  3. Distance is measured from the user's location, or from the school if location is off.
  4. Filters can be combined, and an active-filter count is shown.
  5. If no events match, the screen shows "No events match" with a Clear filters button.

### T9. Search events — P1
- [ ] Done
- **Refs:** SF2, S4
- **AC:**
  1. Searching matches words in event title, description and host name, not case-sensitive.
  2. Results appear within 2 seconds on a 4G connection.
  3. Search works together with active category and date filters.

### T10. Event details screen — P1
- [ ] Done
- **Refs:** F2.3, S5
- **AC:**
  1. Shows title, description, category, start/end date and time, venue and address, host organization (tappable), cost ("Free" when 0), and the number of students going.
  2. If the event has a ticket link, a "Get tickets" button opens it in the browser; no payment happens in the app.
  3. Join, Save and Add to Calendar buttons are visible without scrolling on a standard phone screen.
  4. A canceled event shows a red "Canceled" banner, and Join/Save are disabled.
  5. The same screen opens from the feed, search, Saved tab, notifications and organization profiles.

### T11. Clubs/organizations directory and profile — P1
- [ ] Done
- **Refs:** F2.4, SF3
- **AC:**
  1. Discover → Find Clubs/Organizations lists all organizations alphabetically, with name search.
  2. The organization profile shows name, type, description, contact email and its upcoming events.
  3. Tapping an event on the profile opens Event Details.

---

## M3 — Engage & post

### T12. Join / RSVP to an event — P1
- [ ] Done
- **Refs:** F3.3, S6
- **AC:**
  1. Tapping Join sets the user's `rsvp.status` to `going`, and the button changes to "Joined ✓".
  2. Tapping "Joined ✓" again removes the RSVP.
  3. The going count on Event Details updates without reloading the screen.
  4. Joining a saved event changes the existing RSVP row instead of creating a second one.

### T13. Save / bookmark an event — P1
- [ ] Done
- **Refs:** F4.1, S6
- **AC:**
  1. The Save icon on a feed card or Event Details toggles saved and unsaved (`rsvp.status = 'saved'`).
  2. The saved state shows the same way everywhere the event appears.

### T14. Saved tab — P1
- [ ] Done
- **Refs:** F4.2, S6
- **AC:**
  1. The Saved tab has two lists, Saved and Joined, each sorted by start time with upcoming events first.
  2. Past events are not shown.
  3. Remove from Saved and Cancel RSVP work directly from the list.
  4. Empty lists show a "Browse events" button that opens the Discover tab.

### T15. Add event to calendar — P1
- [ ] Done
- **Refs:** F4.3, S6
- **AC:**
  1. Add to Calendar creates a valid `.ics` file with title, start/end time (correct time zone), address and description.
  2. The file opens in the phone's default calendar app (tested on at least one of Google, Apple or Outlook calendar).

### T16. Create and post an event — P1
- [ ] Done
- **Refs:** F3.1, F3.2, S7
- **AC:**
  1. The Manage Events (+) tab opens the Create Event form.
  2. Required fields: title, category, start date/time, end date/time, venue name, address, description, host organization. Post stays disabled until all are valid.
  3. End time must be after start time, and start time must be in the future; otherwise an inline error shows under the field.
  4. If the user owns no organization, they can create one (name, type, contact email) without leaving the form.
  5. Preview shows the event exactly as Event Details will show it.
  6. After Post, a confirmation appears and the event is in the Home feed within 5 seconds.
  7. The address is converted to latitude/longitude so the event works with distance filters.

### T17. My posted events: edit, cancel, view who joined — P1
- [ ] Done
- **Refs:** SF4, S7, S8
- **AC:**
  1. Manage Events lists events from organizations the user owns, upcoming first.
  2. Edit uses the same validation as Create; saved edits appear in the feed right away.
  3. Cancel asks for confirmation and sets `status = 'canceled'`; the event leaves the feed.
  4. View RSVP List shows the names of joined students and is visible only to the owner.
  5. A user cannot edit or cancel an event they do not own (checked on the server, not only hidden in the UI).

### T18. Auto-archive past events — P1
- [ ] Done
- **Refs:** SF6.4
- **AC:**
  1. Events whose end time has passed get `status = 'archived'` (scheduled job or query filter) and leave the feed, search and Saved lists.
  2. Archived events still appear in the organizer's history as "Past".

---

## M4 — Notify

### T19. Push notification setup and permission — P1
- [ ] Done
- **Refs:** SF5
- **AC:**
  1. The app asks for notification permission the first time the user joins or saves an event, not at launch.
  2. If permission is denied, the app keeps working and Notification Settings explains how to turn it on.

### T20. Upcoming and saved event reminders — P1
- [ ] Done
- **Refs:** F5.1, F5.2, S8
- **AC:**
  1. A user who joined an event gets reminders 24 hours and 1 hour before it starts.
  2. A user who saved (not joined) an event gets one reminder 24 hours before it starts.
  3. No reminder is sent if the RSVP was removed or the event was canceled.
  4. No reminder is sent twice for the same event (`reminder_sent` is used).
  5. Tapping a reminder opens that event's Event Details.
  6. No reminders are sent when the user has turned reminders off.

### T21. Change and cancel alerts — P1
- [ ] Done
- **Refs:** SF5.1, S8
- **AC:**
  1. When an organizer changes an event's date, time or location, every user who saved or joined it gets an alert saying what changed.
  2. When an event is canceled, those users get a "Canceled" alert.
  3. Edits to only the description or image do not send an alert.

### T22. Notification center and settings — P1
- [ ] Done
- **Refs:** SF5
- **AC:**
  1. The Notifications tab lists the user's upcoming reminders and recent alerts, newest first.
  2. Settings has on/off switches for reminders and nearby alerts, and a radius choice (1, 5, 10, 25 miles); changes are saved to `app_user`.

---

## M5 — Polish (P2 unless noted)

### T23. Nearby event alerts — P2
- [ ] Done
- **Refs:** F5.3, S3
- **AC:**
  1. When a new event is posted within the user's radius and matches one of their interests, the user gets an alert.
  2. A user gets at most one nearby alert per day.
  3. No nearby alerts are sent when the setting is off.

### T24. Report an event and review reports — P2
- [ ] Done
- **Refs:** SF6.1, SF6.2, S9
- **AC:**
  1. Event Details has a Report option with the reasons fake, inappropriate, inaccurate, canceled, outdated and an optional details box.
  2. A user can report the same event only once.
  3. An admin can see open reports and either dismiss the report or cancel the event; canceling sends the T21 cancel alert.

### T25. Verified organization badge — P2
- [ ] Done
- **Refs:** SF6.3, S10
- **AC:**
  1. An admin can set an organization's `verification_status` to verified or denied.
  2. Verified organizations show a badge on event cards, Event Details and the organization profile.
  3. Unverified organizations can still post events.

### T26. Accessibility and usability pass — P1
- [ ] Done
- **Refs:** PRD §8
- **AC:**
  1. Every button and icon has an accessibility label that a screen reader reads.
  2. Text and button colors meet WCAG 2.1 AA contrast.
  3. Every P1 feature is reachable within 3 taps of a bottom tab.

### T27. Demo data and end-to-end test — P1
- [ ] Done
- **Refs:** PRD §2.3, §6
- **AC:**
  1. The database is seeded with at least 25 realistic upcoming events across all 5 categories.
  2. All five main flows in PRD §6 are completed on a real phone without errors.
  3. The PRD §2.3 success metrics are timed and recorded in the README.

### T28. Confirm v1 exclusions — P1
- [ ] Done
- **Refs:** PRD §2.2
- **AC:**
  1. The app has no private messaging, in-app payments, crime reporting, social feed or automatic event importing.
