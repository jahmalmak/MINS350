# Workspace Rules — Student Event App

These rules are for the Builder and any AI coding assistant working in this repository (for example, paste them into Cursor/Windsurf workspace rules or an `AGENTS.md` file). Follow them on every task.

## 1. Sources of truth

1. **What to build:** `Product_Requirements_Document.md`. **In what order and when it's done:** `Task_List.md`.
2. **Screens and navigation:** `diagrams/Site_Map.png`. **Logic:** `diagrams/Detailed_Flow_Chart.png`.
3. **Database:** `schema.sql`. Do not add tables or columns without updating `schema.sql` and the ERD first, and noting why in the pull request.
4. If these documents disagree, the PRD wins. Ask the Analyst instead of guessing.

## 2. Tech stack (assumed — change here if the team picks something else)

| Layer | Choice |
|---|---|
| Mobile app | React Native with Expo, TypeScript (strict mode) |
| Backend / database | Supabase (PostgreSQL, Auth, Storage, Edge Functions), set up from `schema.sql` |
| Push notifications | Expo Notifications |
| Maps / geocoding | Expo Location + a geocoding API for event addresses |
| Testing | Jest + React Native Testing Library |
| Lint / format | ESLint + Prettier |

Do not add a new library when the stack above already covers the need. Any new dependency must be well known and maintained, and named in the pull request.

## 3. Scope guardrails

- Build only P1 tasks until every P1 task is done. Then do P2 tasks.
- **Never build v1 exclusions:** private messaging, ticket sales or payments, crime reporting, social feed or general posts, automatic event importing or scraping.
- Do not add features that aren't in the PRD (for example dark mode, ratings, friends, chatbots). Write them up as suggestions instead.
- Keep the 5-tab bottom navigation: Discover, Saved, Manage Events (+), Notifications, Profile.
- Use the fixed category list everywhere: Social, Sports, Clubs, Volunteer, Career/Networking. Define it once in a shared constants file.

## 4. Code conventions

- TypeScript everywhere; no `any` without a comment explaining why.
- Folder layout: `app/` (screens, by tab), `components/` (reusable UI), `lib/` (database, notifications, calendar, location helpers), `types/` (shared types matching `schema.sql`).
- One screen per file; name screens after the site map (for example `EventDetailsScreen`, `CreateEventScreen`).
- Database column names stay `snake_case` as in `schema.sql`; TypeScript variables use `camelCase`.
- Keep components small. Move data access into `lib/` and never call the database directly from UI components.
- Store dates in UTC; show them in the phone's local time zone.
- Comments explain *why*, not *what*.

## 5. Data and security

- Never store plain-text passwords; use Supabase Auth.
- Turn on Row Level Security. Users can only change their own profile, RSVPs, organizations and those organizations' events. Only the event's organizer can see its RSVP list. Only admins can change `verification_status` or resolve reports.
- Check permissions on the server, not just by hiding buttons.
- Never commit secrets or API keys. Use `.env` (listed in `.gitignore`) and commit a `.env.example`.
- Use only fake data in seeds; no real student names or emails.

## 6. UX rules

- Mobile-first. Design for a 375 px-wide screen first.
- Every list has loading, empty and error states.
- Every P1 feature is reachable within 3 taps of a bottom tab.
- Event Details is one shared screen; don't make copies of it for different tabs.
- Buttons have text or accessibility labels; color is never the only signal; meet WCAG 2.1 AA contrast.
- Ask for location and notification permission only when the user first needs them, and keep the app working if they say no.

## 7. Workflow

- Work on one task from `Task_List.md` at a time, on its own branch named `task/T<number>-<short-name>` (for example `task/T12-rsvp`).
- Open a pull request for each task. The description lists the task ID and how each acceptance criterion was checked.
- A task is done only when all of its acceptance criteria pass; then check its box in `Task_List.md` in the same pull request.
- Run lint, type checks and tests before every commit; don't merge with failures.
- Write commit messages in the imperative mood (for example "Add RSVP toggle to event details").
- Don't push directly to `main`.

## 8. When unsure

- If a requirement is unclear or seems to conflict, stop and ask the Analyst. List the question in the pull request.
- If a task turns out bigger than expected, split it into smaller tasks in `Task_List.md` and keep the same acceptance criteria.
