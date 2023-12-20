from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,logout,authenticate
from scrapbox.models import Scrapbox,UserProfile

from django.views.generic import View,DetailView,CreateView
from scrapbox.forms import UserForm,LoginForm,ScrapboxForm
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
                messages.success(request,"logged in  successfully....")
                return redirect("index")
            
        print("invalid credentials..........")
        messages.error(request,"error in login....")
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
                messages.success(request,"....new data created successfully....")
                print("successssssss")
                return redirect('index')
        else:
                messages.error(request,"....error on create new data....")
                print("errorrrrrrr")
                return render(request,"login.html",{"form":form})

        
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
    
#item view 
class ItemView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Scrapbox.objects.get(id=id)
        return render(request,"scrapboxitem_view.html",{"data":qs})
    
#user profile view

class ProfileDetailView(DetailView):
    template_name="profile_details.html"
    model=UserProfile
    context_object_name="data"


#item add view

class IndexView(CreateView):
    template_name="index.html"
    #template_name="newscrapadd.html"
    form_class=ScrapboxForm
    
    
    def get_success_url(self) -> str:
        return reverse("index")

   



    
