"""This file is the view module which contains the lazysensor, where all the good
stuff happens. You will always want to point your applications like Gunicorn
to this file, which will pick up the lazysensor to run their servers.
"""

import os
import sys

from dslbp import create_app

FLASK_ENV = os.environ["FLASK_ENV"]
if FLASK_ENV is None:
    FLASK_ENV = "debug"

# Generate Flask App
try:
    app = create_app(FLASK_ENV)
except Exception as e:
    print(e)
    print("create_app failed.")
    sys.exit(1)


if __name__ == "__main__":
    # Import HTTP server module and run API
    from waitress import serve

    host = app.config["HOST"]
    port = app.config["PORT"]
    print(f"start serve host:{host} / port:{port}")
    serve(app, host=host, port=port, threads=4)
