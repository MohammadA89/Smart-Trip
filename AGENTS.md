# Smart Trip Project Guide

## Project Overview
Smart Trip is a Flask web application that recommends nearby or city-based travel destinations. It combines OpenStreetMap lookups with local demo data and a lightweight recommendation/ranking layer.

## Goals and Requirements
- Provide a runnable local Flask application.
- Recommend five suitable places based on user preferences such as activity, group type, budget, people count, car availability, location, radius, and city search.
- Fall back to demo data when OpenStreetMap is unavailable or returns too few results.
- Persist recommendation events and learned weights in SQLite.

## Technology Stack
- Python 3
- Flask
- SQLite
- OpenStreetMap/Nominatim/Overpass via standard library HTTP calls and `overpy`
- HTML, CSS, and JavaScript frontend assets under `smarttrip/templates` and `smarttrip/static`

## Architecture Decisions
- Use an application factory (`smarttrip.app:create_app`) so the app can be imported by scripts, tests, and WSGI servers.
- Store local state in `instance/smarttrip.sqlite`; keep generated database files out of source control.
- Keep external API access isolated under `smarttrip/services`.
- Keep ranking and recommendation logic separate from Flask route handling.
- Prefer package-style execution from the repository root with `python app.py`.

## Folder Structure
- `app.py`: Root entrypoint for local development.
- `smarttrip/app.py`: Flask application factory and HTTP routes.
- `smarttrip/algorithm.py`: Demo place data and baseline calculations.
- `smarttrip/ai_recommender.py`: Feature building, ranking, and feedback weight updates.
- `smarttrip/chat_parser.py`: Natural language parsing for chat-style user input.
- `smarttrip/storage.py`: SQLite schema and persistence helpers.
- `smarttrip/services/osm_service.py`: OpenStreetMap/Nominatim/Overpass integration.
- `smarttrip/templates/index.html`: Main UI template.
- `smarttrip/static/css/style.css`: Application styles.
- `smarttrip/static/js/main.js`: Client-side UI and API interaction logic.
- `requirements.txt`: Python runtime dependencies.

## Coding Standards
- Write production-quality, readable Python with clear names and focused functions.
- Keep route handlers thin where practical; move reusable logic into services or helper modules.
- Avoid broad exception handling unless a user-facing fallback is intentionally required.
- Add comments only when they explain non-obvious behavior or external-service constraints.
- Preserve existing behavior unless the requested change explicitly modifies it.

## Naming Conventions
- Python modules, functions, and variables use `snake_case`.
- Constants use `UPPER_SNAKE_CASE`.
- JavaScript variables and functions use `camelCase`.
- CSS classes use readable kebab-case.

## API Conventions
- Use JSON request and response bodies for application endpoints.
- Validate and normalize user input at route boundaries.
- Return stable response shapes for frontend consumers.
- Keep health checks simple; `/health` returns application availability.

## Database Conventions
- SQLite is used for local persistence.
- Database files live in Flask's `instance` directory.
- Schema creation is idempotent and handled by `smarttrip.storage.init_db`.
- Use parameterized SQL only.
- Do not commit generated SQLite, WAL, or SHM files.

## Security Requirements
- Never commit secrets, API keys, `.env` files, or generated databases.
- Validate numeric bounds for user-controlled inputs such as radius and coordinates.
- Use parameterized SQL for all database writes and reads.
- Treat external API responses as untrusted input and normalize before use.
- Keep debug mode for local development only.

## Testing Strategy
- At minimum, verify the Flask app imports and `/health` returns `200`.
- Add unit tests for ranking, parsing, storage, and input normalization before larger feature changes.
- Mock OpenStreetMap calls in automated tests to avoid flaky network dependencies.
- Manually verify the main UI after frontend changes.

## Deployment Notes
- Local development command: `python app.py`.
- Windows quick-start command: `.\run.ps1`; it creates `.venv`, installs dependencies, and starts Flask on `127.0.0.1:5000`.
- Install dependencies with `python -m pip install -r requirements.txt`.
- For production, run through a real WSGI server and disable Flask debug mode.
- Ensure outbound access to OpenStreetMap services if live recommendations are required.

## Future Improvements
- Add automated tests and CI.
- Add explicit configuration for host, port, debug mode, and external API timeouts.
- Add rate limiting and caching for OpenStreetMap requests.
- Add structured logging.
- Repair the remaining mojibake-encoded Persian literals in Python source files.
