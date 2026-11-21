# Product Requirements Document — Student Event App

| | |
|---|---|
| **Product** | Student Event App (prototype v1) |
| **Document owner** | [Analyst name] — Analyst |
| **Client** | [Client name] |
| **Team** | [Team name] |
| **Status** | Draft for Builder hand-off |
| **Sources** | Specification 1 (project summary, constituencies, contexts), hand-drawn feature chart, `Level_1_Specification`, `diagrams/Site_Map.png`, `schema.sql` |

## 1. Purpose

College students, especially transfer students and students new to the area, miss campus and local events. Event information is spread across social media accounts, school websites, flyers and organization pages. The Student Event App puts student-focused events in one mobile app. Students can find events that match their interests, save or join them, and get reminders. Students and student organizations can post events for others to find.

## 2. Goals and non-goals

### 2.1 Goals (v1)

| ID | Goal | How v1 meets it |
|---|---|---|
| G1 | Event discovery | Browse feed, category filters, search and event details |
| G2 | Interest matching | Interests picked during onboarding sort and filter the feed |
| G3 | Student involvement | Clubs/organizations directory and organization profiles |
| G4 | Event organization | Save, join (RSVP) and add events to a phone calendar |
| G5 | Event awareness | Reminders for saved and joined events, plus nearby-event alerts |
| G6 | Event sharing | Students and organizations create and post events |

### 2.2 Non-goals (excluded from prototype v1)

- Private messaging between users
- Ticket sales or any payment processing (an external ticket link is allowed)
- Crime reporting
- A full social media feed or general social posts
- Automatic importing of events from outside websites or social media (all events are entered in the app)

### 2.3 Success metrics (prototype)

| Metric | Target |
|---|---|
| A new user can finish onboarding (sign up → interests) | Under 2 minutes |
| A user can find an event in a chosen category from the home screen | 3 taps or fewer |
| A user can post a complete event | Under 3 minutes |
| Reminders delivered for joined or saved events | 100% of eligible events in testing |

## 3. Users

| Persona | Description | Main needs |
|---|---|---|
| **New / transfer student** (primary) | New to campus or the area; doesn't know where to look for events | A quick, single place to see what's happening; events matched to interests |
| **Busy student** | Works part-time or commutes; goes home right after class | Fast filtering; reminders so events aren't missed |
| **Non-social-media student** | Doesn't follow club or school accounts | Event information without needing social media |
| **Student organizer** (club officer or any student hosting) | Posts events for a club, organization or group | A simple form to post events; see who joined |

Excluded roles in v1: parents, professors, paid advertisers.

## 4. Platform and operating assumptions

- Smartphone-first (iOS and Android). Screens should also work in a phone-sized web browser for demos.
- Used on campus, at home, on the go and at community locations, often in short sessions between classes.
- Requires an internet or cellular connection. No offline mode in v1. Show a clear "no connection" message.
- Location access is optional. If it is denied, the app uses the user's school location for "nearby".
- Events are stored in the app's own database (see `schema.sql`).
- Reminders apply only to events the user has saved or joined.
- Important information should be reachable in few screens. A 5-tab bottom navigation bar is always visible after login.

## 5. Feature requirements

Feature IDs follow the hand-drawn feature chart (F1–F5). Supporting features that the app needs to work are labelled SF. Each feature links to the Level 1 user stories (S1–S10) where one applies.

Priority: **P1** = must have for the prototype; **P2** = should have if time allows.

### F1 Manage Profile

| ID | Requirement | Priority | Story |
|---|---|---|---|
| SF1 | **Sign up / log in.** Email + password sign-up and log-in. Log out from Profile. | P1 | S1 |
| F1.1 | **Create profile.** First name, last name, school, major (optional), class year (optional). | P1 | S1, S2 |
| F1.2 | **Edit profile.** User can change any profile field later. | P1 | — |
| F1.3 | **Select interests.** Pick one or more from Social, Sports, Clubs, Volunteer, Career/Networking during onboarding, and edit later. | P1 | S2 |

### F2 Discover Events

| ID | Requirement | Priority | Story |
|---|---|---|---|
| F2.1 | **Browse events.** Home feed of upcoming active events, sorted by date, with events matching the user's interests first. Each card shows title, date/time, location, category and host. | P1 | S2 |
| F2.2 | **Filter events by category.** Category tabs (Social, Sports, Clubs, Volunteer, Career/Networking) plus a filter panel for date range and "nearby" distance. | P1 | S3, S4 |
| SF2 | **Search events.** Keyword search on title, description and host name. Shows an empty-state message with "clear filters". | P1 | S4 |
| F2.3 | **View event details.** Title, description, category, date/time, venue and address, host organization, cost (free or amount), optional external ticket link, and number of students going. Actions: Join/RSVP, Save, Add to Calendar, view host. | P1 | S5 |
| F2.4 | **Find clubs/organizations.** Searchable list of organizations. | P1 | — |
| SF3 | **Organization profile.** Name, type, description, contact email, and the organization's upcoming events. | P1 | — |

### F3 Manage Events

| ID | Requirement | Priority | Story |
|---|---|---|---|
| F3.1 | **Create event.** Form with required fields: title, category, start and end date/time, venue name, address, description, host organization. Optional: image, cost, ticket link. The poster picks an organization they own or creates one in the same flow. | P1 | S7 |
| F3.2 | **Post event.** Preview, then publish. The event appears in the feed immediately. Missing or invalid fields block publishing. | P1 | S7 |
| SF4 | **My posted events.** List of the user's events with Edit, Cancel, and the list of students who joined. Canceling notifies joined and saving students. | P1 | S7, S8 |
| F3.3 | **Join / RSVP to event.** One tap to join or leave. The event's "going" count updates. | P1 | S6 |

### F4 Saved Events

| ID | Requirement | Priority | Story |
|---|---|---|---|
| F4.1 | **Save / bookmark event.** One tap to save or unsave from the feed or event details. | P1 | S6 |
| F4.2 | **View saved events.** Saved tab with two lists: Saved and Joined, upcoming first. | P1 | S6 |
| F4.3 | **Add event to calendar.** Generates a standard `.ics` file (title, time, location, description) that opens in Google, Apple or Outlook calendar. | P1 | S6 |

### F5 Notifications

| ID | Requirement | Priority | Story |
|---|---|---|---|
| F5.1 | **Upcoming event reminder.** Push reminder 24 hours and 1 hour before a joined event. | P1 | S8 |
| F5.2 | **Saved event reminder.** Push reminder 24 hours before a saved event. | P1 | S8 |
| F5.3 | **Nearby event alerts.** Push alert when a new event matching the user's interests is posted within their chosen radius. Maximum one per day. | P2 | S3 |
| SF5 | **Notification center and settings.** Notifications tab lists upcoming reminders and alerts. Settings let the user turn reminders and nearby alerts on or off and set the radius (1, 5, 10 or 25 miles). | P1 | S8 |
| SF5.1 | **Change / cancel alerts.** Users who joined or saved an event are notified when it is edited (time or place) or canceled. | P1 | S8 |

### SF6 Trust (P2)

| ID | Requirement | Priority | Story |
|---|---|---|---|
| SF6.1 | **Report event.** Report an event as fake, inappropriate, inaccurate, canceled or outdated. | P2 | S9 |
| SF6.2 | **Review reports.** Admin can dismiss a report or cancel the event. | P2 | S9 |
| SF6.3 | **Verified organization badge.** Admin can mark an organization as verified. Verification is not required to post in v1. | P2 | S10 |
| SF6.4 | **Auto-archive.** Events whose end time has passed are hidden from the feed. | P1 | S7 |

## 6. Main user flows

1. **Onboarding:** Launch → Sign up → Create profile → Select interests → Allow location (optional) → Home feed.
2. **Discover and join:** Home → category tab or search → Event details → Join → Add to calendar → reminder 24 h and 1 h before.
3. **Save for later:** Event details → Save → Saved tab → reminder 24 h before.
4. **Post an event:** Manage Events (+) → Create event form → Preview → Post → confirmation → event in feed.
5. **Change an event:** My posted events → Edit or Cancel → joined and saving students are notified.

The full screen hierarchy is in `diagrams/Site_Map.png` and the step-by-step logic is in `diagrams/Detailed_Flow_Chart.png`.

## 7. Data requirements

Use the six-table schema in `schema.sql`:

| Table | Purpose |
|---|---|
| `school` | Campus name and location (used as the default "nearby" point) |
| `app_user` | Account, profile, interests, role, location/radius and notification settings |
| `organization` | Event host (club, school department, business, community group); owned by a user |
| `event` | Posted event; `category`, venue/address, coordinates, cost, `status` (active, canceled, archived) |
| `rsvp` | Links a user to an event: `status` = saved, interested or going; `reminder_sent` flag |
| `report` | P2: a user's report on an event and its resolution |

Category, interests, role, verification and notification settings are columns, not separate tables. Calendar entries are generated `.ics` files and are not stored.

## 8. Non-functional requirements

| Area | Requirement |
|---|---|
| Performance | Feed and search results load in under 2 seconds on a typical 4G connection |
| Usability | Every P1 feature is reachable within 3 taps of a bottom tab; text is readable at default phone font size |
| Accessibility | All buttons have text labels; color is never the only signal; meets WCAG 2.1 AA contrast |
| Security & privacy | Passwords are hashed; users only edit their own profile, organizations and events; RSVP lists show names only to the event's organizer |
| Reliability | Reminders are sent once per event (use `rsvp.reminder_sent`) |

## 9. Assumptions, risks and open questions

| # | Item | Type |
|---|---|---|
| 1 | Should sign-up be limited to school (.edu) emails? Level 1 Story S1 assumes yes; Specification 1 doesn't say. | Open question |
| 2 | Can any student post an event, or only verified organizations? This PRD follows Specification 1: any student can post, and verification is a P2 badge. | Decision to confirm |
| 3 | Events will be sparse at launch because there is no auto-import. Mitigation: seed the database with real campus events before demos. | Risk |
| 4 | Push notifications need a physical device for testing. | Risk |
| 5 | Interview answers in the Level 1 Specification were assumed and still need client confirmation. | Assumption |

## 10. Release plan

| Milestone | Contents |
|---|---|
| M1 — Foundation | Project setup, database, sign-up/log-in, profile, interests |
| M2 — Discover | Feed, category filters, search, event details, organizations |
| M3 — Engage & post | Join, save, saved tab, calendar, create/post/edit/cancel events |
| M4 — Notify | Reminders, change/cancel alerts, notification center and settings |
| M5 — Polish (P2) | Nearby alerts, reporting, verified badge, accessibility pass, demo data |

Detailed tasks and acceptance criteria are in `Task_List.md`.
