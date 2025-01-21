from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save 
from datetime import datetime
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    email=models.CharField(max_length=200,null=True)
    

    def __str__(self):
        return self.user.username

class Scrapbox(models.Model):

    name=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    price=models.IntegerField()
    location=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="images",null=True,blank=True)
    phone_no=models.CharField(max_length=200,null=True)
    description=models.CharField(max_length=500,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
   

    def __str__(self):
            
        return self.name
    

class Shipping(models.Model):
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    phone_no=models.CharField(max_length=200)
    
#cartitem


# class Basket(models.Model):     #cart
#     user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_whishlist",default = "")
#     scrap=models.ManyToManyField(Scrapbox,related_name="wished_scrap")
#     created_at=models.DateTimeField(auto_now_add=True)
   
class WishList(models.Model):     #cart
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_whishlist",default = "",null=True)
    scrap=models.ManyToManyField(Scrapbox,related_name="wished_scrap")
    created_at=models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return ', '.join(str(item) for item in self.scrap.all())
    

   
class BasketItem(models.Model):     #cartitem
    basket=models.ForeignKey(WishList,on_delete=models.CASCADE,related_name="cartitem")
    product=models.ForeignKey(Scrapbox,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=1)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.qty * self.product.price
    
 
    
    #then go to form.py




class CartItem(models.Model):
    product = models.ForeignKey(Scrapbox, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
   
 
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'





# class Review(models.Model):
#     user=models.ForeignKey(User,related_name="review",on_delete=models.CASCADE)
#     text=models.CharField(max_length=200)
#     created_date=models.DateTimeField(auto_now_add=True)
#     product=models.ForeignKey(Scrapbox,related_name="scrap_review",on_delete=models.CASCADE)


#     def __str__(self):
#         return self.text















    



def create_profile(sender,created,instance,**kwargs):
        if created:
            UserProfile.objects.create(user=instance)

post_save.connect(create_profile,sender=User)
