import pandas as pd

# note that if an error is thrown in this fxn
# then the user will get a flash() that upload failed
def loadAndScore(submission_path, ans_path, metric=None):
    """function loads the dataset from filePath and scores submission
    against the solution file
    function returns tuple in format public, private, total loss function score"""
    # in a real implementation of this app add more QA in this fxn
    assert metric is not None
    sub = pd.read_csv(submission_path)
    ans = pd.read_csv(ans_path)
    public_score = score(
        sub.Survived[ans.PublicLeaderboardInd == 1],
        ans.Survived[ans.PublicLeaderboardInd == 1],
    )
    private_score = score(
        sub.Survived[ans.PublicLeaderboardInd == 0],
        ans.Survived[ans.PublicLeaderboardInd == 0],
    )
    total_score = score(sub.Survived, ans.Survived)
    return (public_score, private_score, total_score)
