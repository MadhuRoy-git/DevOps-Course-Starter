#!/bin/sh

poetry run gunicorn "app:app" --bind 0.0.0.0:$PORT