from flask import redirect, request, flash, url_for, render_template, Blueprint
from flask_login import login_manager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@auth.route("/login", methods=["GET", "POST"])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

    """Logs the user in."""
    if g.user:
        return redirect(url_for("leaderboard"))
    error = None
    if request.method == "POST":
        user = query_db(
            """select * from user where
            username = ?""",
            [request.form["username"]],
            one=True,
        )
        if user is None:
            error = "Invalid username"
        elif not check_password_hash(user["pw_hash"], request.form["password"]):
            error = "Invalid password"
        else:
            flash("You were logged in")
            session["user_id"] = user["user_id"]
            return redirect(url_for("leaderboard"))
    return render_template("login.html", error=error)


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for("timeline"))
    error = None
    if request.method == "POST":
        if not request.form["username"]:
            error = "You have to enter a username"
        elif not request.form["email"] or "@" not in request.form["email"]:
            error = "You have to enter a valid email address"
        elif not request.form["password"]:
            error = "You have to enter a password"
        elif request.form["password"] != request.form["password2"]:
            error = "The two passwords do not match"
        elif get_user_id(request.form["username"]) is not None:
            error = "The username is already taken"
        else:
            db = get_db()
            db.execute(
                """insert into user (
              username, email, pw_hash) values (?, ?, ?)""",
                [
                    request.form["username"],
                    request.form["email"],
                    generate_password_hash(request.form["password"]),
                ],
            )
            db.commit()
            flash("You were successfully registered and can login now")
            return redirect(url_for("login"))
    return render_template("register.html", error=error)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("leaderboard"))