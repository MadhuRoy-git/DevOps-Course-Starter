#!/bin/sh

poetry run gunicorn "app:create_app()" --bind 0.0.0.0:$PORT