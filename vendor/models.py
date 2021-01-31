from builtins import property

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):
    categoryname = models.CharField(max_length=255)
    categoryimage = models.ImageField(null=True,blank=True,upload_to='category/images')

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Product(models.Model):
    productname = models.CharField(max_length=255)
    price = models.FloatField(null=True)
    stock = models.IntegerField()
    description = models.CharField(max_length=2500)
    image = models.ImageField(null=True,blank=True,upload_to='product/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def ___str___(self):
        return self.productname

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Userdetails(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True,blank=True,upload_to='userdata/images')
    mobile_number = models.CharField(user_id, max_length=10, null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    orderverify = models.BooleanField(default=True,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    status = models.CharField(default='pending', max_length=200,null=True)

    def ___str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping=True
        return shipping


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=200, null=True)
    

    def __str__(self):
        return self.address
