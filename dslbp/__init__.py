# -*- coding: utf-8 -*-
"""
    DataScienceLeaderboardApp
    ~~~~~~~~

    A Leaderboard App for Data Science/Modeling competitions.

    :copyright: (c) 2016 by Josiah Olson (thenomemac@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import os
import time
from contest.helperfxns import loadAndScore
from datetime import datetime
from flask import (
    Flask,
    Markup,
    request,
    session,
    url_for,
    redirect,
    render_template,
    abort,
    g,
    flash,
    send_from_directory,
    _app_ctx_stack,
)
from markdown import markdown
import werkzeug

import os
from flask import Flask, Blueprint

from config import config_dict
from dslbp.extensions import register_extensions

# Setup
def create_app(config_key="common"):
    register_logger()
    app = Flask(__name__)
    print_start_to_logger(app)
    _config = config_dict[config_key]
    _config.init_config()
    app.config.from_object(_config)  # Enabling config initiation
    register_extension(app)
    register_blueprints(app)
    register_cli(app)
    return app


def register_logger():
    """
    > When you want to configure logging for your project, you should do it as soon as possible when the program starts.
    > If app.logger is accessed before logging is configured, it will add a default handler.
    > If possible, configure logging before creating the application object.
    see https://flask.palletsprojects.com/en/1.1.x/logging/
    :return: None
    """
    from logging.config import dictConfig
    from config import BaseConfig

    log_dir = getattr(BaseConfig, "LOG_DIR")
    log_file_path = os.path.join(log_dir, "logdata.log")
    # Creates logs folder if not existent
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "file": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "formatter": "file",
                    "filename": log_file_path,
                    "backupCount": 30,  # 1month
                    "when": "D",
                }
            },
            "root": {"level": "INFO", "handlers": ["file"]},
        }
    )
    return None


def register_extension(app):
    """Register extensions"""
    register_extensions(app)
    app.logger.info("register_extension done")
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    # Registering the view and the api blueprints here
    with app.app_context():
        from dslbp.view import bp_main as main_blueprint

        app.register_blueprint(main_blueprint)
    app.logger.info("register_blueprints done")
    return None


def register_cli(app):
    from dslbp.clis import bp_cli as cli_blueprint

    app.register_blueprint(cli_blueprint)
    app.logger.info("register_cli_command done")
    return None


def print_start_to_logger(app):
    app.logger.info("########## App start ##########")


# create app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar("LEADERBOARDAPP_SETTINGS", silent=True)




@app.before_request
def before_request():
    g.usedPages = usedPages
    g.globalTitle = globalTitle
    g.user = None
    if "user_id" in session:
        g.user = query_db(
            "select * from user where user_id = ?", [session["user_id"]], one=True
        )


@app.route("/")
def defaultlanding():
    """Shows a users leaderboard for modeling contest.
    If not logged in then forward user to contest description.
    """
    # send user to description page if not logged in
    if not g.user:
        return redirect(url_for("description"))
    # display leaderboard for competition if logged in
    return redirect(url_for("leaderboard"))





@app.route("/description")
def description():
    """Displays a markdown doc describing the predictive modeling contest.
    Note ./content/contest/<url calling path>.md must be modified for contest.
    """
    # rule = request.url_rule
    # print(rule)
    file = open("./contest/content/description.md", "r")
    rawText = file.read()
    file.close()
    content = Markup(
        markdown(
            rawText,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
            ],
        )
    )
    return render_template(
        "markdowntemplate.html", title="Description", content=content
    )


@app.route("/evaluation")
def evaluation():
    """Displays a markdown doc describing the predictive modeling contest.
    Note ./content/contest/<url calling path>.md must be modified for contest.
    """
    file = open("./contest/content/evaluation.md", "r")
    rawText = file.read()
    file.close()
    content = Markup(
        markdown(
            rawText,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
            ],
        )
    )
    return render_template("markdowntemplate.html", title="Evaluation", content=content)


@app.route("/rules")
def rules():
    """Displays a markdown doc describing the predictive modeling contest.
    Note ./content/contest/<url calling path>.md must be modified for contest.
    """
    file = open("./contest/content/rules.md", "r")
    rawText = file.read()
    file.close()
    content = Markup(
        markdown(
            rawText,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
            ],
        )
    )
    return render_template("markdowntemplate.html", title="Rules", content=content)


@app.route("/contest/download/<path:path>")
def send_dir(path):
    # this function is used to serve the train/test files linked to in data.md
    return send_from_directory("contest/download", path)


@app.route("/data")
def data():
    """Displays a markdown doc describing the predictive modeling contest.
    Note ./content/contest/<url calling path>.md must be modified for contest.
    """
    file = open("./contest/content/data.md", "r")
    rawText = file.read()
    file.close()
    content = Markup(
        markdown(
            rawText,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
            ],
        )
    )
    return render_template("markdowntemplate.html", title="Data", content=content)


# in dev version of the app the prizes page isn't used due to overlap with description/rules
@app.route("/prizes")
def prizes():
    """Displays a markdown doc describing the predictive modeling contest.
    Note ./content/contest/<url calling path>.md must be modified for contest.
    """
    file = open("./contest/content/prizes.md", "r")
    rawText = file.read()
    file.close()
    content = Markup(
        markdown(
            rawText,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
            ],
        )
    )
    return render_template("markdowntemplate.html", title="Prizes", content=content)


@app.route("/discussion")
def discussion():
    return redirect(externalDiscussionLink)


@app.route("/selectmodel", methods=["POST"])
def select_model():
    """Allow user to select the upload they'd like to use for submission
    Default selection should be most recent submissions
    """
    try:
        # check if contest has ended
        if contestEndBool():
            flash("Error: contest has ended")
            raise Exception("contest has ended")
        input = request.form
        print(str(input))
        for count, x in enumerate(input):
            print(count, x)
        if len(input) != subNbr:
            flash("Error: Wrong number of submissions selected")
        else:
            db = get_db()
            db.execute(
                "delete from selection where user_id = '%s'" % session["user_id"]
            )
            db.commit()
            # upload user defined selections to database
            for count, submission_id in enumerate(input):
                db = get_db()
                db.execute(
                    """insert into selection (user_id, select_nbr, submission_id,     
                           select_date) values (?, ?, ?, ?)""",
                    (
                        session["user_id"],
                        count + 1,
                        int(submission_id),
                        int(time.time()),
                    ),
                )
                db.commit()

            flash("Selection successful!")
    except:
        flash("Error: Your selection was not recorded")
    return redirect("/uploadsubmission")


@app.route("/uploadsubmission", methods=["GET", "POST"])
def upload_file():
    """Allow users to upload submissions to modeling contest
    Users must be logged in."""

    # query the db and render the table used to display the leaderboard to users
    userBoard = query_db(
        """
        select submission_id, submit_date, public_score
        from submission sub
        where user_id = '%s'
        order by public_score %s"""
        % (session["user_id"], orderBy)
    )

    userBoard = [dict(row) for row in userBoard]
    for row in userBoard:
        row["score"] = row["public_score"]
        row["str_time"] = str(datetime.fromtimestamp(row["submit_date"]))

    colNames = ["Submission Time", "Public Score"]

    if request.method == "POST":
        try:
            # check if contest has ended
            if contestEndBool():
                flash("Error: contest has ended")
                raise Exception("contest has ended")

            print("here")
            # ensure user hasn't exceeded daily submission limit
            dailyCnt = query_db(
                """select count(*) sub_cnt
                from submission sub
                where submit_date > %s
                and user_id = %s
                group by user_id"""
                % (time.time() - 60 * 60 * 24, session["user_id"])
            )

            if len(dailyCnt) == 0:
                dailyCnt = 0
            else:
                dailyCnt = int(dict(dailyCnt[0])["sub_cnt"])

            if dailyCnt > dailyLimit:
                flash("Error: exceeded daily upload limit")
                raise Exception("Upload limit exceeded")

            file = request.files["file"]
            # throw error if extension is not allowed
            if not allowed_file(file.filename):
                raise Exception("Invalid file extension")

            if file and allowed_file(file.filename):
                filename = werkzeug.secure_filename(file.filename)
                # append userid and date to file to avoid duplicates
                filename = (
                    str(session["user_id"])
                    + "_"
                    + str(int(time.time()))
                    + "_"
                    + filename
                )
                fullPath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(fullPath)
                model_score = loadAndScore(fullPath)

                # cache the filename and submission to database
                db = get_db()
                db.execute(
                    """insert into submission (user_id, filename, submit_date,     
                           public_score, private_score, total_score) 
                           values (?, ?, ?, ?, ?, ?)""",
                    (session["user_id"], filename, int(time.time()), *model_score),
                )
                db.commit()

                # inform user upload was a success
                flash("Your submission was recorded.")
                return redirect(url_for("leaderboard"))
        except:
            # if exception is thrown in process then flash user
            flash(
                "File did not upload or score! Make sure the submission format is correct."
            )
    return render_template(
        "uploadsubmission.html",
        title="Upload Submission",
        userBoard=userBoard,
        subNbr=subNbr,
    )


@app.route("/public")
def public_timeline():
    """Displays the latest messages of all users."""
    return render_template(
        "timeline.html",
        messages=query_db(
            """
        select message.*, user.* from message, user
        where message.author_id = user.user_id
        order by message.pub_date desc limit ?""",
            [PER_PAGE],
        ),
    )




@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# launch application for dev purposes when leaderBoardApp.py script is run
if __name__ == "__main__":
    # only re-run init_db() on initial launch if you want to truncate you're sql tables
    if not os.path.isfile("dsLeaderboard.db"):
        init_db()
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    app.run()
