# NetWatch — Network Device Manager

A Flask app for tracking network devices. Uses SQLite (no database server required).

## Setup

```bash
pip install -r requirements.txt
python app.py
```

The SQLite database (`devices.db`) is created automatically on first run.

## Migrating from MySQL

If you have existing data to recover, you can export it from MySQL and import into SQLite,
or simply re-add devices through the UI — the schema is identical.

## Structure

```
app.py          # Routes and app config
models.py       # Device SQLAlchemy model
forms.py        # WTForms definitions
templates/      # Jinja2 HTML templates
static/css/     # Stylesheet
```
