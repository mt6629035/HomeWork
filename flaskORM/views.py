#1.只负责写视图
import os
import datetime
from flask import render_template
from main import app
from models import Curriculum#导入这个表
from flask import redirect#跳转 即Django中的重定向功能
import functools
from flask import session
from models import *

class Calendar:
    """
    当前类实现日历功能
    1、返回列表嵌套列表的日历
    2、安装日历格式打印日历

    # 如果一号周周一那么第一行1-7号   0
        # 如果一号周周二那么第一行empty*1+1-6号  1
        # 如果一号周周三那么第一行empty*2+1-5号  2
        # 如果一号周周四那么第一行empty*3+1-4号  3
        # 如果一号周周五那么第一行empyt*4+1-3号  4
        # 如果一号周周六那么第一行empty*5+1-2号  5
        # 如果一号周日那么第一行empty*6+1号   6
        # 输入 1月
        # 得到1月1号是周几
        # [] 填充7个元素 索引0对应周一
        # 返回列表
        # day_range 1-30
    """
    def __init__(self,month = "now"):
        self.result = []

        big_month = [1, 3, 5, 7, 8, 10, 12]
        small_month = [4, 6, 9, 11]

        #获取当前月
        now = datetime.datetime.now()
        if month == "now":
            month = now.month
            first_date = datetime.datetime(now.year, now.month, 1, 0, 0)
            # 年 月 日 时 分
        else:
            #assert int(month) in range(1,13)
            first_date = datetime.datetime(now.year,month, 1, 0, 0)

        if month in big_month:
            day_range = range(1, 32)  # 指定月份的总天数
        elif month in small_month:
            day_range = range(1, 31)
        else:
            day_range = range(1, 29)

        # 获取指定月天数
        self.day_range = list(day_range)
        first_week = first_date.weekday()  # 获取指定月1号是周几 6

        line1 = []  # 第一行数据
        for e in range(first_week):
            line1.append("empty")
        for d in range(7 - first_week):
            line1.append(
                str(self.day_range.pop(0))+"—django开发"
                         )
        self.result.append(line1)
        while self.day_range:  # 如果总天数列表有值，就接着循环
            line = []  # 每个子列表
            for i in range(7):
                if len(line) < 7 and self.day_range:
                    line.append(str(self.day_range.pop(0))+"—django开发")
                else:
                    line.append("empty")
            self.result.append(line)
    def return_month(self):
        """
        返回列表嵌套列表的日历
        """
        return self.result
    def print_month(self):
        """
        安装日历格式打印日历
        """
        print("星期一  星期二  星期三  星期四  星期五  星期六  星期日")
        for line in self.result:
            for day in line:
                day = day.center(6)
                print(day, end="  ")
            print()

def loginValid(fun):#这是一个装饰器
    @functools.wraps(fun)#保留原函数的名称
    def inner(*args,**kwargs):
        username = request.cookies.get('username')#Django中是大写的COOKIE
        id = request.cookies.get('id','0')#是0  下一句就不成立了
        user=User.query.get(int(id))#从数据库中获取id为此值的数据
        session_username = session.get('username')#获取session--------字典可以用这种方法,
        if user:#检测是否有对应id的用户
            if user.user_name == username and username == session_username:#检测用户是否对应
                return fun(*args,**kwargs)
            else:
                return redirect('/login/')
        else:
            return redirect('/login')
    return inner


@app.route("/")#再进行路由
@loginValid#先执行这个
def index():
    name = "laojiu"
    return render_template("index.html",**locals())


@app.route("/login/",methods=['GET','POST'])
def login():
    error = ''#放在这GET请求和POST请求都有error信息了就
    if request.method == 'POST':
        form_data = request.form
        email = form_data.get('email')
        password = form_data.get('password')

        #下面是表单校验
        user = User.query.filter_by(email=email).first()
        if user:
            db_password = user.password
            if password == db_password:
                response = redirect('/index/')
                response.set_cookie('username',user.user_name)
                response.set_cookie('email',user.email)
                response.set_cookie('id',str(user.id))
                session['username'] = user.user_name#设置session--------
                return response#接下来是获取cookie校验
            else:
                error =  '密码错误'
        else:
            error = '用户名不存在'
    return render_template("login.html",error = error)

@app.route('/logout/',methods=['GET','POST'])
def logout():
    response = redirect('/login/')
    response.delete_cookie('username')
    response.delete_cookie('email')
    response.delete_cookie('id')
    session.pop('username')#删除session第1种方法----------
    # del session['username']#第二种方法
    return response


@app.route("/base/")
def base():
    return render_template("base.html")

@app.route("/index/")
def exindex():
    # c = Curriculum()
    # c.c_id = '0001'
    # c.c_name = 'c++基础'
    # c.c_time = datetime.datetime.now()
    # c.save()
    curr_list=Curriculum.query.all()
    return render_template("ex_index.html",curr_list=curr_list)

@app.route("/userinfo/")
def userinfo():
    calendar = Calendar().return_month()
    now = datetime.datetime.now()
    return render_template("userinfo.html",**locals())

from flask import request
from models import User
@app.route('/register/',methods=['GET','POST'])
def register():
    '''
        form表单提交的数据由request.form接收
        request是从models.py中导包导入进来的
    :return:
    '''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user = User()
        user.user_name = username
        user.password = password
        user.email = email
        user.save()
    return render_template('register.html')

@app.route('/holiday_leave/',methods='GET','POST')
def holiday_leave():
    if request.method == 'POST':
        data = request.form
        request_user = data.get('request_user')
        request_type = data.get('request_type')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        phone = data.get('phone')
        request_description = data.get('request_description')

        leave = Leave()
        leave.request_id = request.get_data()  # 请假人id
        request_name = models.Column(models.String(32))  # 姓名
        request_type = models.Column(models.String(32))  # 请假类型
        request_start_time = models.Column(models.String(32))  # 起始时间
        request_end_time = models.Column(models.String(32))  # 结束时间
        request_description = models.Column(models.Text)  # 请假原因
        request_phone = models.Column(models.String(32))  # 联系方式
        request_status = models.Column(models.String(32))  # 假条状态
    return render_template('holiday_leave.html')
# #9-27新增
# @app.route('/picture/',methods='GET','POST')
# def picture():
#     p = {'picture':'img/1.jpg'}
#     if request.method == 'POST':
#         file = request.files.get('photo')
#         file_name = file.filename
#         file_path = 'img/%s'%file_name
#         file_path = os.path.join(STATICFILES_DIR,'img/%s%filename')
#         file.save(file_path)
#         p = Picture()
#         p.picture = file_path
#         p.save()
#
#     return render_template('picture.html',p = p)

# from main import api
# from flask_restful import Resource
#
# @api.resource('/Api/v1/leave/')
# class leaveApi(Resource):
#     def get(self):#查
#         return {'method':'这是get请求，负责返回所有的数据'}
#     def post(self):#增
#         data = request.form
#         request_id = data.get('request_id')
#         request_name = data.get('request_name')
#         request_type = data.get('request_type')
#         request_start_time = data.get('request_start_time')
#         request_end_time = data.get('request_end_time')
#         request_description = data.get('request_description')
#         request_phone = data.get('request_phone')
#         request_status = data.get('request_status')
#
#         leave = Leave()
#         leave.request_id = request_id
#         leave.request_name = request_name
#         leave.request_type = request_type
#         leave.request_start_time = request_start_time
#         leave.request_end_time = request_end_time
#         leave.request_description = request_description
#         leave.request_phone = request_phone
#         leave.request_status = request_status
#         return {'method':'负责保存数据'}
#     def put(self):#改
#         return {'method':'负责修改数据'}
#     def delete(self):#删
#         return {'method':'负责删除数据'}
