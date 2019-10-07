from django.db import models



"""卖家"""
class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    nickname = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    picture = models.ImageField()#头像 要下载Pillow模块
    #ImageField  把字符串封装到一个对象里了，费事又费力
    def __str__(self):
        return '<obj name:{}>'.format(self.name)



"""商品种类"""
class GoodsType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return '<obj name:{}>'.format(self.name)



"""商品图片"""
class GoodsImage(models.Model):
    image_address = models.CharField(max_length=64)
    #搞一个关系
    goods = models.ForeignKey(to='Goods',on_delete=models.CASCADE)

    def __str__(self):
        return '<obj:image_address:{}>'.format(self.image_address)



"""商品"""
class Goods(models.Model):
    goods_num = models.CharField(max_length=32)#商品编号
    goods_name = models.CharField(max_length=32)#商品名字
    goods_oprice = models.CharField(max_length=32)#商品原价
    goods_cprice = models.CharField(max_length=32)#商品现价
    goods_kucun = models.CharField(max_length=32)#商品库存
    goods_desc = models.CharField(max_length=100)#商品描述
    #商品和图片是一对多的关系，所以先不写商品缩略图字段，单写一个图片类
    goods_detail = models.TextField()#商品详情
    #设置关系

    #类型和商品也是一对多，在商品类加一个外键
    type = models.ForeignKey(to='GoodsType',on_delete=models.CASCADE)
    # 商家和商品一对多，在商品类加一个外键
    seller = models.ForeignKey(to='Seller',on_delete=models.CASCADE)
    # 商品和图片是一对多，在图片类加一个外键

    def __str__(self):
        return '<obj goods_name:{}>'.format(self.goods_name)




