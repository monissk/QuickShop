from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    reviews = models.IntegerField(default=0) 
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, default="")
    address = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    zip = models.CharField(max_length=50, default="")
    phone = models.IntegerField(default=0)
    textarea = models.CharField(max_length=300)
    date = models.DateField()


    def __str__(self):
        return self.name
    
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    payment_id = models.CharField(max_length=200, default="")
    paid = models.BooleanField(default=False)
    def __str__(self):
        return str(self.order_id)
    
class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."