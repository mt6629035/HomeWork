import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATICFILES_DIR = os.path.join(BASE_DIR,"static")
# SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(BASE_DIR,"ORM.sqlite")#数据库地址
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# SQLALCHEMY_RTACK_MODIFICATIONS = True
# DEBUG = True

class Config:#分了2份配置
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(BASE_DIR,"ORM.sqlite")#数据库地址
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RTACK_MODIFICATIONS = True

class RunConfig(Config):#第2份配置
    DEBUG = False