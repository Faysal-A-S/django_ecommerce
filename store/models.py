from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User,  on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=500)
    email = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Subcatagory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Subcatagory")
        verbose_name_plural = ("Subcatagories")

    def __str__(self):
        return self.name


class Product(models.Model):

    pname = models.CharField(max_length=50)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True)
    catagory = models.ForeignKey(Subcatagory, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.pname


class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()
        total = sum(item.get_total for item in orderItems)
        return total

    @property
    def get_cart_quantity(self):
        orderItems = self.orderitem_set.all()
        total = sum(item.quantity for item in orderItems)
        return total

    @property
    def shipping(self):
        shipping = False
        Orderitems = self.orderitem_set.all()
        for i in Orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0,  null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    # def __str__(self):
    #     return self.product
    def __str__(self):
        return str(self.order)


class ShippingAddress(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("ShippingAddress")
        verbose_name_plural = ("ShippingAddresses")

    def __str__(self):
        return str(self.order)
