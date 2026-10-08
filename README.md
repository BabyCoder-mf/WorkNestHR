# WorkNest HR — Attendance & Workforce Management

A lightweight HR web app for small teams. Employees clock in with **face
recognition** or a **PIN**, and admins manage staff, view attendance, and
see live check-in activity from a dashboard.

**Live demo:** https://worknesthr.onrender.com
**How it works:** https://lnkd.in/p/eG3iASVb
---

## Try it in 60 seconds

### Employee login (face or PIN)
- **Employee ID:** `TEST001`
- **PIN:** `1234`
- **Face:** log in with PIN first, then use the "Register Face" option
  to upload your photo. Log out. Now try "Face Login."

### Admin login (dashboard)
- **Username:** `admin`  **PIN:** `1234`
- **Username:** `hr`     **PIN:** `5678`

### What to test
1. **PIN login** → enter `TEST001` / `1234`. You'll land on your profile
   with location + attendance recorded.
2. **Face login** → register your face, log out, log back in with the camera.
3. **Admin dashboard** → log in as `admin` / `1234`. See stats, recent
   check-ins, and staff management.
4. **Add an employee** → from the dashboard, create a new staff member
   with their own PIN. They can log in immediately.

> **Heads up:** this is a shared demo. All testers use the same employee
> account (`TEST001`). Uploading your face replaces the previous photo, so
> the next face login matches whoever uploaded most recently.

---

## Features

- **Dual authentication** — PIN or face recognition (via Face++ API)
- **Attendance tracking** — automatic check-in on successful login, with
  location data (country, city, IP) from the visitor's real IP
- **Admin dashboard** — live stats, recent activity, employee management
- **Employee profiles** — contract details, department, location, photo
- **Face registration** — upload a photo once, then log in with your face

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Flask 3, Flask-SQLAlchemy, Flask-Login |
| Database | PostgreSQL (Supabase) / SQLite for local dev |
| Face recognition | Face++ API (compare endpoint) |
| Location | ip-api.com (looked up by visitor IP) |
| Hosting | Render |
| Frontend | Jinja2 templates, Bootstrap 5 |

---

## How it works

### Face login
1. Browser captures a live photo via `getUserMedia`.
2. Photo is sent as base64 to `/api/face-login`.
3. Server compares it against every stored staff face using Face++.
4. Highest-confidence match above 80% wins; the user is logged in and
   an attendance record is created.

### PIN login
1. Employee enters ID + PIN.
2. Server verifies the PIN hash (Werkzeug) against the `Staff` table.
3. On success, an attendance record is written and the profile loads.

### Location
The app reads the visitor's IP from the `X-Forwarded-For` header (set by
Render) and looks it up via ip-api.com — so location reflects the *visitor*,
not the server.

---

## Local development

```bash
git clone <your-repo>
cd <repo>
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
