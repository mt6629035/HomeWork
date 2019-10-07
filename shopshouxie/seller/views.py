from django.shortcuts import render,redirect,HttpResponse
from seller import models
import os


"""用来加密的函数，要调用它"""
import hashlib
def pwd_jm(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result
"""3中校验方式，1.表单校验 2.装饰器校验 3.中间件校验"""

"""form表单校验register，归根到底算是前端，即前台"""
from django import forms
from django.forms import widgets#加提示语需要引入的模块
import time#时间戳需要引用的模块
class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        required=True,
        min_length=3,
        widget=widgets.TextInput(attrs={'placeholder':'用户名','class':'layui-input'})
    )#attrs里面的是input输入框里的属性，即placeholder属性和class属性
    nickname = forms.CharField(
        label='昵称',
        required=True,#require的意思是不能为空，是一个校验条件，自动补出来了
        min_length=3,#自己提示出来了，就不用再也错误信息了，前端给写好了
        widget=widgets.TextInput(attrs={'placeholder':'昵称','calss':'layui-input'})
    )
    password = forms.CharField(
        label='密码',
        required=True,
        min_length=6,
        widget=widgets.PasswordInput(attrs={'placeholder':'密码','class':'layui-input'})
    )
    picture = forms.CharField(
        label='头像',
        required=True,
        widget=widgets.FileInput(attrs={'class':'layui-input'})
    )
"""第一步注册，为对应的后台"""
def register(request):
    registerForm = RegisterForm()#弄一个form表单校验的对象
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST,request.FILES)#POST是校验普通字段，FILES是校验上传字段
        if registerForm.is_valid():
            #1.获取数据，cleaned_data 就是读取表单返回的值，返回类型为字典dict型
            data = registerForm.cleaned_data
            username = data.get('username')
            nickname = data.get('nickname')
            password = data.get('password')
            #picture=data.get('picture')如果这样获取的是图片名称
            picture = request.FILES.get('picture')#获取的是图片对象
            time_temp = time.time()#获取当前时间戳

            #2.保存图片
            path = 'static/touxiang/' + str(time_temp) + '_' + picture.name
            with open(path,mode='wb') as f:
                for content in picture.chunks():
                    f.write(content)

            #3.对密码加密
            password = pwd_jm(password)
            #4.保存到数据库
            models.Seller.objects.create(
                name = username,
                nickname = nickname,
                password = password,
                picture = 'touxiang/'+str(time_temp) + '_' +picture.name
            )

            #4.重定向到登录页面
            return redirect('/seller/login/')
    return render(request,'seller/register.html',{'registerForm':registerForm})





"""第二步form表单校验register，即前端前台"""
class LoginForm(forms.Form):
    #登录就两个输入框，所以校验有两个就行了
    username = forms.CharField(
        label='用户名',
        required=True,
        min_length=3,
        widget=widgets.TextInput(attrs={'placeholder': '用户名', 'class': 'layui-input'})
    )
    password = forms.CharField(
        label='密码',
        required=True,
        min_length=6,
        widget=widgets.PasswordInput(attrs={'placeholder': '密码', 'class': 'layui-input'})
    )






"""登录，即后端后台"""
def login(request):
    loginForm = LoginForm()#创建一个form表单校验类的对象
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)#将POST请求的内容给表单校验类的对象，即输入的账号密码信息给对象
        if loginForm.is_valid():
            # 1. 获取表单提交过来的内容，cleaned_data 就是读取表单返回的值，返回类型为字典dict型
            data = loginForm.cleaned_data
            username = data.get('username')
            password = data.get('password')
            # 2. 先加密，调用之前定义的加密函数
            password = pwd_jm(password)
            # 3. 验证，成功跳转到首页，不成功还返回登录
            ret = models.Seller.objects.filter(name=username, password=password)
            print(ret)#用get还是用filter，用filter，因为用get查不到用户名会报错
            #报错，为了不让程序终止，要捕获异常
            if ret:#有东西是true,没有是false，它返回的是Query  Set[] ，空集合，
                # 转换为布尔值就是false，于是就执行最后一个return，回到首页
                # 登录成功后将用户名保存到session中，用于首页的显示和后期的操作
                request.session['username'] = username
                request.session['seller_id'] = ret[0].id
                # 如果成功，挑战到首页
                return redirect('/seller/index/')# 如果不成功，重新跳转到登录页面
    return render(request, 'seller/login.html', {'loginForm': loginForm})






"""第五步登录装饰器,要写在需要加装饰器的视图函数的前面"""
def login_decorator(func):
    def inner(request):
        username = request.session.get('username')
        if username:
            return func(request)
        else:
            return redirect('/seller/login/')
    return inner








"""第三步主页"""
import datetime
#过滤器不能直接过滤时间戳
#给主页加一个装饰器
# @login_decorator
def index(request):
    # 1.获取当前登录时间
    times = datetime.datetime.now()
    # 2. 获取头像
    seller_id = request.session.get('seller_id')
    seller_obj = models.Seller.objects.get(id=seller_id)
    # models.Seller.objects.get(name=request.session.get('username'))这种方法获取头像也行，要不就整个id出来，即116行
    # print(seller_obj.picture.name)
    # print(type(seller_obj.picture.name))#是一个字符串
    return render(request, 'seller/index.html', {'times': times, 'seller_obj': seller_obj})







"""第四步，登出，也需要加装饰器"""
# @login_decorator
def logout(request):
    # print('--------')用打印来判断装饰器是否失效，没失效登录logout页面不会打印出这句话
    # 1.清除session
    request.session.clear()#clear是删除内容的功能
    # 2. 重定向到登录界面
    return redirect('/seller/login/')
#登出之后直接在地址栏输入主页index的地址，应该不让访问，方法是在def index里面第一行家判断，即下面
# username = request.session.get('username')
# if not username:
#     return redirect('/seller/login/')
#但是这样写太麻烦，登入登出即每个视图函数都得在开始写这个判断语句，所以改用装饰器

"""第六步中间件实现功能，退出登陆后，不能在地址栏输入主页地址就访问进去"""




#第一版注释掉
#第一版type_add注释掉
# def type_add(request):
#     msg=''
#     if request.method == 'POST':
#         # 1. 获取表单提交过来的数据
#         type_name = request.POST.get('type_name')#获取的是type_add下输入框的name
#         if type_name:#有去数据库查询，没有就保存到数据库
#             ret=models.GoodsType.objects.filter(name=type_name)
#             if not ret:#若没有not,意思就是有，查出来了，即数据库中有你输入的这个名字
#                 """如果数据库中没有此商品类型，则保存到数据库"""
#                 # 2. 保存到数据库
#                 models.GoodsType.objects.create(name = type_name)
#                 # 3. 重定向到类型列表展示页面
#                 return redirect('/seller/type_list/')
#             else:
#                 msg='此商品类型已经存在'
# #如果是空就不判断，直接执行下一句话
#     return render(request,'seller/type_add.html')


#第一版的ajax，一块注释掉
# from django.http import JsonResponse
# def type_add_ajax(request):
#     dic={'status':'false'}#默认是false，表示没有
#     #获取ajax提交过来的内容
#     name = request.GET.get('name')
#     #在数据库中查询
#     ret = models.GoodsType.objects.filter(name=name)
#     if ret:#表示数据库中有这个类型
#         dic['status']='true'
#     return JsonResponse(dic)

#第二版，增加按钮,用ajax的post提交，即验证了，又保存了,
def type_add(request):
    return render(request,'seller/type_add.html')
def type_add1_ajax(request):
    dic = {'status': 'false'}
    if request.method == 'POST':
        # 1. 获取ajax 提交过来的内容
        type_name = request.POST.get('name')
        if type_name:
            # 2. 去数据库中查询
            ret = models.GoodsType.objects.filter(name=type_name)
            if ret:
                """数据库中存在"""
                dic['status'] = 'true'
            else:
                # 3. 返回
                """数据库中不存在"""
                models.GoodsType.objects.create(name=type_name)

    return JsonResponse(dic)

from django.http import JsonResponse
def type_add_ajax(request):#ajax类型添加和校验
    return JsonResponse({'name':'xxx'})



"""商品类型展示页面，即list页面"""
def type_list(request):
    # 1. 查询数据库
    goods_type_obj_list = models.GoodsType.objects.all().order_by('-id')
    return render(request,'seller/type_list.html',{'goods_type_obj_list':goods_type_obj_list})








"""删除类型页面"""
def type_delete(request):
    # 1. 获取id
    id = request.GET.get('id')
    # 2. 查询数据库并且删除
    models.GoodsType.objects.filter(id=id).delete()
    # 3. 重定向到列表页面
    return redirect('/seller/type_list/')





#post请求查完之后返回页面
"""编辑页面"""
# def type_change(request):
#     if request.method == 'GET':
#         # 1.获取id
#         type_id = request.GET.get('id')
#         # 2. 查询数据库
#         goods_type_obj=models.GoodsType.objects.get(id=type_id)
#         # 3. 返回页面
#         return render(request,'seller/type_change.html',{'goods_type_obj':goods_type_obj})
#     else:
#         """post请求"""
#         # 1. 获取表单提交过来的内容(id和商品类型名称)
#         id = request.POST.get('id')
#         type_name = request.POST.get('type_name')
#         #判断要改成的名字，是否已经存在了，做一个判断
#         #查询数据库，存在就提示，不存在就修改和保存
#         queryset_obj = models.GoodsType.objects.filter(name=type_name)
#         if not queryset_obj:#意思是要改成的名字可以用，数据库中没有这个名字
#             goods_type_obj = models.GoodsType.objects.get(id=id)
#             goods_type_obj.name = type_name
#             goods_type_obj.save()
#             #重定向到类型列表页面
#             return redirect('/seller/type_list/')
#         else:
#             #如果存在 ：提示
#             return render(request,'seller/type_change.html',{'error':'此类型已经存在'})
#         # 2. 查询数据库并且修改
#         goods_type_obj = models.GoodsType.objects.get(id=id)
#         # 3. 重定向到类型列表展示页面
#         return redirect('/seller/type_list/')



def goods_add(request):
    if request.method == 'GET':
        # 1. 查询数据库中的商品类型
        goods_type_obj_list=models.GoodsType.objects.all()
        return render(request,'seller/goods_add.html',{'goods_type_obj_list':goods_type_obj_list})
    else:
        #post请求
        #1.获取表单提交过来的数据
        goods_num = request.POST.get('goods_num')#编号
        goods_name = request.POST.get('goods_name')#名称
        goods_oprice = request.POST.get('goods_oprice')#原价
        goods_xprice = request.POST.get('goods_xprice')#现价
        goods_count = request.POST.get('goods_count')#库存
        goods_type_id = request.POST.get('goods_type')#商品类型id
        goods_content = request.POST.get('goods_content')#商品详情
        goods_description = request.POST.get('goods_description')#商品描述

        userfiles=request.FILES.getlist('userfiles')#获取多张图片
        #2.保存数据库
        goods_obj = models.Goods.objects.create(
            goods_num=goods_num,
            goods_name=goods_name,
            goods_oprice=goods_oprice,
            goods_cprice=goods_xprice,
            goods_kucun=goods_count,
            type_id=goods_type_id,
            goods_detail=goods_content,
            goods_desc=goods_description,
            seller_id=request.session.get('seller_id')
        )
        #3.保存图片
        import time,datetime
        for userfile in userfiles:
            #时间戳要写在for里面，循环一个生成一个时间戳
            time_temp = str(time.time())#时间戳
            path = 'static/goodsimage/'+time_temp+ '_' + userfile.name
            with open(path,mode='wb') as f:
                for con in userfile.chunks():
                    f.write(con)
            #接下来将图片路径保存到数据库
            models.GoodsImage.objects.create(
                image_address='goodimage/'+time_temp+'-'+userfile.name,
                goods=goods_obj
            )


        #4.重定向到商品列表
    return redirect('/seler/goods_list/')






"""商品列表界面"""
def goods_list(request):
     # 1. 获取当前用户的所有商品
     seller_id = request.session.get('seller_id')
     queryset_obj = models.Goods.objects.filter(seller_id = seller_id)#使用用户的id

     return render(request,'seller/goods_list.html',{'queryset_obj':queryset_obj})



"""删除"""
def goods_delete(request):
    # 1. 获取 商品id
    goods_id = request.GET.get('id')
    queryset_obj = models.GoodsImage.objects.filter(good_id=goods_id)
    for goods_image_obj in queryset_obj:
        path = goods_image_obj.image_address#图片路径
        path = 'static/'+path
        os.remove(path)
    models.Goods.objects.get(id=goods_id).delete()#删除商品了 对应的图片应该也一块删除
    #数据库里不用管删除图片，数据库路径自动删除，但是本地还有图片
    #应该先删图片，再删数据库的路径，应该先查找商品对应的图片路径删除本地图片，在查询数据库删除路径
    # 3. 重定向到商品列表界面
    return redirect('/seller/goods_list/')
