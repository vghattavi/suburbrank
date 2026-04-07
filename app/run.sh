#!/usr/bin/env bash
set -euo pipefail
uvicorn suburbrank.app.main:app --reload --host 0.0.0.0 --port 8000
