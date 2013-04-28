from django.db import models
from django.contrib import admin
#from django.core.files.storage import FileSystemStorage
#fs = FileSystemStorage(location='/prodims')

class Shop(models.Model):
    shop_name = models.CharField(db_index=True, max_length=255)
    shop_description = models.TextField(max_length=100)
    speciality = models.TextField(max_length=30)
    def __unicode__(self):
        return self.shop_name


class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'speciality')
    list_filter = ('shop_name', 'shop_location')
    search_field = ('name')


class ProdImage(models.Model):
    name = models.TextField(db_index=True, max_length=50)
    img = models.ImageField(upload_to='media/', blank=True, null=True)
    def __unicode__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(db_index=True, max_length=50)
    category = models.CharField(db_index=True, max_length=50)
    product_price = models.IntegerField(default=0)
    manufacturer = models.CharField(max_length=100, blank=True)
    product_description = models.TextField(max_length=50, blank=True)
    quantity = models.IntegerField(max_length=10, blank=True)
    shops = models.ManyToManyField(Shop, blank=True)
    image = models.ForeignKey(ProdImage, related_name='image', default=None)
    def __unicode__(self):
        return(self.product_name)


class Illiterate(models.Model):
    common_name = models.CharField(db_index=True, max_length=60)
    actual_name = models.CharField(max_length=60)

    def __unicode__(self):
        return(self.common_name)
"""class Api(models.Model):
    input=models.TextField(max_length=30,blank=False)
    def __unicode__(self):
        return self.input"""
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'manufacturer', 'product_price')
    list_filter = ('product_name', 'manufacturer', 'colour', 'product_price')
    search_field = ('product_name', 'manufacturer')
    order = ('product_name')
class ApiAdmin(admin.ModelAdmin):
    search=('input')
    search_fields=['input']
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(ProdImage)
admin.site.register(Illiterate)
#admin.site.register(Api,ApiAdmin)