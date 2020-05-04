import datetime
from flask import render_template, Blueprint

from dslbp.extensions import db

lb = Blueprint("leaderboard", __name__)


@lb.route("/leaderboard")
def leaderboard():
    # query the db and render the table used to display the leaderboard to users
    if contestEndBool():
        # when evaluating for private score we take user selection table
        # or most recent submission if user didn't specify what submission was final
        board = db.session.execute(
            """
            select username, max(public_score) public_score, 
                max(private_score) private_score, max(sub_cnt) sub_cnt
            from (
                select username, public_score, private_score, sub_cnt
                from submission sub
                left join (
                  select user_id, max(submit_date) max_submit_date
                  from submission 
                  where user_id not in (select distinct user_id from selection)
                  group by user_id
                ) max_sub
                on sub.user_id = max_sub.user_id
                inner join (
                  select user_id, count(*) sub_cnt 
                  from submission 
                  group by user_id
                ) cnt
                on sub.user_id = cnt.user_id
                inner join user
                on sub.user_id = user.user_id
                left join selection 
                on sub.submission_id = selection.submission_id
                where
                  case when select_date is not null then 1 else 
                    case when max_submit_date is not null then 1 else 0 end
                  end = 1
            ) temp
            group by username
            order by private_score %s"""
            % orderBy
        )
    else:
        # display the public leader board when contest hasn't ended yet
        board = db.session.execute(
            """
            select username, public_score, '?' private_score, sub_cnt
            from submission sub
            inner join (
              select user_id, max(submit_date) max_submit_date, count(*) sub_cnt 
              from submission 
              group by user_id
            ) max_sub
            on sub.user_id = max_sub.user_id and
              sub.submit_date = max_sub.max_submit_date 
            inner join user
            on sub.user_id = user.user_id
            order by public_score %s"""
            % orderBy
        )

    # Debug: board = [{'public_score': 0.3276235370053617, 'username': 'test3', 'private_score': 0.32036252335937015}, {'public_score': 0.3276235370053617, 'username': 'test1', 'private_score': 0.32036252335937015}, {'public_score': 0.33944709256230005, 'username': 'test2', 'private_score': 0.32003513414185064}]
    board = [dict(row) for row in board]
    for rank, row in enumerate(board):
        row["rank"] = rank + 1

    colNames = [
        "Rank",
        "Participant",
        "Public Score",
        "Private Score",
        "Submission Count",
    ]
    deadlineStr = str(datetime.fromtimestamp(contestDeadline))
    hoursLeft = abs(round((contestDeadline - time.time()) / 3600, 2))

    return render_template(
        "leaderboard.html",
        title="Leaderboard",
        colNames=colNames,
        leaderboard=board,
        deadlineStr=deadlineStr,
        hoursLeft=hoursLeft,
    )