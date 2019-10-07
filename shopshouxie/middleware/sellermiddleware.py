from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
"""写完本页面需要到项目的setting.py文件下面的MIDDLEWARE里面去注册"""
"""要想测试中间件需要把view里面的装饰器注释掉，完事就可以调试了，会直接跳转到登录界面，
原因是地址栏是空路径，在本页面中，不在白名单里面，也没有username，所以执行最后一句话即30行，
返回到seller/logi n界面,登录后退出，在地址栏中输入seller/index和seller/logout都会跳转到seller/login
界面，实现了功能，即退出登录后不能在地址栏中直接输入地址进入有信息的网站。结束了
如果访问前端即buyer，就都放行，因为前端不需要用中间件来控制，即增加了21.21两行。结束了
如果什么都不写，应该访问首页，在white_list里面加一个/  就可以了
"""
white_list = ['/seller/login/','/seller/register/','/']

class AuthMD(MiddlewareMixin):

    def process_request(self,request):
        # 1. 获取url路径部分
        path_info = request.path_info
        print(path_info)
        # 2. 进行判断，如果路径在白名单中放行
        if path_info in white_list:
            print('放行')
            return
        if path_info.find('/buyer/') !=-1:
            return#!=-1说明找到的，会放行，在没写buyer路由之前会报错，写了之后就不会了
        # 3. 判断是否登录了，如果登陆了，就放行
        username=request.session.get('username')
        if username:#如果用户名有就不操作，放行
            return
        # 4. 如果不在白名单和没有登录，就重定向到登录页面
        return redirect('/seller/login/')