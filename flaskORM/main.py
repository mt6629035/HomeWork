#4.声明文件,是项目的开始脚本文件
import os
#分离出来后from中有报红是环境的问题
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from flask_restful import Api
#老版的pymysql是mysqldb，新版的mysqldb是pymysql
app = Flask(__name__)#实例化app
#第二种方法:
app.config.from_pyfile("settings.py")
# app.config.from_envvar()#来源于环境变量，环境变量的值是python文件名称
# app.config.from_json()#来源于json文件，必须符合json格式
# app.config.from_mapping()#python原生字典格式
app.config.from_object('settings.Config')#来源于类对象,用的比较多#使用配置


#配置参数,第一种方法：直接写配置文件
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# #想换数据库直接换下面一句就可以了



# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(BASE_DIR,"ORM.sqlite")#数据库地址
# # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/demo3"
# app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True#请求结束后自动提交
# app.config["SQLALCHEMY_RTACK_MODIFICATIONS"] = True#flask1版本之后，添加的选项，可以跟踪修改

app.secret_key = '123456'#加盐
models = SQLAlchemy(app)#orm关联应用
#------以上步骤创建了数据库和app'



