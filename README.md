# Address Book API

FastAPI app to create, update, delete and search addresses by distance.
Addresses include coordinates, are validated, and are stored in SQLite.

## Requirements
- Python 3.10 or newer
- Git

## Setup

### Windows (PowerShell)
```powershell
git clone https://github.com/<snehalatamaharana>/address-book-api.git
cd address-book-api
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux
```bash
git clone https://github.com/<snehalatamaharana>/address-book-api.git
cd address-book-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the app
```bash
uvicorn app.main:app --reload
```
Open Swagger docs: http://127.0.0.1:8000/docs

The SQLite file `address_book.db` is created automatically on first start.

## Run the tests
```bash
pytest -v
```

## Endpoints
| Method | Path | Description |
|---|---|---|
| POST | /addresses/ | Create an address |
| GET | /addresses/ | List addresses |
| GET | /addresses/{id} | Get one address |
| PATCH | /addresses/{id} | Update an address |
| DELETE | /addresses/{id} | Delete an address |
| GET | /addresses/nearby?latitude=&longitude=&distance_km= | Addresses within a distance (km) |

## Project structure
- `app/main.py`: app entry point
- `app/routers/`: API endpoints
- `app/crud.py`: database operations
- `app/models.py`: SQLAlchemy models
- `app/schemas.py`: Pydantic validation
- `app/utils/geo.py`: Haversine distance
- `app/logging_config.py`: logging setup
- `tests/`: pytest tests

## Design notes
- Validation: latitude -90 to 90, longitude -180 to 180, string length limits
- Distance search: SQL latitude-band pre-filter, then exact Haversine check
- Logging: create, update, delete and not-found events are logged