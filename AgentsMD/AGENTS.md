# AGENTS.md

## Project Overview

This is a Django 6.0 web application with three main apps:
- **accounts** - User authentication (login, signup, logout)
- **mathematics** - Mathematical calculations with database storage
- **documents** - PDF export of stored calculations

## Environment

- **Python**: >= 3.12
- **Package Manager**: uv (all Python commands must use `uv run`)
- **Framework**: Django 6.0.1
- **Database**: SQLite3

## Important: Always Use `uv run`

This project uses `uv` for dependency management. **Never use bare `python` or `pip` commands.** Always prefix Python commands with `uv run`:

```bash
# Correct
uv run python manage.py runserver
uv run python manage.py migrate

# Incorrect
python manage.py runserver
```

## Project Structure

sample_project
├── accounts
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── documents
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── manage.py
└── mathematics
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    ├── models.py
    ├── templates
    ├── tests.py
    ├── urls.py
    ├── utils.py
    └── views.py

## Code Conventions

- Follow PEP 8, unless specified differently in this file.
- ALWAYS provide type hints for every function that is not a view (especially in utils.py files)
- Each app should have its own `base.html` template
- Avoid using helper functions and complex structures when something can easily be solved with a single function

## Code Style

Use camelCase and make sure there is an empty new line between every single line of code, always.

Bad Example:

```py
def my_function(some_parameter):
    if some_parameter == 'value':
        print(some_parameter)
        return some_parameter
```

Corrected Example:

```py
def myFunction(someParameter: str) -> str:
    
    if someParameter == 'value':

        print(someParameter)

        return someParameter
```


## Boundaries

- Never ever delete files with rm or similar commands
- Never use any git commands at all