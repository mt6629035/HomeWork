from seller import views
from django.urls import path

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('index/', views.index),
    path('logout/', views.logout),
    path('type_add/', views.type_add),
    path('type_add_ajax/', views.type_add_ajax),
    path('type_list/', views.type_list),
    path('type_delete/', views.type_delete),
    # path('type_change/', views.type_change),
    path('goods_add/', views.goods_add),
    path('goods_list/', views.goods_list),
    path('goods_delete/', views.goods_delete),
    # path('type_add/', views.type_add),#没有基础base，先写模型类
]