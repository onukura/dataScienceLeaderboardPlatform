from dslbp.extensions import db

def query_db(query):
    """Queries the database and returns a list of dictionaries."""
    cur = db.session.execute(query)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db("select user_id from user where username = ?", [username], one=True)
    return rv[0] if rv else None