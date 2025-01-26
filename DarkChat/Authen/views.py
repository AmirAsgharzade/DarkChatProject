from django.shortcuts import render ,redirect
from .forms import LoginForm,RegisterForm
from django.views import View
from django.contrib.auth import login,logout , authenticate
from .models import CustomUser
from django.http import HttpResponseBadRequest
# Create your views here.
class MyLoginView(View):
    
    def get(self,request,*args,**kwargs):
        form = LoginForm()
        return render(request,'authen/login.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            login(request,user)
         
            return redirect('index')
        return render(request,'authen/login.html',{'form':form})

def Mylogout(request):
    logout(request)
    return redirect('Authen.login')



class RegisterView(View):
    template_name = 'authen/register.html'
    def get(self,request,*args,**kwargs):
        form = RegisterForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = RegisterForm(request.POST)
        Users = CustomUser.objects.all().values()
        if form.is_valid():
            if form.cleaned_data['username'] in Users:
                return HttpResponseBadRequest('Username already exists',status=400)
            form.save()
            return redirect('Authen.login')
        return render(request, 'authen/register.html', {'form': form})
