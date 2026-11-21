-- CampusConnect: high-level database schema (PostgreSQL)
-- 6 tables. Lookup-style values (role, category, org type, statuses, reasons)
-- are stored as constrained attributes, not separate tables.

CREATE TABLE school (
    school_id     SERIAL PRIMARY KEY,
    name          VARCHAR(150) NOT NULL,
    email_domain  VARCHAR(100) NOT NULL UNIQUE,      -- e.g. 'sjsu.edu'
    city          VARCHAR(80),
    state         CHAR(2),
    latitude      DECIMAL(9,6),
    longitude     DECIMAL(9,6)
);

CREATE TABLE app_user (
    user_id           SERIAL PRIMARY KEY,
    school_id         INT REFERENCES school(school_id),
    email             VARCHAR(255) NOT NULL UNIQUE,
    password_hash     VARCHAR(255) NOT NULL,
    email_verified    BOOLEAN NOT NULL DEFAULT FALSE,
    first_name        VARCHAR(60) NOT NULL,
    last_name         VARCHAR(60) NOT NULL,
    role              VARCHAR(20) NOT NULL DEFAULT 'student'
                      CHECK (role IN ('student','organizer','admin')),
    major             VARCHAR(100),
    class_year        VARCHAR(20),                     -- freshman ... graduate
    interests         TEXT[],                          -- list of event categories
    home_lat          DECIMAL(9,6),                    -- GPS or campus/ZIP fallback
    home_lng          DECIMAL(9,6),
    radius_miles      INT NOT NULL DEFAULT 5,
    notify_reminders  BOOLEAN NOT NULL DEFAULT TRUE,
    notify_digest     BOOLEAN NOT NULL DEFAULT TRUE,
    quiet_start       TIME,
    quiet_end         TIME,
    created_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE organization (
    org_id               SERIAL PRIMARY KEY,
    owner_user_id        INT NOT NULL REFERENCES app_user(user_id),
    school_id            INT REFERENCES school(school_id),  -- NULL for businesses/community orgs
    name                 VARCHAR(150) NOT NULL,
    description          TEXT,
    contact_email        VARCHAR(255),
    org_type             VARCHAR(20) NOT NULL
                         CHECK (org_type IN ('club','school_dept','business','community')),
    verification_status  VARCHAR(20) NOT NULL DEFAULT 'pending'
                         CHECK (verification_status IN ('pending','verified','denied')),
    proof_url            VARCHAR(500),
    verified_at          TIMESTAMP
);

CREATE TABLE event (
    event_id      SERIAL PRIMARY KEY,
    org_id        INT NOT NULL REFERENCES organization(org_id),
    school_id     INT REFERENCES school(school_id),         -- NULL if off campus
    title         VARCHAR(150) NOT NULL,
    description   TEXT NOT NULL,
    image_url     VARCHAR(500),
    category      VARCHAR(30) NOT NULL,                     -- social, academic, career, sports, arts, volunteer, food, ...
    start_time    TIMESTAMP NOT NULL,
    end_time      TIMESTAMP NOT NULL CHECK (end_time > start_time),
    venue_name    VARCHAR(150) NOT NULL,
    address       VARCHAR(255) NOT NULL,
    latitude      DECIMAL(9,6) NOT NULL,
    longitude     DECIMAL(9,6) NOT NULL,
    is_on_campus  BOOLEAN NOT NULL DEFAULT TRUE,
    cost          DECIMAL(7,2) NOT NULL DEFAULT 0,          -- 0 = free
    ticket_url    VARCHAR(500),                             -- external ticketing, no in-app payments
    status        VARCHAR(20) NOT NULL DEFAULT 'active'
                  CHECK (status IN ('active','canceled','archived')),
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE rsvp (
    rsvp_id        SERIAL PRIMARY KEY,
    user_id        INT NOT NULL REFERENCES app_user(user_id),
    event_id       INT NOT NULL REFERENCES event(event_id),
    status         VARCHAR(20) NOT NULL
                   CHECK (status IN ('saved','interested','going')),
    reminder_sent  BOOLEAN NOT NULL DEFAULT FALSE,
    created_at     TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, event_id)
);

CREATE TABLE report (
    report_id    SERIAL PRIMARY KEY,
    event_id     INT NOT NULL REFERENCES event(event_id),
    reporter_id  INT NOT NULL REFERENCES app_user(user_id),
    reason       VARCHAR(20) NOT NULL
                 CHECK (reason IN ('fake','inappropriate','inaccurate','canceled','outdated')),
    details      TEXT,
    status       VARCHAR(20) NOT NULL DEFAULT 'open'
                 CHECK (status IN ('open','resolved','dismissed')),
    resolved_by  INT REFERENCES app_user(user_id),
    created_at   TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_event_start    ON event (start_time);
CREATE INDEX idx_event_category ON event (category);
CREATE INDEX idx_event_location ON event (latitude, longitude);
