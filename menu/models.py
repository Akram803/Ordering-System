from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User

class Item(models.Model):  
    
    name = models.CharField(max_length=100)
    image = models.FileField(null=True, blank=True)
    price = models.FloatField(default=0.0,) 
    availability = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    number = 0

    def __str__(self): 
        return self.name

    def get_absolute_url(self):
        return reverse("menu:item-details", kwargs={"id": self.id})
    
class Category(models.Model):

    name = models.CharField(max_length=50)
    image = models.FileField(null=True, blank=True)
    description = models.TextField(blank=True)

 
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("menu:item-list", kwargs={"cat":self.name})
        
    def get_image(self):
        return reverse("menu:home") + "media/" + str(self.image)

# =====================================
# ============== Orders =============== 
# =====================================

class order(models.Model):
    
    customer = None
    items = None
    checked_out = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(default=now, editable=True)
    submition_time = models.DateTimeField(editable=True, blank=True, null=True)
    check_out_time = models.DateTimeField(editable=True, blank=True, null=True)
    # table_number = models.PositiveIntegerField(default=0)

    
    class Meta:
        abstract = True
    
    def add_price(self, item_id, item_number):
        item = Item.objects.get(id = item_id)
        self.total_price += item.price * item_number
        self.save()

    def submit(self):
        from datetime import datetime
        self.submition_time = datetime.now()
        self.save()
    
    def __str__(self):
        return  str(self.id) +':  '+ str(self.time)
        
    
    def get_absolute_url(self):
        ...

class CustomerOrder(order):

    customer = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING)
    items = models.ManyToManyField("menu.Item", through="CustomerorderItems")

    class Meta:
        db_table = 'order_customerorder'

    
    def get_absolute_url(self):
        return reverse("menu:order-items-list", kwargs={"id":self.id})

class AnonymouseOrder(order):

    customer = models.CharField(max_length=300)
    items = models.ManyToManyField("menu.Item" ,through="AnonymouseOrderItems")

    class Meta:
        db_table = 'order_anonymouseorder'
    

    def get_absolute_url(self):
        return reverse("menu:order-items-list", kwargs={"id":self.id})


class AnonymouseOrderItems(models.Model):
    anonymouseorder = models.ForeignKey("menu.AnonymouseOrder", models.CASCADE)
    item = models.ForeignKey("menu.Item", models.DO_NOTHING)
    number = models.IntegerField(default=0)

    class Meta:
        db_table = 'order_anonymouseorder_items'
        unique_together = (('anonymouseorder', 'item'),)


    def __str__(self):
        return self.anonymouseorder.customer_id +'  '+ self.item.name +'   '+ str(self.number)
    
class CustomerorderItems(models.Model):
    order = models.ForeignKey('CustomerOrder', models.CASCADE)
    item = models.ForeignKey('menu.Item', models.DO_NOTHING)
    number = models.IntegerField(default=0)

    class Meta:
        db_table = 'order_customerorder_items'
        unique_together = (('order', 'item'),)














