import os


class BaseConfig:
    # Root Dir of this app
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # server configuration
    HOST = "localhost"
    PORT = 5000
    SECRET_KEY = "superSecretKeyGoesHere"
    # Directory path for logger
    LOG_DIR = os.path.join(ROOT_DIR, "log")
    # contest specific variables
    globalTitle = "Modeling Contest"
    usedPages = ["description", "evaluation", "rules", "data", "discussion"]
    # discussion navbar link will link to this forum-wiki-like resource
    externalDiscussionLink = "https://www.reddit.com/r/MachineLearning/"
    # consider changing this, uploads can take a lot of drive space
    UPLOAD_FOLDER = "contest/submissions/"
    ALLOWED_EXTENSIONS = ["csv", "txt", "zip", "gz"]
    # order the score function by asc or desc
    orderBy = "asc"
    # set the max number of submissions a user is able to submit for final contest
    # scoring against the private leaderboard, ie best of # selected submissions are considered
    subNbr = 1
    # max number of submissions a user is allowed to make in a rolling 24hr period
    dailyLimit = 2
    # set the contest deadline where users can no longer upload and private score is published
    # contestDeadline = time.mktime(datetime(2016, 10, 21, 0, 0).timetuple())
    # debug variable that if True allows private leaderboard to be displayed before contest deadline
    # normally should be False
    showPrivate = False

    # Database
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "dslbp"

    @classmethod
    def init_config(cls):
        # SQLAlchemy
        cls.SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            cls.DB_USER, cls.DB_PASSWORD, cls.DB_HOST, cls.DB_PORT, cls.DB_NAME
        )
        cls.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_recycle": 120,
            "pool_timeout": 900,
            "pool_size": 30,
            "max_overflow": 30,
        }
        cls.SQLALCHEMY_TRACK_MODIFICATIONS = False
        cls.SQLALCHEMY_RECORD_QUERIES = True


class DebugConfig(BaseConfig):
    DEBUG = True


class DeployConfig(BaseConfig):
    DEBUG = False


# Create a config dictionary which is used while initiating the application.
config_dict = {
    "common": BaseConfig,
    "debug": DebugConfig,
    "deploy": DeployConfig,
}
