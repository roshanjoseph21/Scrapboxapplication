from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,logout,authenticate
from django.http import JsonResponse
from django.views import View

from .models import Scrapbox, WishList
from scrapbox.models import Scrapbox,UserProfile,WishList,BasketItem

from django.views.generic import View,CreateView,UpdateView,DetailView
from scrapbox.forms import UserForm,LoginForm,ScrapboxForm,UserProfileForm,BasketForm,BasketItemForm
from scrapbox.forms import UserCreationForm #UserProfile


from django.contrib import messages

# Create your views here.
class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
        else:
           return render(request,"register.html",{"form":form})
        

#login view
class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        print("login form..........")
        if form.is_valid():
            print("start login session....")
            username1=form.cleaned_data.get("username")
            password1=form.cleaned_data.get("password")
            print("user details....",username1,password1)
            user_object=authenticate(request,username=username1,password=password1)
            if user_object:
                print("valid credentilas..........")
                login(request,user_object)
                return redirect("index")
            
        print("invalid credentials..........")
        return render(request,"login.html",{"form":form})
    
#index view
#http://127.0.0.1:8000/scrap/create
class ScrapCreateView(View):
    def get(self,request,*args,**kwargs):
        form=ScrapboxForm()
        return render(request,"scrapbox_add.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=ScrapboxForm(request.POST,files=request.FILES)
        if form.is_valid():
                form.save()
                return redirect('index')
        else:
               
                return render(request,"login.html",{"form":form})


# scrap update view
#http://127.0.0.1:8000/scrap/{id}/update
        
class ScrapUpdateView(View):
  
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        obj=Scrapbox.objects.get(id=id)
        form=ScrapboxForm(instance=obj)
        return render(request,"scrapupdate.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Scrapbox.objects.get(id=id)
        form=ScrapboxForm(request.POST,instance=obj,files=request.FILES)
        if (form.is_valid()):
            form.save()
            print("data updated sucessfully-----")
            return redirect("index")
        else:
            print("can't update .......")
            return render(request,"scrapupdate.html",{"form":form})


#list view
class ScrapboxListView(View):
    def get(self,request,*args,**kwargs):
        qs=Scrapbox.objects.all()
        return render(request,"scrapboxlist.html",{"data":qs})

#signout

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
#item view -retrive
class ItemView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Scrapbox.objects.get(id=id)
        return render(request,"scrapboxitem_view.html",{"data":qs})
    
    

#user profile view
# 
class ProfileDetailView(DetailView):
        template_name="profile_detail.html"
        model=UserProfile
        context_object_name="data"
        
    
class ProfileUpdateView(UpdateView):
    template_name="profile_add.html"
    form_class=UserProfileForm
    model=UserProfile

    def get_success_url(self) -> str:
        return reverse("index")
  

# add to cart from scraplist
#  url:http://127.0.0.1:8000/scrapbox/{id}/add_to_basket/
# http://127.0.0.1:8000/cart/view
    
# # http://127.0.0.1:8000/listall


class AddToCartView(View) :
    
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Scrapbox.objects.get(id=id)
        return render(request,"scrapboxitem_view.html",{"data":qs})
    
    def post(self,request,*args,**kwargs):
                id=kwargs.get("pk")
                product= Scrapbox.objects.get(id=id)
                cart,created=WishList.objects.get_or_create(user=request.user)
                cart_item,item_created = BasketItem.objects.get_or_create(cart=cart,product=product)
                if not item_created:
                         cart_item.quantity += 1
                         cart_item.save()
    
                return redirect("index")

# add to wishlist
    # http://127.0.0.1:8000/scrapbox/4/addtocart

# class AddToWishList(View):
  
    
    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     scrapbox_object=Scrapbox.objects.get(id=id)
    #     action=request.POST.get("action")
    #     print("++++++",action)
    #     cart,created=WishList.objects.get_or_create(user=request.user)
    #     if action == "addtocart":  #addtocart
    #         cart.scrap.add(scrapbox_object)           #request.user.profile will give the logined user
    #     return redirect("index")
     


class AddToWishListView(View):
  
    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        scrapbox_object = Scrapbox.objects.get(id=id)
        action = request.POST.get("action")
        print("++++++", action)

        # Get or create the user's wishlist
        wishlist, created = WishList.objects.get_or_create(user=request.user)

        if action == "addtocart":
            wishlist.scrap.add(scrapbox_object)
            return JsonResponse({'status': 'success', 'message': 'Item added to wishlist'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'})


     
         
         

#cart -view cart list  
# http://127.0.0.1:8000/cart/view  
     
# class CartListView(View):
#     def get(self,request,*args,**kwargs):
#         qs=WishList.objects.get(user_id=request.user)
#         wish_items=Scrapbox.objects.exclude(user=request.user)
#         return render(request,"cartlist.html",{"data":qs})
        
class CartListView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Assuming the user has only one wishlist, you can use 'get' instead of 'filter'
            wishlist = WishList.objects.get(user=request.user)
            
            # Retrieve items in the wishlist
            wish_items = wishlist.scrap.all()

            return render(request, "cartlist.html", {"data": wish_items})
        except WishList.DoesNotExist:
            # Handle the case where the user doesn't have a wishlist
            return render(request, "cartlist.html", {"data": None})














#item add view

class IndexView(CreateView):
    template_name="index.html"
    form_class=ScrapboxForm
    
    
    def get_success_url(self) -> str:
        return reverse("index")

   



    
