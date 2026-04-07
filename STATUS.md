# SuburbRank Status

## Current state
SuburbRank has been switched from the blocked .NET path to a Python/FastAPI MVP path.

## Implemented in workspace
### Product/spec layer
- product README
- MVP spec
- page map
- build backlog
- open questions

### Python app layer
- FastAPI app entrypoint
- public templates
- dashboard template
- suburb list/detail templates
- reports list/detail templates
- styling system
- SQLite database config
- SQLAlchemy models
- fake data seeding
- deterministic scoring engine
- launch docs and architecture docs

## Environment blockers in current runtime
- dotnet is unavailable
- python venv creation is blocked because python3.13-venv is missing
- pip package install is blocked by externally-managed environment restrictions
- required FastAPI packages are not preinstalled

## Practical result
The codebase structure and core app source are now prepared, but this runtime cannot execute the Python web stack without a proper Python environment.

## Closest meaningful completion state achieved here
A runnable FastAPI MVP source tree prepared for execution in the first normal Python environment with venv + pip access.
