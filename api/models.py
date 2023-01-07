from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255,db_index=True)
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=5,decimal_places=2,db_index=true)
    featured = models.BooleanField(db_index=true)
    category = models.ForeignKey(category,on_delete=models.PROTECT)   
     
#model to contain all the orders made by user
#linked to user and menu item models
class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    class Meta:
        unique_togother =('menuitem','user')
        
# model for the whole order list 
# linked to user who ordered and to delivery crew
class order(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="delivery_crew",null=True)
    status = models.BooleanField(db_index=True,default=0)
    total = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateField(db_index=True)
    
# model for single item in the order list
# relationship with order and menu item models 
class orderITem(models.Model):
    order = models.ForeignKey(order,on_delete=models.CASCADE)
    menuItem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    class Meta:
        unique_togother =('order','menuItem')
        

    
