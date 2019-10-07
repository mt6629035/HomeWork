#3.控制文件,作用是让项目启动
from models import models
from views import app
from flask_script import Manager#flask-script插件引入的模块

manage = Manager(app)


@manage.command
def hello():#安装不是视图函数，是安装hello命令，当在terminal中输入
    #python manage.py hello时候会调用hello函数
    print('hello') #python3有括号，python2没有括号


#加一条同步表格Leave的脚本命令
@manage.command
def migrate():
    models.create_all()#启动项目的命令

# #不能从main里面导，要不不执行models.py
# #那么这里面的表就没有
    # command = sys.argv[1]#argv是相对路径,命令行用来调用脚本时的参数，本身是一个列表
    # if command == 'migrate':#判断传的第一个参数是migrate还是runserver
#     models.create_all() 
# elif command == 'runserver':
#     app.run(host='127.0.0.1',port=8000,debug=True)

if __name__ == '__main__':  #这句话的意思是在当前文件下进行
    manage.run()#启动脚本模式
    # os.system('python manage.py runserver')#执行系统命令用的


