#!/bin/bash
poetry run celery -A src.celery_app worker --loglevel=info
