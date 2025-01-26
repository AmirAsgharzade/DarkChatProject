from django.shortcuts import render
from django.http import JsonResponse ,HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_GET
from .models import GlobeHistory
from Authen.models import CustomUser
import json
global folder 
folder = 'GlobeChat/'

class IndexView(LoginRequiredMixin,TemplateView):
    login_url = 'authen/login'
    redirect_field_name = ''
    template_name = f'{folder}index.html'
    

class GlobeHistoryMessages(View):
    http_method_names = ['get']
    def get(self,request,*args,**kwargs):
        messages = GlobeHistory.objects.all().order_by('timestamp').values()
        # data = {'messages':list(messages)}
        # print(messages)
        return JsonResponse(list(messages),safe=False)

class MessageSent(View):
    def get(self,request,*args,**kwargs):
        return HttpResponse('Method Not allowed',status=405)
    def post(self,request,*args,**kwargs):
        data = json.loads(request.body)
        user = CustomUser.objects.get(username=data['username'])
        if user:
            message = GlobeHistory.objects.create(
            user=user,username=user.username,color=user.color,content= data['content']
            )
        message.save()
        return JsonResponse({'sent':True},status=201)


def test(request):
    return render(request,'GlobeChat/test.html')
