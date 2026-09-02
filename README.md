# Instant Mechanic API

A simple backend API for a mechanic-service platform, built with Django + Django REST Framework (DRF).

Customers can view mechanics and request a service. Built for a Python Development Internship assignment.

---

## What this project does

- Lets you manage mechanics (create, view, update, delete)
- Lets a customer create a "service request" to a mechanic (e.g. oil change, tyre repair)
- Every service request starts with status `PENDING`
- Checks for mistakes (like wrong phone number, non-existent mechanic, etc.) and returns clear error messages

---

## Tech used

- Python 3
- Django (web framework)
- Django REST Framework (turns Django into a JSON API)
- SQLite (database — comes built into Python, no setup needed)

---

## How to run this project on your computer

1. Open a terminal in this project folder.

2. Create and activate a virtual environment (keeps this project's packages separate from the rest of your computer):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   You'll know it worked when you see `(venv)` at the start of your terminal line.

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Start the server:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and go to:
   ```
   http://127.0.0.1:8000/api/mechanics/
   ```
   You should see a page with an empty list `[]` — that means it's working.

---

## The two main things this API can do

### 1. Mechanics — `/api/mechanics/`

A mechanic has: `name`, `phone`, `location`, `rating`, `is_open`, `services` (a list, e.g. `["Oil Change", "Tyre Repair"]`).

| What you want to do | Method | URL |
|---|---|---|
| See all mechanics | GET | `/api/mechanics/` |
| See one mechanic | GET | `/api/mechanics/1/` |
| Add a new mechanic | POST | `/api/mechanics/` |
| Edit a mechanic | PATCH | `/api/mechanics/1/` |
| Remove a mechanic | DELETE | `/api/mechanics/1/` |

**Example — adding a mechanic:**
```bash
curl -X POST http://127.0.0.1:8000/api/mechanics/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Raju Auto Works","phone":"9876543210","location":"Agra","rating":4.5,"is_open":true,"services":["Oil Change","Tyre Repair"]}'
```

**What you get back:**
```json
{
  "id": 1,
  "name": "Raju Auto Works",
  "phone": "9876543210",
  "location": "Agra",
  "rating": "4.5",
  "is_open": true,
  "services": ["Oil Change", "Tyre Repair"]
}
```

### 2. Service Requests — `/api/service-requests/`

A customer uses this to ask a mechanic for a service. It needs: `customer_name`, `customer_phone`, `vehicle_number`, `mechanic` (the mechanic's id), `service`, `problem_description`.

| What you want to do | Method | URL |
|---|---|---|
| See all requests | GET | `/api/service-requests/` |
| See one request | GET | `/api/service-requests/1/` |
| Create a request | POST | `/api/service-requests/` |
| Edit a request | PATCH | `/api/service-requests/1/` |
| Remove a request | DELETE | `/api/service-requests/1/` |

**Example — creating a request:**
```bash
curl -X POST http://127.0.0.1:8000/api/service-requests/ \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Amit","customer_phone":"9123456780","vehicle_number":"UP16AB1234","mechanic":1,"service":"Oil Change","problem_description":"Engine oil leak near the filter"}'
```

**What you get back:**
```json
{
  "id": 1,
  "customer_name": "Amit",
  "customer_phone": "9123456780",
  "vehicle_number": "UP16AB1234",
  "mechanic": 1,
  "service": "Oil Change",
  "problem_description": "Engine oil leak near the filter",
  "status": "PENDING",
  "created_at": "2026-09-02T13:25:00Z"
}
```

---

## What happens if you make a mistake (error handling)

| Mistake | What the API does |
|---|---|
| Phone number isn't a valid 10-digit number | Returns an error explaining the phone format |
| Vehicle number isn't valid | Returns an error explaining the vehicle number format |
| Mechanic id doesn't exist | Returns `400 Bad Request` — "Mechanic with this ID does not exist." |
| A required field is missing (like `name`) | Returns `400 Bad Request` — "This field is required." |
| Requested service isn't one the mechanic offers | Returns `400 Bad Request` listing the mechanic's actual services |

---

## Project structure (what each file does)

```
instant-mechanic-api/
├── core/               → main Django project settings & URLs
├── mechanics/          → the actual app (all the logic lives here)
│   ├── models.py       → defines Mechanic and ServiceRequest (the database tables)
│   ├── serializers.py  → converts data to/from JSON, and does validation
│   ├── views.py        → handles the actual GET/POST/PUT/DELETE logic
│   ├── urls.py         → maps URLs to views
│   └── admin.py        → lets you view/edit data at /admin/
├── manage.py           → Django's command-line tool
└── requirements.txt    → list of Python packages this project needs
```

---

## Notes for the interview

- `Mechanic` and `ServiceRequest` are linked with a `ForeignKey` — one mechanic can have many service requests.
- Validation happens in two places: field-level (regex checks on phone/vehicle number in `models.py`) and object-level (checking the requested service is one the mechanic actually offers, in `serializers.py`).
- `status` and `created_at` on a service request are `read_only` — a customer can't set these themselves; they're controlled by the server.