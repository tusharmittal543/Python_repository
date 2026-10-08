# Transit Tracking

A Django-based vehicle and passenger transport tracking application. It uses SQLite for local development, Django authentication and admin, and Leaflet/OpenStreetMap for trip maps.

## Requirements

- Python 3.10 or later
- pip
- Internet access in the browser for Leaflet, map tiles, and web fonts

## Windows setup

Run these commands in PowerShell from the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations vehicles drivers routes trips tracking
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and sign in. The Django admin is at `/admin/`. Create passenger accounts in the admin, then assign them to trips. Create a Driver record and connect its optional user account to allow that account to submit GPS points.

PowerShell may block activation scripts. In that case, skip activation and invoke `.\.venv\Scripts\python.exe` in place of `python` for each command.

## Features

- Passenger sign-in and a scoped trip dashboard
- Admin-managed vehicles, drivers, routes, ordered stops, trips, passengers, and GPS records
- Staff-only operational report at `/reports/`
- Trip detail pages with a live map that refreshes location history every five seconds
- Authenticated GPS JSON endpoint: `GET` and `POST /api/trips/<trip-id>/locations/`
- Coordinate validation and permission checks; only the assigned driver's account or staff can post points, and only while a trip is in progress

GPS POST body:

```json
{"latitude": 40.7128, "longitude": -74.0060}
```

Requests use Django session authentication and CSRF protection. In browser clients, include the CSRF token for POST requests. Location submissions are intended for a trusted driver device; add a dedicated device credential and rate limiting before exposing ingestion to external clients.

## Configuration

The default settings are for local development. Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` as environment variables before deployment. Set `DJANGO_DEBUG=0`, use a unique secret, configure HTTPS and its proxy headers appropriately, and run `python manage.py check --deploy` before production. SQLite is suitable for development and small single-instance deployments; use PostgreSQL for concurrent production workloads.

## Checks

```powershell
python manage.py check
python manage.py test
```

See [docs/database-er-diagram.md](docs/database-er-diagram.md) for the entity relationship diagram.