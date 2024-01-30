from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from scrapbox.models import Scrapbox,UserProfile,WishList,CartItem

from django.views.generic import View,CreateView,UpdateView,DetailView
from scrapbox.forms import UserForm,LoginForm,ScrapboxForm,UserProfileForm,BasketForm,BasketItemForm,ReviewForm


from django.contrib import messages

#authentication

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Sign in required")
            return redirect("signin")
        else:
            return fn(request,*args, **kwargs)
    return wrapper

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

#http://127.0.0.1:8000/scrap/create
@method_decorator(signin_required,name="dispatch")
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
@method_decorator(signin_required,name="dispatch")
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
            return redirect("list-all")
        else:
            print("can't update .......")
            return render(request,"scrapupdate.html",{"form":form})


#list view
@method_decorator(signin_required,name="dispatch")
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
@method_decorator(signin_required,name="dispatch")
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
  
    def post(self, request, *args, **kwargs):
        scrapbox_id = kwargs.get("pk")
        print(scrapbox_id)
        # scrapbox_object=Scrapbox.objects.get(id=id)
        scrapbox_object = get_object_or_404(Scrapbox, id=scrapbox_id)
        print(scrapbox_object)
        action = request.POST.get("action")
        print("object", action)

        cart, created = WishList.objects.get_or_create(user=request.user)

        if action == "addtocart":
            
            cart.scrap.add(scrapbox_object)
            print("added to cart")

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
     



     
         
         

#cart -view cart list  
# http://127.0.0.1:8000/cart/view  
     
# class CartListView(View):
#     def get(self,request,*args,**kwargs):
#         qs=WishList.objects.get(user_id=request.user)
#         wish_items=Scrapbox.objects.exclude(user=request.user)
#         return render(request,"cartlist.html",{"data":qs})
        
class CartListView(View):
    def get(self, request, *args, **kwargs):
        user_wishlist = WishList.objects.filter(user=request.user).first()

        return render(request, "cartlist.html", {"user_wishlist": user_wishlist})




class RemoveCartItemView(View):
    def get(self, request, *args, **kwargs):
        wishlist_item_id = kwargs.get("pk")
        wishlist_item = get_object_or_404(WishList, id=wishlist_item_id, user=request.user)
        wishlist_item.delete()
        return redirect("cartlist-view")


@method_decorator(signin_required,name="dispatch")      
def add_to_cart(request, product_id):
    product = Scrapbox.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, 
                                                       user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')



#item add view

class IndexView(CreateView):
    template_name="index.html"
    form_class=ScrapboxForm
    
    
    def get_success_url(self) -> str:
        return reverse("index")


@method_decorator(signin_required,name="dispatch")      
class ReviewView(CreateView): #comment is gona create so create view
    template_name="scrapboxitem_view.html"
    form_class=ReviewForm #which form class is gona render

    def get_success_url(self) -> str:
        return reverse("itemview")
    
    def form_valid(self, form) :
        #form.instance ponits to postform user
        id=self.kwargs.get("pk")
        product=Scrapbox.objects.get(id=id)
        form.instance.user=self.request.user
        form.instance.scrap=product
        return super().form_valid(form)








    
