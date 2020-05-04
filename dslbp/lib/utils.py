import datetime
from flask import current_app


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d @ %H:%M")


def allowed_file(filename):
    # checks if extension in filename is allowed
    return "." in filename and filename.rsplit(".", 1)[1] in current_app.config["ALLOWED_EXTENSIONS"]
#
#
# def contestEndBool():
#     # return boolean if contest is over to change 'post' methods behavior
#     return (contestDeadline - time.time()) < 0 or showPrivate