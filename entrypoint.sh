#!/bin/sh
# If the command to be executed is Gunicorn, perform the monkey-patch
if [ "$1" = "gunicorn" ]; then
  python -c "import pkgutil; pkgutil.ImpImporter = pkgutil.zipimporter"
fi
exec "$@"