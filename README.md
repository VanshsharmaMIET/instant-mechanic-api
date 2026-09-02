# Instant Mechanic API

Backend API for a mechanic-service platform, built with Django + Django REST Framework. Customers can view mechanics and create service requests.

## Tech Stack
Python, Django, DRF, SQLite, Token Auth, drf-spectacular (Swagger), django-filter

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Authentication
GET requests are public. POST/PUT/PATCH/DELETE need a token.

Get a token:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ -d "username=YOUR_USERNAME&password=YOUR_PASSWORD"
```

Use it:
```
Authorization: Token YOUR_TOKEN
```

## API Docs
```
http://127.0.0.1:8000/api/docs/
```

## Endpoints

### Mechanics — `/api/mechanics/`
| Method | URL | Auth |
|---|---|---|
| GET | /api/mechanics/ | No |
| GET | /api/mechanics/?search=Agra | No |
| GET | /api/mechanics/{id}/ | No |
| POST | /api/mechanics/ | Yes |
| PATCH | /api/mechanics/{id}/ | Yes |
| DELETE | /api/mechanics/{id}/ | Yes |

### Service Requests — `/api/service-requests/`
| Method | URL | Auth |
|---|---|---|
| GET | /api/service-requests/ | No |
| GET | /api/service-requests/{id}/ | No |
| POST | /api/service-requests/ | Yes |
| PATCH | /api/service-requests/{id}/ | Yes |
| DELETE | /api/service-requests/{id}/ | Yes |

## Sample Request
```bash
curl -X POST http://127.0.0.1:8000/api/mechanics/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Raju Auto Works","phone":"9876543210","location":"Agra","rating":4.5,"is_open":true,"services":["Oil Change","Tyre Repair"]}'
```

## Sample Response
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

## Error Handling
- Invalid phone/vehicle number → 400 with format message
- Mechanic doesn't exist → 400
- Missing required field → 400
- Invalid service (not offered by mechanic) → 400
- No auth token on write → 403

## Tests
```bash
python manage.py test
```

## Project Structure
```
core/           → project settings & URLs
mechanics/      → app (models, serializers, views, urls, admin, tests)
manage.py
requirements.txt
```