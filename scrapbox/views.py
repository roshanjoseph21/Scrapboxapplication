from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,logout,authenticate
from scrapbox.models import Scrapbox,UserProfile,Basket,BasketItem

from django.views.generic import View,DetailView,CreateView
from scrapbox.forms import UserForm,LoginForm,ScrapboxForm,BasketForm,BasketItemForm
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
    template_name="profile_details.html"
    model=UserProfile
    context_object_name="data"



# add to cart from scraplist
#  url:http://127.0.0.1:8000/scrapbox/{id}/add_to_basket/
# http://127.0.0.1:8000/cart/view
    
# # http://127.0.0.1:8000/listall


class AddToCartView(View) :
    
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Scrapbox.objects.get(id=id)
        return render(request,"scrapboxitem_view.html",{"data":qs})
    
    def add_to_cart(self,request,*args,**kwargs):
                id=kwargs.get("pk")
                product= Scrapbox.objects.get(id=id)
                cart,created=Basket.objects.get_or_create(user=request.user)
                cart_item,item_created = BasketItem.objects.get_or_create(cart=cart,product=product)
                if not item_created:
                         cart_item.quantity += 1
                         cart_item.save()
    
                return redirect("index")
         

#cart -view cart list  
# http://127.0.0.1:8000/cart/view  
     
class CartListView(View):
    def get(self,request,*args,**kwargs):
        qs=Basket.objects.all()
        return render(request,"cartlist.html",{"data":qs})













#item add view

class IndexView(CreateView):
    template_name="index.html"
    form_class=ScrapboxForm
    
    
    def get_success_url(self) -> str:
        return reverse("index")

   



    
